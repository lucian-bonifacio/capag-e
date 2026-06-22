# LOG - TASK-021A - Descontinuar TODOLIST.md e alinhar ROADMAP

## Referência

- Task: `tasks/TASK-021A-descontinuar-todolist-e-alinhar-roadmap.md`
- SPEC: `specs/SPEC-001-modulo-0-fundacao-governada.md`
- Status: concluido

## Fontes Consultadas

- `docs/product/PRD.md`
- `docs/architecture/architecture.md`
- `specs/SPEC-001-modulo-0-fundacao-governada.md`
- `specs/README.md`
- `tasks/README.md`
- `tasks/TASK-022-refinar-todolist.md`
- `tasks/TASK-033-atualizar-status-todolist-pos-fundacao.md`
- `tasks/TASK-034-encerrar-spec-001-e-liberar-proxima-spec.md`
- `tasks/TASK-084-testes-governanca-e-documentos-operacionais-finais.md`
- `logs/LOG-007-auditar-documentos-operacionais-e-agentes.md`
- `logs/LOG-021-refinar-agents-md.md`
- `ROADMAP.md`
- `AGENTS.md`

## Execução

- Data: 2026-06-19
- Ação: Descontinuação governada do `TODOLIST.md` como documento operacional.
- Resumo: `SPEC-001` passou a apontar `ROADMAP.md` como painel operacional vivo. A `TASK-022` foi substituída por registro de descontinuidade do `TODOLIST.md`, a `TASK-033` passou a atualizar `ROADMAP.md` após a fundação, e referências pendentes em `TASK-034` e `TASK-084` foram alinhadas. `TODOLIST.md` não foi criado e logs históricos foram preservados.

## Arquivos Alterados

- `specs/SPEC-001-modulo-0-fundacao-governada.md`
- `specs/README.md`
- `tasks/TASK-021A-descontinuar-todolist-e-alinhar-roadmap.md`
- `tasks/TASK-022-registrar-descontinuidade-todolist.md`
- `tasks/TASK-023-criar-ou-refinar-readme-projeto.md`
- `tasks/TASK-033-atualizar-roadmap-pos-fundacao.md`
- `tasks/TASK-034-encerrar-spec-001-e-liberar-proxima-spec.md`
- `tasks/TASK-084-testes-governanca-e-documentos-operacionais-finais.md`
- `ROADMAP.md`
- `logs/LOG-021A-descontinuar-todolist-e-alinhar-roadmap.md`

## Validações

- Comando: `test ! -f TODOLIST.md`
  - Resultado: `TODOLIST.md` não existe na raiz.
- Comando: `rg -n "TODOLIST|todolist" AGENTS.md ROADMAP.md specs tasks logs`
  - Resultado: ocorrências remanescentes são históricas, da própria descontinuidade ou de TASKs concluídas antigas; referências pendentes que exigiam uso operacional foram alinhadas.
- Comando: `git diff -- specs/SPEC-001-modulo-0-fundacao-governada.md specs/README.md ROADMAP.md tasks/TASK-022-registrar-descontinuidade-todolist.md tasks/TASK-033-atualizar-roadmap-pos-fundacao.md tasks/TASK-034-encerrar-spec-001-e-liberar-proxima-spec.md`
  - Resultado: mudanças documentais restritas ao alinhamento `TODOLIST.md` -> `ROADMAP.md` e ao registro futuro de descontinuidade.
- Comando: `git diff --stat`
  - Resultado: alterações documentais; sem código, testes, CI, backend, frontend, assets ou migrations.

## Pendências Ou Bloqueios

- Nenhum.

## Homologação

- Status: aprovada
- Data: 2026-06-22
- Decisão do usuário: aprovado conforme resposta "Acho que pode homologar".
- Observação: TASK homologada; `TODOLIST.md` permanece descontinuado e `ROADMAP.md` permanece como painel operacional vivo.
