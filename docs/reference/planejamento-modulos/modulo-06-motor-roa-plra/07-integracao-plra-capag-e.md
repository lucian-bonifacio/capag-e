# 07 - Integracao com PLRA e CAPAG-E

## Objetivo

Definir como o `ROA` sera combinado com `PLRA`.

## Regras

1. O motor ROA nao recalcula `PLRA`.
2. O motor recebe `PLRA` final do Modulo 01/03.
3. `CAPAG-E = ROA Final + PLRA`.
4. Se `ROA` estiver final e `PLRA` bloqueado, `CAPAG-E` fica bloqueada por `PLRA`.
5. Se `PLRA` estiver final e `ROA` bloqueado, `CAPAG-E` fica bloqueada por `ROA`.

## Compatibilidade com Modulo 03

O metodo usado deve ser:

- `roa_plra`

Ou, quando tambem houver FCA:

- `comparativo_fca_roa`

## Criterio de sucesso

O sistema deve suportar `ROA + PLRA` sem duplicar calculo patrimonial.

