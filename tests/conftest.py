from pathlib import Path
import pytest
from assessment_intelligence.store import Store
ROOT=Path(__file__).resolve().parents[1]
@pytest.fixture
def store(tmp_path):
 s=Store(tmp_path/'data')
 env,_=s.ingest(ROOT/'samples/week-1','2026-11-02','test-agent')
 s.approve('2026-W45','test-reviewer',env['hash'])
 return s
@pytest.fixture
def evolved(store):
 env,_=store.ingest(ROOT/'samples/week-2','2026-11-09','second-agent',store.current()['hash'])
 store.approve('2026-W46','test-reviewer',env['hash'])
 return store
