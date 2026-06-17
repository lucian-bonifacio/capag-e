# TASK-026 - Auditar dependencias frontend

## SPEC De Origem

- `specs/SPEC-001-modulo-0-fundacao-governada.md`

## Dependencias

- `TASK-004-auditar-estrutura-frontend-governada.md`
- `TASK-006-auditar-validacoes-minimas-do-projeto.md`

## Objetivo

Auditar a configuracao de dependencias frontend necessarias para React, Vite, TypeScript, Tailwind CSS e ferramentas previstas em ambiente Docker-only, sem instalar pacotes ou alterar o frontend.

## Fontes Usadas

- `docs/architecture.md`
- `docs/frontend/DESIGN_TOKENS.md`
- `docs/frontend/UI_COMPONENT_RULES.md`
- `docs/frontend/SCREEN_PATTERNS.md`
- `specs/SPEC-001-modulo-0-fundacao-governada.md`

## Escopo Exato

- Verificar `package.json` e arquivos correlatos, se existirem.
- Verificar presenca ou ausencia de React, Vite, TypeScript, Tailwind, Vitest e demais ferramentas aprovadas.
- Verificar se ha qualquer instrucao indevida de `node_modules` no host ou instalacao local/global.
- Registrar lacunas em relatorio.

## Fora De Escopo

- Instalar dependencias.
- Criar ou alterar `package.json`.
- Criar componentes, rotas, telas, testes ou configs.

## Passos Executaveis

1. Auditar arquivos de dependencias frontend.
2. Criar relatorio em `tasks/reports/TASK-026-auditoria-dependencias-frontend.md`.
3. Registrar lacunas sem corrigi-las.

## Arquivos Ou Areas Provaveis

- `tasks/reports/TASK-026-auditoria-dependencias-frontend.md`
- `frontend/` apenas para leitura

## Criterios De Aceite

- Existe relatorio de auditoria.
- O relatorio identifica qualquer exigencia de `node_modules` no host ou instalacao global como lacuna.
- Nenhum arquivo de frontend e alterado.

## Validacao Esperada

- Executar `test -f tasks/reports/TASK-026-auditoria-dependencias-frontend.md`.
- Executar `git diff --stat` e confirmar que apenas o relatorio foi criado.

## Riscos

- Risco: auditoria virar instalacao de stack.
  Mitigacao: bloquear alteracoes no frontend.

## Bloqueios Pendentes

Bloqueada ate a execucao das TASKs 004 e 006.
