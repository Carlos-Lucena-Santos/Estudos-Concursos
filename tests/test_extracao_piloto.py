"""Verifica o extrator em diretório temporário, sem mudar recortes revisados."""
import importlib.util
import json
import shutil
import tempfile
import unittest
from pathlib import Path
import fitz

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('extracao', ROOT / 'scripts/extrair_ifrs_2016_1.py')
extractor = importlib.util.module_from_spec(spec)
spec.loader.exec_module(extractor)

class PilotExtraction(unittest.TestCase):
    def test_sem_inspecao_fica_revisar_e_pixels_correspondem_ao_pdf(self):
        with tempfile.TemporaryDirectory() as directory:
            extractor.ROOT = Path(directory)
            extractor.REVIEW = extractor.ROOT / 'verificacao.json'
            destination = extractor.ROOT / extractor.PDF
            destination.parent.mkdir(parents=True)
            shutil.copyfile(ROOT / extractor.PDF, destination)
            result = extractor.extract()
            self.assertEqual(len(result['questions']), 10)
            self.assertTrue(all(q['status'] == 'revisar' for q in result['questions']))
            document = fitz.open(destination)
            for crop in result['questions']:
                original = document[crop['page'] - 1].get_pixmap(matrix=fitz.Matrix(4, 4),clip=fitz.Rect(crop['bbox']),colorspace=fitz.csRGB,alpha=False)
                image = fitz.Pixmap(extractor.ROOT / crop['image'])
                self.assertEqual(image.samples, original.samples)
            # A inspeção registrada do arquivo real permite reproduzir exatamente o status.
            shutil.copyfile(ROOT / 'dados/questoes/IFRS-2016-1-verificacao.json', extractor.REVIEW)
            verified = extractor.extract()
            self.assertTrue(all(q['status'] == 'ok' for q in verified['questions']))
            # Um hash divergente invalida a aprovação daquele recorte.
            review = json.loads(extractor.REVIEW.read_text())
            review['questions']['IFRS-2016-1-Q01']['imageSha256'] = 'invalido'
            extractor.REVIEW.write_text(json.dumps(review))
            changed = extractor.extract()
            self.assertEqual(changed['questions'][0]['status'], 'revisar')
            self.assertEqual(sum(q['status'] == 'ok' for q in changed['questions']), 9)

if __name__ == '__main__':
    unittest.main()
