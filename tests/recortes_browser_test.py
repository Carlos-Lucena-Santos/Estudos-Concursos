"""Piloto servido num subdiretório, como no GitHub Pages. Requer Playwright/Chromium."""
import json
import subprocess
import time
import urllib.request
from pathlib import Path
from playwright.sync_api import sync_playwright, expect
ROOT = Path(__file__).resolve().parents[1]
server = subprocess.Popen(['python3','-m','http.server','8013','--directory',str(ROOT.parent)],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
try:
    for attempt in range(30):
        try:
            urllib.request.urlopen('http://127.0.0.1:8013/',timeout=1)
            break
        except OSError:
            time.sleep(.1)
    with sync_playwright() as p:
        browser = p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox'])
        page = browser.new_page(accept_downloads=True)
        errors=[]
        page.on('pageerror',lambda error:errors.append(str(error)))
        base=f'http://127.0.0.1:8013/{ROOT.name}/'
        page.goto(base)
        page.get_by_role('heading',name='Início',exact=True).wait_for()
        page.locator('nav').get_by_role('button',name='Questões',exact=True).click()
        page.locator('.filters [name=year]').select_option('2016')
        page.locator('.filters [name=semester]').select_option('1')
        assert page.locator('#questions article').count()==10
        meta=json.loads((ROOT/'dados/questoes/IFRS-2016-1-recortes.json').read_text())
        for index,crop in enumerate(meta['questions']):
            card=page.locator('#questions article').nth(index)
            assert crop['id'] in card.inner_text()
            image=card.locator('.question-image')
            image.scroll_into_view_if_needed()
            image.evaluate('(img)=>img.decode()')
            assert image.evaluate('(img)=>img.naturalWidth')==crop['width']
            assert image.evaluate('(img)=>img.naturalHeight')==crop['height']
            link=card.get_by_role('link',name=f'Abrir PDF original na página {crop["page"]}')
            assert link.get_attribute('href')==base+crop['pdf']+f'#page={crop["page"]}'
            assert page.request.get(link.get_attribute('href').split('#')[0]).status==200
            card.get_by_role('button',name='Ampliar imagem').click()
            dialog=page.get_by_role('dialog')
            dialog.wait_for(state='visible')
            dialog.locator('img').evaluate('(img)=>img.decode()')
            dialog.get_by_role('button',name='Fechar imagem').click()
            expect(page.locator('dialog')).to_have_count(0)
        page.set_viewport_size({'width':390,'height':844})
        assert page.evaluate('document.documentElement.scrollWidth <= innerWidth')
        page.locator('#questions article').first.get_by_role('button',name='Ampliar imagem').click()
        assert page.get_by_role('dialog').is_visible()
        assert page.evaluate('document.documentElement.scrollWidth <= innerWidth')
        page.keyboard.press('Escape')
        page.locator('#questions article').first.get_by_role('button',name='Registrar tentativa no Diário').click()
        page.get_by_role('heading',name='Diário de questões',exact=True).wait_for()
        assert page.locator('#attempt [name=questionId]').input_value()=='IFRS-2016-1-Q01'
        page.locator('#attempt [name=date]').fill('2026-10-21T10:00')
        page.locator('#attempt [name=observations]').fill('Tentativa do piloto sem conferência.')
        page.locator('#attempt button').click()
        page.locator('article').wait_for()
        page.reload()
        page.locator('nav').get_by_role('button',name='Diário de questões',exact=True).click()
        assert 'Tentativa do piloto' in page.locator('article').inner_text()
        assert not errors,errors
        browser.close()
    print('PASS: 10 imagens decodificadas, 10 ampliações e links PDF/páginas corretos sob subdiretório Pages; viewport 390px; diário e persistência.')
finally:
    server.terminate()
    server.wait()
