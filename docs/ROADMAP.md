# V0.1 e próximos passos
Implementado: navegação, cadastros de concursos/disciplinas/assuntos/subassuntos, catálogo importável e filtros, caderno Markdown com edição e exclusão, anexos locais, diário com várias tentativas, histórico com filtros e revisões manuais, dashboard contextual, backup com mesclagem e substituição confirmada, exportação Markdown.

Limitações explícitas:
- Dados oficiais, PDFs e classificação das 180 questões dependem de arquivos ainda não fornecidos e conferência humana.
- XLSX exige conversão para CSV/JSON. Não há renderização rica de Markdown, editor de fórmulas ou edição completa dos cadastros após criação; catálogos são acrescentados sem substituir IDs.
- IndexedDB é local e sujeito à cota do navegador; anexos usam Base64, aumentando o tamanho do backup. Sem sincronização e sem cache para reabrir offline.
- Dashboard conta assuntos vinculados diretamente ao concurso e situação da tentativa de data mais recente. Não calcula acertos ou erros.
- Revisões são manuais, sem algoritmo de repetição espaçada.
- GitHub Projects/Issues podem acompanhar as tarefas, mas a aplicação não precisa de integração ou token. Criação remota depende de acesso à API.

Próximo marco: receber documentos autorizados, validar o conteúdo programático e importar a base real preservando IDs, fontes e classificações originais. Não publicar PDFs sem autorização.
