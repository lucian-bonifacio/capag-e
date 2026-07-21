# LOG - TASK-013B - Ajustar Docker Compose dev e politica de env

## Referência

- Task: `tasks/TASK-013B-ajustar-docker-compose-dev-env.md`
- SPEC: `specs/SPEC-001-modulo-0-fundacao-governada.md`
- Status: concluido

## Fontes Consultadas

- `docs/product/PRD.md`
- `docs/architecture/architecture.md`
- `specs/SPEC-001-modulo-0-fundacao-governada.md`
- `tasks/TASK-013-criar-configuracao-docker-compose-minima.md`
- `tasks/TASK-013A-nomear-containers-docker-compose.md`
- `tasks/TASK-013B-ajustar-docker-compose-dev-env.md`
- `tasks/README.md`
- `AGENTS.md`
- `README.md`

## Execução

- Data: 2026-07-21
- Ação: ajuste do ambiente Docker Compose de desenvolvimento.
- Resumo: `backend` passou a executar Uvicorn com `--reload` lendo `/workspace/backend`; dependências backend ficam em `/tmp/capag-backend-deps`. `frontend` passou a executar Vite sobre workspace de container com mounts diretos de `src`, `e2e` e arquivos de configuração, sem cópia para `/tmp` e sem `node_modules` no host. `AGENTS.md` e `README.md` foram atualizados para uso normal de `docker compose`, mantendo `.env` local fora do Git e proibindo leitura/cópia de seu conteúdo por agentes.
- Data: 2026-07-21
- Ação: correção durante validação.
- Resumo: a primeira tentativa do backend gerou `backend/capag_backend.egg-info` no host. O comando foi corrigido para instalar apenas dependências a partir do `pyproject.toml`, o artefato gerado foi removido e a validação posterior confirmou ausência de `egg-info` no host.

## Arquivos Alterados

- `docker-compose.yml`
- `AGENTS.md`
- `README.md`
- `logs/LOG-013B-ajustar-docker-compose-dev-env.md`
- `ROADMAP.md`

## Validações

- Comando: `docker compose config`
  - Resultado: configuração válida sem `COMPOSE_DISABLE_ENV_FILE=1`.
- Comando: `docker compose up -d postgres backend frontend`
  - Resultado: `capag_postgres`, `capag_backend` e `capag_frontend` em execução; PostgreSQL saudável.
- Comando: alteração temporária em `frontend/src/App.css` + `docker compose exec -T frontend grep -n "capag-dev-reload-frontend" /workspace/frontend/src/App.css`
  - Resultado: frontend em container viu a alteração diretamente pelo mount; marcador temporário revertido.
- Comando: alteração temporária em `backend/app/main.py` + `docker compose logs --tail=40 backend`
  - Resultado: `WatchFiles detected changes in 'app/main.py'. Reloading...`; marcador temporário revertido.
- Comando: `docker compose exec -T backend sh -c 'test ! -d /tmp/capag-backend && test -d /tmp/capag-backend-deps && printf backend_deps_tmp_no_copy'`
  - Resultado: backend sem cópia `/tmp/capag-backend` e com dependências em `/tmp/capag-backend-deps`.
- Comando: `docker compose exec -T frontend sh -c 'test ! -d /tmp/capag-frontend && printf no_tmp_frontend_copy'`
  - Resultado: frontend sem cópia `/tmp/capag-frontend`.
- Comando: `test ! -d frontend/node_modules && test ! -d backend/capag_backend.egg-info`
  - Resultado: nenhum `node_modules` frontend e nenhum `egg-info` backend no host.
- Comando: `docker compose --profile test run --rm backend-tests`
  - Resultado: 64 testes passaram.
- Comando: `docker compose --profile test run --rm frontend-tests`
  - Resultado: 7 testes passaram; build frontend concluído.
- Comando: `docker compose --profile test run --rm frontend-e2e`
  - Resultado: 5 testes E2E passaram.

## Pendências Ou Bloqueios

- Nenhum.

## Homologação

- Status: aprovada
- Data: 2026-07-21
- Decisão do usuário: aprovada.
- Observação: usuário homologou a TASK-013B após validação do ambiente Docker Compose de desenvolvimento.
