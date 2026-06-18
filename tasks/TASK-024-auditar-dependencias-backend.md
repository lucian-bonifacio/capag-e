# TASK-024 - Auditar dependencias backend

## SPEC De Origem

- `specs/SPEC-001-modulo-0-fundacao-governada.md`

## Dependencias

- `TASK-003-criar-estrutura-backend-minima.md`
- `TASK-006-auditar-validacoes-minimas-do-projeto.md`

## Objetivo

Auditar a configuracao de dependencias backend necessarias para a fundacao do projeto em ambiente Docker-only, sem instalar pacotes, criar aplicacao FastAPI ou implementar codigo.

## Fontes Usadas

- `docs/product/PRD.md`
- `docs/architecture/architecture.md`
- `specs/SPEC-001-modulo-0-fundacao-governada.md`
- log esperado de `logs/LOG-006-auditar-validacoes-minimas-do-projeto.md`

## Escopo Exato

- Verificar se ha arquivo de dependencias backend.
- Verificar se a stack aprovada aparece ou esta ausente: FastAPI, Pydantic, SQLAlchemy, Alembic, pytest e openpyxl.
- Verificar se ha qualquer instrucao indevida de instalacao local/global ou uso de `.venv`.
- Registrar lacunas e conflitos em log operacional.
- Propor TASKs pequenas para configuracao de dependencias.

## Fora De Escopo

- Instalar dependencias.
- Criar `pyproject.toml`, `requirements.txt` ou lockfile.
- Criar aplicacao FastAPI.
- Criar codigo backend.
- Criar testes.
- Alterar ambiente local, Docker ou CI.

## Passos Executaveis

1. Ler log da TASK-006.
2. Auditar arquivos de dependencias backend existentes.
3. Criar log em `logs/LOG-024-auditar-dependencias-backend.md`.
4. Registrar lacunas sem corrigi-las.
5. Validar que nenhum arquivo de dependencias foi alterado.

## Arquivos Ou Areas Provaveis

- `logs/LOG-024-auditar-dependencias-backend.md`
- raiz do repositorio apenas para leitura
- `backend/` apenas para leitura

## Criterios De Aceite

- Existe log de auditoria.
- O log identifica dependencias backend existentes e ausentes.
- O log identifica qualquer exigencia de `.venv` ou instalacao no host como lacuna.
- Nenhum arquivo de dependencias, codigo, teste ou config e alterado.

## Validacao Esperada

- Executar `test -f logs/LOG-024-auditar-dependencias-backend.md`.
- Executar `git diff --stat` e confirmar que apenas o log foi criado.

## Riscos

- Risco: auditoria virar instalacao de stack.
  Mitigacao: registrar lacunas e criar TASK futura.

## Bloqueios Pendentes

Bloqueada ate a execucao das TASKs 003 e 006.
