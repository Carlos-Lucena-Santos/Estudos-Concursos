# Estudos-Concursos • V0.4 completa — provas, questões e frequência
Plataforma pessoal gratuita para organizar estudos, com JavaScript nativo, sem serviços externos ou backend obrigatório.

**V0.4 concluída, validada e publicada em 21/10/2026.** A [PR #7](https://github.com/Carlos-Lucena-Santos/Estudos-Concursos/pull/7) foi integrada à `main`, e o usuário confirmou o funcionamento do site no [GitHub Pages](https://carlos-lucena-santos.github.io/Estudos-Concursos/). Este registro de publicação e validação em produção se baseia nessa confirmação, não em uma nova execução de testes de produção.

Funcionalidades concluídas:

- 18 provas do IFRS incorporadas, com 18 PDFs originais e 180 questões com imagens PNG, identificação e links para a página da prova.
- 31 assuntos do conteúdo programático e 287 vínculos temáticos, com múltiplos assuntos por questão.
- Classificação temática automática na apresentação, a partir dos dados editoriais preparados, sem solicitar classificação ou confirmação manual ao estudante.
- Módulos Questões e Assuntos separados no menu; filtros compactos e recolhíveis em Questões.
- Filtros, frequências por assunto, quantidades e links entre questões do mesmo assunto, inclusive entre anos e semestres.
- Demais módulos, IDs, arquivos originais, revisões pessoais, anotações, tentativas, histórico e anexos preservados.

**Próxima versão: V0.5.** Escopo e funcionalidades ainda não definidos. Nenhuma implementação da V0.5 faz parte deste encerramento.

Consulte o [histórico de versões](docs/HISTORICO_VERSOES.md), o [encerramento da V0.4](docs/ENCERRAMENTO_V0.4.md) e o [planejamento da V0.5](docs/PLANEJAMENTO_V0.5.md).

## Executar
Requisitos: Python 3 para o servidor local. Node.js 20+ somente para testes.

```sh
cd Estudos-Concursos
python3 -m http.server 8000
```
Abra o endereço local mostrado pelo servidor no seu navegador. Não abra index.html diretamente pelo protocolo file: os módulos JavaScript precisam de HTTP.

`npm start` é uma alternativa ao comando Python. Não é necessário `npm install`.

## Usar
1. Cadastre concursos e disciplinas, depois assuntos e subassuntos com seus vínculos.
2. Consulte as 180 questões IFRS já disponíveis em **Questões** e os 31 tópicos em **Assuntos**. A frequência dos 31 assuntos oficiais acompanha os filtros e considera somente vínculos confirmados. Novos catálogos podem ser mesclados em **Backup e importação**.
3. Navegue pelo catálogo e seus filtros; registre tentativas no diário.
4. Crie anotações Markdown por assunto, edite ou exclua, e guarde documentos locais no caderno.
5. Registre atividades e revisões manuais no histórico.
6. Exporte backups JSON e cadernos Markdown regularmente.

A demonstração é opcional e fica em um concurso fictício separado. O IFRS Porto Alegre / Tecnologia em Sistemas para Internet / 2027/1 e o edital 15/2026 são metadados fornecidos pelo solicitante: foram incorporadas as 180 classificações e os 31 tópicos dos anexos fornecidos. Esta entrega inclui os PDFs autorizados das 18 provas e 180 imagens de questões. O PDF do edital não é publicado no repositório; sua seção de Matemática foi conferida conforme a documentação. As classificações originais permanecem intactas (166 preliminares e 14 com revisão necessária); a camada editorial separada contém os 287 vínculos temáticos das 180 questões.

## Privacidade
Os dados pessoais e anexos ficam no IndexedDB deste navegador e desta origem. Não são enviados ao GitHub nem sincronizados. Limpeza do navegador, mudança de endereço ou de dispositivo pode tornar os dados indisponíveis. Backups contêm informações privadas: guarde-os em local seguro. O armazenamento está sujeito à cota do navegador; anexos limitados a 10 MB por arquivo. PDFs só são abertos por link fornecido ou arquivo selecionado pelo usuário. Nenhuma prova é publicada automaticamente.

## Testes
```sh
npm test
# Em outro terminal, mantenha o servidor acima em execução:
python3 tests/browser_test.py
```
O teste de navegador requer o pacote Python Playwright e Chromium instalado (`pip install playwright` e `playwright install chromium`, quando necessário). Não são dependências da aplicação.

## Documentação
- [Arquitetura](docs/ARQUITETURA.md)
- [Modelo de dados e importação](docs/MODELO_DADOS.md)
- [Roadmap e limitações](docs/ROADMAP.md)
- [Publicação no GitHub Pages](docs/PUBLICACAO.md)
- [Validação](docs/VALIDACAO.md)

## Dados IFRS da V0.2
O JSON em `dados/fontes/` é a fonte principal; CSV e XLSX foram conferidos e preservados para rastreabilidade. A carga inicial mescla apenas IDs ausentes em memória; uma gravação normal mantém o catálogo junto ao backup, sem substituir registros locais existentes. Reimportar os anexos JSON/CSV não duplica questões. Os 31 tópicos oficiais e os temas específicos da classificação são exibidos separadamente: não foram inferidos vínculos entre um tema e um tópico oficial.

Conferência dos três arquivos: `python3 scripts/conferir_ifrs.py` (requer openpyxl, apenas ferramenta de conferência). Teste adicional de migração: `python3 tests/ifrs_browser_test.py`.

## Piloto V0.3 — questões como imagens
Em **Questões**, filtre ano **2016**, semestre **1**. As dez questões mostram o recorte original, status de integridade, **Ampliar imagem**, link para o PDF na página correspondente e **Registrar tentativa no Diário**. A ampliação mantém a resolução original, com rolagem em telas pequenas; pode ser fechada pelo botão ou por Escape.

Os dez recortes foram conferidos visualmente contra as páginas 2–6 e estão `ok`. Isso se refere à integridade das imagens, não à correção das classificações, que permanecem iguais às da V0.2. Nenhum dado pessoal é incorporado aos metadados de imagem.

A aplicação já contém os PNGs; o GitHub Pages não precisa executar Python. Para reproduzir a extração, com PyMuPDF instalado:

```sh
python3 -m pip install -r scripts/requirements-extracao.txt
python3 scripts/extrair_ifrs_2016_1.py
python3 -m unittest discover -s tests -p 'test_extracao_piloto.py'
python3 tests/recortes_browser_test.py
```

O último teste inicia seu próprio servidor na porta 8013. As suítes anteriores continuam usando o servidor na porta 8000. Veja [relatório do piloto](docs/PILOTO_IFRS_2016_1.md) para limites, revisão e expansão às demais provas.

## V0.4 — múltiplos assuntos por questão
A implementação da V0.4 substitui o painel de oito grupos históricos por frequência dos **31 assuntos oficiais existentes**. A V0.4 está concluída, validada pelo usuário e publicada no GitHub Pages após o merge da PR #7.

No módulo **Questões**, os assuntos são apresentados automaticamente a partir da classificação editorial preparada em `dados/questoes/classificacao-confirmada.json`. Não é necessário classificar, confirmar ou editar vínculos no navegador. Cada assunto da questão é um link: ao acioná-lo, a consulta limpa os filtros anteriores e mostra todas as questões relacionadas no acervo, independentemente de ano ou semestre. As imagens, ampliação, identificação, PDF e Diário continuam disponíveis.

Cada questão conta uma única vez por assunto, mesmo que haja IDs repetidos na entrada. O percentual usa o total de questões selecionadas pelos filtros; uma questão pode contar em vários assuntos e a soma dos percentuais pode ultrapassar 100%. O painel apresenta todos os assuntos da disciplina, incluindo zeros, e o total de pendências: zero não comprova ausência de um assunto nas questões ainda não classificadas. Use **Assuntos** no menu esquerdo para consultar os 31 assuntos, sua frequência e quantidade de questões. Os links abrem as questões do assunto em todos os anos e semestres. Em **Questões**, os filtros de ano, semestre e assunto ficam compactos e recolhíveis, e a tela abre diretamente nos cartões, sem lista de frequência anterior.

**Na etapa estrutural anterior, a base tinha 0 questões com assuntos específicos confirmados e 180 pendentes.** Os arquivos de origem contêm classificações preliminares, não vínculos confirmados com os IDs dos 31 assuntos. Nenhuma associação foi inferida por semelhança de nomes. Grupos e temas antigos ficam como referência histórica; as classificações originais e observações permanecem intactas.

Testes adicionais: `node --test tests/tematica.test.js` e `python3 tests/tematica_browser_test.py` (este inicia seu próprio servidor na porta 8014 e exige Playwright/Chromium). Consulte [detalhes da V0.4](docs/V0.4_TEMATICA.md).

A seção de Matemática do edital anexado foi conferida nas páginas 102–103: os 31 assuntos cadastrados cobrem seu conteúdo como subdivisões e títulos resumidos, não como uma lista oficial numerada ou transcrição literal. Consulte a [matriz de correspondência com o edital](docs/CONFERENCIA_EDITAL_MATEMATICA.md). Isso não confirma automaticamente a classificação de nenhuma questão.

## V0.4 completa — 18 provas e classificação revisada
Os 17 novos PDFs foram organizados e extraídos, preservando o piloto de 2016/1. A entrega contém **18 PDFs, 180 imagens conferidas e 180 questões com classificação editorial revisada**, associadas aos mesmos 31 assuntos, com justificativa por questão. São 287 vínculos ao todo; não há questões sem vínculo na base pública. A consulta e a frequência usam os vínculos editoriais preparados. Revisões pessoais antigas continuam preservadas no banco e nos backups, sem substituir essa apresentação automática.

Em **Questões**, filtre ano/semestre para ver o enunciado original como imagem, ampliá-lo, abrir a página do PDF e registrar uma tentativa. Uma questão com continuação reúne os fragmentos na mesma imagem. O texto extraído automaticamente fica sob aviso: símbolos, fórmulas e OCR podem falhar; use a imagem/PDF como referência. Não foram incluídas respostas ou soluções.

A classificação pública revisada é uma camada separada das fontes originais. Uma projeção de consulta aplica seus vínculos sem sobrescrever revisões pessoais, inclusive uma revisão intencionalmente vazia. Abertura da aplicação não grava o banco automaticamente. Faça backup antes de atualizar ou trocar de navegador.

Detalhes, frequências, justificativas e limitações: [relatório da V0.4 completa](docs/V0.4_COMPLETA.md). Para reproduzir a extração: `python3 scripts/extrair_provas_ifrs.py`, com PyMuPDF/Pillow e Tesseract para a prova digitalizada de 2019/1. O navegador não precisa dessas ferramentas.

Testes adicionais: `python3 -m unittest discover -s tests` e `python3 tests/completa_browser_test.py` (servidor próprio na porta 8015, Playwright/Chromium). A publicação da V0.4 foi concluída e validada pelo usuário após o merge da PR #7.

## Consulta temática automática
Novas questões devem chegar com IDs únicos e `assuntoIds` preparados com os IDs dos 31 assuntos existentes; o catálogo e sua camada editorial devem cobrir as mesmas questões. A frequência é calculada a partir dos registros carregados, sem totais fixos ou inferência por nomes. Questões sem vínculos preparados são sinalizadas sem solicitar classificação ao usuário. Veja [regras atuais](docs/QUESTOES_AUTOMATICAS.md).
