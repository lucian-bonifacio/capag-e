# 05 - Integracao com FCO atual

## Objetivo

Preservar compatibilidade com o `FCO` atual sem chamar `FCO` de `FCA` completo.

## Regras

1. O `FCO` atual vira componente operacional.
2. Enquanto so houver operacional, o status deve ser `FCA parcial`.
3. O valor operacional pode alimentar a transicao, mas nao deve ser apresentado como DFC completa.
4. Overrides manuais de `FCO` precisam ser reavaliados no contexto do `FCA`.

## Impactos

- Dominio deve diferenciar `fco_value` e `fca_value`.
- API deve expor status parcial.
- Frontend deve explicar a limitacao.
- Exportacao deve preservar origem.

## Criterio de sucesso

Compatibilidade mantida sem erro conceitual de nomenclatura.

