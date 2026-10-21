"""Integração real: servidor HTTP na porta 8000, Playwright + Chromium."""
import json
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(executable_path='/usr/bin/chromium', args=['--no-sandbox'])
    context = browser.new_context(accept_downloads=True)
    page = context.new_page()
    errors = []
    page.on('pageerror', lambda error: errors.append(str(error)))
    page.goto('http://127.0.0.1:8000/')
    page.get_by_role('heading', name='Início', exact=True).wait_for()
    def nav(name):
        page.locator('nav').get_by_role('button', name=name, exact=True).click()
        page.get_by_role('heading', name=name, exact=True).wait_for()
    nav('Backup e importação')
    page.get_by_role('button', name='Carregar demonstração opcional').click()
    page.get_by_role('status').get_by_text('Dados salvos neste navegador.').wait_for()
    nav('Questões')
    assert page.locator('#questions article').count() == 181
    page.locator('.filters select[name=contestId]').select_option('ifrs-2027-1')
    assert page.locator('#questions article').count() == 180
    page.locator('.filters select[name=contestId]').select_option('demo-concurso')
    assert page.locator('#questions article').count() == 1
    nav('Caderno de assuntos')
    page.locator('#note [name=title]').fill('Teste persistente')
    page.locator('#note [name=body]').fill('# Conceito\n<script>alert(1)</script>')
    page.locator('#note button').click()
    page.get_by_role('heading', name='Teste persistente').wait_for()
    page.reload()
    nav('Caderno de assuntos')
    page.get_by_role('heading', name='Teste persistente').wait_for()
    assert page.locator('#notes pre').inner_text() == '# Conceito\n<script>alert(1)</script>'
    page.get_by_role('button', name='Editar', exact=True).click()
    page.locator('#note [name=title]').fill('Nota revisada')
    page.locator('#note button').click()
    page.get_by_role('heading', name='Nota revisada').wait_for()
    page.locator('#attachment [name=file]').set_input_files({'name':'pessoal.txt','mimeType':'text/plain','buffer':b'documento local'})
    page.locator('#attachment button').click()
    page.get_by_role('heading', name='pessoal.txt').wait_for()
    nav('Diário de questões')
    for date, status in [('2026-10-18T10:00','estudando'),('2026-10-19T10:00','resolvida')]:
        page.locator('#attempt [name=questionId]').select_option('demo-questao')
        page.locator('#attempt [name=date]').fill(date)
        page.locator('#attempt [name=status]').select_option(status)
        page.locator('#attempt [name=observations]').fill('Tentativa sem conferência')
        page.locator('#attempt button').click()
        page.locator('#attempt [name=date]').wait_for()
        page.wait_for_function("document.querySelector('#attempt [name=date]').value === ''")
    assert page.locator('article').count() == 2
    nav('Histórico de aprendizagem')
    assert page.locator('#events article').count() == 4
    dates = page.locator('#events small').all_text_contents()
    page.locator('.filters [name=from]').fill('2026-10-19')
    page.locator('.filters [name=from]').dispatch_event('change')
    assert page.locator('#events article').count() == 3
    nav('Backup e importação')
    with page.expect_download() as download:
        page.get_by_role('button', name='Exportar backup JSON', exact=True).click()
    backup = json.loads(open(download.value.path()).read())
    assert len(backup['attempts']) == 2 and len(backup['attachments']) == 1
    page.locator('#backup [name=file]').set_input_files({'name':'backup.json','mimeType':'application/json','buffer':json.dumps(backup).encode()})
    page.locator('#backup button').click()
    page.wait_for_function("document.querySelector('#backup [name=file]').files.length === 0")
    with page.expect_download() as download:
        page.get_by_role('button', name='Exportar backup JSON', exact=True).click()
    assert len(json.loads(open(download.value.path()).read())['attempts']) == 2
    invalid = dict(backup, version=99)
    page.locator('#backup [name=file]').set_input_files({'name':'invalid.json','mimeType':'application/json','buffer':json.dumps(invalid).encode()})
    page.locator('#backup button').click()
    page.get_by_role('status').get_by_text('Versão de arquivo incompatível.').wait_for()
    # Substituição cancelada preserva dados; confirmação restaura backup válido.
    for accept in [False, True]:
        page.locator('#backup [name=file]').set_input_files({'name':'backup.json','mimeType':'application/json','buffer':json.dumps(backup).encode()})
        page.locator('#backup [name=mode]').select_option('substituir')
        page.once('dialog', lambda dialog, accept=accept: dialog.accept() if accept else dialog.dismiss())
        page.locator('#backup button').click()
        page.wait_for_timeout(150)
    nav('Início')
    page.locator('[name=activeContest]').select_option('demo-concurso')
    assert 'Resolvidas\n1' in page.locator('#dashboard').inner_text()
    for i, label in enumerate(['Início','Concursos','Disciplinas','Assuntos','Questões','Caderno de assuntos','Diário de questões','Histórico de aprendizagem','Backup e importação']):
        page.set_viewport_size({'width':390,'height':844})
        nav(label)
        page.wait_for_timeout(50)
        assert page.evaluate('document.documentElement.scrollWidth <= innerWidth'), label
        assert not page.locator('main').get_by_text('gabarito', exact=True).count()
    assert not errors, errors
    browser.close()
    print('PASS: filtros, persistência, edição, anexo, tentativas, histórico, backup/restore, segurança do texto e 9 telas em 390px.')
