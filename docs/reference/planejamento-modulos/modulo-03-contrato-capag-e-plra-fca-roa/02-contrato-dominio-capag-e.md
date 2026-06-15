# 02 - Contrato de dominio da CAPAG-E

## Objetivo

Definir o modelo conceitual que representara a avaliacao de `CAPAG-E` por exercicio.

## Arquivos correlatos futuros

- `src/capag/domain/models.py`
- `src/capag/domain/states.py`
- `src/capag/domain/alerts.py`
- `src/capag/engine/capag.py`
- `src/capag/api/schemas.py`
- `src/capag/api/routes.py`

## Entidade principal

Criar ou planejar estrutura equivalente a `CapagEAssessment`.

Campos minimos:

- `exercise_year`
- `method`
- `plra_value`
- `plra_status`
- `fca_value`
- `fca_status`
- `roa_value`
- `roa_status`
- `capag_e_value`
- `capag_e_status`
- `unavailable_reason`
- `calculation_basis`
- `warnings`
- `limitations`

## Mapeamento com sistema atual

| Campo atual | Campo canonico |
|---|---|
| `plr_bruto` | memoria patrimonial bruta |
| `plr_ajustado` | `PLRA` |
| `fco_final_utilizado` | `FCO` ou componente operacional de `FCA` |
| `capag_e` | `CAPAG-E`, quando houver metodo definido |

## Regras de nomenclatura

- `PLR bruto` permanece tecnico e interno.
- `PLR ajustado` pode aparecer em tela tecnica.
- `PLRA` deve ser usado em laudo, exportacao final e contratos externos.
- `FCO` deve ser tratado como fluxo operacional.
- `FCA` deve representar fluxo de caixa ajustado completo ou parcial, sempre com status.
- `ROA` deve representar resultado operacional ajustado.
- `CAPAG-E` deve sempre informar metodo.

## Politica numerica

- Todos os valores monetarios devem usar `Decimal`.
- Valores finais devem ser quantizados em `0.01`.
- Percentuais devem ser fracao `Decimal`.
- O contrato nao deve aceitar `float`.

## Ponto de decisao

Definir se `CapagEAssessment` ficara em:

- `src/capag/domain/models.py`, como modelo de dominio; ou
- arquivo especifico futuro, como `src/capag/domain/capag_assessment.py`.

Preferencia tecnica:

- manter no dominio;
- evitar que a API defina o contrato sozinha;
- deixar schemas da API apenas serializarem o modelo.

## Criterios de sucesso

- Existe um contrato unico para resultado de `CAPAG-E`.
- O contrato e consumivel por API, frontend, exportacao e laudo.
- Nenhum modulo futuro recalcula ou redefine nomes canonicos.

