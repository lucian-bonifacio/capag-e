# LOG - TASK-064 - Criar API DFC/FCA

## Referência

- Task: `tasks/TASK-064-criar-api-dfc-fca.md`
- SPEC: `specs/SPEC-006-modulo-5-dfc-direta-fca.md`
- Status: aguardando_homologacao

## Fontes Consultadas

- `docs/product/PRD.md`
- `docs/architecture/architecture.md`
- `specs/SPEC-006-modulo-5-dfc-direta-fca.md`
- `specs/SPEC-005-modulo-4-evidencias-justificativas-ativos.md`
- `docs/reference/planejamento-modulos/modulo-05-dfc-direto-fca/`

## Execução

- Data: 24/07/2026
- Ação: persistência, serviço de aplicação e API DFC/FCA.
- Resumo: criada migration com snapshots, audit rows e decisões manuais; serviço lê I200/I250/I050/I051, aplica metodologia e evidências, invalida dependentes e expõe execução, consulta e decisão manual nos endpoints governados.

## Arquivos Alterados

- `backend/alembic/versions/0054_dfc_calculations.py`
- `backend/app/repositories/dfc_calculations.py`
- `backend/app/repositories/__init__.py`
- `backend/app/application/dfc_service.py`
- `backend/app/application/evidence_service.py`
- `backend/app/application/__init__.py`
- `backend/app/schemas/dfc.py`
- `backend/app/api/dfc.py`
- `backend/app/main.py`
- `backend/tests/test_dfc_repository.py`
- `backend/tests/test_dfc_api.py`
- `backend/tests/test_app_bootstrap.py`

## Validações

- Comando: migration Alembic via container backend.
  - Resultado: PostgreSQL atualizado para `0054_dfc_calculations (head)`.
- Comando: `docker compose --profile test run --rm backend-tests`
  - Resultado: 213 testes backend aprovados.
- Jornada real: execução via API com `ECD 2024 DATAPACK.txt`.
  - Resultado: 4.251 linhas auditáveis; FCA `92988.06`, operacional `235884.83`, investimento `-28448.78`, financiamento `-114447.99`, status `bloqueado_por_evidencia`; movimentos e pendências permaneceram visíveis.

## Pendências Ou Bloqueios

- Nenhum.

## Homologação

- Status: aguardando_homologacao
- Data: 24/07/2026
- Decisão do usuário: homologação consolidada ao final do grupo autorizado.
- Observação: execução contínua segue para a TASK-065.
