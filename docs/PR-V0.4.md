# V0.4 — múltiplos assuntos e frequência temática

Substitui a frequência dos oito grupos históricos pela análise dos 31 assuntos oficiais existentes. Cada questão pode guardar múltiplos `assuntoIds`, editáveis manualmente, com observações e data de revisão. Contagens deduplicam a questão por assunto; percentuais usam o total selecionado e podem somar mais de 100%. O painel distingue zeros de vínculos ausentes e mostra as pendências, com consulta por assunto, inclusive adicional.

A base inicial tem 0 questões com assuntos específicos confirmados e 180 pendentes: não há confirmação por ID oficial nos arquivos originais, e nenhuma associação foi inferida por semelhança de nomes. As classificações e observações antigas ficam como referência histórica. Não há novos assuntos, alteração dos arquivos de origem nem processamento das outras provas.

A migração é aditiva em memória e não grava o banco ao abrir. Listas já revisadas, Caderno, Diário, Histórico, anexos, IDs, PDF e imagens da V0.3 são preservados. O usuário salva os vínculos no navegador e os exporta no backup existente.

Validação: 22 testes Node e quatro suítes Chromium, cobrindo frequência, edição múltipla, deduplicação, filtros/consultas, persistência, backups, dados antigos, mobile, imagens e caminhos Pages. Nenhum vínculo sintético de teste é incluído no catálogo. Revisão, merge e publicação da V0.4 ainda pendentes; sem merge automático.
