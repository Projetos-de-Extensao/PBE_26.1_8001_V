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

##FUNC1- Autenticar Usuário
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
FUNC2- Criar Solicitação
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


### Descrição:

- Contas
	- Criação
	- Entrada
	- Alteração
	- Recuperar Senha
	- Exclusão Lógica
	- Visualização

- Perfis
	- Edição
	- Pesquisar
	- Visualização
	- Seguir/Deixar de Seguir

- Postagens (Público) 	 	
	- Criação
	- Exclusão
	- Interação
	- Visualização

- Mensagens (Privado)
	- Criação
	- Exclusão
	- Visualização

- Galerias
	- Albuns
- Blogs
- Grupos

### Criação de uma conta no sistema

* Atores:

	- Usuário
	- Sistema

- Pré-Condições:
	- Nenhuma

* Fluxo Básico:
    1. Usuário fornece e-mail, senha e confirmações
    2. Dados do Usuário são validados pelo Sistema
    3. Dados do Usuário são encriptados pelo Sistema
    4. Dados do Usuário são persistidos pelo Sistema
    5. Sistema gera um link com prazo de expiração
    6. Sistema envia e-mail de verificação, com o link, para o Usuário
    7. Usuário confirma o e-mail antes do link expirar
    8. Sistema confirma que o Cadastro do Usuário foi realizado com sucesso
    9. Sistema redireciona o Usuário para a página de Entrada

- Fluxos Alternativos:
	- 2a. E-mail do Usuário é inválido
		2a1. Sistema exibe mensagem de erro
	- 2b. Senha do Usuário não respeita regras de segurança
		- 2b1. Sistema exibe mensagem de erro
	- 3a. Usuário tenta confirmar o e-mail depois de o link expirar
		- 3a1. Sistema sugere que o Usuário realize um novo Cadastro

### Entrada do usuário no sistema

- Atores:
	- Usuário
	- Sistema

- Pré-Condições:
	Usuário deve estar cadastrado

- Fluxo Básico:
    - 1. Usuário fornece e-mail e senha
	- 2. Sistema autentica o Usuário
	- 3. Sistema redireciona o Usuário para a página inicial

- Fluxos Alternativos:
	- 2a. Dados do Usuário Inválidos
		- 2a1. Sistema exibe mensagem de erro
	- 3a. Primeio acesso do Usuário
		- 3a1. Sistema redireciona o Usuário para a página de edição de perfil
