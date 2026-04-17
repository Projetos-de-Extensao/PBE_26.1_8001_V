---
id: prototipo_baixa_fidelidade
title: Protótipo de Baixa Fidelidade
---

## Introdução

<p align="justify">
A construção do protótipo de baixa fidelidade tem como objetivo apresentar de forma visual e simplificada as principais interfaces do Sistema de Validação Automatizada de Documentos de Estágio. Ele auxilia no alinhamento das expectativas e na identificação precoce das necessidades de interação dos perfis: Aluno, Coordenador e Organização Parceira.
</p>

## Metodologia

<p align="justify">
O desenvolvimento do protótipo baseou-se nos casos de uso e requisitos levantados, como submissão de documentos, acompanhamento de solicitações e validação. Utilizamos a integração Kroki com a ferramenta PlantUML (Salt) para a construção das telas, focando no fluxo principal de cada usuário.
</p>

## Protótipo de baixa fidelidade

### Tela Login Base

```kroki-plantuml
@startsalt
{
  Sistema de Validação de Estágios
  ==
  .
  E-mail Institucional / CNPJ: | "                    "
  Senha:                       | "********************"
  .
  [   Acessar   ]
  .
  "Esqueceu a senha?" | "Ajuda"
}
@endsalt
```

<p align="justify">
<b>Componentes da Tela:</b><br/>
• <b>Campos de Texto (E-mail Institucional / CNPJ e Senha):</b> Permitem a inserção das credenciais de acesso. O sistema diferenciará o perfil (Aluno, Coordenador ou Empresa) com base no e-mail ou CNPJ inserido.<br/>
• <b>Botão "Acessar":</b> Aciona a verificação das credenciais (Caso de Uso: Autenticar Usuário).<br/>
• <b>Links "Esqueceu a senha?" e "Ajuda":</b> Opções de recuperação de acesso e suporte para os usuários institucionais e externos.
</p>

### Tela Dashboard - Aluno

```kroki-plantuml
@startsalt
{+
  Olá, Aluno! | [ Meu Perfil ] | [ Sair ]
  ==
  {T
    + Painel
    ++ Nova Solicitação
    ++ Minhas Solicitações
    ++ Modelos de Documentos
  }
  ==
  Minhas Solicitações Recentes
  --
  .
  {#
    ID  | Tipo              | Status      | Última Atualização
    #12 | Validação de TCE  | Em Análise  | 10/04/2026
    #08 | Relatório Parcial | Aprovado    | 15/03/2026
  }
}
@endsalt
```

<p align="justify">
<b>Componentes da Tela:</b><br/>
• <b>Cabeçalho:</b> Exibe a saudação ao aluno logado, com opções de acessar o "Meu Perfil" e "Sair" do sistema.<br/>
• <b>Menu Lateral/Superior (Painel):</b> Links rápidos para as principais ações do aluno ("Nova Solicitação", para iniciar um novo processo; "Minhas Solicitações", para visualizar o histórico; "Modelos de Documentos", para baixar templates necessários).<br/>
• <b>Tabela "Minhas Solicitações Recentes":</b> Apresenta um resumo dinâmico do status dos documentos enviados. Cada linha (ID, Tipo, Status, Última Atualização) permite que o aluno acompanhe rapidamente o andamento do seu estágio sem precisar entrar em detalhes a todo instante.
</p>

### Tela de Nova Solicitação - Aluno

```kroki-plantuml
@startsalt
{+
  Nova Solicitação
  ==
  .
  Tipo de Documento: | ^Termo de Compromisso de Estágio (TCE)^
  Curso:             | "Engenharia de Software"
  Campus:            | "Campus Sede"
  .
  Documentos Necessários (Upload):
  [X] Identidade (PDF) | [ Anexar ]
  [X] Comprovante de Matrícula (PDF) | [ Anexar ]
  [ ] TCE Assinado pela Empresa | [ Anexar ]
  .
  [   Enviar Solicitação   ] | [ Cancelar ]
}
@endsalt
```

<p align="justify">
<b>Componentes da Tela:</b><br/>
• <b>Seletores/Campos Informativos:</b> Permitem escolher o "Tipo de Documento" (ex: TCE, Relatório) e visualizar o "Curso" e "Campus" vinculados ao aluno.<br/>
• <b>Lista de Documentos Necessários (Checklist):</b> Uma lista dinâmica gerada pelo sistema de acordo com o tipo de documento solicitado.<br/>
• <b>Botões "Anexar":</b> Responsáveis pela ação de selecionar e realizar o upload dos arquivos (frequentemente em versão PDF).<br/>
• <b>Checkboxes [X]:</b> Indicadores visuais que mudam de estado automaticamente quando o arquivo é carregado com sucesso.<br/>
• <b>Botões de Ação Final:</b> "Enviar Solicitação" para submeter o pacote para análise, e "Cancelar" para descartar a operação atual.
</p>

### Tela Dashboard - Coordenador

```kroki-plantuml
@startsalt
{+
  Painel do Coordenador | [ Sair ]
  ==
  Pendências de Análise
  --
  Buscar Aluno: | "                " | [ Filtrar ]
  Status:       | ^Aguardando Revisão^ 
  .
  {#
    ID  | Aluno           | Documento         | Data Envio | Ações
    #13 | Carlos Almeida  | Relatório Final   | 11/04/2026 | [ Avaliar ]
    #12 | Maria Souza     | TCE               | 10/04/2026 | [ Avaliar ]
    #10 | Ana Silva       | Plano Atividades  | 05/04/2026 | [ Avaliar ]
  }
}
@endsalt
```

<p align="justify">
<b>Componentes da Tela:</b><br/>
• <b>Cabeçalho:</b> Identificação clara do nível de acesso ("Painel do Coordenador").<br/>
• <b>Área de Filtros:</b> Campos "Buscar Aluno" e "Status", acompanhados do botão "Filtrar", para facilitar a organização das pendências por parte do coordenador.<br/>
• <b>Tabela "Pendências de Análise":</b> Lista das solicitações aguardando ação. Apresenta o nome do aluno, o tipo de documento, a data de envio e, crucialmente, o botão "Avaliar", que direciona o coordenador para a análise aprofundada.
</p>

### Tela de Avaliação e Parecer - Coordenador

```kroki-plantuml
@startsalt
{+
  Avaliar Solicitação #12
  ==
  .
  Aluno:   | Maria Souza
  Arquivo: | TCE_Assinado.pdf [ Visualizar ]
  .
  -- Validação Automática do Sistema --
  Score de Verificação: 95%
  [X] Assinaturas Digitais Identificadas
  [X] Carga horária dentro do limite
  .
  -- Parecer Técnico --
  Conceito: 
  () Aprovado
  () Devolvido para Correção
  () Reprovado
  .
  Observações:
  "                                        "
  "                                        "
  .
  [ Assinar e Encaminhar Institucionalmente ] | [ Cancelar ]
}
@endsalt
```

<p align="justify">
<b>Componentes da Tela:</b><br/>
• <b>Resumo da Solicitação:</b> Traz informações essenciais e um link "Visualizar" que possibilita inspecionar o arquivo anexado.<br/>
• <b>Seção "Validação Automática do Sistema":</b> Exibe o "Score de Verificação" (ex: 95%) e itens de checklist pré-analisados pelo motor sistêmico de IA (Assinaturas digitais, carga horária), facilitando o julgamento humano.<br/>
• <b>Seção "Parecer Técnico":</b> Contém opções de decisão (Aprovado, Devolvido, Reprovado) e uma área de texto livre para "Observações", justificando a escolha feita.<br/>
• <b>Botão "Assinar e Encaminhar Institucionalmente":</b> Confirma a revisão e aciona o fluxo de assinatura digital do coordenador para prosseguimento do processo.
</p>

### Tela Dashboard - Organização Parceira

```kroki-plantuml
@startsalt
{+
  Portal da Empresa | [ Sair ]
  ==
  Validação de Propostas de Estágio
  --
  .
  {#
    Aluno           | Curso        | Tarefa pendente | Ação
    Maria Souza     | Eng. Soft.   | Concordar TCE   | [ Revisar ]
  }
}
@endsalt
```

<p align="justify">
<b>Componentes da Tela:</b><br/>
• <b>Cabeçalho:</b> Identificação do acesso da Organização com ação de saída.<br/>
• <b>Tabela "Validação de Propostas de Estágio":</b> Listagem simples exibindo quais propostas e documentos vinculados a alunos aguardam deliberação por parte da empresa. O botão "Revisar" abre o contrato para aprovação.
</p>

### Tela de Revisão e Aceite - Organização Parceira

```kroki-plantuml
@startsalt
{+
  Revisar Contrato de Estágio
  ==
  .
  Aluno: Maria Souza
  .
  [ Visualizar Minuta do Contrato ]
  .
  [X] Declaro que as informações do plano de atividades conferem.
  [X] Confirmo o compromisso da organização.
  .
  "Insira sua senha/token para assinar digitalmente:" | "******"
  .
  [ Aceitar Proposta e Assinar ] | [ Recusar Proposta ]
}
@endsalt
```

<p align="justify">
<b>Componentes da Tela:</b><br/>
• <b>Botão "Visualizar Minuta do Contrato":</b> Exibe o documento previamente preparado para o supervisor/representante da empresa realizar a devida conferência.<br/>
• <b>Termos de Concordância (Checkboxes):</b> Requisito legal de aceite, onde o parceiro concorda expressamente com os termos do estágio e as obrigações elencadas.<br/>
• <b>Campo de Senha/Token:</b> Viabiliza autenticação da assinatura digital integrada para validação deste termo.<br/>
• <b>Botões Finais:</b> "Aceitar Proposta e Assinar" para deferir, ou "Recusar Proposta", retornando a demanda com status e histórico apropriados.
</p>

## Conclusão

<p align="justify">
A utilização do protótipo de baixa fidelidade possibilitou a visualização inicial das interfaces do sistema, refletindo diretamente os Casos de Uso especificados para os principais atores envolvidos na validação automatizada de documentos de estágio.
</p>

## Referências

> Ferramenta PlantUML para Criação de Protótipos. Disponível em https://plantuml.com/salt

## Autor(es)

| Data       | Versão | Descrição                            | Autor(es)         |
| ---------- | ------ | ------------------------------------ | ----------------- |
| 16/04/2026 | 1.0    | Criação do protótipo com PlantUML    | Davi Jacob, Daniel Studart, João Paulo Dopcke, Gustavo Rezende e Felipe Ultramar |
