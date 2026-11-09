"""Strict domain validation, evidence integrity, and documented measurements."""
from __future__ import annotations
import hashlib
import json
from pathlib import Path, PurePosixPath
from jsonschema import Draft202012Validator, FormatChecker

COLLECTIONS=('dimensions','investigations','findings','evidence','risks','questions','alternatives','estimates','gates','decisions','recommendations','activities')
SCHEMA=json.loads(Path(__file__).with_name('report.schema.json').read_text())
VALIDATOR=Draft202012Validator(SCHEMA,format_checker=FormatChecker())
def validate_document(value,filename):
 schema=json.loads(Path(__file__).with_name(filename).read_text())
 errors=list(Draft202012Validator(schema,format_checker=FormatChecker()).iter_errors(value))
 if errors: raise AssessmentError(f'{filename}: {errors[0].message}')
class AssessmentError(ValueError): pass

def canonical(value): return json.dumps(value,ensure_ascii=False,sort_keys=True,separators=(',',':'),allow_nan=False)
def digest(value): return hashlib.sha256(canonical(value).encode()).hexdigest()
def source_hash(text): return hashlib.sha256(text.encode()).hexdigest()
def safe_path(value):
 p=PurePosixPath(value)
 if not value or '\\' in value or p.is_absolute() or '..' in p.parts or ':' in value or str(p)!=value:
  raise AssessmentError(f'Unsafe source path: {value}')
 return p

def validate(state):
 errors=sorted(VALIDATOR.iter_errors(state),key=lambda e:str(list(e.path)))
 if errors:
  e=errors[0]
  raise AssessmentError(f'Schema {"/".join(map(str,e.path))}: {e.message}')
 for name,source in state['sources'].items():
  safe_path(name)
  if source_hash(source['content'])!=source['hash']: raise AssessmentError(f'Source hash mismatch: {name}')
 for collection in COLLECTIONS:
  for key,record in state[collection].items():
   if key!=record['id']: raise AssessmentError(f'ID/key mismatch: {collection}/{key}')
   if record['createdAt']>record['updatedAt'] or record['updatedAt']>state['asOf']:
    raise AssessmentError(f'Invalid record dates: {key}')
   for ref in record['sourceRefs']:
    safe_path(ref['path'])
    source=state['sources'].get(ref['path'])
    if not source or source['hash']!=ref['sourceHash']: raise AssessmentError(f'Missing or stale source reference: {key}')
    if not 1<=ref['startLine']<=ref['endLine']<=len(source['content'].splitlines()): raise AssessmentError(f'Invalid evidence locator: {key}')
   for ev in record.get('evidenceRefs',[]):
    if ev not in state['evidence']: raise AssessmentError(f'Unknown evidence {ev} in {key}')
   if 'dimensionId' in record and record['dimensionId'] not in state['dimensions']: raise AssessmentError(f'Unknown dimension in {key}')
   if 'investigationId' in record and record['investigationId'] not in state['investigations']: raise AssessmentError(f'Unknown investigation in {key}')
   for target in record.get('supportingFindings',[])+record.get('supersedes',[]):
    if target not in state['findings'] or target==key: raise AssessmentError(f'Invalid finding reference in {key}')
   if collection=='evidence':
    if not record['sourceRefs']: raise AssessmentError(f'Evidence has no source: {key}')
    if record['capturedAt']>state['asOf']: raise AssessmentError(f'Future evidence: {key}')
    if record['verificationStatus']=='validated' and (record['kind']=='assumption' or record['reviewedBy']=='unreviewed'):
     raise AssessmentError(f'Assumption/unreviewed evidence cannot be validated: {key}')
   if collection=='findings' and record['status']=='validated':
    if not record['evidenceRefs'] or any(state['evidence'][e]['verificationStatus']!='validated' for e in record['evidenceRefs']):
     raise AssessmentError(f'Validated finding requires validated evidence: {key}')
   if collection=='estimates':
    if (record['low'] is None)!=(record['high'] is None) or (record['low'] is not None and record['low']>record['high']):
     raise AssessmentError(f'Invalid estimate range: {key}')
   if collection=='gates' and record['status']=='met' and not record['evidenceRefs']: raise AssessmentError(f'Met gate requires evidence: {key}')
   if collection=='gates' and record['status']=='met' and any(state['evidence'][e]['verificationStatus'] not in ('reviewed','validated') for e in record['evidenceRefs']):
    raise AssessmentError(f'Met gate requires reviewed or validated evidence: {key}')
 rec=state['recommendations'].get(state['program']['currentRecommendationId'])
 if not rec: raise AssessmentError('Unknown current recommendation')
 if rec['stance'] in ('proceed','conditional-proceed'):
  if any(g['critical'] and g['status']!='met' for g in state['gates'].values()) or not state['gates']:
   raise AssessmentError('Proceed recommendation blocked by critical/undefined gates')
  if not rec['supportingFindings']: raise AssessmentError('Proceed recommendation needs supporting findings')
  if any(state['findings'][f]['status'] not in ('corroborated','validated') for f in rec['supportingFindings']):
   raise AssessmentError('Proceed recommendation cannot rely on preliminary or contradicted findings')
 return state

def metrics(state):
 terminal={'preliminary','corroborated','validated','inconclusive','contradicted','superseded'}
 dims=[]
 for d in state['dimensions'].values():
  inv=[i for i in state['investigations'].values() if i['dimensionId']==d['id']]
  total=sum(i['scopeWeight'] for i in inv)
  examined=sum(i['scopeWeight'] for i in inv if i['status'] in terminal)
  dims.append({'id':d['id'],'title':d['title'],'weight':d['weight'],'examined':examined,'planned':total,'coverage':round(100*examined/total,1) if total else None})
 weight=sum(d['weight'] for d in dims)
 coverage=round(sum(d['weight']*d['coverage'] for d in dims)/weight,1) if weight and all(d['coverage'] is not None for d in dims) else None
 evidence=list(state['evidence'].values()); validated=sum(e['verificationStatus']=='validated' for e in evidence)
 gates=list(state['gates'].values()); met=sum(g['status']=='met' for g in gates)
 findings=list(state['findings'].values())
 return {'coverage':coverage,'dimensions':dims,'evidenceValidated':validated,'evidenceTotal':len(evidence),'evidencePct':round(100*validated/len(evidence),1) if evidence else None,'corroboratedFindings':sum(f['status'] in ('corroborated','validated') for f in findings),'findingsTotal':len(findings),'openQuestions':sum(q['status']=='open' for q in state['questions'].values()),'gatesMet':met,'gatesTotal':len(gates),'readinessPct':round(100*met/len(gates),1) if gates else None,'blockingGates':[g['id'] for g in gates if g['critical'] and g['status']!='met'],'criticalFindings':sum(f['severity']=='critical' and f['status'] not in ('contradicted','superseded') for f in findings)}
