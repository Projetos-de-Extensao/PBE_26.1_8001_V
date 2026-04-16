---
id: diagrama_de_casos de uso
title: Diagrama de Casos de Uso
---

# Casos de Uso

## Introdução

Os casos de uso têm como objetivo representar as interações essenciasi entre os usuários e o sistema responsável pela validação automatizada de documentos de estágio.

Com base no levantemnto de requisitos realizado, foram definidos dois atores principais: **Coordenadores** e **Alunos**
O aluno é responsavel por iniciar solicitações, anexar documentos e acompanhar o progresso do processo. 
Já o coordenador desempenha o papel de análise, validação complementar, assinatura e encaminhamento dos documentos para as etapas finais.

## Especificaçõs dos Casos de Uso

## FUNC1- Autenticar Usuário
**Atores:** Aluno, Coordenador
**objetos:** Permitir que o usuário acesse o sistema de forma segura.
**Pré-requisito:** Usuários acesse o sistema de forma segura.
**Fluxo principal:**

1. O usuário acessa a página principal inicial.
2. Informa suas credenciais
3. O sistema valida as informações.
4. O acesso é liberado conforme o perfil.

**Fluxo principal:**
1. O usuário acessa a página incial.
2. Informa suas credenciais.
3. O sistema valida as informações.
4. O acesso é liberado conforme o perfil.

**Fluxo alternativo:**
- Dados incorretos -> Será exibido a mensagem de erro.

**Pós-requisito:** Usuário autenticado.
---
## FUNC2- Criar Solicitação
**Ator:** Aluno 
**Obejtivo:** Iniciar um nove pedido de validação de estágio.
**Pré-requisito:** Tem que estar logado no sistema.

**Fluxo principal:**
1. Acessar área de solicitações.
2. Informar curso e campus.
3. O sistema registra a solicitação.
4. O checklist é apresentado.

**Pós-requisitos:** Solicitação criada com sucesso.

---

## FUNC3- Consultar Checklist 

**Ator.** Aluno
**Objetivo:** Verificar documentos obrigatórios.

**Pré- requisito:** Solicitação existente.

**Fluxo principal:**
1. Selecionar a solicitação.
2. O sistema carrega as exigências.
3. Exibe a lista de docuemntos.

**Pós-requisito:** Checklist disponível.
---

## FUNC4- Download de Modelos
**Ator:** Aluno
**Objeto:** Acessar modelos padrão de documentos.

**Pré-requisitos:** Solicitação Ativa.

**Fluxo principal:**
1. Acessar área de modelos.
2. Escolher documento.
3. Download realizado

**Pós-requisitos:** Arquivo disponível no dispositivo

---


## FUNC5
**Ator:** Aluno
**objetivo:** Submeter documentos para validação.

**Pré-requesito:** Documentos obrigatórios disponíveis.

**Fluxo principal:**
1. selecionar arquivos.
2. Upload realizado.
3. Sistema inicia análisa automática.
4. Status atualizado para **Em Processo De Validação**

**Pós-requisito:** Documentos enviados para análise.

---

## FUNC6

**Ator:** Aluno
**Objetivo:** Acompanhar andamento da solicitação.

**Pré-requisito:** solicitação registrada

**Fluxo principal:**

1. Acessar lista de solicitações.
2. Visualizar status atual:
   - Em validação
   - Correção necessária
   - Aprovado
   - Encaminhado
**Pós-requisitos:** Status atualizado visualizado.

---


## FUNC7  - Notificação do Sistema

**Atores>:** Aluno, Coordenador
**Objetivo:** Informar eventos relevantes.

**Eventos:**
- envio realizado
- análise concluida
- aprovação ou reprovação
- solicitação de ajuste
- envio para reitoria

**Pós-requisito** Usuário Notificado

---

## FUNC8 - Listar Solicitação

**Ator:** Coordenador
**Objetivo:** Visualizar solicitação do curso.

**Pré-requerimento:** Estar autenticado.

**fluxo principal:**
1. Acessar painel.
2. Sistema exibe solicitações.
3. Selecionar uma para análise.

**Pós-requisito:** Solicitação disponível para revisão

---

## FUNC9 - Analise Documentos
**Ator:** Coordenador
**Objetivo:** Avaliar os documentos enviados pelo aluno.

**Pré-requisito:** Informações Disposiveis para decisão

---

## FUNC10 - Revisar Solicitação
**ator:** Coordenador 
**objetivo.** Tomar decisão final sobre a solicitação.

**Pré-requisitos:** Análise dos documentos realizada.


**Fluxo principal:**
1. Revisar documentos.  
2. Escolher:
   - aprovar  
   - reprovar  
   - solicitar correção  

**Pós-requisito:** Decisão registrada. 

---

## FUNC11 - Assinatura Digital

**Ator:** Coordenador
**Objetivo:** Formalizar aprovação.

**Pré-requisito:** Documento valido.

## FUNC12 - Encaminhamento Institucional

**Ator:** Coordenador
**Objetivo:** Enviar para validação final.

**Pré-requisito:** Documento assinado.

**fluxo principal:**
1. Sistema encaminha à reitoria.  
2. Atualiza status.  
3. Notifica o aluno.  

**Pós-requisito:** Processo enviado para etapa final.

---

Os casos de uso apresentados organizam as funcionalidades principais do sistema, servindo como base para o desenvolvimento, modelagem e implementação da solução.
