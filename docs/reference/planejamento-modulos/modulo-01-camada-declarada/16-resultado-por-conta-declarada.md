# 16 - Resultado por conta declarada

## Objetivo

Definir a estrutura de resultado por conta para a camada declarada.

## Ponto de decisao

Decidir quais campos devem entrar no dominio, no payload da API, na UI e na exportacao.

## Campos esperados por conta

- conta societaria;
- nome da conta;
- `COD_CTA_REF` informado no `I051`;
- descricao oficial do `COD_CTA_REF`;
- status na tabela oficial;
- regra metodologica aplicada;
- status da regra metodologica;
- categoria PLR;
- categoria FCO;
- categoria CAPAG-e;
- natureza do fluxo;
- tratamento aplicado;
- valor base;
- valor considerado;
- status final;
- observacao;
- acao recomendada, quando houver falha de metodologia.

## Status esperados

- `MAPEADO`;
- `NAO_MAPEADO_METODOLOGICAMENTE`;
- `COD_CTA_REF_NAO_ENCONTRADO_NA_TABELA_OFICIAL`;
- `SEM_VINCULO_REFERENCIAL`;
- `REGRA_BLOQUEADA`;
- `REGRA_EM_REVISAO`;
- `REGRA_DEPRECIADA`;
- `EXCLUIDO_AUTOMATICAMENTE`;
- `INCLUIDO_AUTOMATICAMENTE`.

## Comportamento quando nao existir regra metodologica

Se o codigo existir na tabela oficial, mas nenhuma regra metodologica segura for encontrada:

- nao aplicar prefixo amplo perigoso;
- marcar como `NAO_MAPEADO_METODOLOGICAMENTE`;
- indicar acao `revisar_tabela_metodologica`;
- preservar descricao oficial.

## Comportamento quando codigo nao existir na tabela oficial

Se o `COD_CTA_REF` nao existir na tabela oficial carregada:

- nao inventar descricao;
- marcar como `COD_CTA_REF_NAO_ENCONTRADO_NA_TABELA_OFICIAL`;
- indicar acao `revisar_base_oficial`;
- preservar o codigo declarado na ECD.

## Arquivos correlatos

- `src/capag/domain/models.py`
- `src/capag/api/presentation.py`
- `web/src/components/`
- `src/capag/export/excel.py`
- `tests/unit/test_api_presentation.py`
- `tests/unit/test_excel_export.py`

## Criterios de sucesso

- O usuario consegue rastrear a conta da ECD ate o tratamento final.
- API, UI e Excel falam a mesma linguagem.
- O resultado por conta prepara o terreno para comparacao futura com Modulo 2.

## Fora do escopo

- Criar a analise comportamental.

