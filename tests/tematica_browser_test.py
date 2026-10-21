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
        def row(topic):
            return page.locator('.frequency-row').filter(has=page.locator(f'[data-frequency-subject="{topic["id"]}"]'))
        def edit(qid,indices):
            page.locator(f'[data-edit-subjects="{qid}"]').click()
            dialog=page.get_by_role('dialog')
            checkboxes=dialog.locator('[name=assuntoIds]')
            assert checkboxes.count()==31
            for i in range(31):
                checkboxes.nth(i).set_checked(i in indices)
            dialog.locator('[name=observation]').fill('Vínculos sintéticos do teste; não são classificação real.')
            dialog.get_by_role('button',name='Salvar vínculos confirmados').click()
            dialog.wait_for(state='detached')
        page.goto(base)
        page.get_by_role('heading',name='Início',exact=True).wait_for()
        assert stored()==old
        nav('Questões')
        assert page.locator('.frequency-row').count()==31
        assert '0 com assuntos confirmados; 180 pendentes' in page.locator('#frequency').inner_text()
        page.locator('.filters [name=year]').select_option('2016')
        page.locator('.filters [name=semester]').select_option('1')
        edit('IFRS-2016-1-Q01',[0,1])
        expect(page.locator('#questions article')).to_have_count(10) # filtros preservados após salvar
        assert '1 de 10 (10.0%)' in row(a).inner_text()
        assert '1 de 10 (10.0%)' in row(b).inner_text()
        assert '1 com assuntos confirmados; 9 pendentes' in page.locator('#frequency').inner_text()
        edit('IFRS-2016-1-Q02',[0])
        assert '2 de 10 (20.0%)' in row(a).inner_text()
        page.locator('.filters [name=semester]').select_option('2')
        assert '0 com assuntos confirmados; 10 pendentes' in page.locator('#frequency').inner_text()
        page.locator('.filters [name=semester]').select_option('1')
        row(b).get_by_role('button').click()
        expect(page.locator('#questions article')).to_have_count(1)
        assert '1 de 1 (100.0%)' in row(a).inner_text()
        assert '1 de 1 (100.0%)' in row(b).inner_text()
        nav('Assuntos')
        page.locator(f'[data-subjectquestions="{b["id"]}"]').click()
        expect(page.locator('#questions article')).to_have_count(1)
        assert 'IFRS-2016-1-Q01' in page.locator('#questions').inner_text()
        page.reload()
        nav('Questões')
        assert '2 com assuntos confirmados; 178 pendentes' in page.locator('#frequency').inner_text()
        result=stored()
        for c in ['notes','attempts','events','attachments','subjects','contests','disciplines']:
            assert result[c]==old[c],c
        assert len(result['questions'])==180
        for q in result['questions']:
            original=next(x for x in old['questions'] if x['id']==q['id'])
            for key,value in original.items():
                if q['id'] in ['IFRS-2016-1-Q01','IFRS-2016-1-Q02'] and key in ['assuntoIds','assuntosObservacao','assuntosRevisadosEm']:continue
                assert q[key]==value,(q['id'],key)
        nav('Backup e importação')
        with page.expect_download() as event:
            page.get_by_role('button',name='Exportar backup JSON',exact=True).click()
        backup=json.loads(Path(event.value.path()).read_text())
        assert len(backup['questions'][0]['assuntoIds'])==2
        page.locator('#catalog [name=file]').set_input_files(ROOT/'dados/fontes/IFRS_Matematica_Questoes_2016_2026.json')
        page.locator('#catalog button').click()
        page.wait_for_function("document.querySelector('#catalog [name=file]').files.length===0")
        assert stored()==result
        nav('Questões')
        # Cancelar não altera dados; remover vínculos devolve a questão à pendência.
        page.locator('[data-edit-subjects="IFRS-2016-1-Q01"]').click()
        page.get_by_role('dialog').get_by_role('button',name='Cancelar').click()
        assert stored()==result
        edit('IFRS-2016-1-Q01',[])
        assert '1 com assuntos confirmados; 179 pendentes' in page.locator('#frequency').inner_text()
        page.set_viewport_size({'width':390,'height':844})
        assert page.evaluate('document.documentElement.scrollWidth<=innerWidth')
        page.locator('[data-edit-subjects="IFRS-2016-1-Q01"]').click()
        assert page.get_by_role('dialog').is_visible()
        assert page.evaluate('document.documentElement.scrollWidth<=innerWidth')
        page.keyboard.press('Escape')
        assert not errors,errors
        browser.close()
    print('PASS: 31 frequências, edição múltipla, filtros e consultas por assunto adicional, cancelamento/remoção, persistência e backup, dados V0.3 preservados, mobile e subdiretório Pages.')
finally:
    server.terminate()
    server.wait()
