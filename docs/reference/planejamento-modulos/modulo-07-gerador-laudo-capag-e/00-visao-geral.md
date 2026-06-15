# 00 - Visao geral do Modulo 07

## Objetivo

Planejar o gerador de laudo de `CAPAG-E`.

## Fonte principal

- `docs/specs/spec-11-gerador-laudo-capag-e.md`

## Papel do modulo

Transformar resultados calculados, evidencias, ajustes, bloqueios e ressalvas em um laudo estruturado.

## Regra central

O laudo nao recalcula:

- `PLRA`;
- `FCA`;
- `ROA`;
- `CAPAG-E`.

Ele apenas consome objetos ja calculados.

## Dependencias

- Modulo 03: contrato `CAPAG-E`.
- Modulo 04: evidencias e justificativas.
- Modulo 05: `FCA`.
- Modulo 06: `ROA`.
- Modulo 08: versao metodologica e rastreabilidade.

## Fora do escopo

- Assinatura digital.
- Protocolo no REGULARIZE/SICAR.
- Geracao automatica de anexos externos.

