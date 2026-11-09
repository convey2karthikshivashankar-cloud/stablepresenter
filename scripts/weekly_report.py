"""Schedule-friendly local reporting. Approval must be explicitly requested."""
import argparse
from datetime import date
import json
from pathlib import Path
from assessment_intelligence.reporting import build
from assessment_intelligence.store import Store
p=argparse.ArgumentParser();p.add_argument('--store',default='data');p.add_argument('--out',default='site');p.add_argument('--config',default='config/reporting.json');p.add_argument('--approve',action='store_true');p.add_argument('--reviewer');p.add_argument('--period');p.add_argument('--quarto')
a=p.parse_args();config=json.loads(Path(a.config).read_text());store=Store(a.store)
if a.approve:
 if not a.reviewer:p.error('--reviewer is required with --approve')
 env=store.current();day=date.fromisoformat(env['state']['asOf']);year,week,_=day.isocalendar()
 period=a.period or config['periodFormat'].format(year=year,week=week)
 store.approve(period,a.reviewer,env['hash'])
print(json.dumps(build(store,a.out,a.quarto),indent=2))
