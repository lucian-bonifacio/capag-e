# 05 - Razao por conta e contrapartidas

## Objetivo

Planejar a montagem do razao por conta contabil, base estrutural da analise comportamental.

## Ponto de decisao

Decidir como tratar lancamentos simples, compostos e ambiguos.

## Arquivos correlatos

- `src/capag/domain/models.py`
- `src/capag/io/ecd_parser.py`
- `src/capag/io/ecd_normalizer.py`
- futuro `src/capag/engine/behavioral_ledger.py`
- `tests/unit/`
- `tests/fixtures/ecd/`

## Detalhamento

- Para cada conta analitica, agrupar partidas `I250`.
- Vincular cada partida ao lancamento `I200`.
- Identificar contas do lado oposto como contrapartidas.
- Em lancamentos simples, usar contrapartida direta.
- Em lancamentos compostos:
  - registrar todas as contrapartidas relacionadas;
  - calcular participacao por valor quando possivel;
  - marcar ambiguidade;
  - reduzir score quando contrapartida for incerta.
- Calcular:
  - lista de debitos;
  - lista de creditos;
  - saldos;
  - historicos;
  - meses com movimento;
  - lancamentos simples;
  - lancamentos compostos;
  - concentracao por contraparte.

## Entregavel

Spec do razao comportamental por conta.

## Criterios de sucesso

- Dada uma conta, o sistema consegue mostrar seus movimentos e principais contrapartidas.
- Lancamentos compostos nao geram inferencia agressiva.

## Fora do escopo

- Calcular score.
- Reclassificar conta.

