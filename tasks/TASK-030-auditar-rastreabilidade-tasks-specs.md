# TASK-030 - Auditar rastreabilidade TASKs e SPECs

## SPEC De Origem

- `specs/SPEC-001-modulo-0-fundacao-governada.md`

## Dependencias

- `TASK-005-auditar-indice-e-rastreabilidade-de-specs.md`
- `TASK-012-criar-indice-oficial-de-specs.md`

## Objetivo

Auditar se as TASKs existentes referenciam SPEC de origem suficiente, dependencias, bloqueios, criterios de aceite e validacao esperada.

## Fontes Usadas

- `specs/SPEC-001-modulo-0-fundacao-governada.md`
- `tasks/README.md`
- `specs/README.md`, se criado
- arquivos existentes em `tasks/`

## Escopo Exato

- Listar todas as TASKs existentes.
- Verificar campos obrigatorios.
- Verificar se cada TASK referencia SPEC de origem.
- Verificar se dependencias e bloqueios estao explicitos.
- Registrar lacunas em log.

## Fora De Escopo

- Alterar TASKs.
- Atualizar indice.
- Executar TASKs.
- Criar TASKs funcionais novas durante a auditoria.

## Passos Executaveis

1. Listar arquivos `tasks/TASK-*.md`.
2. Conferir campos obrigatorios.
3. Criar log em `logs/LOG-030-auditar-rastreabilidade-tasks-specs.md`.
4. Registrar lacunas sem corrigir.

## Arquivos Ou Areas Provaveis

- `logs/LOG-030-auditar-rastreabilidade-tasks-specs.md`
- `tasks/` apenas para leitura, exceto o log

## Criterios De Aceite

- Existe log de auditoria.
- Todas as TASKs sao listadas.
- Lacunas sao registradas sem correcao.

## Validacao Esperada

- Executar `test -f logs/LOG-030-auditar-rastreabilidade-tasks-specs.md`.
- Executar `git diff --stat` e confirmar que apenas o log foi criado.

## Riscos

- Risco: auditoria virar reescrita de TASKs.
  Mitigacao: bloquear alteracoes.

## Bloqueios Pendentes

Bloqueada ate a execucao das TASKs 005 e 012.

