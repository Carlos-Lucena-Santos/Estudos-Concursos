# Arquitetura V0.1
Aplicação estática servida por HTTP, compatível com subdiretórios do GitHub Pages. Sem framework, bundler ou dependências de produção: o escopo não exige esses custos.

`app/main.js` contém navegação, componentes de formulário e controladores. `app/estilos` contém o layout responsivo. `app/servicos/model.js` valida referências, importações, filtros e ordenação. `storage.js` grava uma versão consistente do estado em uma transação IndexedDB; a tela só atualiza depois da confirmação da gravação. Falhas de cota e permissões aparecem na interface.

`biblioteca`, `concursos` e `dados/questoes` são espaços para referência pública revisada. O navegador começa apenas com os metadados informados do IFRS e a disciplina Matemática. Importações feitas pela interface ficam locais, inclusive catálogos; nada é enviado automaticamente ao repositório.

As disciplinas e assuntos são compartilhados. Assuntos apontam para vários concursos e podem ter um assunto superior. Questões apontam para assunto principal, secundários e subassunto. Cadernos pertencem ao assunto, evitando duplicação entre concursos. Tentativas pertencem à questão; cada envio acrescenta uma tentativa e um evento. Histórico é acrescentado cronologicamente. A exclusão de uma nota não apaga os eventos passados de aprendizagem.

Texto fornecido pelo usuário é escapado antes de entrar no HTML. Markdown é armazenado e exibido como texto editável, sem interpretação de HTML. Links externos de PDFs aceitam apenas HTTP/HTTPS. Documentos pessoais não são executados na interface; o download abre no visualizador apropriado. O aplicativo funciona sem rede depois de carregado enquanto a aba permanece aberta; não há cache offline de inicialização nesta versão.
