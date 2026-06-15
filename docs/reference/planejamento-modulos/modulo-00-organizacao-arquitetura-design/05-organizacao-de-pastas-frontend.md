# 05 - Organizacao de pastas do frontend

## Objetivo

Definir uma estrutura de pastas mais clara para o React.

## Ponto de decisao

Decidir a arvore-alvo de `web/src/`.

## Arquivos correlatos

- `web/src/App.jsx`
- `web/src/main.jsx`
- `web/src/components/`
- `web/src/lib/api.js`
- `web/src/styles/index.css`

## Detalhamento

- Classificar componentes atuais como paginas, features ou compartilhados.
- Propor arvore-alvo:
  - `web/src/app/`
  - `web/src/routes/`
  - `web/src/pages/`
  - `web/src/features/session/`
  - `web/src/features/ecd-mirror/`
  - `web/src/features/macro-simulator/`
  - `web/src/features/analytic-review/`
  - `web/src/shared/components/`
  - `web/src/shared/formatters/`
  - `web/src/lib/api/`
  - `web/src/styles/`
- Definir ordem segura de migracao.

## Entregavel

Arvore-alvo do frontend e plano de migracao sem alterar comportamento.

## Criterios de sucesso

- Cada nova tela tem lugar claro.
- A migracao para rotas fica mais simples.
- O frontend continua sem regra de negocio central.

