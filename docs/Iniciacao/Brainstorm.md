---
id: brainstorm
title: Brainstorm
---

## Introdução

O brainstorm é uma técnica de elicitação de requisitos que consiste em reunir a equipe e discutir sobre diversos tópicos gerais do projeto apresentados no documento problema de negócio. No brainstorm, o diálogo é incentivado e críticas são evitadas para permitir que todos colaborem com suas próprias ideias.

## Metodologia

A equipe se reuniu para debater ideias gerais sobre o projeto no dia 06/04/2026, por meio do Discord. A atividade teve início às 19:00 e terminou às 20:30. Davi Jacob atuou como moderador, direcionando a equipe com questões pré-elaboradas e registrando as respostas no documento.

## Brainstorm

## Versão 1.0

## Perguntas

### 1. Qual o objetivo principal da aplicação?

**1** - Desenvolver uma API focada na validação automática de propostas de estágio.

**2** - Garantir que a validação respeite rigorosamente a Lei 11.788/08 (limites de horas, apólice de seguro e vigência).

**3** - Reduzir a carga de trabalho operacional dos coordenadores com análise puramente manual e burocrática de documentos.

**4** - Servir como um motor de regras centralizado capaz de aprovar, reprovar ou reter contratos de estágio.

**5** - Tornar a avaliação muito mais rápida para os alunos diminuindo a fila de espera.

---

### 2. Como será o processo para cadastrar um novo cliente?

**1** - O administrador institucional do Ibmec deverá cadastrar o sistema cliente que consumirá essa API.

**2** - O cliente (como o portal institucional) recebe as credenciais para autenticação segura.

**3** - Com o sistema logado, será possível consumir as validações do motor de regras.

**4** - O cliente utilizará um token em todas as requisições como forma de autenticação.

**5** - O acesso não será público, protegendo a segurança das requisições.

---

### 3. Como será a forma de adicionar produtos?

**1** - O cliente enviará as propostas de estágio aos endpoints da API por meio de uma requisição HTTP.

**2** - A requisição ("produto") conterá as informações contratuais que precisam ser confrontadas, como carga horária, duração e dados do seguro.

**3** - O sistema da API validará automaticamente todos esses dados contra a legislação trabalhista brasileira.

**4** - As propostas que passarem ou não na validação serão armazenadas no banco de dados para controle institucional.

---

### 4. Outras perguntas pertinentes ao contexto

**1** - Como o motor validará se os documentos obrigatórios não vieram em branco?

**2** - O que acontecerá com contratos que possuem regras muito subjetivas e a API não consegue concluir com 100% de precisão?

**3** - Estaremos integrados com algum sistema de assinatura digital após confirmar que o modelo possui valor legal e foi aprovado?

**4** - Como o coordenador acompanhará o histórico de cada um desses contratos analisados?

---

### 5. "Outras perguntas pertinentes ao contexto", como seria a forma de o cliente adicionar os produtos?

**1** - O cliente deverá enviar requisições do tipo POST para a API em um formato JSON muito bem estruturado com os dados do TCE (Termo de Compromisso de Estágio).

---

### 6. Quais informações seriam interessantes para o cliente?

**1** - O status claro e exato do resultado do motor de regras: Aprovado, Reprovado ou Pendência de Revisão Humana.

**2** - O cliente usuário receberá descritivo das falhas que motivaram a reprovação (ex: "Excedeu 30 horas semanais").

**3** - O usuário da coordenação poderá extrair histórico contendo todo sucesso ou falha dessas requisições avaliadas.

## Requisitos elicitados

| ID   | Descrição |
|------|-----------|
| BS01 | O sistema deve possuir rota de cadastro para criar aplicações clientes. |
| BS02 | O sistema deve autenticar clientes por meio de utilização de tokens restritos. |
| BS03 | O sistema deve receber os dados de Termo de Compromisso de Estágio (TCE) em formato JSON. |
| BS04 | A API deve analisar e impedir jornada superior a 6 horas/dia e 30 horas/semanais. |
| BS05 | O sistema deve exigir a demonstração de apólice de seguro do modelo recebido. |
| BS06 | O sistema deve avaliar limite de contrato de até 2 anos na mesma concedente. |
| BS07 | O sistema deve registrar o resultado: Aprovado, Reprovado ou Precisa de Revisão. |
| BS08 | O sistema deve retornar qual parte da Lei 11.788/08 exata violada em caso de erros na estrutura do TCE. |
| BS09 | O sistema deve deixar relatórios ou histórico que permitam o coordenador consultar avaliações pretéritas. |
| BS10 | O sistema precisa oferecer segurança das informações e logs (auditoria). |
| BS11 | O sistema poderá incluir funcionalidade conectada para assinatura padrão ICP-Brasil ou gov.br. |
| BS12 | O fluxo tem de encaminhar retensões duvidosas/subjetivas pro coordenador (visão humana). |

## Conclusão

Através da aplicação da técnica, foi possível elicitar alguns dos primeiros requisitos do projeto, permitindo uma melhor compreensão do problema e das funcionalidades esperadas para o sistema de gestão de estágios.

## Referências Bibliográficas

> BARBOSA, S. D. J.; DA SILVA, B. S. *Interação humano-computador*. Elsevier, 2010.

## Autor(es)

| Data       | Versão | Descrição            | Autor(es) |
|------------|--------|----------------------|-----------|
| 06/04/2026 | 1.0    | Criação do documento | Daniel Studart, Davi Jacob, João Paulo Dopcke, Felipe Ultramar, Gustavo Rezende |
