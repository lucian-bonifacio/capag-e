# TASK-025 - Configurar dependencias backend minimas

## SPEC De Origem

- `specs/SPEC-001-modulo-0-fundacao-governada.md`

## Dependencias

- `TASK-024-auditar-dependencias-backend.md`

## Objetivo

Criar configuracao minima de dependencias backend para uso dentro de container conforme arquitetura aprovada, sem implementar aplicacao, endpoints, models, migrations ou regras funcionais.

## Fontes Usadas

- `docs/architecture.md`
- `specs/SPEC-001-modulo-0-fundacao-governada.md`
- relatorio esperado de `tasks/reports/TASK-024-auditoria-dependencias-backend.md`

## Escopo Exato

- Criar ou ajustar arquivo de dependencias backend apenas se a auditoria indicar lacuna.
- Incluir dependencias minimas aprovadas para fundacao.
- Separar dependencias de runtime e teste quando o formato escolhido permitir.
- Documentar comando de instalacao somente via Docker/Docker Compose, se necessario.

## Fora De Escopo

- Implementar FastAPI.
- Criar endpoints, schemas, models, migrations ou repositories.
- Criar testes funcionais.
- Configurar CI ou Docker.
- Criar ou exigir `.venv`.
- Instalar dependencias no host.
- Alterar frontend.

## Passos Executaveis

1. Ler relatorio da TASK-024.
2. Criar ou ajustar configuracao minima de dependencias.
3. Validar formato do arquivo criado.
4. Confirmar que nenhum codigo funcional foi criado.

## Arquivos Ou Areas Provaveis

- `backend/pyproject.toml`, `backend/requirements.txt` ou arquivo equivalente definido pela auditoria
- `backend/README.md`, somente se necessario para comando de instalacao

## Criterios De Aceite

- A configuracao minima de dependencias backend existe.
- Dependencias refletem stack aprovada.
- O fluxo oficial de instalacao e execucao e via container.
- Nenhum `.venv` e criado ou exigido.
- Nenhuma dependencia e instalada no host.
- Nenhum codigo funcional e criado.

## Validacao Esperada

- Executar validacao de formato disponivel para o arquivo escolhido.
- Executar `git diff --stat` e confirmar escopo restrito a dependencias backend/documentacao minima.

## Riscos

- Risco: escolher formato de dependencias sem criterio.
  Mitigacao: seguir relatorio da TASK-024.

## Bloqueios Pendentes

Bloqueada ate a execucao da TASK-024.
