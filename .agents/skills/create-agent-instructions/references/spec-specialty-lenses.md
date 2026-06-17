# Lentes Especializadas Para SPECs

Estas lentes orientam o `AGENTS.md` a instruir agentes na criação de SPECs especializadas.

Elas foram consolidadas nesta skill como pontos de vista especializados para arquitetura, backend FastAPI, frontend React e QA.

O `AGENTS.md` gerado não deve citar materiais históricos de referência como fontes operacionais. As fontes diretas devem ser os documentos oficiais atuais do projeto.

## Lente Arquitetural

Aplicar quando uma SPEC envolver:

- camadas;
- fronteiras;
- contratos;
- responsabilidades;
- ADRs;
- riscos técnicos;
- dependências entre módulos;
- mudança estrutural.

Uma SPEC arquitetural deve explicitar:

- dono da regra ou responsabilidade;
- camadas afetadas;
- camadas que não devem ser afetadas;
- contratos de entrada e saída;
- dependências permitidas e proibidas;
- impacto em dados, migração, compatibilidade e exportação;
- auditoria, rastreabilidade e observabilidade;
- critérios arquiteturais de aceite;
- ADRs necessários e bloqueios.

Bloquear quando a SPEC exigir decisão arquitetural ausente.

## Lente Backend FastAPI

Aplicar quando uma SPEC envolver:

- rotas FastAPI;
- schemas;
- validação;
- serialização;
- contratos HTTP;
- erros;
- upload/importação;
- integração da API com domínio, parser, engine ou exportação.

Uma SPEC backend deve explicitar:

- endpoint, método e path;
- path/query/header/body;
- schemas de request, response e erro;
- códigos de status;
- validações da API;
- validações delegadas ao domínio, IO, engine ou export;
- contrato consumido pelo frontend;
- representação de valores precisos sem `float`;
- observabilidade e diagnósticos;
- testes de contrato e integração.

Bloquear quando faltar contrato de API, formato de erro ou separação de responsabilidade.

## Lente Frontend React

Aplicar quando uma SPEC envolver:

- telas;
- fluxos;
- estados de UI;
- consumo de API;
- tabelas;
- upload;
- erros;
- acessibilidade;
- documentos visuais governados.

Uma SPEC frontend deve explicitar:

- tela ou componente afetado;
- usuário e fluxo;
- estados de vazio, loading, sucesso, erro, alerta e bloqueio;
- contrato de API consumido;
- dados necessários para renderização;
- tabelas, colunas, filtros, ações e formatação;
- interação e acessibilidade mínima;
- critérios visuais de aceite;
- regra que não pode ficar no frontend.

Quando existirem docs frontend governados, a SPEC deve observar:

- `docs/frontend/DESIGN_TOKENS.md`
- `docs/frontend/UI_COMPONENT_RULES.md`
- `docs/frontend/SCREEN_PATTERNS.md`
- `frontend/src/styles/globals.css`

Bloquear quando faltar contrato de API, estado de UI essencial ou critério visual.

## Lente QA

Aplicar quando uma SPEC precisar definir:

- estratégia de validação;
- critérios de aceite;
- testes unitários;
- testes de integração;
- golden tests;
- fixtures;
- regressão;
- evidências de qualidade.

Uma SPEC QA deve explicitar:

- comportamento esperado;
- entradas e saídas;
- critérios verificáveis;
- nível de teste proporcional ao risco;
- fixtures;
- casos nominais;
- casos de borda;
- dados inválidos;
- golden cases quando necessário;
- comandos e evidências esperadas;
- lacunas de cobertura justificadas.

Bloquear quando critério de aceite não for verificável ou resultado esperado estiver indefinido.
