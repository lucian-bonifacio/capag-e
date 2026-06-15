# 04 - Integracao com PLRA e bloqueios

## Objetivo

Definir como evidencias e avaliacao de ativos afetam o `PLRA`.

## Regras gerais

1. O motor de `PLRA` nao deve buscar dados diretamente no frontend.
2. O dominio deve entregar ao motor avaliacoes e evidencias validadas.
3. Na ausencia de avaliacao validada, o motor usa politica default ou bloqueia, conforme materialidade.
4. A auditoria deve mostrar valor contabil, desagio default, valor de liquidacao e valor final.

## Bloqueios de ativos

O `PLRA` deve ser bloqueado ou ressalvado quando:

- ativo material exige laudo e esta pendente;
- ativo material tem valor manual sem justificativa;
- ativo essencial foi excluido sem justificativa operacional;
- ativo com liquidacao forcada nao tem base documental.

## Bloqueios de evidencia

Bloquear ou ressalvar quando:

- evidencia critica esta pendente;
- evidencia foi rejeitada;
- justificativa obrigatoria esta vazia;
- ajuste material nao tem tipo de evidencia definido.

## Integracao com pendencias metodologicas

Ao resolver conta condicional:

- criar ou atualizar evidencia;
- vincular ao exercicio;
- vincular a conta ou grupo metodologico;
- exigir justificativa quando materialidade for `media`, `alta` ou `critica`.

## Ponto de decisao

Definir a diferenca operacional entre:

- bloquear `PLRA`;
- bloquear laudo final;
- permitir laudo com ressalva.

Essa decisao deve ser compativel com Modulo 03 e Modulo 07.

