"""Validação da versão completa em subdiretório Pages e migração do banco V0.4."""
import json,subprocess,time,urllib.request
from pathlib import Path
from playwright.sync_api import sync_playwright,expect
ROOT=Path(__file__).resolve().parents[1]
server=subprocess.Popen(['python3','-m','http.server','8015','--directory',str(ROOT.parent)],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
try:
 for _ in range(30):
  try:urllib.request.urlopen('http://127.0.0.1:8015/',timeout=1);break
  except OSError:time.sleep(.1)
 with sync_playwright() as p:
  browser=p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox'])
  page=browser.new_page(accept_downloads=True);errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
  base=f'http://127.0.0.1:8015/{ROOT.name}/';page.goto(base+'README.md')
  old=page.evaluate('''async base=>{
   const {ifrsCatalog}=await import(base+'app/servicos/ifrs.js');const source=await(await fetch(base+'dados/fontes/IFRS_Matematica_Questoes_2016_2026.json')).json();const state=ifrsCatalog(source);
   state.notes=[{id:'privada',subjectId:state.subjects[0].id,title:'Meu caderno',body:'Não sobrescrever'}];
   await new Promise(resolve=>{const r=indexedDB.open('estudos-concursos',1);r.onupgradeneeded=()=>r.result.createObjectStore('state');r.onsuccess=()=>{const d=r.result,t=d.transaction('state','readwrite');t.objectStore('state').put(state,'personal');t.oncomplete=()=>{d.close();resolve();};};});return state;
  }''',base)
  def stored():return page.evaluate('''()=>new Promise(resolve=>{const r=indexedDB.open('estudos-concursos',1);r.onsuccess=()=>{const d=r.result,q=d.transaction('state').objectStore('state').get('personal');q.onsuccess=()=>{d.close();resolve(q.result);};};})''')
  page.goto(base);page.get_by_role('heading',name='Início',exact=True).wait_for();assert stored()==old
  page.locator('nav').get_by_role('button',name='Questões',exact=True).click()
  expect(page.locator('#questions article')).to_have_count(180)
  expect(page.locator('#question-summary')).to_contain_text('180 questões • 180 classificadas automaticamente')
  crops=json.loads((ROOT/'dados/questoes/recortes-completos.json').read_text())['questions']
  layer=json.loads((ROOT/'dados/questoes/classificacao-confirmada.json').read_text())['questions']
  for crop in crops:
   response=page.request.get(base+crop['image']);assert response.status==200,crop['id'];assert response.body()[:8]==b'\x89PNG\r\n\x1a\n'
  for pdf in {q['pdf'] for q in crops}:
   response=page.request.get(base+pdf);assert response.status==200;assert response.body().startswith(b'%PDF')
  for exam in sorted({q['id'][5:11] for q in crops}):
   page.locator('#question-filters summary').click() if not page.locator('#question-filters').evaluate('(d)=>d.open') else None
   year,semester=exam.split('-');page.locator('.filters [name=year]').select_option(year);page.locator('.filters [name=semester]').select_option(semester)
   expect(page.locator('#questions article')).to_have_count(10)
   rows=[q for q in crops if q['id'][5:11]==exam]
   for index in range(10):
    card=page.locator('#questions article').nth(index);image=card.locator('.question-image');image.scroll_into_view_if_needed();image.evaluate('(im)=>im.decode()');assert image.evaluate('(im)=>im.naturalWidth')==rows[index]['width']
    assert f'#page={rows[index]["page"]}' in card.get_by_role('link',name=f'Abrir PDF original na página {rows[index]["page"]}').get_attribute('href')
   page.locator('nav').get_by_role('button',name='Assuntos',exact=True).click()
   page.locator('[name=subjectYear]').select_option(year);page.locator('[name=subjectSemester]').select_option(semester)
   expect(page.locator('.frequency-row')).to_have_count(31)
   for row in page.locator('.frequency-row').all():
    topic=row.locator('[data-related-subject]').first.get_attribute('data-related-subject');count=sum(q['id'][5:11]==exam and topic in q['assuntoIds'] for q in layer)
    assert f'{count} de 10 ({count*10:.1f}%)' in row.inner_text(),(exam,topic)
   page.locator('nav').get_by_role('button',name='Questões',exact=True).click()
  # Uma revisão antiga é preservada no banco, sem alterar a consulta editorial.
  page.evaluate("""()=>new Promise(resolve=>{const r=indexedDB.open('estudos-concursos',1);r.onsuccess=()=>{const d=r.result,t=d.transaction('state','readwrite'),store=t.objectStore('state'),request=store.get('personal');request.onsuccess=()=>{const data=request.result;data.questions[0].assuntoIds=[];data.questions[0].assuntosRevisadosEm='2026-10-20T10:00:00Z';store.put(data,'personal');};t.oncomplete=()=>{d.close();resolve();};};})""")
  page.reload();page.locator('nav').get_by_role('button',name='Questões',exact=True).click()
  expect(page.locator('#question-summary')).to_contain_text('180 questões • 180 classificadas automaticamente')
  assert stored()['notes']==old['notes'];assert stored()['questions'][0]['assuntoIds']==[]
  assert page.locator('[data-edit-subjects], #thematic-edit').count()==0
  page.set_viewport_size({'width':390,'height':844});assert page.evaluate('document.documentElement.scrollWidth<=innerWidth')
  assert not errors,errors
  browser.close()
 print('PASS: 180 PNGs e 18 PDFs via HTTP, imagens decodificadas nas 18 provas, frequências confrontadas em 18 filtros, migração aditiva e revisão pessoal preservada, mobile e Pages.')
finally:server.terminate();server.wait()
