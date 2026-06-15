# 17 - Frontend da revisao comportamental

## Objetivo

Planejar a interface de revisao humana do modulo reclassificado.

## Ponto de decisao

Decidir se sera uma tela nova ou expansao da Revisao Analitica existente.

## Tela recomendada

Para cada conta:

- painel esquerdo:
  - conta original;
  - hierarquia;
  - `I051` original;
  - saldos;
  - movimentos resumidos.
- painel central:
  - classificacao sugerida;
  - score;
  - explicacao;
  - top evidencias.
- painel direito:
  - lancamentos amostrados;
  - principais contrapartidas;
  - historicos frequentes.

## Acoes

- aprovar sugestao;
- rejeitar sugestao;
- escolher outra classificacao;
- marcar excecao;
- comentar;
- salvar precedente, se essa fase for aprovada.

## Arquivos correlatos

- `web/src/App.jsx`
- futuras rotas React do modulo 0;
- `web/src/components/AnalyticConditionalReview.jsx`
- futuro `web/src/features/behavioral-review/`
- `web/src/lib/api.js`

## Entregavel

Spec da UI do modulo reclassificado.

## Criterios de sucesso

- O usuario consegue entender evidencia e impacto.
- Frontend nao recalcula score nem regra.

## Fora do escopo

- Implementar design agora.

