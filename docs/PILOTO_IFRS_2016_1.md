# V0.3 — piloto IFRS 2016/1 concluído

## Resultado
10 imagens geradas, 10 verificadas e com status `ok`, 0 `revisar`, 0 `nao_extraida`. Inspeção efetiva: os dez PNGs individuais foram abertos e comparados com as cinco páginas originais renderizadas, verificando início, fim, alternativas A–E, fórmulas e as figuras das questões 03, 05 e 08. Não houve resolução nem conferência de respostas.

| IDs | Página original do PDF |
| --- | ---: |
| Q01–Q03 | 2 |
| Q04–Q05 | 3 |
| Q06–Q07 | 4 |
| Q08–Q09 | 5 |
| Q10 | 6 |

Todos os IDs têm prefixo IFRS-2016-1-. As dez questões estão completas na coluna esquerda; não foi encontrada continuação em outra coluna ou página. A qualidade da figura raster da Q03 é limitada pela imagem já existente no PDF: ela foi preservada, sem reconstrução ou melhoria artificial.

## Arquivos e execução
- PDF recebido, copiado sem alteração: `dados/provas/IFRS-2016-1-Superior.pdf` (24 páginas, aproximadamente 1,1 MB). A capa permite reprodução para fins didáticos com citação da fonte; a interface cita o IFRS.
- Dez imagens em `dados/questoes/imagens/2016-1/`, aproximadamente 1,2 MB no total, RGB a 288 dpi.
- Metadados em `dados/questoes/IFRS-2016-1-recortes.json`: ID, PDF, página (base 1), imagem, status, limites em pontos PDF, dimensões, partes, avisos e hashes.
- Registro de inspeção em `dados/questoes/IFRS-2016-1-verificacao.json`: hashes do PDF e de cada imagem efetivamente conferida.
- Rotina: `python3 scripts/extrair_ifrs_2016_1.py`. Dependência de desenvolvimento: PyMuPDF 1.26.6, declarada em `scripts/requirements-extracao.txt`. Não é dependência do site.

A rotina identifica o cabeçalho de Matemática e os marcadores 01–10, parando no início da questão 11. Localiza a divisória vertical, estima intervalos pelos marcadores seguintes e inclui as caixas de texto, figuras raster e elementos vetoriais. Renderiza diretamente o PDF: não transcreve nem reescreve as fórmulas.

Alternativas não confirmadas, conteúdo atravessando limites ou na coluna adjacente geram avisos e `revisar`. Não há aprovação apenas por heurística: sem registro de inspeção com os hashes atuais, os recortes ficam `revisar`. Um PDF ou PNG diferente invalida a aprovação correspondente. Marcadores ausentes/duplicados ou diagramação não suportada interrompem a rotina, sem adivinhar regiões. O status `nao_extraida` é entendido pela interface para futuros metadados sem imagem; não ocorre neste piloto.

## Integração e preservação
`app/servicos/recortes.js` carrega metadados de apresentação separados do IndexedDB. A interface associa as imagens pelo ID existente, sem adicionar questões ou alterar assuntos/classificações. O botão do Diário abre o formulário com a questão correta selecionada. O estado pessoal, backup e migração continuam como na V0.2.

Os arquivos originais em `dados/fontes/` permanecem inalterados. Continuam presentes as 180 classificações e os 31 tópicos. Os novos arquivos estáticos usam URLs relativas ao módulo, compatíveis com o subdiretório do GitHub Pages.

## Validação
- `npm test`: 14 testes aprovados; os 12 anteriores mais vínculos/páginas e integridade de PNG/status/hashes.
- `python3 -m unittest discover -s tests -p 'test_extracao_piloto.py'`: aprovado. Reexecuta o extrator em pasta temporária, compara os pixels ao PDF e confirma que ausência de revisão ou hash divergente impede `ok`.
- `python3 tests/recortes_browser_test.py`: aprovado em Chromium. Decodificou as dez imagens, abriu/fechou as dez ampliações, confirmou os dez links PDF/páginas e acesso HTTP, viewport 390px, seleção da questão no Diário e persistência da tentativa após recarga. Execução sob subdiretório equivalente ao GitHub Pages.
- `python3 tests/browser_test.py` e `python3 tests/ifrs_browser_test.py`: aprovados; regressão das funcionalidades anteriores e preservação de notas, tentativas, eventos, anexos e reimportação sem duplicação.

**Encerramento em 21/10/2026:** o usuário confirmou que a PR #3 foi integrada à `main`, a publicação no GitHub Pages foi concluída e as dez imagens estão corretas, vinculadas aos IDs originais, visíveis no módulo Questões e com ampliação funcionando. Esta validação em produção foi realizada pelo usuário; os testes locais acima são o registro da implementação.

A V0.3 está concluída e validada no escopo do piloto. A classificação temática detalhada e a expansão às outras 17 provas permanecem pendentes, conforme o [planejamento da V0.4](PLANEJAMENTO_V0.4.md).

## Limites e próximas 17 provas
Somente o PDF de 2016/1 foi processado. Para ampliar, é necessário receber os outros PDFs autorizados, conferir se têm texto selecionável, identificar suas colunas e limites, tratar explicitamente questões com múltiplas partes/páginas e conferir cada recorte. PDFs digitalizados poderão exigir OCR para localizar marcadores; a imagem final ainda deverá preservar o original. A rotina atual é um piloto específico, não um extrator geral validado para todas as diagramações.

As imagens não oferecem transcrição acessível completa: o PDF original permanece disponível. Não foram incluídos respostas, soluções ou correção automática. Nenhuma classificação temática foi alterada com base na leitura do PDF.
