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

#Especificação dos Casos de Uso

## Especificaçõs dos Casso de Uso

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
