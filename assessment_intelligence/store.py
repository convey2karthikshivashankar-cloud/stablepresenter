"""Atomic local knowledge base, optimistic concurrency, approval, recovery."""
from __future__ import annotations
from contextlib import contextmanager
from copy import deepcopy
from datetime import date, datetime, timezone
import json
import os
from pathlib import Path
import re
from .model import COLLECTIONS, AssessmentError, canonical, digest, validate, validate_document
from .ingestion import read_sources
from .diff import compare

def read_json(path): return json.loads(Path(path).read_text(encoding='utf-8'))
def atomic_json(path,value):
 path=Path(path); path.parent.mkdir(parents=True,exist_ok=True)
 tmp=path.with_name(path.name+'.tmp')
 try:
  with tmp.open('w',encoding='utf-8') as f:
   f.write(json.dumps(value,ensure_ascii=False,sort_keys=True,indent=2,allow_nan=False)+'\n'); f.flush(); os.fsync(f.fileno())
  os.replace(tmp,path)
 finally:
  if tmp.exists(): tmp.unlink()

class Store:
 def __init__(self,path): self.path=Path(path)
 def current(self):
  p=self.path/'current.json'
  if not p.exists(): return None
  return self.check_envelope(read_json(p))
 @staticmethod
 def check_envelope(env):
  validate_document(env,'snapshot.schema.json')
  validate(env['state'])
  if env['hash']!=digest(env['state']): raise AssessmentError('State digest mismatch')
  if 'reportingPeriod' in env and env['id']!=env['reportingPeriod']: raise AssessmentError('Snapshot ID/period mismatch')
  return env
 @contextmanager
 def lock(self):
  self.path.mkdir(parents=True,exist_ok=True)
  p=self.path/'.write.lock'
  try: fd=os.open(p,os.O_CREAT|os.O_EXCL|os.O_WRONLY,0o600)
  except FileExistsError: raise AssessmentError('Store busy: another writer holds .write.lock') from None
  try:
   os.write(fd,str(os.getpid()).encode()); os.close(fd); yield
  finally: p.unlink(missing_ok=True)
 def _base(self,expected):
  current=self.current()
  if (current['hash'] if current else None)!=expected: raise AssessmentError('Conflict: stale/missing base hash; inspect current state and retry')
  return current
 def _commit(self,state,old,actor,operation,as_of,details=None):
  try: date.fromisoformat(as_of)
  except ValueError: raise AssessmentError('as-of must be an ISO calendar date') from None
  if old and as_of<old['state']['asOf']: raise AssessmentError('Assessment date cannot go backwards')
  state['asOf']=as_of
  for collection in COLLECTIONS:
   for key,record in state[collection].items():
    prior=old['state'][collection].get(key) if old else None
    content={k:v for k,v in record.items() if k not in ('createdAt','updatedAt','revision')}
    previous={k:v for k,v in (prior or {}).items() if k not in ('createdAt','updatedAt','revision')}
    if content==previous:
     state[collection][key]=deepcopy(prior)
    else:
     record['createdAt']=prior['createdAt'] if prior else as_of
     record['updatedAt']=as_of
     record['revision']=prior['revision']+1 if prior else 1
  validate(state)
  h=digest(state)
  if old and h==old['hash']: return old
  env={'hash':h,'parentHash':old['hash'] if old else None,'state':state,'provenance':{'actor':actor,'operation':operation,'at':datetime.now(timezone.utc).isoformat(),'details':details or {}}}
  revision=self.path/'revisions'/f'{h}.json'
  if not revision.exists(): atomic_json(revision,env)
  atomic_json(self.path/'current.json',env)
  return env
 def ingest(self,root,as_of,actor,expected=None):
  with self.lock():
   old=self._base(expected)
   state=deepcopy(old['state']) if old else {'schemaVersion':'1.0','uiVersion':'1.0','asOf':as_of,'program':{},'executiveSummary':[],'sources':{},**{c:{} for c in COLLECTIONS}}
   docs,sources,skipped=read_sources(root,state)
   state['sources'].update(sources)
   for doc in docs:
    for collection,items in doc.items():
     if collection in ('program','executiveSummary'): state[collection]=items
     elif collection in COLLECTIONS and isinstance(items,list):
      for rec in items: state[collection][rec['id']]=rec
     else: raise AssessmentError(f'Unknown ingestion field: {collection}')
   # Resolve references only after the entire changed source set is known.
   for collection in COLLECTIONS:
    for record in state[collection].values():
     for ref in record.get('sourceRefs',[]):
      if 'sourceHash' not in ref and ref.get('path') in state['sources']: ref['sourceHash']=state['sources'][ref['path']]['hash']
   env=self._commit(state,old,actor,'ingest',as_of,{'changedSources':sorted(sources),'skippedSources':skipped})
   return env,{'changed':sorted(sources),'skipped':skipped}
 def records(self,payload,as_of,actor,expected):
  with self.lock():
   old=self._base(expected)
   if not old: raise AssessmentError('Initialize with Markdown ingestion first')
   state=deepcopy(old['state'])
   for collection,items in payload.items():
    if collection not in COLLECTIONS or not isinstance(items,list): raise AssessmentError('Record updates must map collection names to lists')
    seen=set()
    for rec in items:
     if not isinstance(rec,dict) or 'id' not in rec or rec['id'] in seen: raise AssessmentError('Invalid/duplicate record ID')
     seen.add(rec['id']); state[collection][rec['id']]=deepcopy(rec)
   return self._commit(state,old,actor,'records',as_of)
 def patch(self,operations,as_of,actor,expected):
  with self.lock():
   old=self._base(expected)
   if not old: raise AssessmentError('No state to patch')
   state=deepcopy(old['state'])
   validate_document(operations,'patch.schema.json')
   if not isinstance(operations,list) or not 1<=len(operations)<=1000: raise AssessmentError('Patch must contain 1..1000 operations')
   for op in operations:
    if not isinstance(op,dict) or set(op)-{'op','path','value'} or op.get('op') not in ('add','replace','remove','test'): raise AssessmentError('Unsupported JSON Patch operation')
    path=op.get('path','')
    if not isinstance(path,str) or not path.startswith('/') or re.search(r'~(?![01])',path): raise AssessmentError('Invalid JSON pointer')
    tokens=[v.replace('~1','/').replace('~0','~') for v in path[1:].split('/')]
    if tokens[0] not in COLLECTIONS+('executiveSummary','program') or any(t in ('revision','createdAt','updatedAt') for t in tokens): raise AssessmentError('Patch path outside agent content contract')
    if len(tokens)==1 and tokens[0] in COLLECTIONS: raise AssessmentError('Patch individual entities, not an entire collection')
    if tokens[0]=='program' and (len(tokens)<2 or tokens[1] in ('id','exampleData')): raise AssessmentError('Program identity is fixed')
    try:
     parent=state
     for t in tokens[:-1]: parent=parent[int(t)] if isinstance(parent,list) else parent[t]
     last=tokens[-1]
     if isinstance(parent,list):
      idx=len(parent) if last=='-' and op['op']=='add' else int(last)
      if idx<0 or idx>len(parent) or (op['op']!='add' and idx==len(parent)): raise AssessmentError('Array pointer out of bounds')
      if last!='-' and str(idx)!=last: raise AssessmentError('Invalid array index')
      if op['op']=='add': parent.insert(idx,deepcopy(op['value']))
      elif op['op']=='remove': parent.pop(idx)
      elif op['op']=='test':
       if parent[idx]!=op['value']: raise AssessmentError('Patch test failed')
      else: parent[idx]=deepcopy(op['value'])
     elif isinstance(parent,dict):
      if op['op']!='add' and last not in parent: raise AssessmentError('Patch target missing')
      if op['op']=='remove': del parent[last]
      elif op['op']=='test':
       if parent[last]!=op['value']: raise AssessmentError('Patch test failed')
      else: parent[last]=deepcopy(op['value'])
     else: raise AssessmentError('Patch parent is not a container')
    except (KeyError,IndexError,TypeError,ValueError) as e:
     if isinstance(e,AssessmentError): raise
     raise AssessmentError(f'Invalid patch target: {path}') from None
   return self._commit(state,old,actor,'patch',as_of,{'paths':[o['path'] for o in operations]})
 def snapshots(self):
  return sorted([self.check_envelope(read_json(p)) for p in (self.path/'snapshots').glob('*.json')],key=lambda e:(e['state']['asOf'],e['reportingPeriod']))
 def approve(self,period,reviewer,expected):
  if not re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9_-]{0,63}',period): raise AssessmentError('Unsafe reporting period')
  with self.lock():
   old=self._base(expected)
   if not old: raise AssessmentError('No state to approve')
   path=self.path/'snapshots'/f'{period}.json'
   if path.exists(): raise AssessmentError('Immutable snapshot already exists; choose a new period')
   previous=self.snapshots()
   if previous and old['state']['asOf']<previous[-1]['state']['asOf']: raise AssessmentError('Snapshot date precedes latest approved report')
   env=deepcopy(old); env.update({'id':period,'reportingPeriod':period,'createdAt':datetime.now(timezone.utc).isoformat(),'reviewer':reviewer,'changeSummary':compare(previous[-1]['state'] if previous else {},old['state'])})
   atomic_json(path,env); return env
 def rollback(self,target_hash,as_of,actor,expected):
  if not re.fullmatch('[a-f0-9]{64}',target_hash): raise AssessmentError('Invalid revision hash')
  with self.lock():
   old=self._base(expected)
   p=self.path/'revisions'/f'{target_hash}.json'
   if not p.exists(): raise AssessmentError('Unknown revision')
   target=self.check_envelope(read_json(p))
   return self._commit(deepcopy(target['state']),old,actor,'rollback',as_of,{'restoredHash':target_hash})
