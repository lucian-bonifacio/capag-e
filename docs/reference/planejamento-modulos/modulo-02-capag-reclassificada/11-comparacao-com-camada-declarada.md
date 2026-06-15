# 11 - Comparacao com a camada declarada

## Objetivo

Definir como comparar a classificacao comportamental sugerida com o `I051` original.

## Ponto de decisao

Decidir estados oficiais da comparacao.

## Estados sugeridos

- `manter`: o `I051` original e compativel com o comportamento observado.
- `reclassificar`: o `I051` original parece incompatível e o sistema tem alta confianca.
- `revisar`: ha indicio de divergencia, mas existe ambiguidade.
- `sem_conclusao`: dados insuficientes.

## Detalhamento

- Comparar codigo referencial original com codigo sugerido.
- Comparar familia declarada com familia comportamental.
- Registrar divergencia e motivo.
- Calcular impacto potencial no PLR.
- Calcular impacto potencial na CAPAG-e quando houver FCO final utilizavel.
- Nao alterar silenciosamente o resultado declarado.

## Arquivos correlatos

- `tmp_deu_a_louca/modulo-01-camada-declarada/`
- futuro `src/capag/engine/behavioral_compare.py`
- `src/capag/engine/plr.py`
- `src/capag/engine/capag.py`

## Entregavel

Contrato de comparacao declarado vs reclassificado.

## Criterios de sucesso

- As duas leituras coexistem.
- O usuario entende por que houve divergencia.

## Fora do escopo

- Substituir o resultado declarado.

