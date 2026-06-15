# 06 - API, frontend e fluxo do laudo

## API

Endpoints sugeridos:

- `GET /api/report/preview`
- `POST /api/report/generate`
- `GET /api/report/export`

## Payload minimo

- `assessment_method`
- `capag_p_value`
- `responsible_name`
- `include_preliminary_sections`

## Frontend

Fluxo de laudo com:

- selecao do metodo;
- campo para `CAPAG-P`;
- responsavel pela analise;
- preview de secoes;
- lista de bloqueios;
- lista de ressalvas;
- botao de exportacao.

## Rotas explicitas

- `/laudo`
- `/laudo/preview`
- `/laudo/metodo`
- `/laudo/exportar`

## Criterio de sucesso

O frontend deve mostrar o estado do laudo sem recalcular resultado.

