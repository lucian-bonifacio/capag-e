# LOG - TASK-103 - Reprocessar importações ECD legadas

## Referência

- Task: `tasks/TASK-103-reprocessar-importacoes-ecd-legadas.md`
- SPEC: `specs/SPEC-012-modulo-1c-balanco-patrimonial-declarado.md`
- Status: aguardando_homologacao

## Fontes Consultadas

- `docs/product/PRD.md`
- `docs/architecture/architecture.md`
- `specs/SPEC-012-modulo-1c-balanco-patrimonial-declarado.md`
- `tasks/TASK-041M-gerenciar-importacoes-ecd-existentes.md`
- `tasks/TASK-102-persistir-ecd-balanco-declarado.md`

## Execução

- Data: 2026-07-29
- Ação: implementação e validação.
- Resumo: importações legadas incompletas passaram a aceitar reenvio apenas com SHA-256 idêntico, preservar identificadores, substituir dados normalizados em transação, invalidar resultados derivados e registrar versão, data, estado e resultado do reprocessamento. Importações completas mantêm conflito `409`.

## Arquivos Alterados

- `backend/alembic/versions/0057_reimport_status.py`
- `backend/app/api/imports.py`
- `backend/app/application/__init__.py`
- `backend/app/application/ecd_import_service.py`
- `backend/app/domain/__init__.py`
- `backend/app/domain/imports.py`
- `backend/app/repositories/ecd_imports.py`
- `backend/app/schemas/imports.py`
- `backend/tests/test_ecd_reprocessing.py`

## Validações

- Comando: testes focados via `docker compose run --rm backend-tests`.
  - Resultado: 9 testes aprovados.
- Comando: suíte backend completa via `docker compose run --rm backend-tests`.
  - Resultado: 248 testes aprovados.
- Comando: migração e revisão atual do Alembic via serviço `backend`.
  - Resultado: PostgreSQL em `0057_reimport_status (head)`.
- Comando: busca por `float` e `git diff --check`.
  - Resultado: nenhuma ocorrência de `float` no escopo alterado e nenhuma inconsistência de whitespace.

## Pendências Ou Bloqueios

- Nenhum.

## Homologação

- Status: aguardando_homologacao
- Data: 2026-07-29
- Decisão do usuário: grupo TASK-101 a TASK-108 autorizado para execução contínua.
- Observação: homologação consolidada será solicitada ao final do grupo.
