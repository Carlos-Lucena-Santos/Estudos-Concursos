# Preparação da V0.4

Situação em 21/10/2026: planejamento, sem funcionalidades implementadas nesta etapa. A V0.3 está encerrada e validada pelo usuário no GitHub Pages. Este documento organiza pendências; não autoriza processar arquivos ausentes nem presume que toda a expansão será entregue em uma única versão.

## Base de partida
- 180 questões classificadas, distribuídas por 18 provas, com IDs permanentes.
- 31 tópicos do edital e temas da classificação mantidos separadamente.
- Piloto 2016/1 com dez imagens corretas, visualização e ampliação validadas em produção pelo usuário.
- Classificações originais preservadas: 166 preliminares e 14 com revisão necessária.
- Caderno, Diário, Histórico e dados pessoais locais preservados.

## Pendência: outras 17 provas
Provas presentes no catálogo que ainda não passaram pelo piloto de extração:
2016/2; 2017/1; 2017/2; 2018/1; 2018/2; 2019/1; 2019/2; 2020/1; 2022/2; 2023/1; 2023/2; 2024/1; 2024/2; 2025/1; 2025/2; 2026/1; 2026/2.

Pré-requisitos: receber os PDFs autorizados, conferir identidade e páginas, examinar as diagramações e definir o lote que fará parte da V0.4. O extrator de 2016/1 não está validado para as outras provas. Questões em várias colunas/páginas e documentos digitalizados podem exigir tratamento específico.

Critérios propostos para a expansão: associação aos IDs existentes sem duplicação, recortes completos conferidos individualmente, status `revisar` quando houver dúvida, rastreabilidade por PDF/página/hash e validação das imagens e links no caminho do GitHub Pages. Não processar provas ausentes nem preencher lacunas com dados fictícios.

## Pendência: classificação temática detalhada
Revisar os temas e suas associações a assuntos/subassuntos do edital com base nas questões e nas fontes fornecidas, priorizando os 14 registros sinalizados. A validação dos recortes não constitui revisão temática.

Critérios propostos: manter a classificação original e as observações, registrar separadamente a revisão e sua justificativa, distinguir vínculos confirmados de pendentes e não inferir associações por semelhança de nomes. Não consultar respostas corretas, resolver questões ou modificar classificações silenciosamente.

## Preservação e validação para a próxima etapa
Antes da implementação, confirmar arquivos disponíveis, escopo do lote e critérios de aceite. Durante a futura entrega, manter os IDs, os 31 tópicos, as 180 questões, filtros e vínculos; preservar Caderno, Diário, Histórico, backups e IndexedDB pessoal. Os testes de regressão e de recortes existentes formam a base da validação, complementada pelos novos casos que o escopo exigir.

Código, dados, imagens e PDFs não são alterados pelo encerramento documental da V0.3. A próxima implementação deverá usar branch e PR próprias, sem merge automático.
