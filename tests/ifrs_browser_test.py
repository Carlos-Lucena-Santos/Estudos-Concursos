"""Migração de estado V0.1, reimportação dos anexos e caminhos Pages em Chromium."""
import json
from pathlib import Path
from playwright.sync_api import sync_playwright
ROOT = Path(__file__).resolve().parents[1]
with sync_playwright() as p:
    browser = p.chromium.launch(executable_path='/usr/bin/chromium', args=['--no-sandbox'])
    context = browser.new_context(accept_downloads=True)
    page = context.new_page()
    errors = []
    page.on('pageerror', lambda error: errors.append(str(error)))
    # Página da mesma origem antes de executar o aplicativo para semear estado V0.1.
    page.goto('http://127.0.0.1:8000/README.md')
    old = {'version':1,'contests':[{'id':'pessoal','name':'Concurso pessoal'}],
           'disciplines':[{'id':'minha-disciplina','name':'Minha disciplina'}],
           'subjects':[{'id':'meu-assunto','name':'Meu assunto','disciplineId':'minha-disciplina','status':'concluído'}],
           'questions':[{'id':'minha-questao','number':9,'disciplineId':'minha-disciplina','subjectId':'meu-assunto','pdfUrl':'https://example.org/p.pdf'}],
           'notes':[{'id':'minha-nota','title':'Nota privada V0.1','body':'Texto privado','subjectId':'meu-assunto'}],
           'attempts':[{'id':'tentativa-antiga','questionId':'minha-questao','date':'2026-10-18T12:00:00Z','status':'revisar'}],
           'events':[{'id':'evento-antigo','questionId':'minha-questao','subjectId':'meu-assunto','date':'2026-10-18T12:00:00Z','type':'Revisão'}],
           'attachments':[{'id':'anexo-antigo','subjectId':'meu-assunto','name':'privado.txt','type':'text/plain','data':'data:text/plain;base64,cHJpdmFkbw=='}]}
    page.evaluate('''state => new Promise((resolve,reject)=>{const r=indexedDB.open('estudos-concursos',1);r.onupgradeneeded=()=>r.result.createObjectStore('state');r.onsuccess=()=>{const d=r.result,t=d.transaction('state','readwrite');t.objectStore('state').put(state,'personal');t.oncomplete=()=>{d.close();resolve();};t.onerror=()=>reject(t.error);};})''',old)
    page.goto('http://127.0.0.1:8000/')
    page.get_by_role('heading',name='Início',exact=True).wait_for()
    def nav(label):
        page.locator('nav').get_by_role('button',name=label,exact=True).click()
        page.get_by_role('heading',name=label,exact=True).wait_for()
    def backup():
        nav('Backup e importação')
        with page.expect_download() as event:
            page.get_by_role('button',name='Exportar backup JSON',exact=True).click()
        return json.loads(Path(event.value.path()).read_text())
    # Abrir V0.2 mescla em memória e não substitui o estado persistido silenciosamente.
    stored=page.evaluate('''() => new Promise(resolve=>{const r=indexedDB.open('estudos-concursos',1);r.onsuccess=()=>{const d=r.result,q=d.transaction('state').objectStore('state').get('personal');q.onsuccess=()=>{d.close();resolve(q.result);};};})''')
    assert stored == old
    result=backup()
    assert len(result['questions']) == 181
    for collection in ['notes','attempts','events','attachments']:
        assert result[collection] == old[collection]
    for collection in ['contests','disciplines','subjects','questions']:
        for row in old[collection]:
            assert next(x for x in result[collection] if x['id']==row['id']) == row
    # Reimportar ambos os formatos reais, duas vezes, não duplica IDs nem apaga dados.
    for extension in ['json','csv','json','csv']:
        page.locator('#catalog [name=file]').set_input_files(ROOT/'dados'/'fontes'/f'IFRS_Matematica_Questoes_2016_2026.{extension}')
        page.locator('#catalog button').click()
        page.wait_for_function("document.querySelector('#catalog [name=file]').files.length === 0")
    assert backup() == result
    nav('Questões')
    page.locator('#question-filters summary').click()
    page.locator('.filters [name=disciplineId]').select_option('matematica')
    assert page.locator('#questions article').count()==180
    page.locator('.filters [name=year]').select_option('2016')
    page.locator('.filters [name=semester]').select_option('1')
    assert page.locator('#questions article').count()==10
    assert 'IFRS-2016-1-Q01' in page.locator('#questions').inner_text()
    assert 'Página 2' in page.locator('#questions').inner_text()
    assert page.locator('#questions .question-original a').count()==10 # Dez PDFs; links temáticos são verificados separadamente.
    nav('Assuntos')
    page.locator('#frequency [data-related-subject]').first.click()
    page.get_by_role('heading',name='Questões',exact=True).wait_for()
    nav('Caderno de assuntos')
    page.get_by_role('heading',name='Nota privada V0.1',exact=True).wait_for()
    nav('Diário de questões')
    assert 'revisar' in page.locator('article').inner_text()
    page.reload()
    assert backup() == result
    # Falha de rede do catálogo não bloqueia o uso do estado local.
    page.route('**/dados/fontes/*.json',lambda route:route.abort())
    page.reload()
    page.get_by_role('heading',name='Início',exact=True).wait_for()
    assert 'Catálogo IFRS indisponível' in page.get_by_role('status').inner_text()
    nav('Caderno de assuntos')
    page.get_by_role('heading',name='Nota privada V0.1',exact=True).wait_for()
    assert not errors,errors
    browser.close()
    print('PASS: migração V0.1 sem sobrescrita, 180 questões, filtros reais, reimportação JSON/CSV idempotente e dados pessoais preservados após recarga/falha de rede.')
