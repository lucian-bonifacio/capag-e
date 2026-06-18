# TASK-031 - Criar matriz de execucao das TASKs de fundacao

## SPEC De Origem

- `specs/SPEC-001-modulo-0-fundacao-governada.md`

## Dependencias

- `TASK-030-auditar-rastreabilidade-tasks-specs.md`

## Objetivo

Criar matriz documental de ordem de execucao das TASKs derivadas da SPEC-001, com dependencias, bloqueios e criterios de liberacao.

## Fontes Usadas

- `tasks/README.md`
- `tasks/TASK-*.md`
- log esperado de `logs/LOG-030-auditar-rastreabilidade-tasks-specs.md`

## Escopo Exato

- Criar matriz em log/documento de planejamento.
- Ordenar TASKs por dependencias.
- Indicar quais TASKs sao auditorias, estruturais, configuracao ou gate.
- Nao executar nenhuma TASK.

## Fora De Escopo

- Alterar TASKs existentes.
- Marcar status como concluido.
- Executar TASKs.
- Alterar README ou indices.

## Passos Executaveis

1. Ler log da TASK-030.
2. Montar matriz de execucao.
3. Registrar achados em `logs/LOG-031-criar-matriz-execucao-tasks-fundacao.md`.
4. Validar que nenhuma TASK foi alterada.

## Arquivos Ou Areas Provaveis

- `logs/LOG-031-criar-matriz-execucao-tasks-fundacao.md`

## Criterios De Aceite

- Existe matriz de execucao.
- A matriz respeita dependencias.
- Nenhuma TASK e executada ou alterada.

## Validacao Esperada

- Executar `test -f logs/LOG-031-criar-matriz-execucao-tasks-fundacao.md`.
- Executar `git diff --stat` e confirmar escopo restrito ao log.

## Riscos

- Risco: matriz virar execucao.
  Mitigacao: manter documento somente orientativo.

## Bloqueios Pendentes

Bloqueada ate a execucao da TASK-030.

