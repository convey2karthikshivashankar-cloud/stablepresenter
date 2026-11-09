"""Quarto builds, real Chromium workflows, offline rendering and visual regression."""
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import threading
from functools import partial
from http.server import SimpleHTTPRequestHandler,ThreadingHTTPServer
import pytest
from PIL import Image,ImageChops
from playwright.sync_api import sync_playwright,expect
from assessment_intelligence.store import Store
from assessment_intelligence.reporting import build
from .conftest import ROOT

@pytest.fixture(scope='module')
def reports(tmp_path_factory):
 folder=tmp_path_factory.mktemp('quarto-report');store=Store(folder/'data')
 for week,day,period in [('week-1','2026-11-02','2026-W45'),('week-2','2026-11-09','2026-W46')]:
  current=store.current();env,_=store.ingest(ROOT/'samples'/week,day,'test-agent',current['hash'] if current else None)
  store.approve(period,'Demonstration reviewer',env['hash'])
 build(store,folder/'site')
 return folder,store

class QuietHandler(SimpleHTTPRequestHandler):
 def log_message(self,*args): pass
@pytest.fixture(scope='module')
def web(reports):
 handler=partial(QuietHandler,directory=str(reports[0]/'site'))
 server=ThreadingHTTPServer(('127.0.0.1',0),handler)
 thread=threading.Thread(target=server.serve_forever,daemon=True);thread.start()
 yield f'http://127.0.0.1:{server.server_port}'
 server.shutdown();thread.join();server.server_close()
@pytest.fixture(scope='module')
def browser():
 with sync_playwright() as p:
  executable=os.environ.get('CHROMIUM_BIN') or shutil.which('chromium')
  b=p.chromium.launch(**({'executable_path':executable} if executable else {}),headless=True,args=['--no-sandbox'])
  yield b
  b.close()
@pytest.fixture
def page(browser,web):
 context=browser.new_context(viewport={'width':1440,'height':1080},device_scale_factor=1,locale='en-US',timezone_id='UTC',reduced_motion='reduce')
 p=context.new_page();p.goto(web+'/index.html',wait_until='networkidle')
 yield p
 context.close()

def test_repeated_quarto_build_semantically_identical(reports):
 folder,store=reports;build(store,folder/'repeat')
 assert (folder/'site/_app.html').read_bytes()==(folder/'repeat/_app.html').read_bytes()
 assert (folder/'site/_style.html').read_bytes()==(folder/'repeat/_style.html').read_bytes()
 # No volatile rendering timestamp is added; the approved data includes explicit approval metadata.
 assert (folder/'site/index.html').read_bytes()==(folder/'repeat/index.html').read_bytes()
 assert json.loads((folder/'site/build-manifest.json').read_text())==json.loads((folder/'repeat/build-manifest.json').read_text())

def test_archive_contains_only_information_known_at_that_time(reports):
 folder,_=reports
 html=(folder/'site/history/2026-W45/index.html').read_text()
 match=re.search(r'id="assessment-data">(.*?)</script>',html,re.S)
 payload=json.loads(match.group(1))
 assert len(payload['snapshots'])==1
 s=payload['snapshots'][0]['state'];assert s['asOf']=='2026-11-02'
 assert 'F-ADAPTER' not in s['findings'] and 'E-SERIAL' not in s['evidence']
 assert s['findings']['F-SERIAL']['status']=='preliminary'

def test_full_management_workflow(page,web,tmp_path):
 errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
 expect(page.locator('#program-title')).to_have_text('Atlas modernization assessment')
 expect(page.locator('#panel-overview')).to_contain_text('74.2%')
 # Executive conclusion -> finding -> line-located source evidence.
 page.locator('#panel-overview [data-finding="F-API"]').click()
 expect(page.locator('#section-title')).to_have_text('Findings & Evidence')
 expect(page.locator('[data-finding-id="F-API"]')).to_contain_text('validated')
 page.locator('[data-finding-id="F-API"] [data-evidence="E-TX"]').click()
 expect(page.locator('#evidence-dialog')).to_be_visible()
 expect(page.locator('#dialog-content')).to_contain_text('L5–L')
 expect(page.locator('#dialog-content')).to_contain_text('SHA-256')
 with page.expect_download() as dl:page.locator('[data-download-source]').click()
 download=dl.value;download.save_as(tmp_path/download.suggested_filename)
 assert 'Synthetic run ID' in (tmp_path/download.suggested_filename).read_text()
 page.locator('#close-dialog').click()
 page.select_option('#finding-filter','contradicted')
 assert page.locator('.finding:visible').count()==1
 expect(page.locator('.finding:visible')).to_contain_text('F-SERIAL')
 page.fill('#global-search','zz-not-present');assert page.locator('.finding:visible').count()==0
 page.fill('#global-search','');page.select_option('#finding-filter','all')
 # Every stable section renders and no global horizontal overflow appears.
 for id in ['overview','coverage','findings','risks','alternatives','economics','evolution','readiness','appendix']:
  page.locator('[data-nav="'+id+'"]').click()
  expect(page.locator('#panel-'+id)).to_be_visible()
  assert not page.evaluate('document.documentElement.scrollWidth > innerWidth')
 page.locator('[data-nav="evolution"]').click()
 expect(page.locator('#panel-evolution')).to_contain_text('contradicted')
 expect(page.locator('#panel-evolution')).to_contain_text('Namespace-only adaptation')
 page.locator('[data-nav="economics"]').click()
 expect(page.locator('#panel-economics')).to_contain_text('95–155')
 expect(page.locator('#panel-economics')).to_contain_text('Not yet measurable')
 page.select_option('#snapshot-select','0');page.locator('[data-nav="findings"]').click()
 expect(page.locator('[data-finding-id="F-SERIAL"]')).to_contain_text('preliminary')
 assert page.locator('[data-finding-id="F-ADAPTER"]').count()==0
 page.select_option('#snapshot-select','1')
 with page.expect_download() as dl:page.locator('#export-json').click()
 dl.value.save_as(tmp_path/'state.json');assert json.loads((tmp_path/'state.json').read_text())['state']['asOf']=='2026-11-09'
 page.locator('#theme-toggle').click();expect(page.locator('body')).to_have_class(re.compile(r'.*\bdark\b.*'))
 page.locator('#theme-toggle').click()
 # Source text containing script terminators is displayed literally, never executed.
 page.locator('[data-nav="appendix"]').click();page.locator('[data-source="02-technical-analysis.md"]').click()
 expect(page.locator('#dialog-content')).to_contain_text('<script>window.__sourceExecuted = true</script>')
 assert page.evaluate('window.__sourceExecuted') is None
 page.locator('#close-dialog').click()
 page.goto(web+'/weekly-delta.html');expect(page.locator('#section-title')).to_have_text('Weekly Evolution')
 page.goto(web+'/history/2026-W45/index.html');assert page.locator('#snapshot-select option').count()==1
 expect(page.locator('#report-period')).to_contain_text('2026-11-02')
 assert not errors

def test_mobile_tablet_keyboard_print_and_offline(browser,web,reports,tmp_path):
 for width in (390,768,1024):
  context=browser.new_context(viewport={'width':width,'height':900});page=context.new_page();page.goto(web+'/index.html')
  for id in ['overview','coverage','findings','risks','alternatives','economics','evolution','readiness','appendix']:
   page.locator('[data-nav="'+id+'"]').click()
   assert not page.evaluate('document.documentElement.scrollWidth > innerWidth'),(width,id)
  if width==390:
   page.locator('[data-nav="overview"]').click();page.screenshot(path=str(ROOT/'test-results/mobile.png'),full_page=True)
  context.close()
 context=browser.new_context(viewport={'width':1440,'height':1080});page=context.new_page()
 # Deliberately offline: load the generated bytes, with every external request aborted.
 requests=[];page.on('request',lambda r:requests.append(r.url));page.route('**/*',lambda r:r.abort())
 context.set_offline(True);page.set_content((reports[0]/'site/index.html').read_text(),wait_until='load')
 expect(page.locator('#program-title')).to_contain_text('Atlas modernization assessment')
 page.locator('[data-nav="readiness"]').focus();page.keyboard.press('Enter');expect(page.locator('#panel-readiness')).to_be_visible()
 page.emulate_media(media='print');assert page.locator('.panel:visible').count()==9
 page.pdf(path=str(tmp_path/'report.pdf'),format='A4',print_background=True)
 assert (tmp_path/'report.pdf').stat().st_size>20000
 assert not [u for u in requests if u.startswith('http')]
 context.close()

def difference(actual,baseline,diff_path=None):
 a=Image.open(actual).convert('RGB');b=Image.open(baseline).convert('RGB')
 assert a.size==b.size,'Visual regression: viewport size changed'
 diff=ImageChops.difference(a,b)
 pixels=list(diff.getdata());ratio=sum(max(p)>24 for p in pixels)/len(pixels)
 if diff_path:diff.save(diff_path)
 assert ratio<0.005,f'Visual regression: {ratio:.2%} of pixels changed (>0.5% tolerance)'
 return ratio

def test_visual_baseline_and_negative_control(page):
 result=ROOT/'test-results';result.mkdir(exist_ok=True)
 page.screenshot(path=str(result/'overview.png'),animations='disabled')
 golden=ROOT/'tests/visual/overview.png'
 if os.environ.get('UPDATE_VISUALS')=='1':golden.parent.mkdir(exist_ok=True);shutil.copyfile(result/'overview.png',golden)
 assert golden.exists(),'Missing visual baseline; see readme.md for intentional baseline creation'
 difference(result/'overview.png',golden,result/'visual-difference.png')
 page.add_style_tag(content='.workspace{margin-left:310px!important}')
 page.screenshot(path=str(result/'layout-mutation.png'),animations='disabled')
 with pytest.raises(AssertionError,match='Visual regression'):
  difference(result/'layout-mutation.png',golden)
