---
id: dt
title: Design Thinking
---

# Design Thinking

## 1. Introdução

- **Contexto do Projeto**: O processo de validação de estágios curriculares no Ibmec é realizado de forma manual e descentralizada, envolvendo trocas de e-mail, planilhas e documentos físicos entre alunos, coordenadores e empresas parceiras.
- **Objetivo**: Desenvolver um sistema back-end (API REST) que centralize e automatize o fluxo de gestão e validação de documentos de estágio.
- **Público-Alvo**: Alunos que precisam submeter documentos de estágio, coordenadores que analisam e validam as solicitações, e organizações parceiras que participam do processo de assinatura.
- **Escopo**: API RESTful com Django + DRF cobrindo o fluxo completo desde a criação da solicitação até o encaminhamento institucional.

---

## 2. Fases do Design Thinking

### 2.1. Empatia

**Pesquisa realizada:**

A equipe realizou entrevistas informais e observação do processo atual com alunos e coordenadores do Ibmec para entender as dores de cada perfil.

**Insights principais:**

| Perfil | Dor Identificada |
|---|---|
| **Aluno** | Não sabe quais documentos são obrigatórios para cada tipo de estágio |
| **Aluno** | Não tem visibilidade do status da sua solicitação — precisa perguntar por e-mail |
| **Aluno** | Perde tempo reunindo documentos que depois são rejeitados por erro de formato |
| **Coordenador** | Gerencia dezenas de solicitações em paralelo usando planilhas Excel |
| **Coordenador** | Perde tempo notificando alunos manualmente sobre pendências |
| **Coordenador** | Não tem histórico rastreável de aprovações/reprovações |
| **Empresa** | Não tem canal direto para confirmar dados do contrato de estágio |

**Personas criadas:**

- **Ana (Aluna):** Estudante de Engenharia de Software, 5° período. Precisa validar seu TCE para iniciar o estágio. Quer saber exatamente quais documentos precisa enviar e acompanhar o status em tempo real.
- **Prof. Carlos (Coordenador):** Coordenador do setor de Computação. Analisa ~30 solicitações por semestre. Quer um painel centralizado com filtros e a capacidade de aprovar/reprovar com um clique.
- **Tech Corp (Empresa):** Empresa parceira que recebe estagiários. Precisa confirmar os dados do contrato e assinar digitalmente.

### 2.2. Definição

**Problema Central:**

> "Como podemos centralizar e automatizar o processo de validação de estágios do Ibmec, dando visibilidade ao aluno, reduzindo a carga operacional do coordenador e incluindo a empresa parceira no fluxo?"

**Pontos de Vista (POV):**

- *Ana precisa* de um checklist claro de documentos obrigatórios *porque* ela não sabe o que enviar e perde tempo com reenvios.
- *Prof. Carlos precisa* de um sistema que notifique automaticamente os alunos *porque* ele gasta horas por semana enviando e-mails de cobrança.
- *Tech Corp precisa* de um canal digital para validar propostas *porque* hoje o processo depende de documentos físicos.

### 2.3. Ideação

**Brainstorming realizado:**

A equipe realizou sessões de brainstorming documentadas em [Brainstorming](brainstorm.md), onde foram levantadas diversas ideias para solucionar os problemas identificados.

**Ideias selecionadas:**

1. **API REST com fluxo de estados** — cada solicitação percorre: CRIADA → EM_VALIDACAO → APROVADA/REPROVADA → ENCAMINHADA
2. **Checklist automático** — ao criar uma solicitação, o sistema gera automaticamente a lista de documentos obrigatórios
3. **Notificações automáticas** — cada evento do fluxo dispara uma notificação para o usuário relevante
4. **Permissões por perfil** — aluno vê apenas suas solicitações, coordenador vê as do seu setor
5. **Assinatura digital interna** — hash gerado pelo servidor para rastreabilidade
6. **Aceite da empresa** — endpoint dedicado para a empresa aceitar/recusar a proposta

**Critérios de seleção:**

- Viabilidade técnica com Django + DRF
- Impacto direto na redução de carga operacional
- Alinhamento com a Lei 11.788/08

### 2.4. Prototipagem

**Protótipo de Baixa Fidelidade:**

Foi desenvolvido um protótipo de baixa fidelidade utilizando PlantUML (Salt), documentado em [Protótipo de Baixa Fidelidade](prototipo_baixa_fidelidade.md). O protótipo cobre:

- Tela de login base
- Dashboard do Aluno com solicitações recentes
- Tela de nova solicitação com checklist e upload
- Dashboard do Coordenador com pendências de análise
- Tela de avaliação e parecer
- Portal da Empresa com validação de propostas

**Protótipo de Alta Fidelidade:**

O protótipo de alta fidelidade consiste nas interfaces reais da API: Swagger UI para documentação interativa, Django Admin para gestão, e exemplos de requisição/resposta JSON. Documentado em [Protótipo de Alta Fidelidade](../Elaboracao/prototipo_alta_fidelidade.md).

### 2.5. Teste

**Feedback obtido:**

- A documentação Swagger facilita a compreensão dos endpoints e permite testar a API sem ferramentas externas
- O checklist automático foi bem recebido — reduz dúvidas sobre quais documentos enviar
- As notificações automáticas eliminam a necessidade de comunicação manual
- O fluxo de estados garante rastreabilidade de cada decisão

**Ajustes realizados:**

- Adição de `@action` para aprovar/reprovar/solicitar-correcao em vez de alterar status diretamente
- Filtro de notificações por destinatário (cada usuário vê apenas as suas)
- Hash de assinatura digital gerado pelo servidor (não pelo cliente)

---

## 3. Conclusão

- **Resultados Obtidos:** Sistema back-end funcional com API REST cobrindo o fluxo completo de validação de estágios, com autenticação JWT, permissões por perfil, notificações automáticas e documentação OpenAPI.
- **Próximos Passos:** Desenvolvimento de frontend para consumir a API; integração com provedores externos de assinatura digital; utilização do SQLite em produção pela simplicidade da aplicação.
- **Aprendizados:** A aplicação do Design Thinking permitiu identificar dores reais dos usuários antes de implementar, resultando em funcionalidades como checklist automático e notificações que atacam diretamente os problemas mais citados.

---

## Referências

> BROWN, Tim. Design Thinking: Uma metodologia poderosa para decretar o fim das velhas ideias. Campus, 2010.

> Processo de estágio do Ibmec — observação e entrevistas informais realizadas pela equipe em 2026.

---

## Autor(es)

| Data       | Versão | Descrição                            | Autor(es)         |
|---|---|---|---|
| 07/06/2026 | 1.0    | Preenchimento completo do Design Thinking com conteúdo real do projeto | Equipe PBE |
