# LOG - TASK-021 - Refinar AGENTS.md

## Referência

- Task: `tasks/TASK-021-refinar-agents-md.md`
- SPEC: `specs/SPEC-001-modulo-0-fundacao-governada.md`
- Status: concluido

## Fontes Consultadas

- `docs/product/PRD.md`
- `docs/architecture/architecture.md`
- `docs/architecture/layer-boundaries.md`
- `specs/SPEC-001-modulo-0-fundacao-governada.md`
- `tasks/README.md`
- `logs/LOG-005-auditar-indice-e-rastreabilidade-de-specs.md`
- `logs/LOG-006-auditar-validacoes-minimas-do-projeto.md`
- `logs/LOG-007-auditar-documentos-operacionais-e-agentes.md`
- `AGENTS.md`

## Execução

- Data: 2026-06-19
- Ação: Refinamento instrucional do `AGENTS.md`.
- Resumo: Incluída regra conservadora para reaproveitar fontes já consultadas na mesma sessão quando o contexto estiver íntegro e o arquivo não tiver mudado. Reforçada a separação entre criação e execução de TASK e mantida regra curta sobre validações esperadas conforme maturidade do projeto.
- Data: 2026-06-19
- Ação: Ajuste solicitado em homologação.
- Resumo: Removida seção redundante de fontes obrigatórias para SPECs e TASKs. A seção de validações foi revisada e reduzida para evitar repetição de conteúdo já presente na TASK, na SPEC-001 e nas regras de ambiente oficial.

## Arquivos Alterados

- `AGENTS.md`
- `logs/LOG-021-refinar-agents-md.md`
- `ROADMAP.md`

## Validações

- Comando: `git diff -- AGENTS.md`
  - Resultado: mudanças restritas a instruções operacionais em `AGENTS.md`.
- Comando: `git diff --stat`
  - Resultado: antes do registro operacional, apenas `AGENTS.md` estava alterado.
- Comando: `rg -n 'Fonte|fontes|Valid|valid|docker compose|TASK deve|PRD ->|git diff|migrations|pytest|build|CI|valida' AGENTS.md tasks/README.md specs/SPEC-001-modulo-0-fundacao-governada.md tasks/TASK-021-refinar-agents-md.md`
  - Resultado: identificada repetição da seção de fontes e de detalhes de validação; ajuste aplicado em `AGENTS.md`.
- Conferência manual:
  - Resultado: a mudança não altera PRD, arquitetura, SPECs, TASKs, código, testes, CI, backend, frontend, assets ou migrations.

## Pendências Ou Bloqueios

- Nenhum.

## Homologação

- Status: aprovada
- Data: 2026-06-19
- Decisão do usuário: aprovada
- Observação: Usuário informou que gostou da forma final e não tinha mais nada a acrescentar.
