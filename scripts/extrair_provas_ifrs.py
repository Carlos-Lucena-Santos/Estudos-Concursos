"""Extrai as provas fornecidas sem resolver questões. PyMuPDF + Pillow.
OCR (Tesseract eng) serve à localização; imagem original permanece autoritativa.
Status ok depende de revisão registrada do PNG/PDF exatos; nunca só da heurística.
"""
import hashlib,json,re
from pathlib import Path
import fitz
from PIL import Image
ROOT=Path(__file__).resolve().parents[1]
CACHE=Path('/tmp/ifrs-ocr-cache');CACHE.mkdir(exist_ok=True)

def digest(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def pages_data(doc,pdf):
    data=[];started=False;seen=set()
    for i,page in enumerate(doc):
        if i>12:break
        blocks=page.get_text('blocks');ocr=False
        if not blocks and i>0:
            cache=CACHE/f'{digest(pdf)[:16]}-{i}.json'
            if cache.exists():blocks=json.loads(cache.read_text())
            else:
                tp=page.get_textpage_ocr(language='eng',dpi=220,full=True,tessdata='/usr/share/tesseract-ocr/5/tessdata')
                blocks=page.get_text('blocks',textpage=tp);cache.write_text(json.dumps(blocks))
            ocr=True
        markers=[]
        words=page.get_text('words') if not ocr else []
        for b in blocks:
            # Exact two-digit headings; OCR can read a dot as comma.
            m=re.match(r'^\s*(\d{2})[.,]\s',b[4])
            if m and 1<=int(m[1])<=11 and b[1]<page.rect.height-45:
                actual=[w for w in words if w[4]==m[1]+'.' and abs(w[0]-b[0])<9 and b[1]-1<=w[1]<=b[3]]
                y=actual[0][1] if actual else b[1]
                markers.append({'n':int(m[1]),'y':y,'x':b[0],'bbox':b[:4]})
        if not started and any(m['n']==1 for m in markers):started=True
        if not started:continue
        if any(m['n']==11 for m in markers):break
        if not markers and len(seen)==10:break
        seen.update(m['n'] for m in markers)
        markers.sort(key=lambda m:m['n'])
        mid=page.rect.width/2
        wide=any(m['bbox'][0]<mid and m['bbox'][2]>mid+40 for m in markers)
        right=any(m['x']>mid for m in markers) or (not wide and any(b[0]>mid and len(b[4].strip())>35 and 24<b[1]<page.rect.height-24 for b in blocks))
        right_images=any(r['bbox'][0]>mid and r['bbox'][2]-r['bbox'][0]>50 and r['bbox'][3]-r['bbox'][1]>50 for r in page.get_image_info()) if not ocr else False
        right=right or (right_images and not wide)
        # Diagramações conferidas nas páginas originais: alternativas gráficas/matemáticas.
        forced={(2017,1,2),(2023,2,6),(2024,2,3)}
        year,semester=map(int,re.search(r'(\d{4})-([12])',pdf.name).groups())
        if (year,semester,i+1) in forced:right=True
        for marker in markers:
            col=1 if marker['x']>mid else 0
            candidates=[b for b in blocks if b[4].strip() and b[1]>20 and b[1]<marker['y'] and (b[0]>mid)==bool(col) and not re.search(r'IFRS|MATEM.TICA E SUAS',b[4])]
            earlier=any(other['n']<marker['n'] and (other['x']>mid)==bool(col) for other in markers)
            lines=[d['rect'] for d in page.get_drawings() if d['rect'].width>150 and d['rect'].height<3 and marker['y']-45<d['rect'].y0<marker['y']-3 and (d['rect'].x0>mid)==bool(col)]
            marker['top']=max(r.y1 for r in lines)+1 if lines else marker['y']-16
            if not earlier and marker['y']<100 and candidates and not lines:marker['top']=min(marker['top'],min(b[1] for b in candidates)-4)
        data.append({'page':i+1,'blocks':blocks,'markers':markers,'columns':2 if right else 1,'ocr':ocr})
    return data

def extract(pdf):
    exam=re.search(r'(\d{4}-[12])',pdf.name)[1];doc=fitz.open(pdf);pages=pages_data(doc,pdf)
    markers=[(p,m) for p in pages for m in p['markers']]
    markers.sort(key=lambda pair:pair[1]['n'])
    if [m['n'] for p,m in markers]!=list(range(1,11)):raise ValueError(f'{exam}: marcadores encontrados {[m["n"] for p,m in markers]}')
    records=[]
    for idx,(start,m) in enumerate(markers):
        end,nextm=markers[idx+1] if idx<9 else (start,None)
        parts=[];texts=[];images=[]
        for pd in pages:
            if not start['page']<=pd['page']<=end['page']:continue
            page=doc[pd['page']-1];mid=page.rect.width/2
            startcol=1 if m['x']>mid else 0
            endcol=1 if nextm and nextm['x']>mid else 0
            for col in range(pd['columns']):
                if pd['page']==start['page'] and col<startcol:continue
                if nextm and pd['page']==end['page'] and col>endcol:continue
                top=m['top'] if pd['page']==start['page'] and col==startcol else 24
                bottom=nextm['top']-1 if nextm and pd['page']==end['page'] and col==endcol else page.rect.height-24
                if bottom<=top:continue
                if nextm and pd['page']==end['page'] and col==endcol and nextm['y']<100 and not (pd['page']==start['page'] and col==startcol):continue
                left=mid+3 if col else 20
                right=page.rect.width-24 if pd['columns']==1 or col else mid-3
                # Markers can be insets within the text frame. Collect all content boxes.
                box=fitz.Rect(left,top,right,bottom)
                blocks=[b for b in pd['blocks'] if b[4].strip() and not (b[1]>page.rect.height-45 and re.fullmatch(r'\s*\[?\d+\]?\s*',b[4])) and not re.search(r'IFRS\s*[–—-].*Cursos Superiores|^MATEM.TICA E SUAS TECNOLOGIAS',b[4]) and b[3]>top and b[1]<bottom and b[0]<right and b[2]>left and b[3]<page.rect.height-18]
                if not blocks:continue
                visual=[]
                if not pd['ocr']:
                    visual=[d['rect'] for d in page.get_drawings() if d['rect'].width>3 and d['rect'].height>3]
                    visual += [fitz.Rect(d['bbox']) for d in page.get_image_info()]
                    visual=[r for r in visual if r.y0>=top and r.y1<=bottom and r.x0>=left-3 and r.x1<=right+3]
                rects=[fitz.Rect(b[:4]) for b in blocks]+visual
                # Blank continuation slots are discarded only if they have no content.
                x0=max(left,min(r.x0 for r in rects)-5);x1=min(right,max(r.x1 for r in rects)+5)
                y1=min(bottom,max(r.y1 for r in rects)+15)
                clip=fitz.Rect(x0,top,x1,y1)
                pix=page.get_pixmap(matrix=fitz.Matrix(3,3),clip=clip,colorspace=fitz.csRGB,alpha=False)
                images.append(Image.frombytes('RGB',(pix.width,pix.height),pix.samples))
                parts.append({'page':pd['page'],'bbox':list(clip),'width':pix.width,'height':pix.height,'ocr':pd['ocr']})
                texts.append('\n'.join(b[4] for b in blocks))
        if not images:raise ValueError(f'{exam} Q{idx+1}: nenhum fragmento')
        canvas=Image.new('RGB',(max(im.width for im in images),sum(im.height for im in images)), 'white')
        y=0
        for im in images:canvas.paste(im,(0,y));y+=im.height
        identifier=f'IFRS-{exam}-Q{idx+1:02}'
        dest=ROOT/f'dados/questoes/imagens/{exam}/{identifier}.png';dest.parent.mkdir(parents=True,exist_ok=True);canvas.save(dest,compress_level=6)
        records.append({'id':identifier,'pdf':str(pdf.relative_to(ROOT)),'page':start['page'],'pages':sorted(set(p['page'] for p in parts)), 'image':str(dest.relative_to(ROOT)), 'status':'revisar','parts':parts,'width':canvas.width,'height':canvas.height,'imageSha256':digest(dest),'pdfSha256':digest(pdf),'text':'\n'.join(texts),'textStatus':'revisar','warnings':['OCR em inglês: confira transcrição contra imagem.'] if any(p['ocr'] for p in parts) else [],'verification':'Revisão visual pendente.'})
    return records

def main():
    # Preserva os dez recortes e a revisão do piloto original.
    pilot=json.loads((ROOT/'dados/questoes/IFRS-2016-1-recortes.json').read_text())
    records=[]
    for pdf in sorted((ROOT/'dados/provas').glob('*.pdf')):
        if '2016-1-' in pdf.name:
            for crop in pilot['questions']:
                record=dict(crop);record['pdfSha256']=pilot['pdfSha256'];record['pages']=[crop['page']]
                record['text']='\n'.join(fitz.open(pdf)[crop['page']-1].get_text(clip=fitz.Rect(part['bbox'])) for part in crop['parts']);record['textStatus']='revisar';records.append(record)
            continue
        extracted=extract(pdf);records.extend(extracted);print(pdf.name,len(extracted),flush=True)
    reviewpath=ROOT/'dados/questoes/verificacao-completa.json'
    review=json.loads(reviewpath.read_text()) if reviewpath.exists() else {}
    for record in records:
        proof=review.get(record['id'],{})
        if proof.get('imageSha256')==record['imageSha256'] and proof.get('pdfSha256')==record['pdfSha256']:
            record['status']=proof['status'];record['verification']=proof['verification']
    output={'version':1,'questions':records}
    (ROOT/'dados/questoes/recortes-completos.json').write_text(json.dumps(output,ensure_ascii=False,indent=2)+'\n')
    print('TOTAL',len(records),flush=True)
if __name__=='__main__':main()
