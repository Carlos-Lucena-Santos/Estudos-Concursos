# Implementa plataforma pessoal Estudos-Concursos V0.1

O repositório continha apenas uma descrição. Esta versão oferece uma aplicação estática em português para organizar assuntos compartilhados, catálogos de questões, cadernos Markdown, tentativas e eventos de aprendizagem. Os dados pessoais e documentos ficam no IndexedDB, com backup JSON validado e exportação Markdown.

Inclui filtros, dashboard sem estatísticas fictícias, revisões manuais, demonstração opcional separada, layout responsivo e documentação de uso/publicação. Não contém gabaritos, documentos oficiais nem as 180 questões ainda não fornecidas. XLSX exige conversão para CSV/JSON; não há sincronização entre dispositivos.

Validação: seis testes Node aprovados; integração em Chromium com persistência após recarga, múltiplas tentativas, histórico, backups, anexos, texto escapado e nove telas em 390px; carregamento pelo subdiretório /Estudos-Concursos/ confirmado. A CI adicionada executa os testes Node.
