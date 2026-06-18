# TASK-065 - Criar UI DFC/FCA

## SPEC De Origem

- `specs/SPEC-006-modulo-5-dfc-direta-fca.md`

## Dependencias

- `TASK-064-criar-api-dfc-fca.md`

## Objetivo

Criar tela de DFC/FCA para exibir fluxos, componentes, pendências, evidências e status sem recalcular no frontend.

## Fontes Usadas

- `docs/product/PRD.md`
- `docs/architecture/architecture.md`
- `specs/SPEC-006-modulo-5-dfc-direta-fca.md`
- `docs/frontend/DESIGN_TOKENS.md`
- `docs/frontend/UI_COMPONENT_RULES.md`
- `docs/frontend/SCREEN_PATTERNS.md`
- `frontend/src/styles/globals.css`

## Escopo Exato

- Exibir resumo de fluxos operacional, investimento e financiamento.
- Exibir `FCA` e status.
- Exibir audit rows e pendências.
- Cobrir estados essenciais.

## Fora De Escopo

- Recalcular DFC/FCA.
- Criar revisão metodológica livre.
- Criar laudo.
- Alterar tokens.

## Passos Executaveis

1. Ler contrato da API.
2. Criar tela conforme padrões governados.
3. Criar testes frontend mínimos.

## Arquivos Ou Areas Provaveis

- `frontend/src/routes/`
- `frontend/src/components/`
- `frontend/src/api/`

## Criterios De Aceite

- UI não recalcula `FCA`.
- Pendências ficam visíveis.
- `FCA parcial` não aparece como final.

## Validacao Esperada

- Executar testes/build frontend via `docker compose`.

## Riscos

- Risco: UI esconder fluxo não classificado.
  Mitigação: tabela de pendências e status obrigatório.

## Bloqueios Pendentes

Bloqueada até API DFC/FCA existir.
