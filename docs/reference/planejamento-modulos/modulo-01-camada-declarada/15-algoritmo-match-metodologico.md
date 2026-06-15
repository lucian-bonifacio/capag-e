# 15 - Algoritmo de match metodologico

## Objetivo

Definir o algoritmo oficial para encontrar regra metodologica segura a partir do `COD_CTA_REF`.

## Ponto de decisao

Decidir se o algoritmo sera compartilhado entre PLR, FCO e CAPAG-e ou se cada finalidade tera wrapper proprio sobre um mesmo matcher.

## Arquivos correlatos

- `docs/reference/ajuste_modulo_principal.md`
- `src/capag/engine/plr.py`
- `src/capag/engine/fco.py`
- futuro motor/metodologia compartilhado
- `src/capag/domain/models.py`
- `tests/unit/`

## Ordem de prioridade

1. Codigo exato ativo.
2. Prefixo de maior profundidade ativo.
3. Prefixo de menor profundidade ativo.
4. Regra generica somente se for explicitamente segura.

## Regras de status

- Pular `BLOQUEADA`.
- Pular `GENERICA_PERIGOSA`.
- Pular `EM_REVISAO`, salvo em relatorio diagnostico.
- Pular `DEPRECIADA` para calculos novos.
- Aceitar `ATIVA`.
- Aceitar `GENERICA_SEGURA`.

## Fluxo do algoritmo

Entrada:

- `cod_cta_ref`;
- ano;
- leiaute;
- tipo de entidade, se aplicavel;
- finalidade: PLR, FCO, CAPAG-e, auditoria ou outra.

Processo:

1. Buscar codigo na tabela oficial.
2. Se nao existir, retornar `COD_CTA_REF_NAO_ENCONTRADO_NA_TABELA_OFICIAL`.
3. Gerar candidatos metodologicos por especificidade.
4. Ignorar candidatos com status bloqueado/perigoso/em revisao/depreciado.
5. Para cada candidato seguro, obter tratamento da finalidade solicitada.
6. Se tratamento existir, retornar `MAPEADO`.
7. Se nenhum candidato seguro existir, retornar `NAO_MAPEADO_METODOLOGICAMENTE`.

## Pseudosaida `MAPEADO`

- status;
- `cod_cta_ref`;
- descricao oficial;
- regra aplicada;
- finalidade;
- tratamento;
- categoria PLR;
- categoria FCO;
- categoria CAPAG-e;
- natureza do fluxo;
- observacao.

## Pseudosaida sem regra

- status `NAO_MAPEADO_METODOLOGICAMENTE`;
- `cod_cta_ref`;
- descricao oficial;
- acao `revisar_tabela_metodologica`.

## Pseudosaida sem codigo oficial

- status `COD_CTA_REF_NAO_ENCONTRADO_NA_TABELA_OFICIAL`;
- `cod_cta_ref`;
- acao `revisar_base_oficial`.

## Relacao com o sistema atual

O sistema atual ja faz:

- busca exata;
- prefixos ordenados por tamanho decrescente.

O sistema atual ainda precisa planejar/adicionar:

- tabela oficial completa;
- status de regra;
- bloqueio de prefixo amplo perigoso;
- tratamento por finalidade;
- status padronizados de retorno.

## Criterios de sucesso

- Regra mais especifica vence.
- Regra ampla perigosa nao classifica.
- Ausencia de regra segura nao cai em categoria generica.

## Fora do escopo

- Implementar matcher nesta etapa de planejamento.

