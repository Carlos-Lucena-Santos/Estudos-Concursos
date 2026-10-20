"""Confere os três anexos sem dependências de produção. Requer openpyxl para o teste."""
import csv
import json
from collections import Counter
from pathlib import Path
from openpyxl import load_workbook

root = Path(__file__).resolve().parents[1] / 'dados' / 'fontes'
source = json.loads((root / 'IFRS_Matematica_Questoes_2016_2026.json').read_text())
with (root / 'IFRS_Matematica_Questoes_2016_2026.csv').open(encoding='utf-8-sig', newline='') as f:
    csv_rows = list(csv.DictReader(f, delimiter=';'))
book = load_workbook(root / 'IFRS_Matematica_Classificacao_Etapa1.xlsx', read_only=True, data_only=True)
def sheet(name):
    rows = list(book[name].values)
    return [dict(zip(rows[0], row)) for row in rows[1:]]
def normalize(rows):
    return [{k: '' if v is None else str(v) for k, v in r.items()} for r in rows]
rows = source['classificacoes']
assert normalize(rows) == normalize(csv_rows) == normalize(sheet('Questões'))
assert source['conteudo_programatico'] == [
    {'grupo': r['Grupo do edital'], 'topico': r['Tópico do edital - síntese fiel']}
    for r in sheet('Conteúdo programático')
]
assert len(rows) == len({r['ID'] for r in rows}) == 180
exams = Counter(r['Prova'] for r in rows)
assert len(exams) == 18 and set(exams.values()) == {10}
counts = Counter(r['Grupo do edital'] for r in rows)
for r in sheet('Estatísticas'):
    if r['Grupo do edital'] in counts:
        assert r['Questões classificadas'] == counts[r['Grupo do edital']]
print('PASS: 180 questões idênticas em JSON/CSV/XLSX; 31 tópicos JSON/XLSX; estatísticas Excel conferidas.')
for exam, count in exams.items():
    print(f'{exam}: {count}')
print(dict(Counter(r['Confiança'] for r in rows)))
