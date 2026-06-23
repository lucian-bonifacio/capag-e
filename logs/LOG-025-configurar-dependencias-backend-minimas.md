# LOG - TASK-025 - Configurar dependencias backend minimas

## Referência

- Task: `tasks/TASK-025-configurar-dependencias-backend-minimas.md`
- SPEC: `specs/SPEC-001-modulo-0-fundacao-governada.md`
- Status: concluido

## Fontes Consultadas

- `docs/architecture/architecture.md`
- `specs/SPEC-001-modulo-0-fundacao-governada.md`
- `tasks/README.md`
- `tasks/TASK-025-configurar-dependencias-backend-minimas.md`
- `logs/LOG-024-auditar-dependencias-backend.md`
- `backend/README.md`
- `docker-compose.yml`

## Execução

- Data: 2026-06-22
- Ação: Configuração mínima de dependências backend.
- Resumo: Criado `backend/pyproject.toml` como manifesto mínimo de dependências backend, com dependências de runtime e extra de teste. Atualizado `backend/README.md` para apontar o manifesto e reforçar que instalação e validação ocorrem somente em containers via Docker Compose. Nenhum código funcional, endpoint, schema, model, migration, repository, teste funcional, Docker, CI ou frontend foi criado ou alterado.

- Data: 2026-06-22
- Ação: Validação complementar via Docker após ambiente ser ativado.
- Resumo: O manifesto `backend/pyproject.toml` foi validado dentro do container `backend-tests`.

## Dependências Declaradas

- Runtime: `fastapi`, `pydantic`, `SQLAlchemy`, `alembic`, `psycopg[binary]`, `openpyxl`.
- Teste: `pytest`, em `project.optional-dependencies.test`.

## Arquivos Alterados

- `backend/pyproject.toml`
- `backend/README.md`
- `logs/LOG-025-configurar-dependencias-backend-minimas.md`
- `ROADMAP.md`

## Validações

- Comando: `sed -n '1,120p' backend/pyproject.toml`
  - Resultado: manifesto criado com `requires-python = ">=3.12,<3.13"`, dependências de runtime e extra de teste.
- Comando: `COMPOSE_DISABLE_ENV_FILE=1 docker compose --profile test run --rm backend-tests python - <<'PY' ...`
  - Resultado: não executado; o ambiente retornou `docker: command not found` neste WSL. A limitação foi registrada sem usar Python, pip ou ambiente virtual no host.
- Comando: `COMPOSE_DISABLE_ENV_FILE=1 docker compose --profile test run --rm backend-tests python - <<'PY' ...`
  - Resultado: executado após Docker ser ativado; `backend pyproject ok`.
- Comando: `find . -maxdepth 5 -type d \( -name '.venv' -o -name 'venv' -o -name 'node_modules' \) -not -path './.git/*' -print | sort`
  - Resultado: nenhum diretório encontrado.
- Comando: `find backend/app -maxdepth 4 -type f ! -name '__init__.py' -print | sort`
  - Resultado: nenhum código funcional encontrado.
- Comando: `git status --short backend/pyproject.toml backend/README.md ROADMAP.md logs/LOG-025-configurar-dependencias-backend-minimas.md`
  - Resultado: alterações esperadas no manifesto, README backend, log e `ROADMAP.md`.

## Pendências Ou Bloqueios

- Nenhum.

## Homologação

- Status: aprovada
- Data: 2026-06-22
- Decisão do usuário: aprovado conforme resposta "Aprovo".
- Observação: TASK homologada; manifesto mínimo de dependências backend permanece criado para uso via container.
