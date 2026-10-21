"""Piloto restrito ao PDF IFRS 2016/1. Requer PyMuPDF 1.26.6.

Sem OCR, resolução ou interpretação matemática. Regenerar não concede status ok:
este exige inspeção visual registrada e hashes correspondentes à saída atual.
"""
import hashlib
import json
import re
from pathlib import Path
import fitz

ROOT = Path(__file__).resolve().parents[1]
PDF = Path('dados/provas/IFRS-2016-1-Superior.pdf')
OUTPUT = Path('dados/questoes/imagens/2016-1')
META = Path('dados/questoes/IFRS-2016-1-recortes.json')
REVIEW = ROOT / 'dados/questoes/IFRS-2016-1-verificacao.json'

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def extract():
    pdf_hash = sha(ROOT / PDF)
    document = fitz.open(ROOT / PDF)
    markers = []
    started = False
    for index, page in enumerate(document):
        blocks = page.get_text('blocks')
        if 'MATEMÁTICA E SUAS TECNOLOGIAS' in page.get_text() and index > 0:
            started = True
        if not started:
            continue
        stop = False
        for block in blocks:
            match = re.match(r'^(\d{2})\.\s', block[4])
            if not match:
                continue
            number = int(match[1])
            if number == 11:
                stop = True
                break
            if 1 <= number <= 10:
                markers.append((number, index, fitz.Rect(block[:4])))
        if stop:
            break
    if [m[0] for m in markers] != list(range(1, 11)):
        raise ValueError('Marcadores 01 a 10 ausentes, duplicados ou fora de ordem. Nada foi gerado.')
    reviews = json.loads(REVIEW.read_text()) if REVIEW.exists() else {}
    records = []
    (ROOT / OUTPUT).mkdir(parents=True, exist_ok=True)
    for position, (number, index, marker) in enumerate(markers):
        identifier = f'IFRS-2016-1-Q{number:02}'
        page = document[index]
        drawings = page.get_drawings()
        dividers = [d['rect'].x0 for d in drawings if d['rect'].width < 2 and d['rect'].height > page.rect.height * .8]
        if len(dividers) != 1:
            raise ValueError(f'{identifier}: diagramação desconhecida; piloto não deve adivinhar colunas.')
        divider = dividers[0]
        if marker.x0 >= divider:
            raise ValueError(f'{identifier}: início em coluna não suportada pelo piloto.')
        following = markers[position + 1] if position + 1 < len(markers) else None
        limit = following[2].y0 - 6 if following and following[1] == index else page.rect.height - 40
        top = marker.y0 - 5
        region = fitz.Rect(marker.x0 - 5, top, divider - 3, limit)
        content = [fitz.Rect(b[:4]) for b in page.get_text('blocks') if b[1] >= top and b[1] < limit and b[0] < divider and b[3] < page.rect.height - 40]
        # Acrescentar caixas raster e vetoriais integralmente contidas no intervalo.
        visuals = [d['rect'] for d in drawings if d['rect'].height > 2 and d['rect'].width > 2]
        for image in page.get_image_info():
            visuals.append(fitz.Rect(image['bbox']))
        content += [r for r in visuals if r.y0 >= top and r.y1 <= limit and r.x0 < divider]
        bottom = min(limit, max(r.y1 for r in content) + 6)
        clip = fitz.Rect(region.x0, top, region.x1, bottom)
        text = page.get_text(clip=clip)
        alternatives = sorted(set(re.findall(r'(?m)^\(?([A-E])\)', text)))
        reasons = []
        if alternatives != list('ABCDE'):
            reasons.append('Alternativas A–E não confirmadas: possível continuação em coluna/página ou extração textual insuficiente.')
        if any(r.x1 > clip.x1 or r.y1 > clip.y1 for r in content):
            reasons.append('Conteúdo atravessa os limites estimados.')
        # Não recorta silenciosamente conteúdo em outra coluna: sinaliza para revisão.
        right_text = page.get_text(clip=fitz.Rect(divider + 2, top, page.rect.width, bottom)).strip()
        if right_text:
            reasons.append('Conteúdo na coluna adjacente: verificar ordem de leitura/continuação.')
        image_path = OUTPUT / f'{identifier}.png'
        pixmap = page.get_pixmap(matrix=fitz.Matrix(4, 4), clip=clip, colorspace=fitz.csRGB, alpha=False)
        pixmap.save(ROOT / image_path)
        image_hash = sha(ROOT / image_path)
        review = reviews.get('questions', {}).get(identifier, {})
        verified = (not reasons and reviews.get('pdfSha256') == pdf_hash
                    and review.get('imageSha256') == image_hash and review.get('checked') is True)
        records.append({'id': identifier, 'pdf': PDF.as_posix(), 'page': index + 1,
                        'image': image_path.as_posix(), 'status': 'ok' if verified else 'revisar',
                        'bbox': [round(v, 4) for v in clip], 'width': pixmap.width, 'height': pixmap.height,
                        'imageSha256': image_hash, 'parts': [{'page': index + 1, 'bbox': [round(v, 4) for v in clip]}],
                        'possibleContinuation': bool(reasons), 'warnings': reasons,
                        'verification': review.get('method') if verified else 'Inspeção visual pendente.'})
    result = {'version': 1, 'exam': '2016/1', 'pdf': PDF.as_posix(), 'pdfSha256': pdf_hash,
              'source': 'IFRS — Processo Seletivo 2016/1 — Cursos Superiores. Reprodução para fins didáticos, conforme capa.',
              'dpi': 288, 'pymupdf': fitz.VersionBind, 'questions': records}
    (ROOT / META).write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
    print(f'{len(records)} PNGs: {sum(r["status"] == "ok" for r in records)} ok; {sum(r["status"] == "revisar" for r in records)} revisar.')
    return result

if __name__ == '__main__':
    extract()
