# Questões — classificação preparada e consulta automática

Os 180 registros usam as classificações editoriais existentes, com 287 vínculos entre os mesmos 31 assuntos cadastrados a partir do edital. A aplicação associa e apresenta esses vínculos automaticamente; o estudante não precisa classificar, confirmar ou editar assuntos. Não houve nova classificação nem associação por semelhança de nomes.

A preparação continua sendo feita no conjunto de dados editorial (`dados/questoes/classificacao-confirmada.json`), validado junto ao catálogo. Para incorporar novas questões, acrescentar seus IDs únicos no catálogo e os vínculos `assuntoIds` na camada editorial correspondente, mantendo sua cobertura completa. Essa etapa exige evidência do conteúdo e revisão editorial; não é um classificador por inferência executado no navegador.

Cada assunto exibido em um cartão é um link. Ele limpa ano, semestre, concurso, disciplina e situação, aplica somente o assunto e mostra todas as questões relacionadas, incluindo a questão de origem. Uma questão com vários assuntos aparece em todas as consultas pertinentes. O painel de frequência continua respeitando os filtros selecionados; seu botão de consulta mantém o recorte atual. Os links dos cartões oferecem a consulta ao acervo inteiro.

Frequências são recalculadas a cada renderização a partir dos registros classificados carregados, sem constantes de 180 questões. IDs repetidos de assunto contam uma única vez por questão. O denominador é o total de questões selecionadas e a soma dos percentuais pode ultrapassar 100%. Questões sem classificação preparada são sinalizadas, sem formulários de classificação.

A imagem completa, ampliação, identificação, PDF na página original e registro de tentativa no Diário são preservados. Os demais módulos continuam disponíveis.

## Dados pessoais
Uma projeção de consulta usa a classificação editorial sem modificar a revisão pessoal armazenada. Revisões antigas, suas datas/observações, cadernos, tentativas, eventos e anexos continuam no IndexedDB e no backup. A frequência de Questões passa a usar os vínculos preparados, mesmo que uma revisão pessoal antiga seja diferente. Não há migração destrutiva nem gravação automática ao abrir o site.

Os arquivos originais Excel/CSV/JSON, PDFs e PNGs não foram alterados. O serviço de edição de vínculos permanece compatível com dados antigos/importações, mas não há controles dessa edição no módulo Questões.

## Validação
Testes de lógica cobrem projeção sem mutação, múltiplos vínculos, deduplicação, filtros e incremento da frequência quando novas questões preparadas são incorporadas. Testes Chromium verificam links entre provas após filtros restritivos, ausência de controles temáticos, preservação integral de revisões antigas e backup, além das imagens, PDFs, módulos e caminhos sob subdiretório Pages.
