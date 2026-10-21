# Importação IFRS — V0.2

Fonte principal: JSON fornecido pelo usuário; CSV e XLSX utilizados na conferência. Não foram consultados documentos externos, provas ou respostas.

180 IDs únicos; 18 provas; 10 questões por prova. 31 tópicos em oito grupos. Classificações: 166 preliminares e 14 com revisão necessária, preservadas integralmente. Todos os assuntos secundários estão vazios na fonte e não foram preenchidos.

## Distribuição das provas

| Prova | Questões |
| --- | ---: |
| 2016/1 | 10 |
| 2016/2 | 10 |
| 2017/1 | 10 |
| 2017/2 | 10 |
| 2018/1 | 10 |
| 2018/2 | 10 |
| 2019/1 | 10 |
| 2019/2 | 10 |
| 2020/1 | 10 |
| 2022/2 | 10 |
| 2023/1 | 10 |
| 2023/2 | 10 |
| 2024/1 | 10 |
| 2024/2 | 10 |
| 2025/1 | 10 |
| 2025/2 | 10 |
| 2026/1 | 10 |
| 2026/2 | 10 |

Não há registros de 2020/2, 2021 ou 2022/1 nos anexos; nenhuma prova foi inventada.

## Frequência original por grupo principal

| Grupo | Questões |
| --- | ---: |
| Conjuntos Numéricos Fundamentais | 12 |
| Funções | 36 |
| Trigonometria | 10 |
| Álgebra | 48 |
| Geometria Espacial | 17 |
| Geometria Analítica | 14 |
| Tratamento da informação | 21 |
| Geometria Plana | 22 |

## Rastreabilidade

SHA-256 dos anexos preservados:

- `IFRS_Matematica_Classificacao_Etapa1.xlsx`: `f81808f08640aeff9020b77b047f9ff9f1648b24240eb0669c4d4e974ba795a5`
- `IFRS_Matematica_Questoes_2016_2026.csv`: `7dbc2689941836f3750bcb788dd6cbfa92e4061809815a5cbb5040309d1d0002`
- `IFRS_Matematica_Questoes_2016_2026.json`: `7295c54a75f59e1f610e026c98a83ed02ea58c5e004a4c976a389ee169b108a7`

Conferência reproduzível: `python3 scripts/conferir_ifrs.py` (openpyxl disponível no ambiente de desenvolvimento). Compara todos os campos e registros, os tópicos e as contagens da planilha. A aplicação não depende dessa biblioteca. PDFs e vínculos específicos entre temas e tópicos oficiais continuam pendentes.
