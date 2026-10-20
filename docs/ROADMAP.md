# V0.1 e próximos passos
Implementado: navegação, cadastros de concursos/disciplinas/assuntos/subassuntos, catálogo importável e filtros, caderno Markdown com edição e exclusão, anexos locais, diário com várias tentativas, histórico com filtros e revisões manuais, dashboard contextual, backup com mesclagem e substituição confirmada, exportação Markdown.

Limitações explícitas:
- V0.2: as 180 classificações e 31 tópicos dos arquivos fornecidos estão incorporados. PDFs continuam ausentes. Há 14 classificações com revisão necessária e 166 preliminares; a conferência temática humana permanece pendente.
- XLSX exige conversão para CSV/JSON. Não há renderização rica de Markdown, editor de fórmulas ou edição completa dos cadastros após criação; catálogos são acrescentados sem substituir IDs.
- IndexedDB é local e sujeito à cota do navegador; anexos usam Base64, aumentando o tamanho do backup. Sem sincronização e sem cache para reabrir offline.
- Dashboard conta assuntos vinculados diretamente ao concurso e situação da tentativa de data mais recente. Não calcula acertos ou erros.
- Revisões são manuais, sem algoritmo de repetição espaçada.
- GitHub Projects/Issues podem acompanhar as tarefas, mas a aplicação não precisa de integração ou token. Criação remota depende de acesso à API.

Próximo marco: receber PDFs autorizados e revisar as classificações sinalizadas sem alterar a fonte original. Não publicar PDFs sem autorização.
