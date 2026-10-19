# Estudos-Concursos • V0.1
Plataforma pessoal gratuita para organizar estudos, com JavaScript nativo, sem serviços externos ou backend obrigatório.

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
2. Importe questões em **Backup e importação**, seguindo docs/MODELO_DADOS.md.
3. Navegue pelo catálogo e seus filtros; registre tentativas no diário.
4. Crie anotações Markdown por assunto, edite ou exclua, e guarde documentos locais no caderno.
5. Registre atividades e revisões manuais no histórico.
6. Exporte backups JSON e cadernos Markdown regularmente.

A demonstração é opcional e fica em um concurso fictício separado. O IFRS Porto Alegre / Tecnologia em Sistemas para Internet / 2027/1 e o edital 15/2026 são metadados fornecidos pelo solicitante: os documentos oficiais e as 180 questões não estão presentes nem foram importados.

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
