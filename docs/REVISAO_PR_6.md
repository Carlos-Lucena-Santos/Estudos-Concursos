# Validação final da PR #6 — 21/10/2026

## Escopo e parecer
Revisada a branch `feature/estudos-concursos-v0.4-completa`, inicialmente no commit `e30083c`, igual à referência remota obtida por `git fetch`. Não houve merge ou publicação. A API de consulta da PR retornou `Forbidden`; a identificação da PR #6 segue a informação do usuário e sua branch de origem.

A entrega está tecnicamente apta para merge, com as limitações editoriais e de produção abaixo explicitadas. Não foi identificado defeito funcional bloqueante. Os testes locais sob subdiretório confirmam compatibilidade com GitHub Pages; não equivalem à validação do site publicado.

## Testes executados
- `npm test`: cinco arquivos de testes aprovados. Execução adicional `node --test --test-isolation=none tests/*.test.js`: **28 casos individuais aprovados**, incluindo o novo cruzamento exaustivo de anos, semestres e 31 assuntos, com vínculo duplicado proposital e conjuntos vazios.
- `python3 scripts/conferir_ifrs.py`: 180 registros idênticos em JSON/CSV/XLSX, 31 tópicos correspondentes JSON/XLSX, 18 provas com dez questões e estatísticas originais preservadas.
- `python3 -m unittest discover -s tests`: **dois testes aprovados**, reprodução do piloto e comparação pixel a pixel de todos os fragmentos das 180 imagens com os PDFs. As mensagens intermediárias `revisar` do teste do piloto são cenários de invalidação deliberada em diretório temporário, não o estado dos arquivos publicados.
- **Seis suítes Chromium aprovadas**: `browser_test.py`, `completa_browser_test.py`, `ifrs_browser_test.py`, `recortes_browser_test.py`, `storage_browser_test.py`, `tematica_browser_test.py`.
- A suíte completa foi ampliada e passou novamente: as **180 imagens** são decodificadas na interface, os 180 PNGs e 18 PDFs respondem HTTP 200, os links contêm a página verificada e cada uma das 18 provas apresenta dez cartões. Os 31 totais e percentuais são confrontados com a camada editorial em cada prova.
- Navegação, ampliação, assuntos adicionais, filtros/consulta, diário, histórico, caderno, backup e revisão pessoal persistida após recarga aprovados. A leitura inicial não regrava o banco antigo. Uma revisão pessoal vazia prevalece sobre a classificação pública.
- Subdiretório equivalente ao Pages, largura móvel de 390px e ausência de erros JavaScript verificados. Navegador precisou de execução fora da restrição local de sockets; não foi necessário alterar a aplicação para contornar isso.

## Integridade e preservação
Há 18 PDFs distintos, 180 PNGs e 180 IDs únicos. SHA-256 de cada PDF/PNG, dimensões, cobertura dos IDs e correspondência dos recortes foram validados. Os status dos 180 recortes continuam `ok`, vinculados aos hashes da inspeção anterior. Não se repetiu uma inspeção humana integral das 180 imagens nesta revisão: repetiram-se os testes de integridade e reprodução, com inspeção direta dos enquadramentos temáticos destacados abaixo.

Comparação com a base anterior à entrega: nenhum arquivo original em `dados/fontes`, nenhum PNG do piloto e nenhum PDF de 2016/1 alterado. Nenhum PDF, imagem, ID ou assunto foi excluído. A correção editorial descrita abaixo afeta exclusivamente a camada nova de classificação, não as fontes originais.

## Classificação: resultados e pontos para revisão pedagógica
A auditoria de cobertura das 180 entradas confirma **287 vínculos**, apenas com os 31 IDs existentes e sem repetição por questão. Toda entrada possui justificativa; nenhuma questão está sem assunto na camada editorial. A matriz anterior de correspondência dos 31 registros ao Anexo VIII continua aplicável: são subdivisões/sínteses do edital, não uma lista oficial numerada com nomes literalmente iguais.

Os testes verificam referências e frequência, mas não demonstram por si só correção pedagógica. Foram destacados dois enquadramentos amplos, conferidos diretamente nas imagens, para eventual refinamento humano:

| Questão | Vínculo atual | Ponto de atenção |
| --- | --- | --- |
| IFRS-2025-2-Q02 | Números reais: operações, propriedades, intervalos | O enunciado é de periodicidade de uma sequência de letras; o vínculo é pela operação com inteiros/restos. O rótulo amplo não descreve diretamente o objeto. Não classificar como PA/PG apenas por ser sequência. |
| IFRS-2019-2-Q07 | Números reais: operações, propriedades, intervalos | Contagem de múltiplos em intervalo. Pode receber discussão pedagógica sobre um vínculo adicional com PA; esse vínculo adicional não foi inserido sem confirmação específica. |

Esses vínculos atuais têm base no conteúdo numérico observado; não foram retirados nem substituídos automaticamente. As sugestões de vínculos adicionais permanecem não confirmadas e fora da frequência. Os casos são recomendações de refinamento pedagógico, não declaração de equivalência literal entre seus enunciados e os títulos resumidos. Não se certifica uma classificação única ou exaustiva: outros métodos podem motivar vínculos adicionais mediante revisão.

Também foi inspecionada IFRS-2020-1-Q08: o diagrama cartesiano com circunferências e triângulo sustenta os vínculos geométricos existentes. Nenhuma questão foi resolvida e nenhum gabarito foi consultado.

## Correções na própria branch da PR
1. Texto introdutório do módulo Questões atualizado: a camada pública é editorial revisada; as classificações originais permanecem preservadas e revisões pessoais prevalecem.
2. Justificativa de IFRS-2025-2-Q02 corrigida de sequência periódica “finita” para “infinita”, conforme o enunciado original. Nenhum vínculo foi alterado.
3. Teste de frequência ampliado para todas as combinações de ano, semestre e assunto, com duplicidade intencional na entrada.
4. Teste de navegador ampliado de duas imagens por prova para as dez imagens de cada prova.

## Pendências e limites de publicação
- O acesso externo ao Pages retornou **HTTP 403** pelo proxy do ambiente, mesmo com execução de rede autorizada. A API do GitHub também retornou `Forbidden`. Não foi possível confirmar o estado dos checks remotos ou a versão em produção. Isso não é evidência de indisponibilidade pública do site.
- Após merge autorizado pelo usuário, é necessária a validação do deploy e abertura de questões/PDFs no endereço publicado. Esta revisão não realizou merge.
- As 180 transcrições automáticas continuam `revisar`, sobretudo fórmulas e OCR. Imagens/PDFs são as referências; não há promessa de transcrição perfeita.
- Os dois enquadramentos amplos acima ficam registrados para revisão pedagógica futura, pelo editor existente. Não impedem o funcionamento da frequência atual.
