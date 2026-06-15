---
name: backend-fastapi-spec
description: Apoiar a criação e revisão de SPECs do CAPAG com impacto em backend FastAPI. Use quando uma SPEC precisar definir rotas, schemas, validações, erros, serialização, contratos com frontend ou integrações da API com domain, io, engine ou export.
---

# Backend FastAPI Spec CAPAG

## Objetivo

Esta skill apoia a criação de qualquer SPEC do CAPAG que envolva backend FastAPI, garantindo que contrato HTTP, schemas, validações, erros, serialização e integrações estejam claros antes de uma task ser escrita.

Use quando houver necessidade de criar, revisar ou completar uma SPEC que toque rotas FastAPI, schemas, validação de entrada, serialização de saída, erros HTTP, contratos com frontend ou integração da API com `domain`, `io`, `engine` ou `export`. Não use para implementar código, criar task, aprovar documento ou substituir `document-control`.

## Pergunta Central

Ao criar ou revisar uma SPEC que envolva backend FastAPI, responda sempre:
> Para executar a task futura com segurança, qual contrato de API, validação, erro, serialização e integração precisa estar explícito para evitar comportamento ambíguo ou regra de negócio duplicada na camada FastAPI?

Se a SPEC não puder definir esse contrato com as decisões existentes, registre bloqueio ou decisão pendente.

## Fontes

Antes de apoiar uma SPEC, leia o mínimo necessário:

- `AGENTS.md`;
- `docs/architecture/ARCHITECTURE.md`;
- PRD e documentos oficiais relacionados ao escopo;
- SPEC alvo, quando já existir;
- ADRs relacionados em `docs/decisions/`;
- arquivos em `src/capag/api/` apenas quando for necessário confirmar contrato atual;
- arquivos em `src/capag/domain/`, `src/capag/io/`, `src/capag/engine/` ou `src/capag/export/` apenas quando for necessário confirmar fronteira de integração.

Se houver divergência material entre fontes, pare e faça uma pergunta direta ao usuário antes de prosseguir.

## Visão Backend Obrigatória

Ao criar ou revisar uma SPEC que envolva backend FastAPI, garanta que ela cubra os blocos aplicáveis.

Contrato HTTP:

- endpoint, método, path e propósito;
- parâmetros de path, query, headers e body;
- formato de request e response;
- códigos de status esperados;
- compatibilidade com contratos existentes e consumidores atuais;
- impacto em versões de API ou necessidade de migração de contrato.

Schemas e serialização:

- schemas de entrada e saída;
- campos obrigatórios, opcionais, defaults e nulabilidade;
- tipos de dados, enumerações e formatos especiais;
- representação de `Decimal` sem perda de precisão;
- serialização de datas, valores contábeis, indicadores, alertas e erros;
- estabilidade dos nomes de campos consumidos pelo frontend.

Validação:

- validações que pertencem à API;
- validações que pertencem ao domínio, parser, engine ou exportação;
- mensagens ou códigos de erro esperados;
- comportamento para arquivo inválido, payload incompleto, tipo incorreto, estado incompatível ou fluxo fora de ordem;
- limites de tamanho, formato e conteúdo quando houver upload/importação.

Integração entre camadas:

- qual função, serviço ou módulo a API deve chamar;
- dados que entram na camada de integração;
- dados retornados pela integração;
- responsabilidades que a API não deve assumir;
- regras de negócio que devem permanecer em `domain` ou `engine`;
- leitura/parsing que deve permanecer em `io`;
- geração de Excel que deve permanecer em `export`.

Frontend e experiência de erro:

- contrato que o frontend pode assumir;
- estados de carregamento, sucesso, erro e alerta que a API precisa diferenciar;
- formato de erro legível e acionável;
- estabilidade necessária para tabelas, grids e fluxos de usuário.

Qualidade operacional:

- logs, diagnósticos e erros esperados;
- rastreabilidade de requisições e etapas relevantes;
- observabilidade mínima para upload, processamento, cálculo e exportação;
- impacto esperado em testes unitários de schema, testes de endpoint e testes de integração.

## Regras de Camada

A SPEC deve preservar:

- `src/capag/api/` como camada de rotas, schemas, validação de entrada e serialização;
- `src/capag/domain/` como camada de conceitos, invariantes, estados e alertas;
- `src/capag/io/` como camada de leitura, parsing e normalização de ECD;
- `src/capag/engine/` como camada de cálculo, auditoria e regra prudencial;
- `src/capag/export/` como camada de serialização Excel com `openpyxl`;
- `web/` como consumidor do contrato, sem regra de negócio central.

A API não deve recalcular regra prudencial, não deve duplicar lógica do engine e não deve usar `float` para valores contábeis, fiscais, financeiros ou prudenciais.

## Fluxo para SPEC

1. Identifique o fluxo de usuário ou sistema que passa pela API.
2. Defina endpoint, método, path e contrato HTTP.
3. Especifique schemas de request, response e erro.
4. Separe validação de API, validação de domínio e regra de negócio.
5. Descreva integração com `domain`, `io`, `engine` ou `export`.
6. Defina compatibilidade com frontend e contratos existentes.
7. Inclua observabilidade, diagnósticos e erros esperados.
8. Escreva critérios de aceite verificáveis para a task futura.
9. Declare riscos, decisões pendentes e fora de escopo.

## Critérios Backend de Aceite

Uma SPEC que envolva backend FastAPI só está clara quando permite responder:

- qual endpoint será criado ou alterado;
- qual request é aceito;
- qual response é produzido;
- quais erros podem ocorrer e em qual formato;
- qual validação é feita na API;
- qual validação ou regra é delegada a outra camada;
- como valores `Decimal` serão recebidos ou serializados;
- como o frontend consumirá sucesso, erro, alerta ou estado intermediário;
- quais testes comprovam o contrato.

## Bloqueios

Pare imediatamente, não tente contornar a regra e faça uma pergunta direta ao usuário quando houver:

- ausência de contrato de API necessário para escrever a SPEC;
- regra de negócio indefinida;
- tentativa de calcular regra prudencial na API;
- tentativa de duplicar regra do engine ou domínio na API;
- necessidade de mudar arquitetura, stack, persistência ou paths oficiais;
- divergência material entre contrato documentado e código existente;
- ausência de decisão sobre formato de erro, schema ou compatibilidade relevante.

## Formato Esperado da SPEC

Ao redigir texto para uma SPEC ou seção backend de SPEC, use esta estrutura em Markdown. Preserve o front matter e o `Controle Documental` definidos pela governança do projeto quando estiver editando o documento inteiro.

```markdown
# [Título da SPEC]

## Contexto e Fluxo

[Explique o fluxo que passa pela API e o problema que a SPEC precisa resolver.]

## Contrato FastAPI

### Endpoint

- Método:
- Path:
- Propósito:

### Request

- Path params:
- Query params:
- Headers:
- Body:

### Response

- Status de sucesso:
- Schema de resposta:
- Estados ou alertas retornados:

### Erros

- [Código HTTP] [Condição] [Formato da resposta]

## Validação e Responsabilidades

- API:
- Domain:
- IO:
- Engine:
- Export:
- Fora da API:

## Compatibilidade e Frontend

- [Contrato consumido pelo frontend, estabilidade de campos e impacto em fluxos existentes.]

## Observabilidade e Diagnóstico

- [Logs, erros esperados, rastreabilidade e pontos de diagnóstico.]

## Critérios Backend de Aceite

- [ ] [Critério verificável que uma task futura consiga confirmar.]

## Riscos e Decisões Pendentes

- [Risco, decisão pendente ou bloqueio.]

## Fora de Escopo

- [O que a SPEC não deve resolver.]
```

## Limites

Esta skill não cria task, não implementa backend, não define regra de negócio, não aprova documento e não substitui `document-control` ou `architect-spec`.

O produto esperado é orientação ou texto para a parte backend FastAPI de uma SPEC, com contrato suficiente para que a task futura não precise decidir API, validação, erro ou integração durante a execução.
