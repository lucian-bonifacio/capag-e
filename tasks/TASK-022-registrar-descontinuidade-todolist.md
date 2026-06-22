# TASK-022 - Registrar descontinuidade do TODOLIST.md

## SPEC De Origem

- `specs/SPEC-001-modulo-0-fundacao-governada.md`

## Dependencias

- `TASK-007-auditar-documentos-operacionais-e-agentes.md`
- `TASK-012-criar-indice-oficial-de-specs.md`
- `TASK-021A-descontinuar-todolist-e-alinhar-roadmap.md`

Esta TASK registra a descontinuidade governada do `TODOLIST.md`. Ela nao deve criar, restaurar ou refinar `TODOLIST.md`.

## Objetivo

Registrar em log proprio que `TODOLIST.md` foi descontinuado como documento operacional e que `ROADMAP.md` passou a ser o painel vivo de proxima tarefa, status, TASKs e logs.

## Fontes Usadas

- `docs/product/PRD.md`
- `docs/architecture/architecture.md`
- `specs/SPEC-001-modulo-0-fundacao-governada.md`
- `tasks/README.md`
- `tasks/TASK-021A-descontinuar-todolist-e-alinhar-roadmap.md`
- `logs/LOG-007-auditar-documentos-operacionais-e-agentes.md`
- `logs/LOG-021A-descontinuar-todolist-e-alinhar-roadmap.md`
- `specs/README.md`
- `ROADMAP.md`

## Escopo Exato

- Confirmar que `TODOLIST.md` nao existe na raiz.
- Confirmar que `SPEC-001` e `ROADMAP.md` nao exigem mais `TODOLIST.md` como documento operacional vigente.
- Criar `logs/LOG-022-registrar-descontinuidade-todolist.md` registrando a descontinuidade da TASK original de refinamento.
- Registrar que `ROADMAP.md` e o fluxo de TASKs/logs substituem o antigo papel operacional esperado para `TODOLIST.md`.
- Marcar esta TASK como concluida apos homologacao, sem criar `TODOLIST.md`.

## Fora De Escopo

- Alterar `AGENTS.md`.
- Alterar `tasks/README.md`.
- Alterar SPECs.
- Alterar PRD ou arquitetura.
- Alterar configuracao real do Codex.
- Criar ou executar novas TASKs.
- Criar `TODOLIST.md`.
- Implementar codigo.
- Criar testes, CI, backend, frontend, assets ou migrations.
- Resolver pendencias tecnicas.

## Passos Executaveis

1. Ler `logs/LOG-021A-descontinuar-todolist-e-alinhar-roadmap.md`.
2. Confirmar que `TODOLIST.md` nao existe.
3. Confirmar que `ROADMAP.md` aponta para esta TASK quando ela for executada.
4. Criar `logs/LOG-022-registrar-descontinuidade-todolist.md`.
5. Registrar no log que a antiga tarefa de refinamento foi substituida por registro de descontinuidade.
6. Atualizar `ROADMAP.md` para `aguardando_homologacao` ao final da execucao.

## Arquivos Ou Areas Provaveis

- `logs/LOG-022-registrar-descontinuidade-todolist.md`
- `ROADMAP.md`

## Criterios De Aceite

- A TASK-021A foi executada antes desta TASK.
- `TODOLIST.md` nao e criado.
- O log da TASK registra que a tarefa original de refinamento foi descontinuada.
- O log registra `ROADMAP.md` como painel operacional vivo.
- Nenhuma regra tecnica, contrato funcional, configuracao secreta ou decisao arquitetural e criada.

## Validacao Esperada

- Executar `test ! -f TODOLIST.md`.
- Executar `test -f logs/LOG-022-registrar-descontinuidade-todolist.md`.
- Executar `git diff --stat` e confirmar escopo restrito ao log e ao `ROADMAP.md`.

## Riscos

- Risco: reintroduzir `TODOLIST.md` como fonte operacional paralela.
  Mitigacao: registrar apenas a descontinuidade e manter `ROADMAP.md` como painel vivo.

- Risco: perder rastreabilidade da decisao.
  Mitigacao: criar log especifico da TASK-022 explicando a substituicao.

- Risco: confundir criacao de TASK com execucao de TASK.
  Mitigacao: manter esta TASK restrita ao registro de descontinuidade.

## Bloqueios Pendentes

Bloqueada ate a execucao da TASK-021A.

Permanece bloqueado qualquer trabalho que tente criar `TODOLIST.md`, alterar documentos governados, configs reais, SPECs, TASKs, codigo, testes, CI, backend, frontend, assets ou migrations durante esta TASK.
