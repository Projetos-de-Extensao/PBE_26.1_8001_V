# Documentação do Schema OpenAPI

## Objetivo

Este projeto agora conta com o arquivo `openapi_schema.yaml` gerado estaticamente. 
A decisão de incluir este arquivo no versionamento do projeto foi tomada com foco em trazer melhores práticas de mercado e integração contínua (CI/CD) para a nossa arquitetura.

## Por que adicionar o `openapi_schema.yaml`?

Embora o nosso backend já possua a interface visual do Swagger (gerada dinamicamente via rotas do Django), a exportação estática do contrato da API (OpenAPI 3.0) traz os seguintes benefícios fundamentais que a visualização web não entrega sozinha:

1. **Garantia de Qualidade (QA) e Automação:** Com o schema fixo e versionado no Git, qualquer membro da equipe ou ferramenta de DevOps consegue validar automaticamente se novos commits quebraram contratos antigos da API.
2. **Integração com Ferramentas Externas:** O arquivo `.yaml` permite a importação direta para coleções do Postman ou Insomnia, permitindo que as equipes de teste validem todos os endpoints (`solicitacoes`, `documentos`, `analises`, etc) com exatidão, sem precisar mapear manualmente.
3. **Geração de Código Frontend:** O schema permite que ferramentas geradoras criem automaticamente o código client-side em frameworks como React ou Vue, economizando tempo de desenvolvimento.

Com a adição deste arquivo, a infraestrutura da API do sistema de Gestão de Estágios torna-se mais corporativa, robusta e fácil de integrar com outras tecnologias no futuro.
