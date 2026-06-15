# 02 - Entrada de contas de resultado da ECD

## Objetivo

Definir as fontes usadas pelo motor ROA.

## Registros e fontes

- `I050`
- `I051`
- `I150`
- `I155`
- contas referenciais de resultado
- `J150`, quando parser suportar conferencia de DRE

## Regra incremental

A implementacao inicial pode calcular a partir de `I155 + referencial`, mas deve registrar ausencia de conferencia `J150` quando ainda nao houver suporte.

## Pontos de atencao

- Identificar contas de resultado corretamente.
- Separar contas patrimoniais usadas como pressoes complementares.
- Garantir sinal contabil correto.
- Nao depender de nome livre da conta.

## Criterio de sucesso

O `ROA` deve ser auditavel por conta e por codigo referencial.

