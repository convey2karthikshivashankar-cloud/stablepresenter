"""Quarto composition; fixed assets, approved snapshots, offline distributions."""
from __future__ import annotations
from html import escape
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
from .model import AssessmentError, canonical, metrics, source_hash
from .diff import compare
from .store import atomic_json
ASSETS=Path(__file__).with_name('assets')

def markdown_report(snapshot,changes):
 s=snapshot['state']; m=metrics(s)
 lines=[f"# {s['program']['title']}",f"\nReporting period: {snapshot['reportingPeriod']} · As of {s['asOf']} · Approved by {snapshot['reviewer']}", '\n**Synthetic demonstration data**' if s['program']['exampleData'] else '\nAssessment research report', '\n## Executive summary',*['- '+x for x in s['executiveSummary']]]
 rec=s['recommendations'][s['program']['currentRecommendationId']]
 lines+=['\n## Current assessment',rec['conclusion'],rec['rationale'],f"\nAnalysis coverage: {m['coverage'] if m['coverage'] is not None else 'Unknown'}%. Validated evidence: {m['evidenceValidated']}/{m['evidenceTotal']}. Decision gates met: {m['gatesMet']}/{m['gatesTotal']}.",'\n## Coverage']
 lines += [f"- {d['title']}: {d['coverage'] if d['coverage'] is not None else 'Unknown'}%; examined scope {d['examined']}/{d['planned']}." for d in m['dimensions']]
 for c,title in [('findings','Findings and evidence'),('risks','Risks'),('questions','Open questions'),('alternatives','Alternatives and trade-offs'),('estimates','Effort, cost and benefit'),('decisions','Management decisions'),('gates','Decision readiness'),('investigations','Next research priorities')]:
  lines+=['\n## '+title]
  for r in s[c].values():
   lines+=[f"\n### {r['id']} · {r.get('title',r.get('question',r.get('description',r['id'])))}",f"Status: {r.get('status',r.get('verdict',r.get('confidence','unknown')))}"]
   for field in ('conclusion','implications','rationale','nextStep','effortEstimate'):
    if field in r: lines.append(r[field])
   if c=='estimates': lines.append(f"Range: {r['low']}–{r['high']} {r['unit']} (Unknown when null). Assumptions: {'; '.join(r['assumptions'])}")
   if c=='alternatives':lines.append('Benefits: '+'; '.join(r['benefits'])+'\nDrawbacks: '+'; '.join(r['drawbacks']))
   if c=='findings':lines.append(f"Confidence: {r['confidence']}; uncertainties: {'; '.join(r['uncertainties']) or 'None recorded'}")
   for e in r.get('evidenceRefs',[]):
    ev=s['evidence'][e]
    lines.append(f"- Evidence {e} ({ev['verificationStatus']}): {ev['description']}")
    for ref in ev['sourceRefs']: lines.append(f"  - {ref['path']}:L{ref['startLine']}–L{ref['endLine']} · SHA-256 {ref['sourceHash']}")
 lines+=['\n## Weekly evolution']+[f"- {x['kind'].upper()}: {x['id']} · {x['title']}" for x in changes]
 lines+=['\n## Measurement methodology','Coverage = weighted mean of dimension examined-scope / planned-scope ratios. Examined statuses: preliminary, corroborated, validated, inconclusive, contradicted, superseded. Investigating and not-examined count as zero; missing planned scope yields Unknown.','Evidence validation = validated evidence count / all evidence records, including assumptions and rejected evidence. Evidence maturity also exposes corroborated-or-validated findings / all findings.','Decision readiness = met gates / all gates. Any unmet or unknown critical gate blocks a proceed recommendation. No metric measures migration implementation or implies feasibility.']
 return '\n\n'.join(lines)+'\n'

def build(store,out,quarto=None):
 snapshots=store.snapshots()
 if not snapshots: raise AssessmentError('No approved snapshots. Run approve before building reports.')
 quarto=quarto or os.environ.get('QUARTO_BIN') or shutil.which('quarto')
 if not quarto or not Path(quarto).is_file(): raise AssessmentError('Quarto is required. Install Quarto or set QUARTO_BIN to its executable.')
 out=Path(out).resolve(); out.mkdir(parents=True,exist_ok=True)
 if out==store.path.resolve() or out in store.path.resolve().parents or out.is_relative_to(ASSETS.parent.resolve()): raise AssessmentError('Report output must be separate from store and application source')
 versions=subprocess.run([str(quarto),'--version'],capture_output=True,text=True,check=True).stdout.strip()
 records=[]
 for index,snap in enumerate(snapshots):
  records.append({**snap,'metrics':metrics(snap['state']),'changes':compare(snapshots[index-1]['state'] if index else {},snap['state'])})
 payload={'uiVersion':'1.0','snapshots':records,'templateHashes':{p.name:source_hash(p.read_text()) for p in sorted(ASSETS.iterdir()) if p.is_file()}}
 # Escape HTML parser terminators even though the JSON script is non-executable.
 serialized=canonical(payload).replace('<','\\u003c').replace('>','\\u003e').replace('&','\\u0026').replace('\u2028','\\u2028').replace('\u2029','\\u2029')
 shell=ASSETS.joinpath('shell.html').read_text()
 with tempfile.TemporaryDirectory(prefix='assess-quarto-') as temporary:
  folder=Path(temporary)
  app=shell+'\n<script type="application/json" id="assessment-data">'+serialized+'</script>\n<script>\n'+ASSETS.joinpath('app.js').read_text()+'\n</script>'
  (folder/'_app.html').write_text(app,encoding='utf-8')
  (folder/'_style.html').write_text('<style>'+ASSETS.joinpath('theme.css').read_text()+'</style>',encoding='utf-8')
  qmd='''---
+pagetitle: "Assessment Intelligence | Executive Report"
+lang: en
+page-layout: custom
+format:
+  html:
+    theme: default
+    toc: false
+    embed-resources: true
+    anchor-sections: false
+    smooth-scroll: false
+    html-math-method: plain
+    include-in-header: _style.html
+    include-after-body: _app.html
+    output-file: index.html
+---
+
+<!-- Content is supplied to the fixed, versioned assessment component catalog. -->
+'''.replace('\n+','\n')
  (folder/'report.qmd').write_text(qmd)
  env={**os.environ,'XDG_CACHE_HOME':str(folder/'.cache'),'XDG_DATA_HOME':str(folder/'.data')}
  result=subprocess.run([str(quarto),'render','report.qmd','--quiet'],cwd=folder,env=env,capture_output=True,text=True,timeout=180)
  if result.returncode: raise AssessmentError('Quarto render failed: '+result.stderr[-3000:])
  html=(folder/'index.html').read_bytes()
  (out/'index.html').write_bytes(html); (out/'weekly-delta.html').write_bytes(html)
  # Keep a complete, independently rerenderable Quarto composition in the report archive.
  for filename in ('report.qmd','_style.html','_app.html'): shutil.copyfile(folder/filename,out/filename)
  historical_html={snapshots[-1]['reportingPeriod']:html}
  for index,snapshot in enumerate(snapshots[:-1]):
   historical_payload={**payload,'snapshots':records[:index+1]}
   encoded=canonical(historical_payload).replace('<','\\u003c').replace('>','\\u003e').replace('&','\\u0026').replace('\u2028','\\u2028').replace('\u2029','\\u2029')
   historical_app=shell+'\n<script type="application/json" id="assessment-data">'+encoded+'</script>\n<script>\n'+ASSETS.joinpath('app.js').read_text()+'\n</script>'
   (folder/'_app.html').write_text(historical_app,encoding='utf-8')
   result=subprocess.run([str(quarto),'render','report.qmd','--quiet'],cwd=folder,env=env,capture_output=True,text=True,timeout=180)
   if result.returncode: raise AssessmentError('Historical Quarto render failed: '+result.stderr[-2000:])
   historical_html[snapshot['reportingPeriod']]=(folder/'index.html').read_bytes()
 latest=snapshots[-1]
 (out/'report.md').write_text(markdown_report(latest,records[-1]['changes']),encoding='utf-8')
 atomic_json(out/'current.json',latest)
 for index,snap in enumerate(snapshots):
  period=snap['reportingPeriod']; archive=out/'history'/period; archive.mkdir(parents=True,exist_ok=True)
  # Archives contain only what was known at that period, including its prior history.
  (archive/'index.html').write_bytes(historical_html[period])
  atomic_json(archive/'snapshot.json',snap)
  (archive/'report.md').write_text(markdown_report(snap,records[index]['changes']),encoding='utf-8')
  atomic_json(out/'deltas'/f'{period}.json',records[index]['changes'])
 for name,source in latest['state']['sources'].items():
  p=out/'sources'/name; p.parent.mkdir(parents=True,exist_ok=True); p.write_text(source['content'],encoding='utf-8')
 atomic_json(out/'build-manifest.json',{'schemaVersion':'1.0','uiVersion':'1.0','quartoVersion':versions,'approvedHashes':[x['hash'] for x in snapshots],'templateHashes':payload['templateHashes'],'htmlSha256':source_hash(html.decode()),'renderedAsOf':latest['state']['asOf']})
 return {'report':str(out/'index.html'),'weeklyDelta':str(out/'weekly-delta.html'),'snapshots':len(snapshots),'quartoVersion':versions}
