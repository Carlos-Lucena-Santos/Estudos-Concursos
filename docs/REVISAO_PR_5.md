# Revisão da PR #5 — V0.4

Revisão em 21/10/2026, na branch `feature/estudos-concursos-v0.4`, sem merge. O ref remoto `refs/pull/5/head` correspondeu ao commit `ccca0bd91f5c484f61156ef9a552abf869f7a681`, usado como início da revisão.

## Resultado por requisito

| Verificação | Resultado |
| --- | --- |
| 31 assuntos exatamente iguais ao edital oficial | **Conferido com o PDF posteriormente anexado**, Anexo VIII, p. 102–103. Os 31 registros cobrem o conteúdo por subdivisões compatíveis. Os nomes são títulos resumidos, não transcrição literal nem enumeração oficial. Ver a matriz de correspondência em CONFERENCIA_EDITAL_MATEMATICA.md. |
| 180 questões e múltiplos vínculos | Aprovado: 180 IDs únicos, 18 provas com dez registros cada; campos originais, observações e páginas preservados. `assuntoIds` aceita vários assuntos oficiais da mesma disciplina. |
| Frequência sem duplicação | Aprovado: uma questão conta uma vez por assunto, mesmo quando a lista de entrada contém IDs repetidos. Percentuais usam o total selecionado; podem somar mais de 100%. Ano, semestre, disciplina e consulta por assunto foram testados. |
| Associações não confirmadas | Aprovado: zero vínculos confirmados e 180 questões pendentes na base pública. Grupos e temas históricos não são promovidos por nomes. IDs desconhecidos, grupos históricos e vínculos com outra disciplina são rejeitados. |
| Persistência e preservação | Aprovado: salvamento/recarga, cancelamento/remoção, exportação, reimportação e leitura de estado anterior preservam os registros pessoais. Não há gravação automática do banco na abertura. Fontes originais, PDF, imagens e metadados não foram alterados. |

## Pendência inicial do edital — resolvida pelo anexo
O PDF oficial do Edital nº 15/2026, Anexo VIII, páginas 102–103 (referência presente nos anexos), não foi encontrado entre os arquivos disponíveis. Tentativas de acessar `https://ingresso.ifrs.edu.br/` e a busca no domínio `https://ifrs.edu.br/` retornaram bloqueio do proxy, `403 Forbidden`.

Na etapa inicial, a consistência dos três anexos não permitia comprovar o edital. Posteriormente, o usuário forneceu o PDF, e a seção indicada foi extraída e conferida visualmente nas páginas 102–103. A comparação está documentada, com os 31 títulos e respectivos trechos, em [CONFERENCIA_EDITAL_MATEMATICA.md](CONFERENCIA_EDITAL_MATEMATICA.md). Nenhum tópico, ID ou vínculo de questão foi alterado.

## Problema corrigido na própria PR
A leitura IndexedDB executava `validate` dentro de `onsuccess` sem capturar exceções. Um estado local inválido — por exemplo, um campo extra `assuntoIds` com referência desconhecida aceito anteriormente — causava exceção fora da promessa, deixando `load()` pendente e impedindo a mensagem de erro da aplicação.

Correção em `app/servicos/storage.js`: capturar o erro de validação e rejeitar a promessa. A aplicação agora informa o problema em vez de ficar aguardando indefinidamente. Não limpa, reescreve ou “corrige” silenciosamente o banco. O teste novo `tests/storage_browser_test.py` semeia esse estado em contexto isolado, verifica o aviso e compara o conteúdo persistido antes/depois. Não foi adicionada funcionalidade nova.

## Testes executados
- `npm test`: 22 testes aprovados.
- `python3 scripts/conferir_ifrs.py`: 180 registros iguais entre JSON/CSV/XLSX; 31 tópicos iguais entre JSON/XLSX; distribuição e estatísticas da planilha conferidas.
- `python3 -m unittest discover -s tests -p 'test_extracao_piloto.py'`: aprovado; reproduz os pixels dos recortes e testa a invalidação da aprovação quando falta inspeção ou o hash diverge.
- Chromium: `tests/browser_test.py`, `tests/ifrs_browser_test.py`, `tests/recortes_browser_test.py`, `tests/tematica_browser_test.py` e `tests/storage_browser_test.py` aprovados. Incluem persistência, migração, vínculos múltiplos, consulta de assunto adicional, percentuais, filtros, backups, preservação de registros, dez imagens/PDFs, viewport móvel e subdiretório Pages.
- Comparação de `dados/` com `origin/main`: nenhuma alteração. Os SHA-256 dos três arquivos-fonte coincidem com os registrados em `IMPORTACAO_IFRS.md`. Os testes usam contextos e dados pessoais sintéticos isolados.

## Parecer
A implementação e os testes funcionais foram aprovados, com o problema de carregamento local corrigido. **A PR #5 está pronta para merge quanto aos critérios revisados**, após a conferência do edital anexado: os 31 assuntos correspondem às subdivisões documentadas do conteúdo. A ressalva é terminológica: os títulos são resumos, e não uma lista oficial numerada nem cópia literal. A classificação das questões permanece pendente por desenho desta entrega. Nenhum merge ou publicação foi realizado.
