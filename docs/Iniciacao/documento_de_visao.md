---
id: documento_de_visao
title: Documento de Visão
---
## Introdução

<p align = "justify">
O propósito deste documento é fornecer uma visão geral sobre o projeto <strong>Sistema de Gestão e Validação de Estágios</strong>, desenvolvido na disciplina de Prática Baseada em Evidências (PBE) no Ibmec. Nele são descritas de maneira resumida as principais funcionalidades, usabilidades, o problema que será abordado e os objetivos da equipe.
</p>

## Descrição do Problema 

<p align = "justify">
Atualmente, o processo de validação de estágios curriculares no Ibmec envolve etapas manuais e descentralizadas: o aluno precisa reunir diversos documentos, enviá-los por e-mail ou presencialmente, e aguardar análise da coordenação sem visibilidade sobre o andamento. A coordenação, por sua vez, gerencia múltiplas solicitações em paralelo utilizando planilhas e trocas de e-mail, o que gera atrasos, perda de documentos e retrabalho.
</p>

### Problema

Dificuldade em gerenciar, organizar e validar as solicitações de estágio de forma eficiente, segura e rastreável, resultando em atrasos no processo e falta de transparência para os alunos.

### Impactados

- **Alunos**: que precisam submeter documentos de estágio e acompanhar o status de suas solicitações.
- **Coordenadores**: responsáveis por analisar, aprovar ou rejeitar as solicitações e seus documentos.
- **Organizações Parceiras**: empresas que participam do processo de validação e assinatura de contratos de estágio.

### Consequência

A ausência de um sistema centralizado causa perda de documentos, falta de padronização, atrasos na validação, ausência de rastreabilidade e dificuldade de comunicação entre as partes envolvidas no processo de estágio.

### Solução

Utilizar uma aplicação web (API REST) que centraliza todo o fluxo de gestão de estágios — desde a criação da solicitação pelo aluno, passando pela submissão de documentos, análise pela coordenação, assinatura digital e encaminhamento institucional — oferecendo transparência, segurança e eficiência ao processo.

## Objetivos

<p align = "justify">
O objetivo da equipe de desenvolvimento é fornecer um sistema completo de gerenciamento de estágios que permita:
</p>

- Digitalizar e padronizar o processo de validação de estágios.
- Oferecer um checklist claro de documentos obrigatórios para cada tipo de solicitação.
- Permitir o envio e a análise de documentos de forma centralizada.
- Notificar automaticamente os envolvidos sobre mudanças de status.
- Disponibilizar modelos de documentos para download pelos alunos.
- Suportar assinatura digital para formalização de contratos.
- Permitir o encaminhamento de documentos assinados à reitoria.

## Descrição do Usuário 

<p align = "justify">
Os usuários do sistema são divididos em três perfis com funcionalidades específicas:
</p>

- **Aluno**: Cria solicitações, consulta checklists, baixa modelos de documentos, envia documentos para validação e acompanha o status da sua solicitação.
- **Coordenador**: Lista e analisa solicitações, revisa documentos, aprova/reprova/solicita correção, assina documentos digitalmente e encaminha para a reitoria.
- **Organização Parceira**: Valida propostas de estágio, confirma dados do estagiário e assina contratos.

## Recursos do produto

### Autenticação e Autorização

<p align = "justify">
O sistema implementa autenticação via JWT (JSON Web Token), garantindo que apenas usuários autenticados acessem os recursos da API conforme seu perfil (aluno, coordenador ou organização parceira).
</p>

### Gestão de Solicitações

<p align = "justify">
O aluno pode criar solicitações de validação de estágio informando curso e campus. A solicitação percorre os status: Criada → Em Validação → Aprovada / Reprovada / Correção Necessária → Encaminhada.
</p>

### Checklist e Documentos

<p align = "justify">
Cada solicitação possui um checklist de documentos obrigatórios. O aluno pode baixar modelos de documentos disponibilizados pela coordenação e enviar os documentos preenchidos para validação.
</p>

### Análise e Revisão

<p align = "justify">
A coordenação pode listar todas as solicitações do seu curso, analisar os documentos enviados e emitir um parecer (aprovado, reprovado ou correção necessária).
</p>

### Notificações

<p align = "justify">
O sistema notifica automaticamente alunos e coordenadores sobre eventos relevantes como criação de solicitação, envio de documentos, conclusão de análise e encaminhamentos.
</p>

### Assinatura Digital e Encaminhamento

<p align = "justify">
O sistema suporta assinatura digital de documentos e permite o encaminhamento institucional de solicitações aprovadas para a reitoria.
</p>

## Restrições

<p align = "justify">
A aplicação não será responsável pela integração direta com sistemas externos de assinatura digital (como gov.br ou ICP-Brasil) nesta versão, sendo a funcionalidade de assinatura implementada de forma interna para registro e rastreabilidade. A aplicação também não cobre a gestão acadêmica além do escopo de estágios.
</p>

## Referências Bibliográficas

> Django REST Framework. Disponível em https://www.django-rest-framework.org/. Acesso em 01/06/2026.

> Django Documentation. Disponível em https://docs.djangoproject.com/en/4.2/. Acesso em 01/06/2026.

## Versionamento
| Data | Versão | Descrição | Autor(es) |
| -- | -- | -- | -- |
| 01/06/2026 | 1.0 | Preenchimento do documento de visão com conteúdo real do projeto | Equipe PBE | 
