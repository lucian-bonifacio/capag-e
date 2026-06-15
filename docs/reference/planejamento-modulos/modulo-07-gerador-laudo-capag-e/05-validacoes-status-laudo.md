# 05 - Validacoes e status do laudo

## Objetivo

Definir quando o laudo pode ser emitido.

## Status permitidos

- `rascunho`
- `preliminar`
- `com_ressalvas`
- `final`
- `bloqueado`

## Validacoes para laudo final

1. Metodo de calculo definido.
2. `PLRA` final disponivel.
3. `FCA` ou `ROA` final disponivel conforme metodo.
4. Evidencias criticas nao pendentes.
5. Nenhuma conta metodologica bloqueante.

## Regras

- Falha de validacao deve virar status, bloqueio ou ressalva.
- O laudo nao deve tentar resolver ausencias recalculando motores.
- Um laudo preliminar pode existir, desde que a limitacao esteja clara.

## Criterio de sucesso

O usuario deve conseguir ver exatamente por que o laudo esta final, preliminar, com ressalvas ou bloqueado.

