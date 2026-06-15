# 04 - Frontend com rotas explicitas

## Objetivo

Planejar a troca de navegacao por `activeView` para URLs explicitas no React.

## Ponto de decisao

Decidir se sera usado `react-router-dom` e qual sera a tabela oficial de rotas.

## Arquivos correlatos

- `web/package.json`
- `web/src/main.jsx`
- `web/src/App.jsx`
- `web/src/lib/api.js`
- `web/src/components/HubDashboard.jsx`
- `web/src/components/EcdMirrorView.jsx`
- `web/src/components/MacroScenarioSimulator.jsx`
- `web/src/components/AnalyticConditionalReview.jsx`
- `src/capag/api/routes.py`
- `src/capag/api/schemas.py`

## Detalhamento

- Documentar o estado atual: uma SPA com navegacao por estado interno.
- Definir rotas:
  - `/`
  - `/exercicios/:year`
  - `/exercicios/:year/espelho`
  - `/exercicios/:year/simulador`
  - `/exercicios/:year/revisao`
- Definir que refresh e link direto exigem API de recuperacao de sessao ativa.
- Avaliar endpoints necessarios:
  - `GET /api/session`
  - `GET /api/exercises/{year}`
- Definir comportamento de upload, nova analise e erro de sessao inexistente.

## Entregavel

Spec de arquitetura de rotas do frontend.

## Criterios de sucesso

- URLs passam a ter significado.
- O usuario consegue copiar link de uma tela.
- O comportamento de refresh fica definido antes da implementacao.

