# TASK-053 - Criar UI de resultado CAPAG-E

## SPEC De Origem

- `specs/SPEC-004-modulo-3-contrato-capag-e-plra-fca-roa.md`

## Dependencias

- `TASK-052-criar-api-capag-assessment.md`

## Objetivo

Criar tela de resultado CAPAG-E para exibir método, fórmula, componentes, status, limitações e bloqueios sem recalcular no frontend.

## Fontes Usadas

- `docs/product/PRD.md`
- `docs/architecture.md`
- `specs/SPEC-004-modulo-3-contrato-capag-e-plra-fca-roa.md`
- `docs/frontend/DESIGN_TOKENS.md`
- `docs/frontend/UI_COMPONENT_RULES.md`
- `docs/frontend/SCREEN_PATTERNS.md`
- `frontend/src/styles/globals.css`

## Escopo Exato

- Criar rota/tela de resultado.
- Exibir `PLRA`, `FCA`, `ROA` e `CAPAG-E` com status.
- Destacar bloqueios e limitações.
- Evitar linguagem de final quando status for parcial/bloqueado.

## Fora De Escopo

- Recalcular valores.
- Criar motores `FCA` ou `ROA`.
- Criar laudo.
- Alterar tokens visuais.

## Passos Executaveis

1. Ler contrato da API.
2. Criar tela conforme padrões governados.
3. Criar estados de loading, vazio, erro, parcial e calculado.
4. Criar testes frontend mínimos.

## Arquivos Ou Areas Provaveis

- `frontend/src/routes/`
- `frontend/src/components/`
- `frontend/src/api/`

## Criterios De Aceite

- UI não recalcula CAPAG-E.
- Status parcial/bloqueado é visível.
- Valores usam `.tnum`.
- Tokens governados são preservados.

## Validacao Esperada

- Executar testes/build frontend via `docker compose`.

## Riscos

- Risco: UI mascarar resultado parcial como final.
  Mitigação: badges e textos derivados do status da API.

## Bloqueios Pendentes

Bloqueada até API CAPAG assessment existir.
