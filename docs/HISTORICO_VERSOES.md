# Histórico de versões

## V0.3 — concluída e validada em 21/10/2026
Piloto IFRS 2016/1: PDF original, extração com Python/PyMuPDF, dez PNGs vinculados aos IDs IFRS-2016-1-Q01 a Q10 e metadados de integridade. Módulo Questões com imagens, ampliação, link para a página do PDF e acesso ao Diário.

O usuário confirmou diretamente no GitHub Pages:
- Dez recortes corretos e vinculados aos IDs originais.
- Visualização no módulo Questões e ampliação funcionando.
- [PR #3](https://github.com/Carlos-Lucena-Santos/Estudos-Concursos/pull/3) integrada à `main` e publicação concluída.

As 180 classificações, os 31 tópicos e as funcionalidades anteriores foram preservados. A validação do piloto encerra a entrega de imagens de 2016/1; não conclui a classificação temática detalhada nem o processamento das demais provas. Evidências locais e confirmação do usuário constam em [VALIDACAO.md](VALIDACAO.md) e no [relatório do piloto](PILOTO_IFRS_2016_1.md).

## V0.2 — base IFRS incorporada
180 classificações de 18 provas, dez questões por prova, e 31 tópicos importados a partir dos arquivos fornecidos. JSON, CSV e Excel conferidos. IDs, páginas, observações e classificações originais preservados: 166 preliminares e 14 com revisão necessária. Inclui consulta por assunto e frequência por grupo. [PR #2](https://github.com/Carlos-Lucena-Santos/Estudos-Concursos/pull/2).

## V0.1 — base funcional
Aplicação estática com navegação, biblioteca compartilhada, catálogo, caderno Markdown, diário de tentativas, histórico, dashboard, armazenamento local IndexedDB e exportação/importação de backups. [PR #1](https://github.com/Carlos-Lucena-Santos/Estudos-Concursos/pull/1).

## V0.4 — implementação para revisão
Estrutura `assuntoIds` com múltiplos vínculos confirmados por questão, editor manual e painel de frequência pelos 31 assuntos oficiais existentes, com consulta, percentuais, zeros e pendências. Nenhuma associação automática por nomes: a base inicial possui zero questões confirmadas e 180 pendentes. Classificações originais, dados pessoais, PDF e imagens da V0.3 preservados. Sem novos assuntos ou processamento das demais provas.

Branch `feature/estudos-concursos-v0.4`; merge, publicação e validação em produção permanecem pendentes. Ver [V0.4_TEMATICA.md](V0.4_TEMATICA.md). As outras 17 provas e a revisão temática humana continuam pendências futuras.
