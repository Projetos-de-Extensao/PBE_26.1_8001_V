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
