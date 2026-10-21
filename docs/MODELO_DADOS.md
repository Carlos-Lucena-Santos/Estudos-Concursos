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

## V0.4 — classificação temática explícita
Cada questão admite `assuntoIds: string[]`, lista de vínculos **confirmados** com entidades `kind: editalTopic` da mesma disciplina, usando exatamente os IDs dos 31 assuntos já cadastrados. `assuntosObservacao` guarda a observação da revisão e `assuntosRevisadosEm` seu horário ISO. Não há ordenação de importância: todos os assuntos associados participam da frequência e da consulta.

A migração acrescenta `assuntoIds: []` em memória apenas aos registros do catálogo IFRS que não possuem o campo. Não grava automaticamente o IndexedDB na abertura, não sobrescreve listas já revisadas e não altera IDs nem campos originais. Backups anteriores sem o campo são aceitos e interpretados como pendentes. A versão do backup continua 1: o acréscimo é opcional e compatível. Os vínculos são persistidos ao salvar e incluídos no backup; reimportar a fonte preserva os registros existentes.

Grupos, temas, `subjectId`, `subsubjectId`, `secondaryIds`, `original`, `classification`, `originalClassification`, `observations` e os indicadores antigos de revisão permanecem como referências históricas. Não são convertidos automaticamente em confirmações oficiais. A interface ativa de Assuntos usa os assuntos oficiais e preserva cadastros pessoais; referências antigas continuam disponíveis aos registros já associados, sem criar novos assuntos.

Frequência: `quantidade = número de questões distintas que contêm o ID em assuntoIds`; `percentual = 100 × quantidade / total selecionado`, ou zero sem questões selecionadas. Todos os filtros ativos são aplicados, incluindo ano, semestre e disciplina. Percentuais independentes podem somar mais de 100%. Pendência significa nenhum vínculo oficial confirmado, não ausência comprovada de um conteúdo. Questões com algum vínculo são contadas como confirmadas para esse indicador, sem presumir que todos os possíveis assuntos tenham sido identificados.

Validação rejeita vínculos para IDs inexistentes, grupos/temas históricos ou outra disciplina. O editor normaliza IDs duplicados e mantém a contagem única por assunto. A consulta oficial considera `assuntoIds`; consultas históricas preservam os vínculos antigos para compatibilidade com o Caderno. Caderno, Diário, Histórico e anexos permanecem associados aos mesmos IDs.

## Camada editorial da V0.4 completa
`dados/questoes/classificacao-confirmada.json` registra uma revisão pública separada: versão da camada, ID da questão, lista de assuntos oficiais, status, justificativa e método de leitura. `classificacao-publica.js` valida cobertura integral e referências, anexando a lista ao catálogo sem alterar os registros originais. A questão recebe `classificacaoPublicaVersao` e `classificacaoPublicaJustificativa` como proveniência da lista padrão.

Ao mesclar, a camada pública completa listas antigas vazias ou ausentes sem revisão pessoal. Uma lista com `assuntosRevisadosEm`, mesmo vazia, permanece intacta; uma lista não vazia importada sem marca de origem pública também é mantida. Uma revisão pública futura só atualiza o que não foi revisado pessoalmente. Notas, histórico, tentativas e anexos não são modificados, e não há gravação automática do banco na abertura.

`recortes-completos.json` associa os 180 IDs a arquivos, páginas e fragmentos, com hashes de integridade. `text` é a extração automática e `textStatus: revisar` explicita suas limitações. A página de abertura do PDF é a verificada nos recortes, inclusive para oito páginas que estavam vazias na fonte antiga, sem substituir esse dado original. `verificacao-completa.json` vincula a inspeção visual aos hashes do PDF e PNG.

## Apresentação automática em Questões
`classifiedCollection(personal, catalog)` projeta os `assuntoIds` preparados do catálogo sobre os mesmos IDs, sem alterar o estado pessoal. A consulta e frequência usam essa projeção. `assuntosObservacao` e `assuntosRevisadosEm` antigos continuam no banco e no backup; não são editados pelo módulo Questões. Novos registros classificados participam da frequência sem atualizar constantes.
