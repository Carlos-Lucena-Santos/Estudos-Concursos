# Importa a base IFRS de Matemática — V0.2

Incorpora as 180 classificações de 18 provas (10 por prova) e os 31 tópicos do Edital 15/2026 fornecidos pelo usuário. JSON é a fonte principal; CSV e XLSX foram conferidos campo a campo e preservados para rastreabilidade. Os IDs, páginas, observações, 166 classificações preliminares e 14 indicadores de revisão permanecem intactos.

Adiciona adaptador estático, carga aditiva por ID, importação manual dos formatos JSON/CSV fornecidos, consulta de questões a partir dos assuntos e frequência por grupo conforme os filtros. A biblioteca distingue tópicos do edital de temas classificados sem inferir associações ausentes. Cadernos, tentativas, histórico e anexos locais são preservados; nenhum PDF, solução ou resposta é incluído.

Validação: 12 testes Node aprovados; conferência dos três anexos aprovada; suites Chromium de regressão e migração V0.1 aprovadas, incluindo dados pessoais, reimportações, filtros, backup, 9 telas móveis e falha de rede; catálogo de 180 questões validado sob /Estudos-Concursos/.

Pendências: PDFs autorizados não fornecidos, revisão humana das classificações sinalizadas e eventual associação explícita entre temas e tópicos oficiais. Sem merge ou publicação automática.
