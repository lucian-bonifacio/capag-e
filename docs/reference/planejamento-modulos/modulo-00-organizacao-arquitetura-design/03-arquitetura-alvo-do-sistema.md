# 03 - Arquitetura-alvo do sistema

## Objetivo

Definir a arquitetura-alvo do backend, motor, dominio, IO, exportacao, frontend e testes.

## Ponto de decisao

Decidir se o projeto adotara uma camada `src/capag/application/` para casos de uso.

## Arquivos correlatos

- `src/capag/api/main.py`
- `src/capag/api/routes.py`
- `src/capag/api/presentation.py`
- `src/capag/api/session_state.py`
- `src/capag/domain/models.py`
- `src/capag/io/`
- `src/capag/engine/`
- `src/capag/export/`
- `web/src/`
- `tests/`

## Detalhamento

- Definir que `api/` recebe requests, valida contrato, chama casos de uso e serializa resposta.
- Definir que `application/`, se criada, orquestra upload, sessao, simulacao, analise e exportacao.
- Definir que `domain/` contem modelos, estados, invariantes e alertas.
- Definir que `io/` contem leitura, parser e normalizacao da ECD.
- Definir que `engine/` contem PLR, FCO, CAPAG, auditoria, metodologia e analises.
- Definir que `export/` serializa estado calculado, sem recalcular.
- Definir que `web/` nao duplica regra de negocio.

## Camada `application/`

A camada `application/` deve ser avaliada como fronteira entre API e regras internas.

O objetivo e evitar que `src/capag/api/routes.py` concentre:

- composicao de simulacao macrometodologica;
- parse de `FCO` manual simulado;
- soma de `CAPAG` simulada;
- `deepcopy` e simulacao de decisoes condicionais;
- loops de aplicacao de decisoes em grupo;
- restauracao de defaults metodologicos;
- orquestracao de upload, sessao, analise e exportacao.

Casos de uso candidatos:

- `upload_ecd_to_session`;
- `update_fco_for_exercise`;
- `simulate_macro_scenario`;
- `simulate_methodology_decisions`;
- `apply_methodology_decision`;
- `apply_group_decisions`;
- `restore_methodology_defaults`;
- `export_session_workbook`.

Responsabilidade esperada de `routes.py`:

- receber request;
- validar contrato HTTP;
- chamar caso de uso;
- converter excecao em resposta HTTP;
- serializar resposta.

Responsabilidade esperada de `application/`:

- coordenar dominio, engine, IO e exportacao;
- preservar contratos sem depender de FastAPI;
- manter logica testavel por unidade;
- impedir que API vire camada de negocio.

Arquivos futuros possiveis:

- `src/capag/application/__init__.py`;
- `src/capag/application/session_service.py`;
- `src/capag/application/analysis_service.py`;
- `src/capag/application/simulation_service.py`;
- `src/capag/application/export_service.py`;
- `tests/unit/test_application_*.py`.

## Entregavel

Arquitetura-alvo documentada e arvore tecnica proposta.

## Criterios de sucesso

- A API deixa de ser candidata a concentrar regra.
- O motor e a camada declarada ficam bem posicionados.
- O frontend fica explicitamente separado de regra central.
