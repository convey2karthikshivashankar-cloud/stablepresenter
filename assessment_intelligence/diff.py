"""Deterministic field-level evolution, never semantic LLM comparison."""
from .model import COLLECTIONS
RANK={'unknown':0,'low':1,'medium':2,'high':3}
def compare(before,after):
 changes=[]
 for c in COLLECTIONS:
  old=before.get(c,{}); new=after.get(c,{})
  for key in sorted(set(old)|set(new)):
   a=old.get(key); b=new.get(key)
   if a==b: continue
   fields=[]
   if a and b:
    ignored=('updatedAt','revision') if c=='evidence' else ('updatedAt','revision','sourceRefs')
    fields=[{'field':f,'before':a.get(f),'after':b.get(f)} for f in sorted(set(a)|set(b)) if a.get(f)!=b.get(f) and f not in ignored]
    if not fields: continue
   kind='added' if a is None else 'removed' if b is None else 'revised'
   if c=='findings' and a and b:
    if b['status'] in ('contradicted','superseded') and a['status']!=b['status']: kind=b['status']
    elif RANK[b['confidence']]>RANK[a['confidence']]: kind='strengthened'
    elif RANK[b['confidence']]<RANK[a['confidence']]: kind='weakened'
   if c=='questions' and a and b and a['status']=='open' and b['status']=='answered': kind='resolved'
   changes.append({'collection':c,'id':key,'kind':kind,'title':(b or a).get('title',(b or a).get('question',(b or a).get('description',(b or a).get('conclusion',key)))),'fields':fields,'beforeRevision':a.get('revision') if a else None,'afterRevision':b.get('revision') if b else None})
 if before.get('executiveSummary')!=after.get('executiveSummary'):
  changes.append({'collection':'executiveSummary','id':'summary','kind':'revised','title':'Executive synthesis updated','fields':[{'field':'executiveSummary','before':before.get('executiveSummary'),'after':after.get('executiveSummary')}],'beforeRevision':None,'afterRevision':None})
 return changes
