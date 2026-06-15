# 12 - Cenario CAPAG reclassificada

## Objetivo

Planejar como gerar um cenario alternativo de PLR e CAPAG-e com base na reclassificacao comportamental.

## Ponto de decisao

Decidir se o MVP gerara somente divergencias/impactos potenciais ou um cenario completo recalculado.

## Alternativas

1. Relatorio de divergencias e impactos potenciais.
2. Cenario completo de PLR e CAPAG-e reclassificados.

## Detalhamento

- Definir como uma reclassificacao comportamental altera a entrada do motor PLR.
- Definir como decisoes manuais humanas interagem com sugestoes comportamentais.
- Definir como distinguir:
  - resultado declarado;
  - resultado reclassificado automatico;
  - resultado revisado pelo humano;
  - simulacoes.
- Definir se FCO tambem tera leitura comportamental ou se usa o FCO final vigente.

## Arquivos correlatos

- `src/capag/engine/plr.py`
- `src/capag/engine/capag.py`
- `src/capag/engine/fco.py`
- futuro `src/capag/engine/behavioral_scenario.py`

## Entregavel

Spec do cenario reclassificado.

## Criterios de sucesso

- O resultado reclassificado nao se confunde com o declarado.
- O impacto por conta e consolidado fica rastreavel.

## Fora do escopo

- Recalcular exportacao dentro do Excel.

