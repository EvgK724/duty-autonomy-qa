"""Isolated synthetic QA only. No live reader, owner input, credentials or production target.
Builds a deterministic fixed approved fixture and artifacts. Never claims this tests real owner intake.
"""
from pathlib import Path
import hashlib,json,os,sys,shutil,re,html
ROOT=Path(__file__).resolve().parents[3]
APP=ROOT/'dezhurstva'
def digest(v):return hashlib.sha256(json.dumps(v,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def main():
 if os.environ.get('GITHUB_ACTIONS')=='true' and (os.environ.get('GITHUB_REPOSITORY')!='EvgK724/duty-autonomy-qa' or os.environ.get('GITHUB_REF')!='refs/heads/main'):raise ValueError('QA_TARGET_ONLY')
 fixture=json.loads((ROOT/'qa/approved-fixture.json').read_text());p=fixture['payload'];d=p['draft']
 if set(fixture)!={'schema','syntheticOnly','payload','payloadHash'} or fixture['schema']!=1 or fixture['syntheticOnly'] is not True or digest(p)!=fixture['payloadHash']:raise ValueError('QA_FIXTURE')
 if set(p)!={'approvalId','baseVersion','version','draft'} or p['approvalId']!='9a7c09b1099e4aa1b802e2d0060a0001' or p['baseVersion']!=0 or p['version']!=1 or d['month']!='2099-01' or d['order']!=['synthetic_a','synthetic_b'] or d['marks']!=[]:raise ValueError('QA_SYNTHETIC_ONLY')
 expected={f'2099-01-{i:02}':['synthetic_a' if i%2 else 'synthetic_b'] for i in range(1,32)}
 if d['duty']!=expected or d['off']!=[] or d['shift']!={'work':['08:00','20:00'],'off':['08:00','08:00']} or set(d)!={'month','order','off','shift','duty','marks'}:raise ValueError('QA_FIXED_DRAFT')
 month={k:v for k,v in d.items() if k!='month'};month.update(title='Январь 2099',status='preliminary',version=1)
 data={'tz':'Asia/Yekaterinburg','updated':'2098-12-15T12:00:00Z','doctors':{'synthetic_a':{'name':'Synthetic Doctor A'},'synthetic_b':{'name':'Synthetic Doctor B'}},'months':{'2099-01':month}}
 (APP/'data').mkdir(exist_ok=True);(APP/'data/schedule.json').write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
 sys.path.insert(0,str(APP/'tools'));import build
 build.main(artifact_months=['2099-01'])
 from pypdf import PdfReader
 from openpyxl import load_workbook
 for suffix in ('','-print'):
  path=APP/'files'/f'2099-01{suffix}.pdf';r=PdfReader(path);assert len(r.pages)==1 and 'SYNTHETIC' in r.pages[0].extract_text().upper() and r.pages[0].extract_text().count('+')==31
  assert abs(float(r.pages[0].mediabox.width)-841.8898)<0.02
 wb=load_workbook(APP/'files/2099-01.xlsx');assert any('SYNTHETIC' in str(c.value).upper() for ws in wb for row in ws for c in row)
 for who in ('all','synthetic_a','synthetic_b'):
  text=(APP/'cal'/f'{who}.ics').read_text();assert 'BEGIN:VCALENDAR' in text and 'END:VCALENDAR' in text
 # Stateless QA page intentionally does not emulate production authentication/storage UI.
 rows=''.join('<tr><td>'+date+'</td><td>'+html.escape(data['doctors'][ids[0]]['name'])+'</td></tr>' for date,ids in expected.items())
 page='<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta http-equiv="Content-Security-Policy" content="default-src \'none\'; style-src \'unsafe-inline\'; base-uri \'none\'; form-action \'none\'"><title>Isolated synthetic duty QA</title><style>body{font:16px system-ui;max-width:48rem;margin:2rem auto;padding:1rem}td{padding:.25rem 1rem}a{display:inline-block;margin:.5rem}</style><h1>Synthetic QA · January 2099</h1><p>Not a real duty schedule. No real owner intake, personal data, forms, scripts or persistent storage.</p><a href="files/2099-01.pdf">PDF</a><a href="files/2099-01-print.pdf">Print PDF</a><a href="files/2099-01.xlsx">XLSX</a><a href="cal/all.ics">ICS</a><table><tr><th>Date</th><th>Synthetic doctor</th></tr>'+rows+'</table></html>'
 (APP/'index.html').write_text(page)
 receipt={'approvalId':p['approvalId'],'payloadHash':fixture['payloadHash'],'month':d['month'],'version':1}
 (APP/'data/publication-receipts.json').write_text(json.dumps([receipt],indent=2)+'\n')
 # Publish only exact generated artifacts, never tools/workflow/config/fixture.
 dist=ROOT/'_site';shutil.rmtree(dist,ignore_errors=True);(dist/'dezhurstva').mkdir(parents=True)
 paths=['index.html','data/schedule.json','data/publication-receipts.json','files/2099-01.pdf','files/2099-01-print.pdf','files/2099-01.xlsx','files/pdf.json','files/hashes.json','cal/all.ics','cal/synthetic_a.ics','cal/synthetic_b.ics']
 hashes={}
 for rel in paths:
  raw=(APP/rel).read_bytes();target=dist/'dezhurstva'/rel;target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(raw);hashes['dezhurstva/'+rel]=hashlib.sha256(raw).hexdigest()
  if rel.endswith(('.html','.json','.ics')):
   assert not re.search(r'test01|script\.google|AKfy|gmail\.com|localStorage|sessionStorage|serviceWorker|<script',raw.decode(),re.I)
 (dist/'.nojekyll').write_text('');(dist/'index.html').write_text('<!doctype html><meta charset="utf-8"><title>Synthetic QA only</title><a href="dezhurstva/">Synthetic QA artifacts</a>')
 (ROOT/'qa/last-build.json').write_text(json.dumps({'syntheticOnly':True,'payloadHash':fixture['payloadHash'],'artifacts':hashes},indent=2)+'\n')
 print('Synthetic artifacts verified. No production/real-owner proof implied.')
if __name__=='__main__':main()
