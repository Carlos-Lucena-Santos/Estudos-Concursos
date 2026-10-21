"""Confere os 180 PNGs contra os pixels dos fragmentos dos PDFs fornecidos."""
import hashlib,json,unittest
from pathlib import Path
import fitz
from PIL import Image,ImageChops
ROOT=Path(__file__).resolve().parents[1]
class CompletePapers(unittest.TestCase):
 def test_pixels_identidade_e_registro_de_revisao(self):
  metadata=json.loads((ROOT/'dados/questoes/recortes-completos.json').read_text())
  review=json.loads((ROOT/'dados/questoes/verificacao-completa.json').read_text())
  docs={}
  try:
   for q in metadata['questions']:
    with self.subTest(question=q['id']):
     pdf=ROOT/q['pdf'];path=ROOT/q['image'];digest=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
     self.assertEqual(digest(path),review[q['id']]['imageSha256']);self.assertEqual(digest(pdf),review[q['id']]['pdfSha256']);self.assertEqual(review[q['id']]['status'],'ok')
     if q['pdf'] not in docs:docs[q['pdf']]=fitz.open(pdf)
     scale=4 if q['id'].startswith('IFRS-2016-1-') else 3
     images=[]
     for part in q['parts']:
      page=docs[q['pdf']][part['page']-1];rect=fitz.Rect(part['bbox']);self.assertTrue(page.rect.contains(rect))
      pix=page.get_pixmap(matrix=fitz.Matrix(scale,scale),clip=rect,colorspace=fitz.csRGB,alpha=False)
      images.append(Image.frombytes('RGB',(pix.width,pix.height),pix.samples))
     expected=Image.new('RGB',(max(im.width for im in images),sum(im.height for im in images)),'white');y=0
     for im in images:expected.paste(im,(0,y));y+=im.height
     actual=Image.open(path).convert('RGB');self.assertEqual(actual.size,expected.size)
     self.assertIsNone(ImageChops.difference(actual,expected).getbbox())
   self.assertEqual(len(metadata['questions']),180);self.assertEqual(len(docs),18)
  finally:
   for d in docs.values():d.close()
if __name__=='__main__':unittest.main()
