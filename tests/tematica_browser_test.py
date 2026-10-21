"""Revisões pessoais pendentes em contexto isolado: nenhum vínculo de teste vai ao catálogo."""
import json
import subprocess
import time
import urllib.request
from pathlib import Path
from playwright.sync_api import sync_playwright, expect
ROOT=Path(__file__).resolve().parents[1]
server=subprocess.Popen(['python3','-m','http.server','8014','--directory',str(ROOT.parent)],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
try:
    for attempt in range(30):
        try:
            urllib.request.urlopen('http://127.0.0.1:8014/',timeout=1)
            break
        except OSError:
            time.sleep(.1)
    with sync_playwright() as p:
        browser=p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox'])
        page=browser.new_page(accept_downloads=True)
        errors=[]
        page.on('pageerror',lambda error:errors.append(str(error)))
        base=f'http://127.0.0.1:8014/{ROOT.name}/'
        page.goto(base+'README.md')
        old=page.evaluate('''async base=>{
          const {ifrsCatalog}=await import(base+'app/servicos/ifrs.js');
          const source=await (await fetch(base+'dados/fontes/IFRS_Matematica_Questoes_2016_2026.json')).json();
          const old=ifrsCatalog(source);old.questions.forEach(q=>{q.assuntoIds=[];q.assuntosRevisadosEm='2026-10-20T10:00:00Z';});
          const subjectId=old.subjects[0].id;
          old.notes=[{id:'n',subjectId,title:'Caderno V0.3',body:'Nota privada preservada'}];
          old.attempts=[{id:'a',questionId:'IFRS-2016-1-Q01',date:'2026-10-20T12:00:00Z',status:'revisar'}];
          old.events=[{id:'e',date:'2026-10-20T12:00:00Z',subjectId,questionId:'IFRS-2016-1-Q01',type:'Revisão'}];
          old.attachments=[{id:'f',subjectId,name:'privado.txt',type:'text/plain',data:'data:text/plain;base64,cHJpdmFkbw=='}];
          await new Promise(resolve=>{const r=indexedDB.open('estudos-concursos',1);r.onupgradeneeded=()=>r.result.createObjectStore('state');r.onsuccess=()=>{const d=r.result,t=d.transaction('state','readwrite');t.objectStore('state').put(old,'personal');t.oncomplete=()=>{d.close();resolve();};};});
          return old;
        }''',base)
        topics=[s for s in old['subjects'] if s.get('kind')=='editalTopic']
        a,b=topics[:2]
        def nav(label):
            page.locator('nav').get_by_role('button',name=label,exact=True).click()
            page.get_by_role('heading',name=label,exact=True).wait_for()
        def stored():
            return page.evaluate('''()=>new Promise(resolve=>{const r=indexedDB.open('estudos-concursos',1);r.onsuccess=()=>{const d=r.result,q=d.transaction('state').objectStore('state').get('personal');q.onsuccess=()=>{d.close();resolve(q.result);};};})''')
        page.goto(base);nav('Questões')
        expect(page.locator('#questions article')).to_have_count(180)
        assert page.locator('#frequency, .frequency-row').count()==0
        assert not page.locator('#question-filters').evaluate('(d)=>d.open')
        assert page.locator('nav').bounding_box()['x']<page.locator('main').bounding_box()['x']
        expect(page.locator('#question-summary')).to_contain_text('180 questões • 180 classificadas automaticamente')
        assert stored()==old
        assert page.locator('[data-edit-subjects], #thematic-edit, [name=assuntoIds]').count()==0
        layer=json.loads((ROOT/'dados/questoes/classificacao-confirmada.json').read_text())['questions']
        q=next(q for q in layer if q['id']=='IFRS-2016-1-Q01')
        page.locator('#question-filters summary').click()
        page.locator('.filters [name=year]').select_option('2016')
        page.locator('.filters [name=semester]').select_option('1')
        page.locator('.filters [name=status]').select_option('revisar')
        expect(page.locator('#questions article')).to_have_count(1)
        card=page.locator('#questions article').first
        links=card.locator('[data-related-subject]')
        assert links.count()==len(q['assuntoIds'])
        topic=q['assuntoIds'][-1];links.last.click()
        expected=[r['id'] for r in layer if topic in r['assuntoIds']]
        expect(page.locator('#questions article')).to_have_count(len(expected))
        for key in ['year','semester','status','disciplineId','contestId']:
            assert page.locator(f'.filters [name={key}]').input_value()==''
        assert page.locator('.filters [name=subjectId]').input_value()==topic
        assert len({r[5:11] for r in expected})>1
        assert page.locator('#questions article').evaluate_all('(cards)=>cards.map(c=>c.querySelector("p b").textContent)')==expected
        assert stored()==old
        page.reload();nav('Questões');assert stored()==old
        nav('Assuntos')
        expect(page.locator('#frequency .frequency-row')).to_have_count(31)
        page.locator('[name=subjectYear]').select_option('2026')
        page.locator('[name=subjectSemester]').select_option('2')
        expect(page.locator('#frequency')).to_contain_text('10 questões no recorte')
        page.locator('[name=subjectSearch]').fill('Números reais')
        expect(page.locator('#frequency .frequency-row')).to_have_count(1)
        expect(page.locator('#frequency .frequency-row')).to_contain_text('0 de 10 (0.0%)')
        page.locator('#frequency [data-related-subject]').first.click()
        expect(page.locator('#questions article')).to_have_count(len(expected))
        assert page.locator('.filters [name=year]').input_value()==''
        assert page.locator('.filters [name=semester]').input_value()==''
        assert not page.locator('#question-filters').evaluate('(d)=>d.open')
        assert stored()==old
        nav('Backup e importação')
        with page.expect_download() as event:
            page.get_by_role('button',name='Exportar backup JSON',exact=True).click()
        backup=json.loads(Path(event.value.path()).read_text())
        for collection in ['questions','notes','attempts','events','attachments']:
            assert backup[collection]==old[collection]
        nav('Assuntos')
        first=page.locator('#frequency .frequency-row').first
        first.locator('summary').click()
        first.locator('[data-substatus]').select_option('estudando')
        first.get_by_role('button',name='Atualizar situação de estudo').click()
        page.get_by_role('status').get_by_text('Dados salvos neste navegador.').wait_for()
        assert next(s for s in stored()['subjects'] if s['id']==a['id'])['status']=='estudando'
        for collection in ['questions','notes','attempts','events','attachments']:
            assert stored()[collection]==old[collection]
        page.reload();nav('Assuntos')
        expect(page.locator('#frequency .frequency-row').first.locator('[data-substatus]')).to_have_value('estudando')
        page.set_viewport_size({'width':390,'height':844})
        assert page.evaluate('document.documentElement.scrollWidth<=innerWidth')
        nav('Questões');page.set_viewport_size({'width':390,'height':844})
        assert page.evaluate('document.documentElement.scrollWidth<=innerWidth')
        assert not errors,errors
        browser.close()
    print('PASS: classificação automática, múltiplos assuntos, links entre provas sem filtros herdados, ausência de editor, preservação integral de revisões privadas e backup, mobile e Pages.')
finally:
    server.terminate();server.wait()
