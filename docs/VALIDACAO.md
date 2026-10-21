# Evidência de validação

Os resultados abaixo são registros das respectivas versões.

## V0.1 — validação inicial
Executado no ambiente de desenvolvimento com Node.js 24, Python 3.12 e Chromium real via Playwright.

`npm test`: 6 testes aprovados. Cobrem filtros combinados (concurso, disciplina, ano, semestre, assunto secundário, subassunto, situação), múltiplas tentativas e situação mais recente, ordenação sem mutação, backup e duplicidades, referências inválidas/ciclos/versões e CSV com delimitadores/aspas/quebras de linha.

`python3 tests/browser_test.py`: aprovado. Exercita catálogo demonstrativo separado do IFRS, filtros de concurso, criação/persistência após recarga/edição de notas, texto HTML tratado como texto, anexo local, duas tentativas preservadas, histórico por período, exportação/mesclagem sem duplicação/rejeição de versão inválida, confirmação e cancelamento de substituição, dashboard e ausência de transbordamento horizontal nas nove telas em viewport de 390px. Nenhum erro JavaScript capturado.

A aplicação não contém questões oficiais ou campos de respostas corretas. O teste usa dados demonstrativos e não prova a classificação ou fidelidade de dados oficiais ainda ausentes. Publicação real no GitHub Pages e restauração em uma nova tarefa dependem de ações externas, não são estabelecidas pelo teste local.

Validação adicional em servidor com raiz /workspace: HTML, CSS, módulos e navegação carregaram corretamente pelo caminho /Estudos-Concursos/, reproduzindo a estrutura de URL do GitHub Pages.

## V0.2 — importação IFRS
- `npm test`: 12 testes aprovados, incluindo os seis testes anteriores. Novos testes conferem os 180 IDs e campos originais, 18 provas de 10 questões, 31 tópicos, vínculos por grupo/tema, 14 indicadores de revisão, filtros, frequências, CSV e mesclagem idempotente sem sobrescrita.
- `python3 scripts/conferir_ifrs.py`: todos os campos das 180 questões coincidem entre JSON, CSV e XLSX; os 31 tópicos coincidem entre JSON e XLSX; contagens da aba Estatísticas conferidas.
- `python3 tests/browser_test.py`: aprovado com a base real e demonstração separada; funcionalidades V0.1 preservadas, nove telas em 390px sem transbordamento e sem erros JavaScript.
- `python3 tests/ifrs_browser_test.py`: aprovado; estado V0.1 semeado em IndexedDB, catálogo adicionado sem alteração silenciosa no banco, importações JSON/CSV repetidas sem duplicação, notas/tentativas/eventos/anexos preservados, filtros reais e funcionamento do estado local mesmo em falha de rede.
- Chromium em servidor com raiz /workspace: 180 questões carregadas pelo caminho /Estudos-Concursos/, incluindo o JSON relativo ao módulo.

Não foi feita revisão temática das classificações nem consulta a provas ou respostas. Nenhum PDF é publicado. A integração preserva as classificações dos anexos, não comprova sua correção matemática. Testes usam dados privados sintéticos em contextos isolados, sem acessar o navegador pessoal do usuário.

## V0.3 — piloto de imagens
As três suítes Chromium, o teste Python do extrator e os 14 testes Node passaram. Os dez PNGs foram também inspecionados visualmente contra o PDF. Detalhes, limites e critérios para status `ok` estão em [PILOTO_IFRS_2016_1.md](PILOTO_IFRS_2016_1.md). Não houve modificação dos arquivos originais da V0.2 nem publicação remota.

## Encerramento da V0.3 — 21/10/2026
Validação realizada pelo usuário diretamente no GitHub Pages, conforme confirmação nesta data:
- Dez questões recortadas corretamente como PNG e vinculadas aos IDs originais.
- Visualização no módulo Questões e ampliação funcionando.
- PR #3 integrada à `main` e publicação concluída.

A V0.3 está concluída e validada para o piloto IFRS 2016/1. Esta confirmação complementa os testes locais registrados acima; não representa nova execução das suítes de navegador nesta atualização documental. A classificação temática detalhada e as outras 17 provas não fazem parte do escopo encerrado e permanecem pendentes.

Na atualização documental de encerramento, `npm test` foi executado novamente: 14 testes aprovados.

## V0.4 — vínculos oficiais e frequência temática
`npm test`: 22 testes aprovados. Incluem os casos anteriores, o novo contrato de frequência dos 31 assuntos e oito testes temáticos de múltiplos vínculos, contagem única, percentuais, filtros, consulta, edição/remoção, validação, compatibilidade e preservação.

As quatro suítes Chromium passaram: `tests/tematica_browser_test.py`, `tests/browser_test.py`, `tests/ifrs_browser_test.py` e `tests/recortes_browser_test.py`. A suíte temática usa vínculos sintéticos em contexto isolado, confirma editor com 31 opções, consultas de assuntos adicionais pelos módulos Questões/Assuntos, filtros preservados ao salvar, cancelamento, remoção, persistência, backup, reimportação e preservação do estado V0.3. Inclui viewport 390px e caminho sob subdiretório como no Pages. As demais cobrem regressões de módulos, dados e as dez imagens com ampliação/PDF.

Na base pública fornecida, 0 questões têm vínculos oficiais confirmados e 180 estão pendentes. Nenhum dado sintético do teste foi salvo no repositório. A comparação com `origin/main` confirmou que fontes Excel/CSV/JSON, PDF, imagens e metadados de recortes estão inalterados. A publicação e a validação em produção da V0.4 permanecem pendentes.

## Revisão da PR #5
Os 22 testes Node, a conferência dos três anexos, o teste Python do extrator e cinco suítes Chromium passaram. Foi corrigida a rejeição da promessa de leitura IndexedDB em caso de validação inválida, com teste de regressão e preservação do estado. Na etapa inicial, a equivalência dos 31 tópicos com o edital ficou pendente de acesso ao documento primário; essa pendência foi resolvida pelo complemento abaixo. Evidências e parecer em [REVISAO_PR_5.md](REVISAO_PR_5.md).

Complemento da revisão da PR #5: o edital foi posteriormente anexado e a seção de Matemática (Anexo VIII, p. 102–103) conferida por extração textual e inspeção visual. Os 31 registros têm correspondência documentada com toda a seção; seus títulos são resumos, não cópia literal. A pendência de fonte primária foi resolvida. Ver [CONFERENCIA_EDITAL_MATEMATICA.md](CONFERENCIA_EDITAL_MATEMATICA.md). Nenhum vínculo de questão foi confirmado automaticamente.

## V0.4 completa — 18 provas
Nesta etapa, a nova camada editorial passa a confirmar 180 questões, com 287 vínculos nos 31 assuntos, substituindo o estado público inicial de zero vínculos descrito nas etapas históricas acima.

Validação executada: 27 testes Node; dois testes Python (reprodução do piloto e comparação pixel a pixel dos fragmentos das 180 imagens); seis suítes Chromium (módulos, IFRS, armazenamento, recortes, temática e catálogo completo). A suíte completa verifica as 18 provas, filtros, frequência dos 31 assuntos, carregamento de 180 PNGs/18 PDFs, persistência de revisão pessoal e ausência de gravação automática ao abrir a aplicação. A conferência JSON/CSV/XLSX também passou.

Inspeção visual: 180 recortes aprovados; oito questões com múltiplos fragmentos. A transcrição automática continua marcada para revisão. Originais da V0.2 e arquivos do piloto preservados. Relatório e frequências em [V0.4_COMPLETA.md](V0.4_COMPLETA.md). Publicação no GitHub Pages depende da integração da entrega; não foi realizado merge automático.

## Validação final da PR #6
Reexecução: 28 casos Node, dois testes Python, conferência dos três arquivos-fonte e seis suítes Chromium aprovados. Teste ampliado decodifica as 180 imagens no site local e confronta os filtros combinados de ano, semestre e assunto. Duas imprecisões de texto corrigidas; dois enquadramentos temáticos amplos documentados para eventual refinamento pedagógico. Acesso à produção bloqueado por HTTP 403 do ambiente. Parecer e limites em [REVISAO_PR_6.md](REVISAO_PR_6.md). Sem merge automático.

## Questões — classificação automática a partir dos dados editoriais
Validados 30 casos individuais Node (`node --test --test-isolation=none tests/*.test.js`), `npm test` (seis arquivos aprovados), dois testes Python e seis suítes Chromium. A suíte temática agora valida a ausência de controles de edição, múltiplos links por questão, consulta entre provas após limpar filtros e preservação integral das revisões antigas no banco e backup. A suíte IFRS passou a contar especificamente links PDF, pois os cartões também contêm links temáticos. A suíte completa decodifica os 180 PNGs e verifica os 18 PDFs. A conferência JSON/CSV/XLSX e dos 31 assuntos passou; nenhum arquivo em `dados/` foi modificado nesta alteração. Regras atuais em [QUESTOES_AUTOMATICAS.md](QUESTOES_AUTOMATICAS.md).
