# Roadmap — V0.4 completa preparada para revisão
**Situação em 21/10/2026:** V0.3 concluída, com piloto validado pelo usuário no GitHub Pages, PR #3 integrada à `main` e publicação concluída. Histórico em [HISTORICO_VERSOES.md](HISTORICO_VERSOES.md).

Implementado: navegação, cadastros de concursos/disciplinas/assuntos/subassuntos, catálogo importável e filtros, caderno Markdown com edição e exclusão, anexos locais, diário com várias tentativas, histórico com filtros e revisões manuais, dashboard contextual, backup com mesclagem e substituição confirmada, exportação Markdown.

Limitações explícitas:
- V0.2: as 180 classificações e 31 tópicos dos arquivos fornecidos estão incorporados. Os 18 PDFs e 180 recortes foram incorporados na entrega V0.4 completa. As classificações originais permanecem preservadas; uma camada editorial revisada contém 287 vínculos para as 180 questões.
- XLSX exige conversão para CSV/JSON. Não há renderização rica de Markdown, editor de fórmulas ou edição completa dos cadastros após criação; catálogos são acrescentados sem substituir IDs.
- IndexedDB é local e sujeito à cota do navegador; anexos usam Base64, aumentando o tamanho do backup. Sem sincronização e sem cache para reabrir offline.
- Dashboard conta assuntos vinculados diretamente ao concurso e situação da tentativa de data mais recente. Não calcula acertos ou erros.
- Revisões são manuais, sem algoritmo de repetição espaçada.
- GitHub Projects/Issues podem acompanhar as tarefas, mas a aplicação não precisa de integração ou token. Criação remota depende de acesso à API.

V0.4 completa preparada para revisão: múltiplos vínculos nos 31 assuntos, frequência específica, 18 PDFs e 180 imagens conferidas. Relatório em [V0.4_COMPLETA.md](V0.4_COMPLETA.md). Próximo marco: revisar e integrar a branch, publicar pelo GitHub Pages e validar em produção. Pendências futuras: revisão da transcrição automática (especialmente fórmulas/OCR) e eventuais ajustes pedagógicos da classificação pelo editor existente. Os PDFs recebidos foram incorporados conforme autorização do usuário; nenhuma outra prova foi buscada.
