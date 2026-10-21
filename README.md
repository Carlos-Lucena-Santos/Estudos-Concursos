# Estudos-Concursos • V0.4 — classificação temática e frequência
Plataforma pessoal gratuita para organizar estudos, com JavaScript nativo, sem serviços externos ou backend obrigatório.

**V0.3 encerrada em 21/10/2026:** o usuário confirmou a validação do piloto IFRS 2016/1 diretamente no GitHub Pages, com dez PNGs corretos, vinculados aos IDs originais, visualização e ampliação funcionando. A [PR #3](https://github.com/Carlos-Lucena-Santos/Estudos-Concursos/pull/3) foi integrada à `main` e a publicação foi concluída, conforme informado pelo usuário.

Próxima etapa: planejar a V0.4. Permanecem pendentes as outras 17 provas e a classificação temática detalhada. Consulte o [histórico de versões](docs/HISTORICO_VERSOES.md) e a [preparação da V0.4](docs/PLANEJAMENTO_V0.4.md).

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

A demonstração é opcional e fica em um concurso fictício separado. O IFRS Porto Alegre / Tecnologia em Sistemas para Internet / 2027/1 e o edital 15/2026 são metadados fornecidos pelo solicitante: foram incorporadas as 180 classificações e os 31 tópicos dos anexos fornecidos. O piloto V0.3 inclui o PDF autorizado de 2016/1; os demais PDFs e o edital não estão incluídos. As classificações permanecem preliminares (166) ou com revisão necessária (14), sem reclassificação.

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
A implementação da V0.4 substitui o painel de oito grupos históricos por frequência dos **31 assuntos oficiais existentes**. A V0.3 continua sendo o marco publicado e validado pelo usuário; a V0.4 depende da revisão e publicação desta entrega.

No módulo **Questões**, clique em **Editar assuntos** na questão desejada, marque um ou vários assuntos cuja associação você confirmou, acrescente observações e use **Salvar vínculos confirmados**. A seleção vazia mantém a questão pendente. **Cancelar** ou Escape não grava alterações. Os vínculos ficam no navegador e no backup JSON; não são enviados ao GitHub. Faça backups para transferi-los entre dispositivos.

Cada questão conta uma única vez por assunto, mesmo que haja IDs repetidos na entrada. O percentual usa o total de questões selecionadas pelos filtros; uma questão pode contar em vários assuntos e a soma dos percentuais pode ultrapassar 100%. O painel apresenta todos os assuntos da disciplina, incluindo zeros, e o total de pendências: zero não comprova ausência de um assunto nas questões ainda não classificadas. Use **Consultar questões deste assunto** no painel ou **Consultar questões relacionadas** em Assuntos.

**Base inicial: 0 questões com assuntos específicos confirmados; 180 pendentes.** Os arquivos de origem contêm classificações preliminares, não vínculos confirmados com os IDs dos 31 assuntos. Nenhuma associação foi inferida por semelhança de nomes. Grupos e temas antigos ficam como referência histórica; as classificações originais e observações permanecem intactas.

Testes adicionais: `node --test tests/tematica.test.js` e `python3 tests/tematica_browser_test.py` (este inicia seu próprio servidor na porta 8014 e exige Playwright/Chromium). Consulte [detalhes da V0.4](docs/V0.4_TEMATICA.md).
