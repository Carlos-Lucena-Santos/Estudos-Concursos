# Modelo e importação
O backup é JSON UTF-8: `version: 1` e arrays `contests`, `disciplines`, `subjects`, `questions`, `notes`, `attempts`, `events`, `attachments`. Todos os registros exigem ID string permanente e único dentro da coleção. Gere UUIDs para registros novos; preserve IDs ao reimportar. Validação implementada em app/servicos/model.js.

| Coleção | Campos |
| --- | --- |
| contests | id, name, notice, institution, campus, course, entry, pending, demo |
| disciplines | id, name |
| subjects | id, name, disciplineId, parentId opcional, noticeTopic, contestIds[], materials, status |
| questions | id, institution, year, semester, number, disciplineId, subjectId, secondaryIds[], subsubjectId opcional, theme, page, source, pdfUrl opcional autorizado, contestIds[], classification, originalClassification |
| notes | id, subjectId, title, body (Markdown) |
| attempts | id, questionId, date (ISO), status, difficulty, observations, reasoning, learned, doubts, concepts, materials, review, duration, result (não conferido) |
| events | id, date (ISO), type, disciplineId, subjectId, questionId opcional, duration, observations, difficulties, review |
| attachments | id, name, type, subjectId, questionId opcional, data (Data URL Base64, até 10 MB) |

Datas de revisão: YYYY-MM-DD. Duração em minutos. Situação de tentativa: não iniciada, estudando, resolvida, revisar. Situação de assunto: não iniciado, estudando, concluído. A classificação original não é substituída pela classificação revisada. A interface não utiliza campos de respostas ou soluções.

## Catálogo
O JSON de referência aceita apenas as quatro primeiras coleções. IDs já existentes são preservados, sem sobrescrita. Referências podem apontar a entidades já locais ou presentes na mesma importação. Importe concursos e disciplinas antes de assuntos; assuntos antes de questões quando usar arquivos separados.

CSV aceita cabeçalho com os mesmos nomes, vírgula ou ponto e vírgula, aspas duplas para escapar texto e listas de IDs separadas por `|`. Escolha a coleção correspondente na interface. Exporte planilhas XLSX para CSV UTF-8 antes de importar; leitura nativa de XLSX não está implementada.

Exemplo de referência **fictícia**:
```json
{"subjects":[{"id":"demo-a","name":"DEMONSTRAÇÃO — assunto fictício","disciplineId":"matematica","contestIds":["ifrs-2027-1"],"status":"não iniciado","demo":true}],"questions":[{"id":"demo-q","number":1,"year":2026,"semester":1,"disciplineId":"matematica","subjectId":"demo-a","contestIds":["ifrs-2027-1"],"classification":"pendente de revisão","originalClassification":"demonstração","demo":true}]}
```
Esse exemplo não é conteúdo oficial. Não é carregado automaticamente.

## Backups
Exportação inclui todas as coleções. Mesclar mantém registros locais de IDs iguais e adiciona os novos; substituir troca todo o estado após confirmação. A validação precede a transação e rejeita estrutura inválida, referências inexistentes, duplicidades internas, ciclos de assuntos, datas inválidas e anexos fora do formato. Não há atualização destrutiva silenciosa. Guarde uma cópia antes de substituir.
