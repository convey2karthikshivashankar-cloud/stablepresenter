"""Read just changed Markdown files; parse explicitly delimited YAML records."""
from pathlib import Path
import re
import yaml
from .model import AssessmentError, source_hash, safe_path, COLLECTIONS
class UniqueLoader(yaml.SafeLoader): pass
def unique_mapping(loader,node,deep=False):
 result={}
 for k,v in node.value:
  key=loader.construct_object(k,deep=deep)
  if key in result: raise AssessmentError(f'Duplicate YAML key: {key}')
  result[key]=loader.construct_object(v,deep=deep)
 return result
UniqueLoader.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG,unique_mapping)
BLOCK=re.compile(r'^```assessment\s*\n(.*?)^```\s*$',re.M|re.S)
def read_sources(root,state):
 root=Path(root).resolve()
 if not root.is_dir(): raise AssessmentError(f'Not a source directory: {root}')
 docs=[]; skipped=[]; sources={}; seen=set()
 files=sorted(root.rglob('*.md'))
 if not files: raise AssessmentError('No Markdown sources found')
 for file in files:
  if file.is_symlink() or not file.resolve().is_relative_to(root): raise AssessmentError('Source symlinks are not allowed')
  if file.stat().st_size>2_000_000: raise AssessmentError('Markdown file exceeds 2 MB limit')
  path=file.relative_to(root).as_posix(); safe_path(path)
  content=file.read_text(encoding='utf-8'); h=source_hash(content)
  if state and state['sources'].get(path,{}).get('hash')==h:
   skipped.append(path); continue
  if len(content)>2_000_000: raise AssessmentError('Oversized source')
  sources[path]={'hash':h,'content':content}
  for m in BLOCK.finditer(content):
   try:
    if any(isinstance(t,(yaml.tokens.AliasToken,yaml.tokens.AnchorToken)) for t in yaml.scan(m.group(1))):
     raise AssessmentError('YAML aliases/anchors are not accepted in agent records')
    data=yaml.load(m.group(1),Loader=UniqueLoader)
   except yaml.YAMLError as error:
    raise AssessmentError(f'Invalid assessment YAML in {path}: {error}') from None
   if not isinstance(data,dict): raise AssessmentError(f'Assessment block must be a mapping: {path}')
   for collection,records in data.items():
    if collection in COLLECTIONS and isinstance(records,list):
     for rec in records:
      if not isinstance(rec,dict) or 'id' not in rec: raise AssessmentError('Records need stable IDs')
      key=(collection,rec['id'])
      if key in seen: raise AssessmentError(f'Duplicate entity update: {key}')
      seen.add(key)
      refs=rec.setdefault('sourceRefs',[{'path':'@self','startLine':1,'endLine':content[:m.start()].count('\n') or 1}])
      for ref in refs:
       if ref['path']=='@self': ref['path']=path
       target=sources.get(ref['path']) or (state or {}).get('sources',{}).get(ref['path'])
       if target: ref['sourceHash']=target['hash']
   docs.append(data)
 return docs,sources,skipped
