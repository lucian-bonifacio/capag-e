# 03 - Status, bloqueios e metodos de calculo

## Objetivo

Definir como o sistema decide se uma `CAPAG-E` esta final, parcial, bloqueada ou indisponivel.

## Metodos permitidos

- `fca_plra`
- `roa_plra`
- `comparativo_fca_roa`
- `nao_definido`

## Status de componente

Valores permitidos:

- `nao_calculado`
- `calculado`
- `parcial`
- `bloqueado_por_pendencia`
- `bloqueado_por_evidencia`
- `erro_metodologico`

## Regras de formula

1. `CAPAG-E` so pode ser calculada quando `PLRA` final estiver disponivel.
2. `CAPAG-E = PLRA + FCA` so pode ser final com `FCA` final.
3. `CAPAG-E = PLRA + ROA` so pode ser final com `ROA` final.
4. Se houver apenas `FCO`, o resultado deve ser `FCA parcial`.
5. Se houver pendencia metodologica em ativos/passivos, `PLRA` final fica bloqueado.
6. Se houver evidencia critica pendente, o componente afetado pode ficar bloqueado.
7. Valores intermediarios devem ser preservados mesmo quando o resultado final estiver bloqueado.

## Bloqueios minimos

- Sem `PLRA`: bloqueia qualquer `CAPAG-E`.
- Sem metodo: bloqueia laudo final.
- Sem `FCA` final no metodo `fca_plra`: bloqueia resultado final.
- Sem `ROA` final no metodo `roa_plra`: bloqueia resultado final.
- Evidencia critica pendente: bloqueia ou gera ressalva, conforme decisao do Modulo 04.
- Pendencia metodologica bloqueante: bloqueia componente afetado.

## Resultado parcial

O sistema pode mostrar resultado parcial, desde que:

- o status esteja explicito;
- a limitacao esteja descrita;
- o frontend nao apresente como valor final;
- a exportacao registre a restricao.

## Criterios de sucesso

- Nenhum valor final e exibido sem status.
- O usuario entende por que um resultado esta bloqueado.
- O laudo futuro consegue consumir o status sem deduzir regra.

