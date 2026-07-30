# LOG - TASK-107 - Integrar validade do balanço ao PLRA e CAPAG-E

## Referência

- Task: `tasks/TASK-107-integrar-validade-balanco-plra-capag.md`
- SPEC: `specs/SPEC-012-modulo-1c-balanco-patrimonial-declarado.md`
- Status: concluido

## Fontes Consultadas

- `docs/product/PRD.md`
- `docs/architecture/architecture.md`
- `specs/SPEC-004-modulo-3-contrato-capag-e-plra-fca-roa.md`
- `specs/SPEC-011-modulo-1b-motor-plra.md`
- `specs/SPEC-012-modulo-1c-balanco-patrimonial-declarado.md`
- `tasks/TASK-095-implementar-motor-plra.md`
- `tasks/TASK-097-criar-api-integracao-plra-capag-e.md`
- `tasks/TASK-105-criar-api-balanco-declarado.md`

## Execução

- Data: 2026-07-29
- Ação: implementação e validação.
- Resumo: PLRA passou a consumir o `balance_status` oficial sem recalcular o balanço. Somente `VALIDO` permite resultado final; os demais estados preservam valores diagnósticos e propagam bloqueio e limitação para CAPAG-E, API, UI e Excel. Fórmulas e tratamentos prudenciais permaneceram inalterados.

## Arquivos Alterados

- `backend/alembic/versions/0058_balance_status_plra_capag.py`
- `backend/app/application/capag_service.py`
- `backend/app/application/plra_service.py`
- `backend/app/domain/capag.py`
- `backend/app/domain/plra.py`
- `backend/app/engine/capag.py`
- `backend/app/engine/plra.py`
- `backend/app/export/capag_excel.py`
- `backend/app/export/plra_excel.py`
- `backend/app/repositories/capag_assessments.py`
- `backend/app/repositories/plra_calculations.py`
- `backend/app/schemas/capag.py`
- `backend/app/schemas/plra.py`
- `backend/tests/`
- `frontend/src/api/capag.ts`
- `frontend/src/api/plra.ts`
- `frontend/src/routes/CapagAssessmentPage.tsx`
- `frontend/src/routes/PlraPage.tsx`
- `frontend/src/test/`

## Validações

- Comando: testes backend focados via `docker compose`.
  - Resultado: 70 testes aprovados.
- Comando: `docker compose run --rm backend-tests`.
  - Resultado: 271 testes aprovados.
- Comando: `docker compose run --rm frontend-tests`.
  - Resultado: 27 testes aprovados e build de produção concluído.
- Comando: recriação do backend e `alembic current` via `docker compose`.
  - Resultado: PostgreSQL migrado para `0058_balance_status (head)` e serviço saudável.
- Cobertura: todos os cinco estados do balanço foram testados em PLRA e CAPAG-E; reprocessamento continua invalidando resultados dependentes.
- Comando: busca focada por `float` e `parseFloat`.
  - Resultado: nenhuma ocorrência nos arquivos alterados.

## Pendências Ou Bloqueios

- Nenhum.

## Homologação

- Status: aprovado
- Data: 2026-07-30
- Decisão do usuário: grupo `TASK-101` a `TASK-108` homologado.
- Observação: TASK concluída por homologação consolidada do grupo.
