# 07 - API, payload e frontend da camada declarada

## Objetivo

Planejar como a camada declarada sera exposta pela API e exibida no frontend sem duplicar regra de negocio.

## Ponto de decisao

Decidir quais campos do payload precisam ser adicionados ou renomeados para deixar a camada declarada clara.

## Arquivos correlatos

- `src/capag/api/routes.py`
- `src/capag/api/schemas.py`
- `src/capag/api/presentation.py`
- `web/src/lib/api.js`
- `web/src/components/HubDashboard.jsx`
- `web/src/components/EcdMirrorView.jsx`
- `web/src/components/MacroScenarioSimulator.jsx`
- `web/src/components/AnalyticConditionalReview.jsx`
- `web/src/components/AccountAuditRows.jsx`

## Detalhamento

- Definir se o payload deve explicitar:
  - `reference_code_declared`;
  - `reference_description_official`;
  - `methodology_rule_applied`;
  - `methodology_group_declared`;
  - `declared_analysis_result`.
- Revisar se `EcdMirrorView` esta calculando agregados visuais que deveriam vir do backend.
- Garantir que frontend exiba camada declarada sem recalcular resultado oficial.
- Definir labels de UI para diferenciar:
  - classificacao declarada;
  - tratamento metodologico;
  - ajuste manual;
  - futuro comportamento sugerido.

## Entregavel

Plano de contrato API/frontend da camada declarada.

## Criterios de sucesso

- O usuario consegue entender o que foi declarado na ECD.
- O frontend nao reimplementa metodologia.
- O payload fica preparado para coexistir futuramente com analise comportamental.

## Fora do escopo

- Implementar React Router.
- Implementar modulo comportamental.

