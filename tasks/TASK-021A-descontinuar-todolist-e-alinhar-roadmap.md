# TASK-021A - Descontinuar TODOLIST.md e alinhar ROADMAP

## SPEC De Origem

- `specs/SPEC-001-modulo-0-fundacao-governada.md`

## Dependencias

- `TASK-007-auditar-documentos-operacionais-e-agentes.md`
- `TASK-012-criar-indice-oficial-de-specs.md`
- `TASK-021-refinar-agents-md.md`

Esta TASK deve ser executada antes da `TASK-022-registrar-descontinuidade-todolist.md`, porque a ausência do `TODOLIST.md` deixou de ser tratada como lacuna a preencher e passou a ser uma decisão operacional a consolidar: o projeto trabalha com `ROADMAP.md` como painel vivo de execução.

## Objetivo

Descontinuar o uso planejado de `TODOLIST.md` como documento operacional do CAPAG, consolidar `ROADMAP.md` como fonte operacional viva para próxima tarefa e status, e alinhar as referências governadas que ainda apontam para `TODOLIST.md`.

## Fontes Usadas

- `docs/product/PRD.md`
- `docs/architecture/architecture.md`
- `specs/SPEC-001-modulo-0-fundacao-governada.md`
- `specs/README.md`
- `tasks/README.md`
- `tasks/TASK-022-registrar-descontinuidade-todolist.md`
- `tasks/TASK-033-atualizar-roadmap-pos-fundacao.md`
- `tasks/TASK-034-encerrar-spec-001-e-liberar-proxima-spec.md`
- `logs/LOG-007-auditar-documentos-operacionais-e-agentes.md`
- `logs/LOG-021-refinar-agents-md.md`
- `ROADMAP.md`
- `AGENTS.md`

## Escopo Exato

- Atualizar `specs/SPEC-001-modulo-0-fundacao-governada.md` para remover `TODOLIST.md` da estrutura-alvo mínima e registrar `ROADMAP.md` como documento operacional vivo.
- Atualizar critérios e validações documentais da `SPEC-001` que ainda mencionem `todolist`.
- Atualizar ou substituir TASKs pendentes que dependam de `TODOLIST.md`, especialmente:
  - `tasks/TASK-022-registrar-descontinuidade-todolist.md`;
  - `tasks/TASK-033-atualizar-roadmap-pos-fundacao.md`;
  - referências em `tasks/TASK-034-encerrar-spec-001-e-liberar-proxima-spec.md`, se aplicável.
- Atualizar `ROADMAP.md` para remover o bloqueio operacional causado pela `TASK-022` original e manter a próxima tarefa executável coerente com o novo fluxo.
- Atualizar `specs/README.md` somente se a lista de TASKs relacionadas à `SPEC-001` ou a descrição do módulo ficar desatualizada após o ajuste.
- Registrar no log da execução que `TODOLIST.md` foi descontinuado como fonte operacional, sem criar o arquivo.

## Fora De Escopo

- Criar `TODOLIST.md`.
- Implementar código.
- Criar testes, CI, backend, frontend, assets ou migrations.
- Alterar regra prudencial, fórmula, fonte normativa, arredondamento ou contrato de API.
- Alterar documentos de módulos funcionais fora da fundação.
- Executar a próxima TASK funcional após o ajuste.
- Remover logs históricos que mencionem `TODOLIST.md`.

## Passos Executaveis

1. Confirmar que `TODOLIST.md` não existe na raiz.
2. Buscar referências a `TODOLIST.md` e `todolist` em `AGENTS.md`, `ROADMAP.md`, `specs/`, `tasks/` e `logs/`.
3. Separar referências históricas em logs, que devem permanecer, de referências governadas vigentes, que devem ser alinhadas.
4. Atualizar `SPEC-001` para refletir `ROADMAP.md` como documento operacional vivo e remover a expectativa de `TODOLIST.md`.
5. Atualizar TASKs pendentes relacionadas a `TODOLIST.md` para que não exijam criação, leitura ou atualização desse arquivo.
6. Atualizar `ROADMAP.md` para manter a próxima tarefa executável correta após a descontinuação.
7. Criar ou atualizar o log correspondente em `logs/LOG-021A-descontinuar-todolist-e-alinhar-roadmap.md`.
8. Validar que nenhuma referência governada vigente continue exigindo `TODOLIST.md`.

## Arquivos Ou Areas Provaveis

- `specs/SPEC-001-modulo-0-fundacao-governada.md`
- `specs/README.md`
- `tasks/TASK-022-registrar-descontinuidade-todolist.md`
- `tasks/TASK-033-atualizar-roadmap-pos-fundacao.md`
- `tasks/TASK-034-encerrar-spec-001-e-liberar-proxima-spec.md`
- `ROADMAP.md`
- `logs/LOG-021A-descontinuar-todolist-e-alinhar-roadmap.md`

## Criterios De Aceite

- `TODOLIST.md` não é criado.
- `SPEC-001` deixa de exigir `TODOLIST.md` como estrutura-alvo ou critério de validação.
- `ROADMAP.md` permanece documentado como documento operacional vivo.
- TASKs pendentes não exigem leitura, criação ou atualização de `TODOLIST.md`.
- Referências históricas em logs permanecem preservadas.
- A próxima tarefa indicada no `ROADMAP.md` fica coerente com o fluxo governado.
- Nenhuma regra técnica, prudencial, contrato de API, fórmula ou padrão visual é alterado.

## Validacao Esperada

- Executar `test ! -f TODOLIST.md`.
- Executar `rg -n "TODOLIST|todolist" AGENTS.md ROADMAP.md specs tasks logs`.
- Revisar manualmente quais ocorrências remanescentes são históricas e quais são governadas vigentes.
- Executar `git diff -- specs/SPEC-001-modulo-0-fundacao-governada.md ROADMAP.md tasks/TASK-022-registrar-descontinuidade-todolist.md tasks/TASK-033-atualizar-roadmap-pos-fundacao.md tasks/TASK-034-encerrar-spec-001-e-liberar-proxima-spec.md`.
- Executar `git diff --stat`.

## Riscos

- Risco: remover rastreabilidade histórica ao apagar menções antigas de `TODOLIST.md`.
  Mitigação: preservar logs históricos e ajustar apenas documentos governados vigentes.

- Risco: deixar TASK pendente bloqueada por arquivo descontinuado.
  Mitigação: buscar referências em `ROADMAP.md`, `specs/` e `tasks/` antes de concluir.

- Risco: transformar `ROADMAP.md` em substituto de SPEC ou TASK.
  Mitigação: manter `ROADMAP.md` apenas como painel operacional vivo; regras e contratos continuam em PRD, arquitetura, SPECs e TASKs.

## Bloqueios Pendentes

Bloqueada qualquer execução que tente implementar código, criar `TODOLIST.md`, alterar regra técnica ou apagar logs históricos durante esta TASK.
