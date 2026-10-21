# Piloto IFRS 2016/1: dez questões originais como imagens

Adiciona o PDF fornecido, dez PNGs e metadados associados aos IDs IFRS-2016-1-Q01 a Q10. A extração com PyMuPDF preserva a apresentação original e registra páginas, limites e hashes. Os dez recortes foram inspecionados visualmente contra as páginas 2–6: 10 ok, 0 revisar, 0 não extraídas. A figura raster de Q03 mantém a qualidade limitada da fonte.

O módulo Questões exibe os PNGs, ampliação em diálogo, fonte, status, PDF na página correspondente e acesso ao Diário com a questão selecionada. As 180 classificações e os 31 tópicos permanecem intactos, assim como os arquivos originais da V0.2 e o armazenamento pessoal.

Validação: 14 testes Node; teste Python de reprodução fiel ao PDF e invalidação da aprovação por hash; três suítes Chromium de regressão, migração e piloto, com dez imagens, ampliações e links PDF sob subdiretório Pages, mobile e persistência.

Apenas esta prova foi processada. Para as outras 17, faltam os PDFs autorizados, validação de suas diagramações e eventual tratamento de continuações/OCR. Não inclui respostas ou correção automática. A publicação ocorrerá somente após revisão e merge manual.
