# 04 - Motor ROA e calculo

## Objetivo

Definir o calculo do `ROA`.

## Entidade principal

Planejar estrutura equivalente a `RoaCalculation`.

Campos minimos:

- `gross_revenue`
- `deductions`
- `revenue_taxes`
- `net_operating_revenue`
- `operating_costs`
- `operating_expenses`
- `financial_result`
- `non_operating_result`
- `cash_pressure_adjustments`
- `roa_preliminary`
- `roa_final`
- `status`
- `component_summaries`
- `audit_rows`
- `pending_groups`
- `alerts`

## Formula

```text
ROL = Receita Bruta - Deducoes - Tributos sobre Receita

ROA = ROL
    - Custos Operacionais
    - Despesas Operacionais
    +/- Resultado Financeiro
    +/- Resultado Nao Operacional

ROA Final = ROA - Pressoes Complementares de Caixa
```

## Regras de sinal

1. Receitas aumentam resultado.
2. Deducoes reduzem resultado.
3. Tributos sobre receita reduzem resultado.
4. Custos reduzem resultado.
5. Despesas reduzem resultado.
6. Resultado financeiro depende da natureza e sinal.
7. Resultado nao operacional depende da natureza e sinal.
8. Pressoes complementares reduzem `ROA Final`.

## Criterio de sucesso

O `ROA` deve ser calculado com `Decimal` e auditavel ate a conta.
