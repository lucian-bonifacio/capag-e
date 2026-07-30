# LOG - TASK-105 - Criar API do balanço declarado

## Referência

- Task: `tasks/TASK-105-criar-api-balanco-declarado.md`
- SPEC: `specs/SPEC-012-modulo-1c-balanco-patrimonial-declarado.md`
- Status: aguardando_homologacao

## Fontes Consultadas

- `docs/product/PRD.md`
- `docs/architecture/architecture.md`
- `specs/SPEC-002-modulo-1-camada-declarada.md`
- `specs/SPEC-012-modulo-1c-balanco-patrimonial-declarado.md`
- `tasks/TASK-039-criar-api-camada-declarada.md`
- `tasks/TASK-104-implementar-conciliacao-balanco-declarado.md`

## Execução

- Data: 2026-07-29
- Ação: implementação e validação.
- Resumo: a rota do balanço passou a entregar contrato específico com estado, período, totais, árvore J100 e conciliação; foi criada rota sob demanda para componentes I050/I052/I155. Comparações diretas incorretas entre COD_AGL e COD_CTA foram removidas.
- Data: 2026-07-29
- Ação: ajuste de homologação.
- Resumo: a API de importação passou a rejeitar ECDs inelegíveis ao fluxo CAPAG-E anual antes de persistir (`OBRIGATORIO_AUSENTE`, `NAO_OBRIGATORIO`, `ESTRUTURA_INVALIDA`) e a retornar erro objetivo com `balance_status` e limitações. `DIVERGENTE` permanece consultável pela API do balanço para diagnóstico.

## Arquivos Alterados

- `backend/app/api/declared.py`
- `backend/app/application/declared_service.py`
- `backend/app/schemas/declared.py`
- `backend/tests/test_app_bootstrap.py`
- `backend/tests/test_declared_api.py`
- `backend/tests/test_declared_end_to_end.py`
- `backend/tests/test_ecd_import_api.py`
- `backend/tests/test_declared_run_service.py`
- `backend/app/api/imports.py`
- `backend/app/application/ecd_balance_preflight.py`

## Validações

- Comando: testes focados de API e serviço via `docker compose run --rm backend-tests`.
  - Resultado: contratos, componentes, OpenAPI, erros e ausência de escrita aprovados.
- Comando: suíte backend completa via `docker compose run --rm backend-tests`.
  - Resultado: 260 testes aprovados.
- Comando: busca por `float`, warnings removidos e `git diff --check`.
  - Resultado: nenhuma ocorrência proibida ou inconsistência de whitespace.
- Comando: `docker compose --profile test run --rm backend-tests`.
  - Resultado: 279 testes aprovados.
- Comando: `git diff --check`.
  - Resultado: aprovado, sem inconsistência de whitespace.

## Pendências Ou Bloqueios

- Nenhum.

## Homologação

- Status: aguardando_homologacao
- Data: 2026-07-29
- Decisão do usuário: grupo TASK-101 a TASK-108 autorizado para execução contínua.
- Observação: homologação consolidada será solicitada ao final do grupo.
