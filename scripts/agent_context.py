"""Emit only relevant records, evidence excerpts and their schema for an agent."""
import argparse
import json
from assessment_intelligence.model import COLLECTIONS,SCHEMA
from assessment_intelligence.store import Store
p=argparse.ArgumentParser();p.add_argument('--store',default='data');p.add_argument('--collection',choices=COLLECTIONS,required=True);p.add_argument('--id',required=True)
a=p.parse_args();env=Store(a.store).current();state=env['state'];record=state[a.collection][a.id]
evidence=[state['evidence'][id] for id in record.get('evidenceRefs',[])]
refs=record['sourceRefs']+[ref for e in evidence for ref in e['sourceRefs']]
excerpts=[{'reference':r,'text':'\n'.join(state['sources'][r['path']]['content'].splitlines()[r['startLine']-1:r['endLine']])} for r in refs]
print(json.dumps({'baseHash':env['hash'],'record':record,'evidence':evidence,'excerpts':excerpts,'recordSchema':SCHEMA['properties'][a.collection]['additionalProperties']},indent=2))
