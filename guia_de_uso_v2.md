# Guia de Uso: Sistema de Gestão e Validação de Estágios

Bem-vindo ao guia visual de uso do backend do sistema de estágios. Este documento detalha como o sistema funciona através de fluxogramas, como utilizá-lo na prática e fornece um roteiro recomendado para a sua apresentação.

---

## 1. Processos do Sistema (Como o fluxo funciona)

O sistema foi desenhado para automatizar o fluxo de aprovação de estágios acadêmicos. O diagrama abaixo ilustra o caminho desde a criação da solicitação até a sua aprovação final.

![Fluxograma do Processo do Sistema](https://mermaid.ink/img/Z3JhcGggVEQKICAgIEFbQWx1bm9dIC0tPnxBYnJlfCBCKFNvbGljaXRhw6fDo28gZGUgRXN0w6FnaW8pCiAgICBCIC0tPiBDe0NoZWNrbGlzdCBHZXJhZG99CiAgICBDIC0tPnxQZW5kZW50ZXwgRFtEb2N1bWVudG9zIE9icmlnYXTDs3Jpb3NdCiAgICBBIC0tPnxFbnZpYXwgRAogICAgRCAtLT58QXZhbGlhw6fDo298IEVbQ29vcmRlbmFkb3JdCiAgICBFIC0tPnxBbmFsaXNhfCBGe1Jlc3VsdGFkb30KICAgIEYgLS0+fEFwcm92YWRvfCBHW0VuY2FtaW5oYW1lbnRvIHBhcmEgRW1wcmVzYV0KICAgIEYgLS0+fFJlcHJvdmFkb3wgSFtGaW0gZG8gUHJvY2Vzc29dCiAgICBGIC0tPnxDb3JyZcOnw6NvfCBE)

<!-- COMENTÁRIO: Este diagrama usa blocos de decisão para mostrar que caso a análise seja "Correção Necessária", o fluxo volta para o aluno enviar novos documentos. -->

**Etapas Principais:**
1. **Abertura da Solicitação:** O Aluno inicia o processo abrindo uma Solicitação de estágio.
2. **Envio de Documentos:** Um Checklist é gerado automaticamente e o aluno submete os Documentos obrigatórios (PDF, Word, etc.).
3. **Análise:** O Coordenador visualiza e analisa os documentos, emitindo um resultado (Aprovado, Reprovado ou Correção Necessária).
4. **Encaminhamento:** Se aprovado, a solicitação gera um encaminhamento oficial para a Empresa parceira.

---

## 2. Como se Autenticar

A API utiliza segurança baseada em **Tokens JWT** (JSON Web Tokens). Abaixo você pode visualizar como ocorre a troca de mensagens entre você, a interface do Swagger e o servidor backend.

![Fluxograma de Autenticação JWT](https://mermaid.ink/img/c2VxdWVuY2VEaWFncmFtCiAgICBwYXJ0aWNpcGFudCBVc2VyIGFzIFVzdcOhcmlvCiAgICBwYXJ0aWNpcGFudCBTd2FnZ2VyIGFzIFN3YWdnZXIgVUkKICAgIHBhcnRpY2lwYW50IEFQSSBhcyBCYWNrZW5kIChEamFuZ28pCiAgICBVc2VyLT4+U3dhZ2dlcjogSW5mb3JtYSBsb2dpbiBlIHNlbmhhCiAgICBTd2FnZ2VyLT4+QVBJOiBQT1NUIC9hcGkvdG9rZW4vCiAgICBBUEktLT4+U3dhZ2dlcjogUmV0b3JuYSB0b2tlbnMgKGFjY2VzcyBlIHJlZnJlc2gpCiAgICBTd2FnZ2VyLS0+PlVzZXI6IEV4aWJlIG8gYWNjZXNzX3Rva2VuCiAgICBVc2VyLT4+U3dhZ2dlcjogQ2xpY2EgZW0gQXV0aG9yaXplIGUgaW5zZXJlIEJlYXJlciB0b2tlbgogICAgU3dhZ2dlci0+PkFQSTogUmVxdWlzacOnw7VlcyBjb20gSGVhZGVyIGRlIEF1dGVudGljYcOnw6NvCiAgICBBUEktLT4+U3dhZ2dlcjogRGFkb3MgcHJvdGVnaWRvcw==)

<!-- COMENTÁRIO: A partir do momento em que o Header Authorization é definido, o backend reconhece o usuário conectado e filtra os dados de acordo com seu perfil. -->

### Passo a Passo no Swagger:
1. Acesse o **Swagger UI** (geralmente em `http://127.0.0.1:8000/api/docs/swagger/`).
2. Vá até a seção `token` e abra o endpoint `POST /api/token/`. Clique em **"Try it out"**.
3. Insira as credenciais em formato JSON:
   ```json
   {
     "username": "admin",
     "password": "Admin123!"
   }
   ```
4. Clique em **"Execute"**. O servidor retornará um campo chamado `access`. Copie o valor numérico dele.
5. No topo da página, clique no botão verde **"Authorize"** (com o cadeado).
6. Digite `Bearer <seu_token_copiado>` e autorize.

---

## 3. Como Preencher os Formulários (Campos da API)

Ao utilizar o Swagger, você enviará dados no formato JSON. Veja o que cada formulário essencial exige:

* **Alunos (`/api/alunos/`)**: Requer `usuario` (ID numérico), `nome`, `matricula` e `curso`.
* **Organizações Parceiras (`/api/organizacoes/`)**: Requer `usuario`, `razao_social` e `cnpj`.
* **Modelos de Documento (`/api/modelos-documento/`)**: Requer `nome`, `descricao` e indica se é `obrigatorio`. Serve como base para o checklist.
* **Solicitações (`/api/solicitacoes/`)**: Requer `aluno`, `curso`, `campus` e `status` (que inicia como `CRIADA`).
* **Documentos (`/api/documentos/`)**: Requer a `solicitacao` atrelada, `nome`, `tipo` e o upload do `arquivo`.
* **Análises (`/api/analises/`)**: Requer `solicitacao`, `coordenador` (ID), o `resultado` (APROVADO/REPROVADO/CORRECAO_NECESSARIA) e `observacoes`.

<!-- COMENTÁRIO: Note que as chaves estrangeiras (ForeignKeys) como "aluno" ou "coordenador" exigem apenas o ID (número inteiro) do respectivo registro no banco de dados. -->

---

## 4. Roteiro e Dicas para a Apresentação

Para brilhar na sua apresentação, siga este roteiro de demonstração ao vivo:

1. **A Interface e Documentação (Swagger):**
   Mostre a tela inicial do Swagger. Destaque que a documentação é gerada de forma automática pelo próprio código.
   * *"Isso facilita a criação de aplicativos web ou mobile no futuro, porque o desenvolvedor frontend já tem um manual interativo pronto!"*

2. **Segurança Ao Vivo:**
   * Faça o login no endpoint `/api/token/` e obtenha o token.
   * Aplique o token no cadeado do Swagger, provando que o sistema restringe o acesso.

3. **O Caminho Feliz (Simulação de um fluxo completo):**
   * **Base:** Liste os `alunos` cadastrados usando a rota `GET`.
   * **Nova Solicitação:** Vá em `POST /api/solicitacoes/` e crie uma nova. Mostre que o sistema gera um ID único.
   * **Análise do Professor:** Use o endpoint `POST /api/analises/` para aprovar a solicitação criada.
   * **Auditoria/Notificações:** Vá em `GET /api/notificacoes/` e mostre que a ação do coordenador gerou um log de evento avisando o aluno!

> **Dica Extra:** Mostre os campos de *paginação* na resposta do Swagger para evidenciar que a API foi pensada para lidar com grandes volumes de dados de forma eficiente.
