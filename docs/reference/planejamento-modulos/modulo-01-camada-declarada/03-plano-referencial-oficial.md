# 03 - Plano referencial oficial

## Objetivo

Definir o artefato interno que traduz `COD_CTA_REF` para sua descricao oficial.

## Ponto de decisao

Decidir se o projeto criara `src/capag/assets/reference/plano_referencial_oficial.csv` ou evoluira `catalogo_referencial.csv`.

## Arquivos correlatos

- `docs/reference/ajuste_modulo_principal.md`
- `src/capag/assets/reference/catalogo_referencial.csv`
- `src/capag/io/ecd_normalizer.py`
- `src/capag/domain/models.py`
- `src/capag/api/presentation.py`
- `src/capag/export/excel.py`

## Detalhamento

- Definir colunas minimas, seja em CSV versionado ou tabela persistida, conforme decisao arquitetural de banco:
  - `cod_cta_ref`;
  - `descricao_oficial`;
  - `cod_cta_ref_pai`;
  - `nivel`;
  - `natureza`;
  - `vigencia_inicio`;
  - `vigencia_fim`;
  - `leiaute`;
  - `tipo_entidade`;
  - `fonte`;
  - `status`.
- Definir que este artefato nao decide calculo.
- Definir como o normalizador ou presentation enriquece contas com descricao oficial.
- Definir comportamento quando o codigo nao existir no plano oficial.
- Definir que upload nao deve ser rejeitado apenas por ausencia no catalogo/plano oficial, salvo decisao futura.

## Entregavel

Especificacao do artefato de plano referencial oficial.

## Criterios de sucesso

- O sistema separa significado oficial de tratamento metodologico.
- O plano oficial fica rastreavel e versionado, seja como asset no repositorio ou como tabela com controle de versao, conforme decisao de persistencia.

## Fora do escopo

- Popular toda a tabela oficial.
- Criar interface de administracao.
