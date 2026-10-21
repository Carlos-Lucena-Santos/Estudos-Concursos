# Histórico de versões

## V0.4 — concluída, validada e publicada
**V0.4 concluída, validada e publicada em 21/10/2026.** A [PR #7](https://github.com/Carlos-Lucena-Santos/Estudos-Concursos/pull/7) foi integrada à `main`, e o usuário confirmou o funcionamento do site no [GitHub Pages](https://carlos-lucena-santos.github.io/Estudos-Concursos/). Este registro de publicação e validação em produção se baseia nessa confirmação, não em uma nova execução de testes de produção.

Funcionalidades concluídas:

- 18 provas do IFRS incorporadas, com 18 PDFs originais e 180 questões com imagens PNG, identificação e links para a página da prova.
- 31 assuntos do conteúdo programático e 287 vínculos temáticos, com múltiplos assuntos por questão.
- Classificação temática automática na apresentação, a partir dos dados editoriais preparados, sem solicitar classificação ou confirmação manual ao estudante.
- Módulos Questões e Assuntos separados no menu; filtros compactos e recolhíveis em Questões.
- Filtros, frequências por assunto, quantidades e links entre questões do mesmo assunto, inclusive entre anos e semestres.
- Demais módulos, IDs, arquivos originais, revisões pessoais, anotações, tentativas, histórico e anexos preservados.

**Próxima versão: V0.5.** Escopo e funcionalidades ainda não definidos. Nenhuma implementação da V0.5 faz parte deste encerramento.

As seções anteriores de implementação e revisão, mantidas abaixo, descrevem etapas históricas; suas pendências de merge/publicação foram superadas pelo encerramento. Limitações de transcrição/OCR continuam documentadas e não definem o escopo da V0.5.

## V0.3 — concluída e validada em 21/10/2026
Piloto IFRS 2016/1: PDF original, extração com Python/PyMuPDF, dez PNGs vinculados aos IDs IFRS-2016-1-Q01 a Q10 e metadados de integridade. Módulo Questões com imagens, ampliação, link para a página do PDF e acesso ao Diário.

O usuário confirmou diretamente no GitHub Pages:
- Dez recortes corretos e vinculados aos IDs originais.
- Visualização no módulo Questões e ampliação funcionando.
- [PR #3](https://github.com/Carlos-Lucena-Santos/Estudos-Concursos/pull/3) integrada à `main` e publicação concluída.

As 180 classificações, os 31 tópicos e as funcionalidades anteriores foram preservados. A validação do piloto encerra a entrega de imagens de 2016/1; não conclui a classificação temática detalhada nem o processamento das demais provas. Evidências locais e confirmação do usuário constam em [VALIDACAO.md](VALIDACAO.md) e no [relatório do piloto](PILOTO_IFRS_2016_1.md).

## V0.2 — base IFRS incorporada
180 classificações de 18 provas, dez questões por prova, e 31 tópicos importados a partir dos arquivos fornecidos. JSON, CSV e Excel conferidos. IDs, páginas, observações e classificações originais preservados: 166 preliminares e 14 com revisão necessária. Inclui consulta por assunto e frequência por grupo. [PR #2](https://github.com/Carlos-Lucena-Santos/Estudos-Concursos/pull/2).

## V0.1 — base funcional
Aplicação estática com navegação, biblioteca compartilhada, catálogo, caderno Markdown, diário de tentativas, histórico, dashboard, armazenamento local IndexedDB e exportação/importação de backups. [PR #1](https://github.com/Carlos-Lucena-Santos/Estudos-Concursos/pull/1).

## V0.4 — implementação para revisão
Estrutura `assuntoIds` com múltiplos vínculos confirmados por questão, editor manual e painel de frequência pelos 31 assuntos oficiais existentes, com consulta, percentuais, zeros e pendências. Nenhuma associação automática por nomes: a base inicial possui zero questões confirmadas e 180 pendentes. Classificações originais, dados pessoais, PDF e imagens da V0.3 preservados. Sem novos assuntos ou processamento das demais provas.

Branch `feature/estudos-concursos-v0.4`; merge, publicação e validação em produção permanecem pendentes. Ver [V0.4_TEMATICA.md](V0.4_TEMATICA.md). As outras 17 provas e a revisão temática humana continuam pendências futuras.

## V0.4 completa — preparada para revisão e publicação
18 PDFs organizados e 180 imagens conferidas (170 novas e dez do piloto). Camada editorial com justificativas e vínculos para as 180 questões nos 31 assuntos existentes, preservando fontes originais e revisões pessoais. Oito referências de página antes vazias foram identificadas nos metadados dos recortes. Texto extraído é apoio não validado para fórmulas/OCR; a imagem/PDF permanece autoritativa. Ver [V0.4_COMPLETA.md](V0.4_COMPLETA.md). Branch `feature/estudos-concursos-v0.4-completa`; merge/publicação ainda não realizados nesta tarefa.

## V0.4 — consulta temática automática (21/10/2026)
- Classificações editoriais preparadas apresentadas automaticamente em Questões, sem editor ou confirmação pelo estudante.
- Links por assunto consultam o acervo inteiro, limpando filtros anteriores.
- Frequência dinâmica, múltiplos vínculos e revisões pessoais antigas preservadas em armazenamento e backup.
- Imagens, PDFs, IDs, dados originais e demais módulos preservados. Entrega em branch/PR, sem merge automático.

### Ajuste de interface na própria PR #7
Questões abre diretamente nos cartões, com filtros compactos e recolhíveis. Assuntos concentra os 31 temas, busca, filtros, quantidades, percentuais e links para questões entre provas. Cadastro pessoal e situação de estudo preservados em seções recolhíveis. Sem nova PR, sem merge automático e sem alterações nos arquivos de dados.
