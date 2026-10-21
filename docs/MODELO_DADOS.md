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

## Adaptador IFRS — V0.2
`dados/fontes/IFRS_Matematica_Questoes_2016_2026.json` é carregado automaticamente. O JSON original e o CSV com cabeçalhos portugueses também são aceitos na importação manual. O Excel é somente conferência, não é necessário ao navegador.

Mapeamento: ID → id (inalterado); Prova → exam; Ano/Semestre/Questão → year/semester/number; Grupo do edital → subjectId e originalClassification; Assunto específico → theme e subsubjectId; Assunto secundário → secondaryIds (sem inferir grupo); Página PDF → page; Arquivo PDF → source; Confiança → classification; Observações → observations. O objeto `original` conserva todos os campos da linha original. `reviewRequired` indica exatamente a marca “Revisão necessária”.

`kind` de assunto: editalGroup, editalTopic ou classificationTheme. Os IDs usam texto original codificado, incluindo grupo no identificador para evitar homônimos. Os 31 tópicos são filhos dos oito grupos. Os temas da classificação também são filhos do grupo informado, sem afirmar que correspondem a um dos tópicos oficiais. Consultar um tópico sem associação explícita retorna zero questões; selecionar um grupo ou tema consulta os vínculos fornecidos. Cadernos podem pertencer a qualquer um desses assuntos.

A migração não altera nem remove IDs existentes, mesmo em conflito com o catálogo. Anotações, tentativas, eventos, anexos e situação de estudo são preservados. Catálogos e dados pessoais continuam separados em suas fontes: só o JSON público é servido; o IndexedDB nunca é enviado para o repositório. A exportação inclui o estado mesclado.
