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
