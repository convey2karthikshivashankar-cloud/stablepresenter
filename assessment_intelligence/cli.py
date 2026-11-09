"""Automation-friendly CLI. No vendor APIs and no presentation mutation commands."""
import argparse
import json
from pathlib import Path
import sys
from .model import AssessmentError, validate, metrics
from .store import Store, read_json
from .diff import compare
from .reporting import build

def main(argv=None):
 p=argparse.ArgumentParser(description='Local-first assessment intelligence and Quarto reporting')
 p.add_argument('--store',default='data',help='Knowledge-base directory')
 sub=p.add_subparsers(dest='command',required=True)
 for name in ('ingest','records','patch','rollback'):
  q=sub.add_parser(name);q.add_argument('--as-of',required=True);q.add_argument('--actor',required=True);q.add_argument('--base-hash')
  if name=='ingest':q.add_argument('--sources',required=True)
  elif name=='rollback':q.add_argument('--revision',required=True)
  else:q.add_argument('--file',required=True)
 q=sub.add_parser('status');q.add_argument('--hash',action='store_true')
 q=sub.add_parser('validate');q.add_argument('--file')
 q=sub.add_parser('approve');q.add_argument('--period',required=True);q.add_argument('--reviewer',required=True);q.add_argument('--base-hash',required=True)
 q=sub.add_parser('build');q.add_argument('--out',default='site');q.add_argument('--quarto')
 q=sub.add_parser('diff');q.add_argument('before');q.add_argument('after')
 q=sub.add_parser('demo');q.add_argument('--samples',default='samples');q.add_argument('--out',default='site');q.add_argument('--quarto')
 q=sub.add_parser('history')
 a=p.parse_args(argv);store=Store(a.store)
 try:
  if a.command=='ingest': env,detail=store.ingest(a.sources,a.as_of,a.actor,a.base_hash); result={'hash':env['hash'],**detail,'status':'draft'}
  elif a.command=='records':result={'hash':store.records(read_json(a.file),a.as_of,a.actor,a.base_hash)['hash'],'status':'draft'}
  elif a.command=='patch':result={'hash':store.patch(read_json(a.file),a.as_of,a.actor,a.base_hash)['hash'],'status':'draft'}
  elif a.command=='rollback':result={'hash':store.rollback(a.revision,a.as_of,a.actor,a.base_hash)['hash'],'status':'draft'}
  elif a.command=='status':
   env=store.current()
   if a.hash:
    print(env['hash'] if env else '');return 0
   result={'hash':env['hash'] if env else None,'asOf':env['state']['asOf'] if env else None,'metrics':metrics(env['state']) if env else None,'approvedPeriods':[x['reportingPeriod'] for x in store.snapshots()]}
  elif a.command=='validate':
   if a.file:
    value=read_json(a.file);validate(value.get('state',value))
   else:
    if not store.current():raise AssessmentError('No state')
    for snapshot in store.snapshots(): store.check_envelope(snapshot)
   result={'valid':True}
  elif a.command=='approve':result={'period':store.approve(a.period,a.reviewer,a.base_hash)['reportingPeriod'],'status':'approved'}
  elif a.command=='build':result=build(store,a.out,a.quarto)
  elif a.command=='diff':
   before=read_json(a.before);after=read_json(a.after);result=compare(before.get('state',before),after.get('state',after))
  elif a.command=='history':result=[{'hash':x['hash'],'period':x['reportingPeriod'],'asOf':x['state']['asOf'],'reviewer':x['reviewer']} for x in store.snapshots()]
  elif a.command=='demo':
   if store.current(): raise AssessmentError('Demo requires an empty store; use a new --store path')
   for week,day,period in [('week-1','2026-11-02','2026-W45'),('week-2','2026-11-09','2026-W46')]:
    current=store.current();env,_=store.ingest(Path(a.samples)/week,day,'synthetic-research-agent',current['hash'] if current else None)
    store.approve(period,'Demonstration reviewer',env['hash'])
   result=build(store,a.out,a.quarto)
  print(json.dumps(result,indent=2,ensure_ascii=False));return 0
 except (AssessmentError,OSError,ValueError,KeyError) as e:
  print(json.dumps({'error':str(e)}),file=sys.stderr);return 2
if __name__=='__main__':raise SystemExit(main())
