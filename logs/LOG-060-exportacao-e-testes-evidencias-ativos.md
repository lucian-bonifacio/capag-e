# LOG - TASK-060 - Exportacao e testes de evidencias e ativos

## Referência

- Task: `tasks/TASK-060-exportacao-e-testes-evidencias-ativos.md`
- SPEC: `specs/SPEC-005-modulo-4-evidencias-justificativas-ativos.md`
- Status: aguardando_homologacao

## Fontes Consultadas

- `docs/product/PRD.md`
- `docs/architecture/architecture.md`
- `specs/SPEC-005-modulo-4-evidencias-justificativas-ativos.md`

## Execução

- Data: 24/07/2026
- Ação: exportação Excel e consolidação dos testes de evidências e ativos.
- Resumo: criada exportação sem recálculo com as planilhas `evidencias_justificativas` e `avaliacao_ativos`, incluindo status, materialidade, justificativas e bloqueios; adicionada jornada E2E reproduzível com o DATAPACK para bloqueio e liberação de PLRA/CAPAG.
- Ajuste: o E2E revelou leitura inconsistente de contas com múltiplos registros mensais I155; a seleção do saldo foi alinhada ao último período tanto na avaliação do ativo quanto no cálculo do PLRA.

## Arquivos Alterados

- `backend/app/export/evidence_excel.py`
- `backend/app/export/__init__.py`
- `backend/app/api/evidence.py`
- `backend/app/application/evidence_service.py`
- `backend/app/application/plra_service.py`
- `backend/tests/test_evidence_excel_export.py`
- `backend/tests/test_evidence_api.py`
- `backend/tests/test_app_bootstrap.py`
- `frontend/src/api/evidence.ts`
- `frontend/src/routes/EvidencePage.tsx`
- `frontend/src/routes/EvidencePage.css`
- `frontend/src/test/evidence.test.tsx`
- `frontend/e2e/evidence.spec.ts`
- `frontend/playwright.config.ts`

## Validações

- Comando: `docker compose --profile test run --rm backend-tests`
  - Resultado: 186 testes backend aprovados.
- Comando: `docker compose --profile test run --rm frontend-tests`
  - Resultado: 21 testes frontend aprovados e build Vite concluído.
- Comando: `docker compose --profile test run --rm frontend-e2e`
  - Resultado: 10 testes Playwright aprovados em execução serial; jornada DATAPACK confirmou bloqueio, exportação, regularização e liberação de PLRA/CAPAG.

## Pendências Ou Bloqueios

- Nenhum.

## Homologação

- Status: aguardando_homologacao
- Data: 24/07/2026
- Decisão do usuário: homologação consolidada ao final do grupo autorizado.
- Observação: execução contínua segue para a TASK-061.
