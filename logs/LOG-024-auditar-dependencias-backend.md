# LOG - TASK-024 - Auditar dependencias backend

## Referência

- Task: `tasks/TASK-024-auditar-dependencias-backend.md`
- SPEC: `specs/SPEC-001-modulo-0-fundacao-governada.md`
- Status: concluido

## Fontes Consultadas

- `docs/product/PRD.md`
- `docs/architecture/architecture.md`
- `specs/SPEC-001-modulo-0-fundacao-governada.md`
- `tasks/README.md`
- `tasks/TASK-024-auditar-dependencias-backend.md`
- `logs/LOG-006-auditar-validacoes-minimas-do-projeto.md`
- `backend/README.md`
- `backend/pytest.ini`
- `backend/alembic.ini`
- `backend/alembic/env.py`
- `docker-compose.yml`

## Execução

- Data: 2026-06-22
- Ação: Auditoria de dependencias backend.
- Resumo: Nao foi encontrado manifesto de dependencias backend (`pyproject.toml`, `requirements.txt`, lockfile ou equivalente). A fundacao possui configuracao minima de `pytest` e estrutura Alembic, mas as dependencias seguem instaladas apenas em containers efemeros nas validacoes existentes. Nenhum pacote foi instalado e nenhum arquivo de dependencia, codigo, teste, Docker ou CI foi alterado.

## Dependencias Auditadas

| Dependencia | Status | Evidencia |
| --- | --- | --- |
| FastAPI | ausente em manifesto | Nao ha `pyproject.toml`, `requirements.txt` ou arquivo equivalente; apenas referencias normativas em arquitetura/TASKs. |
| Pydantic | ausente em manifesto | Nao ha manifesto backend de dependencias. |
| SQLAlchemy | ausente em manifesto | `backend/alembic.ini` referencia URL SQLAlchemy, mas nao ha dependencia declarada em manifesto. |
| Alembic | configuracao minima presente; dependencia nao declarada | `backend/alembic.ini` e `backend/alembic/` existem; validacoes anteriores instalaram Alembic apenas dentro do container. |
| pytest | configuracao minima presente; dependencia nao declarada | `backend/pytest.ini` e testes sentinela existem; `docker-compose.yml` instala `pytest` apenas dentro do container efemero `backend-tests`. |
| openpyxl | ausente em manifesto | Apenas referencia normativa na arquitetura para exportacao Excel futura. |

## Lacunas E Conflitos

- Lacuna: falta manifesto backend oficial de dependencias.
- Lacuna: stack backend aprovada ainda nao esta declarada de forma instalavel/reprodutivel em arquivo de dependencias.
- Lacuna: `psycopg` aparece implicitamente na URL do Alembic, mas nao ha dependencia declarada.
- Conflito: nao foi encontrada exigencia vigente de `.venv`, instalacao global ou instalacao no host.
- Conformidade: comandos existentes usam `docker compose` e instalam dependencias temporarias apenas dentro de containers.

## Encaminhamentos Para Execucoes Futuras

- Executar `TASK-025 - Configurar dependencias backend minimas` para criar o manifesto backend aprovado, sem usar `.venv` no host.
- Manter `TASK-028 - Criar app FastAPI minimo` separada da configuracao de dependencias.

## Arquivos Alterados

- `logs/LOG-024-auditar-dependencias-backend.md`
- `ROADMAP.md`

## Validações

- Comando: `find . -maxdepth 4 -type f \( -name 'pyproject.toml' -o -name 'requirements*.txt' -o -name 'setup.py' -o -name 'setup.cfg' -o -name 'Pipfile' -o -name 'poetry.lock' -o -name 'uv.lock' -o -name 'pdm.lock' -o -name 'tox.ini' -o -name 'pytest.ini' \) -not -path './.git/*' -not -path './docs/reference/*' | sort`
  - Resultado: encontrado apenas `backend/pytest.ini` entre arquivos backend relevantes; nenhum manifesto de dependencias encontrado.
- Comando: `find . -maxdepth 5 -type d \( -name '.venv' -o -name 'venv' -o -name 'node_modules' \) -not -path './.git/*' -print | sort`
  - Resultado: nenhum diretorio encontrado.
- Comando: `rg -n "fastapi|pydantic|sqlalchemy|alembic|pytest|openpyxl|\\.venv|venv|pip install|python -m pip|requirements|pyproject|poetry|uv|pdm" AGENTS.md README.md backend docs tasks logs -g '!docs/reference/**' -g '!*.env'`
  - Resultado: stack aparece em documentos governados e configuracoes minimas; nao ha manifesto backend de dependencias nem instrucao para instalar no host.
- Comando: `test -f logs/LOG-024-auditar-dependencias-backend.md`
  - Resultado: log da auditoria criado.
- Comando: `git status --short backend README.md ROADMAP.md logs/LOG-024-auditar-dependencias-backend.md`
  - Resultado: nenhum arquivo em `backend/` foi alterado; alteracoes da TASK restritas ao log e ao `ROADMAP.md`.

## Pendências Ou Bloqueios

- Nenhum.

## Homologação

- Status: aprovada
- Data: 2026-06-22
- Decisão do usuário: aprovado conforme resposta "Aprovo".
- Observação: TASK homologada; auditoria confirmou ausência de manifesto backend de dependências e encaminhou configuração para TASK futura.
