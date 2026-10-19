# Evidência de validação
Executado no ambiente de desenvolvimento com Node.js 24, Python 3.12 e Chromium real via Playwright.

`npm test`: 6 testes aprovados. Cobrem filtros combinados (concurso, disciplina, ano, semestre, assunto secundário, subassunto, situação), múltiplas tentativas e situação mais recente, ordenação sem mutação, backup e duplicidades, referências inválidas/ciclos/versões e CSV com delimitadores/aspas/quebras de linha.

`python3 tests/browser_test.py`: aprovado. Exercita catálogo demonstrativo separado do IFRS, filtros de concurso, criação/persistência após recarga/edição de notas, texto HTML tratado como texto, anexo local, duas tentativas preservadas, histórico por período, exportação/mesclagem sem duplicação/rejeição de versão inválida, confirmação e cancelamento de substituição, dashboard e ausência de transbordamento horizontal nas nove telas em viewport de 390px. Nenhum erro JavaScript capturado.

A aplicação não contém questões oficiais ou campos de respostas corretas. O teste usa dados demonstrativos e não prova a classificação ou fidelidade de dados oficiais ainda ausentes. Publicação real no GitHub Pages e restauração em uma nova tarefa dependem de ações externas, não são estabelecidas pelo teste local.

Validação adicional em servidor com raiz /workspace: HTML, CSS, módulos e navegação carregaram corretamente pelo caminho /Estudos-Concursos/, reproduzindo a estrutura de URL do GitHub Pages.
