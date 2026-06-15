# 04 - API, frontend e exportacao do contrato

## Objetivo

Planejar como o contrato canonico da `CAPAG-E` sera exposto ao frontend e a exportacao.

## API

Payload minimo:

- `assessment_method`
- `plra_value`
- `plra_status`
- `fca_value`
- `fca_status`
- `roa_value`
- `roa_status`
- `capag_e_value`
- `capag_e_status`
- `methodology_label`
- `methodology_formula`
- `limitations`
- `warnings`

## Fronteira de responsabilidade

- O backend calcula/define status.
- A API serializa.
- O frontend exibe.
- A exportacao serializa.
- O laudo consome.

O frontend nao deve recalcular `CAPAG-E`.

## Frontend

A UI deve:

- mostrar `PLRA` em contexto de laudo;
- manter `PLR ajustado` apenas em contexto tecnico;
- indicar metodo usado;
- diferenciar `FCO`, `FCA parcial` e `FCA final`;
- exibir bloqueios e limitacoes;
- evitar linguagem ambigua como "CAPAG final" quando o status for parcial.

## Exportacao

Criar bloco ou aba futura:

- `contrato_capag_e`

Campos minimos:

- exercicio;
- metodo;
- formula;
- `PLRA`;
- status do `PLRA`;
- `FCA`;
- status do `FCA`;
- `ROA`;
- status do `ROA`;
- `CAPAG-E`;
- status final;
- limitacoes metodologicas.

## Rotas explicitas

Este modulo deve conversar com o Modulo 00 sobre rotas React.

Rotas provaveis:

- `/analise/contrato-capag-e`
- `/analise/resultado`
- `/laudo/metodo`

## Criterios de sucesso

- O contrato aparece de forma consistente em API, frontend e Excel.
- A UI nao mascara status parcial.
- A exportacao nao recalcula resultado.

