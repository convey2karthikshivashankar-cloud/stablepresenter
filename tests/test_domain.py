from copy import deepcopy
import json
import pytest
from assessment_intelligence.model import AssessmentError,metrics,digest
from assessment_intelligence.diff import compare
from .conftest import ROOT

def test_incremental_cumulative_and_evolution(evolved):
 before,after=evolved.snapshots();s=after['state']
 assert len(s['sources'])==6
 assert s['alternatives']==before['state']['alternatives']
 assert s['findings']['F-API']['revision']==2
 assert s['findings']['F-API']['createdAt']=='2026-11-02'
 assert s['findings']['F-SERIAL']['status']=='contradicted'
 changes=compare(before['state'],s)
 assert any(x['id']=='F-SERIAL' and x['kind']=='contradicted' for x in changes)
 assert any(x['id']=='F-API' and x['kind']=='strengthened' for x in changes)
 assert any(x['id']=='Q-SERIAL' and x['kind']=='resolved' for x in changes)
 assert any(x['id']=='REC-ATLAS' for x in changes)
 assert any(x['id']=='EST-EFFORT' and any(f['field']=='high' and f['before']==100 and f['after']==155 for f in x['fields']) for x in changes)

def test_documented_measurement(evolved):
 m=metrics(evolved.current()['state'])
 assert m['coverage']==74.2
 assert (m['evidenceValidated'],m['evidenceTotal'])==(2,8)
 assert m['evidencePct']==25
 assert m['gatesMet']==2 and m['gatesTotal']==4 and m['readinessPct']==50
 assert m['blockingGates']==['G-ECON','G-OPS']
 assert m['openQuestions']==3

def test_missing_planned_scope_is_unknown(store):
 s=deepcopy(store.current()['state'])
 s['investigations']={k:v for k,v in s['investigations'].items() if v['dimensionId']!='D-OPS'}
 assert metrics(s)['coverage'] is None

def test_no_evidence_or_gates_denominators_unknown(store):
 s=deepcopy(store.current()['state']);s['evidence']={};s['gates']={}
 m=metrics(s);assert m['evidencePct'] is None and m['readinessPct'] is None

def test_immutable_approval_and_draft_separation(store):
 path=store.path/'snapshots/2026-W45.json';frozen=path.read_bytes();h=store.current()['hash']
 store.patch([{'op':'replace','path':'/findings/F-API/conclusion','value':'Revised hypothesis requiring review.'}],'2026-11-03','agent-b',h)
 assert path.read_bytes()==frozen
 assert store.snapshots()[-1]['state']['findings']['F-API']['conclusion']!='Revised hypothesis requiring review.'
 with pytest.raises(AssessmentError,match='Immutable'):store.approve('2026-W45','reviewer',store.current()['hash'])

def test_stale_patch_rejected_without_mutation(store):
 h=store.current()['hash'];store.patch([{'op':'replace','path':'/findings/F-API/confidence','value':'low'}],'2026-11-03','agent-a',h)
 prior=(store.path/'current.json').read_bytes()
 with pytest.raises(AssessmentError,match='Conflict'):store.patch([{'op':'replace','path':'/findings/F-API/confidence','value':'high'}],'2026-11-03','agent-b',h)
 assert (store.path/'current.json').read_bytes()==prior

@pytest.mark.parametrize('patch',[
 [{'op':'replace','path':'/findings/F-API/status','value':'deployed'}],
 [{'op':'replace','path':'/findings/F-API/investigationId','value':'MISSING'}],
 [{'op':'replace','path':'/findings/F-API/revision','value':999}],
 [{'op':'replace','path':'/uiVersion','value':'99'}],
 [{'op':'replace','path':'/findings/F-API/title','value':'temporary'},{'op':'test','path':'/findings/F-API/confidence','value':'wrong'}],
 [{'op':'replace','path':'/evidence/E-SCAN/sourceRefs/0/path','value':'../../secret'}],
 [{'op':'replace','path':'/evidence/E-SCAN/sourceRefs/0/endLine','value':99999}],
 [{'op':'replace','path':'/findings/F-API/status','value':'validated'}],
 [{'op':'replace','path':'/estimates/EST-EFFORT/low','value':10000}],
 [{'op':'replace','path':'/recommendations/REC-ATLAS/stance','value':'proceed'}],
 [{'op':'add','path':'/findings/F-API/arbitraryUi','value':'<script>bad()</script>'}],
 [{'op':'move','path':'/findings/F-API/title','from':'/findings/F-DEPS/title'}],
 [{'op':'replace','path':'/program/id','value':'OTHER'}],
])
def test_invalid_updates_atomic(store,patch):
 prior=(store.path/'current.json').read_bytes();count=len(list((store.path/'revisions').glob('*.json')))
 with pytest.raises(AssessmentError):store.patch(patch,'2026-11-03','hostile-agent',store.current()['hash'])
 assert (store.path/'current.json').read_bytes()==prior
 assert len(list((store.path/'revisions').glob('*.json')))==count

def test_patch_only_affected_entity_and_assets_unchanged(store):
 old=store.current();assets=ROOT/'assessment_intelligence/assets';hashes={p.name:p.read_bytes() for p in assets.iterdir()}
 updated=store.patch([{'op':'test','path':'/findings/F-API/confidence','value':'medium'},{'op':'replace','path':'/findings/F-API/confidence','value':'low'}],'2026-11-03','agent-a',old['hash'])
 assert updated['state']['findings']['F-DEPS']==old['state']['findings']['F-DEPS']
 assert updated['state']['risks']==old['state']['risks']
 assert [x['id'] for x in compare(old['state'],updated['state'])]==['F-API']
 assert hashes=={p.name:p.read_bytes() for p in assets.iterdir()}

def test_unchanged_sources_not_reprocessed(store):
 before=store.current()['hash'];count=len(list((store.path/'revisions').glob('*.json')))
 env,result=store.ingest(ROOT/'samples/week-1','2026-11-02','agent-a',before)
 assert env['hash']==before and len(result['skipped'])==3 and not result['changed']
 assert len(list((store.path/'revisions').glob('*.json')))==count

def test_records_api_and_recovery(store):
 before=store.current();r=deepcopy(before['state']['findings']['F-API']);r['confidence']='low'
 after=store.records({'findings':[r]},'2026-11-03','agent',before['hash'])
 assert after['state']['findings']['F-API']['revision']==2
 recovered=store.rollback(before['hash'],'2026-11-04','reviewer',after['hash'])
 assert recovered['state']['findings']['F-API']['confidence']=='medium'
 assert recovered['state']['findings']['F-API']['revision']==3
 assert recovered['provenance']['details']['restoredHash']==before['hash']
 assert len(store.snapshots())==1

def test_lock_and_integrity(store):
 with store.lock():
  with pytest.raises(AssessmentError,match='busy'):store.approve('next','reviewer',store.current()['hash'])
 p=store.path/'current.json';j=json.loads(p.read_text());j['hash']='0'*64;p.write_text(json.dumps(j))
 with pytest.raises(AssessmentError,match='digest'):store.current()

def test_source_path_and_yaml_safety(store,tmp_path):
 folder=tmp_path/'hostile';folder.mkdir();p=folder/'bad.md';p.write_text('```assessment\nfindings: []\nfindings: []\n```\n')
 with pytest.raises(AssessmentError,match='Duplicate YAML'):store.ingest(folder,'2026-11-03','agent',store.current()['hash'])
 p.write_text('```assessment\n!!python/object/apply:os.system ["touch BAD"]\n```\n')
 with pytest.raises(Exception):store.ingest(folder,'2026-11-03','agent',store.current()['hash'])
 p.unlink();p.symlink_to(ROOT/'samples/week-1/01-assessment-charter.md')
 with pytest.raises(AssessmentError,match='symlink'):store.ingest(folder,'2026-11-03','agent',store.current()['hash'])

def test_hash_canonical_and_weakened_diff(store):
 s=store.current()['state'];copy=deepcopy(s);copy['findings']['F-API']['confidence']='low'
 assert any(x['id']=='F-API' and x['kind']=='weakened' for x in compare(s,copy))
 assert digest({'a':1,'b':2})==digest({'b':2,'a':1})
