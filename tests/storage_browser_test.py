"""Dados locais inválidos devem gerar erro explícito, sem apagar o estado."""
from playwright.sync_api import sync_playwright, expect

with sync_playwright() as p:
    browser=p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox'])
    page=browser.new_page()
    page.goto('http://127.0.0.1:8000/README.md')
    old=page.evaluate('''async()=>{
      const {ifrsCatalog}=await import('/app/servicos/ifrs.js');
      const source=await (await fetch('/dados/fontes/IFRS_Matematica_Questoes_2016_2026.json')).json();
      const state=ifrsCatalog(source);
      // Uma lista de vínculos inexistentes era aceita como campo extra pela V0.3.
      state.questions[0].assuntoIds=['vinculo-inexistente'];
      state.notes=[{id:'nota-privada',subjectId:state.subjects[0].id,title:'Preservar',body:'Não apagar'}];
      await new Promise(resolve=>{const r=indexedDB.open('estudos-concursos',1);r.onupgradeneeded=()=>r.result.createObjectStore('state');r.onsuccess=()=>{const d=r.result,t=d.transaction('state','readwrite');t.objectStore('state').put(state,'personal');t.oncomplete=()=>{d.close();resolve();};};});
      return state;
    }''')
    page.goto('http://127.0.0.1:8000/')
    expect(page.get_by_role('status')).to_contain_text('Não foi possível abrir o armazenamento local')
    expect(page.get_by_role('status')).to_contain_text('Vínculo temático exige assunto oficial')
    stored=page.evaluate('''()=>new Promise(resolve=>{const r=indexedDB.open('estudos-concursos',1);r.onsuccess=()=>{const d=r.result,q=d.transaction('state').objectStore('state').get('personal');q.onsuccess=()=>{d.close();resolve(q.result);};};})''')
    assert stored==old
    browser.close()
    print('PASS: erro de validação local sinalizado, sem promessa pendente e sem apagar dados pessoais.')
