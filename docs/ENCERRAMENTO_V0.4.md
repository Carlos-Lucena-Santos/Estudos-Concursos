# Encerramento oficial da V0.4

**V0.4 concluída, validada e publicada em 21/10/2026.** A [PR #7](https://github.com/Carlos-Lucena-Santos/Estudos-Concursos/pull/7) foi integrada à `main`, e o usuário confirmou o funcionamento do site no [GitHub Pages](https://carlos-lucena-santos.github.io/Estudos-Concursos/). Este registro de publicação e validação em produção se baseia nessa confirmação, não em uma nova execução de testes de produção.

Funcionalidades concluídas:

- 18 provas do IFRS incorporadas, com 18 PDFs originais e 180 questões com imagens PNG, identificação e links para a página da prova.
- 31 assuntos do conteúdo programático e 287 vínculos temáticos, com múltiplos assuntos por questão.
- Classificação temática automática na apresentação, a partir dos dados editoriais preparados, sem solicitar classificação ou confirmação manual ao estudante.
- Módulos Questões e Assuntos separados no menu; filtros compactos e recolhíveis em Questões.
- Filtros, frequências por assunto, quantidades e links entre questões do mesmo assunto, inclusive entre anos e semestres.
- Demais módulos, IDs, arquivos originais, revisões pessoais, anotações, tentativas, histórico e anexos preservados.

**Próxima versão: V0.5.** Escopo e funcionalidades ainda não definidos. Nenhuma implementação da V0.5 faz parte deste encerramento.

## Evidências e limites
O merge da PR #7 está presente na história da `main`. A confirmação do usuário fundamenta a validação do site publicado. Os testes anteriores estão registrados em [VALIDACAO.md](VALIDACAO.md): 30 casos Node, dois testes Python, seis suítes Chromium e conferência dos arquivos JSON/CSV/XLSX. Não se afirma que essas suítes foram reexecutadas em produção neste encerramento.

As imagens e PDFs continuam sendo as referências para leitura; a transcrição automática permanece sujeita a erros de fórmulas, caracteres e OCR. A classificação editorial pode ser refinada na preparação dos dados. Essas limitações não reabrem a versão nem definem funcionalidades da V0.5.

Esta entrega altera exclusivamente documentação. Código, dados e funcionalidades permanecem integralmente preservados. A PR de documentação não realiza merge automático.
