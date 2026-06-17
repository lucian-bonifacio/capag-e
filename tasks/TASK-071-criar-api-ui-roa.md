# TASK-071 - Criar API e UI ROA

## SPEC De Origem

- `specs/SPEC-007-modulo-6-motor-roa-plra.md`

## Dependencias

- `TASK-070-integrar-roa-plra-capag-e.md`

## Objetivo

Criar API e tela ROA para consultar cálculo, componentes, audit rows, pendências e integração com `CAPAG-E = ROA + PLRA`, sem recalcular no frontend.

## Fontes Usadas

- `docs/product/PRD.md`
- `docs/architecture.md`
- `specs/SPEC-007-modulo-6-motor-roa-plra.md`
- `docs/frontend/DESIGN_TOKENS.md`
- `docs/frontend/UI_COMPONENT_RULES.md`
- `docs/frontend/SCREEN_PATTERNS.md`
- `frontend/src/styles/globals.css`

## Escopo Exato

- Criar schemas e endpoints ROA.
- Criar rota/tela ROA.
- Exibir componentes, pendências, evidências e status.
- Usar valores da API sem recalcular.

## Fora De Escopo

- Recalcular PLRA no frontend.
- Criar laudo.
- Criar DFC.
- Alterar tokens.

## Passos Executaveis

1. Criar API ROA.
2. Criar UI ROA.
3. Criar testes backend/frontend.

## Arquivos Ou Areas Provaveis

- `backend/app/api/`
- `frontend/src/routes/`
- `frontend/src/components/`
- `backend/tests/`

## Criterios De Aceite

- API expõe `RoaCalculation` e audit rows.
- UI não recalcula ROA.
- Pendências e status ficam visíveis.

## Validacao Esperada

- Executar testes backend e build/testes frontend via `docker compose`.

## Riscos

- Risco: UI tratar ROA parcial como final.
  Mitigação: status renderizado da API.

## Bloqueios Pendentes

Bloqueada até integração ROA + PLRA existir.
