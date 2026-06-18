---
name: task-planner
description: Criar novas TASKs governadas do CAPAG após confirmação explícita do usuário. Use quando scope-resolution classificar uma solicitação como nova TASK, houver SPEC suficiente, for preciso numerar com sufixo alfabético e inserir a TASK no ROADMAP.md sem implementar.
---

# Task Planner

Use esta skill para criar nova TASK oficial no CAPAG após confirmação explícita do usuário.

Não use para executar TASK. Não use para criar SPEC. Não implemente a TASK criada.

## Pré-Condições

Antes de criar a TASK:

- confirmar que `scope-resolution` classificou a solicitação como `nova_task`;
- confirmar que o usuário autorizou criar a TASK;
- ler PRD, arquitetura, SPEC aplicável, `tasks/README.md` e TASK relacionada;
- verificar se existe SPEC suficiente.

Se não houver SPEC suficiente, bloqueie e oriente criação ou ajuste de SPEC.

## Numeração

Use sufixo alfabético para inserir TASKs entre TASKs existentes:

```text
TASK-002A-descricao-curta.md
TASK-002B-descricao-curta.md
```

Regras:

- não renumerar TASKs existentes;
- usar a próxima letra disponível;
- posicionar a nova TASK no `ROADMAP.md` na ordem lógica;
- criar log correspondente no roadmap como `logs/LOG-002A-descricao-curta.md`.

## Template

Siga o template obrigatório definido em `tasks/README.md`.

A TASK deve conter:

- SPEC de origem;
- objetivo;
- fontes usadas;
- escopo exato;
- fora de escopo;
- passos executáveis;
- arquivos ou áreas prováveis;
- critérios de aceite;
- validação esperada;
- riscos;
- bloqueios pendentes.

## Regras

- TASK nova não decide arquitetura, contrato de API, regra de domínio, fórmula, fonte normativa, arredondamento, padrão visual ou estratégia crítica de teste.
- Se a solicitação couber na TASK atual, não crie TASK nova.
- Se exigir nova SPEC, não crie TASK ainda.
- Após criar a TASK, use `roadmap-manager` para inserir no `ROADMAP.md`.
- Não implementar a TASK criada sem novo fluxo de execução pelo `AGENTS.md`.
