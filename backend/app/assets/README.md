# Assets Da Camada Declarada

Este diretorio guarda assets metodologicos e fontes oficiais versionadas do
repositorio.

O plano referencial publicado deriva da fonte oficial SPED/RFB aprovada,
preserva origem e hash e continua separado da metodologia prudencial.

## Estrutura

- `reference/official_reference_accounts.json`: plano referencial oficial
  publicado para `PJ_GERAL`, ECF Leiaute 11, ano-calendario 2024.
- `reference/official_reference_accounts.template.json`: modelo vazio para estrutura do plano referencial oficial.
- `reference/sources/`: documento oficial de origem preservado para
  reproducibilidade.
- `methodology/internal_methodology_rules.template.json`: modelo para metodologia interna por finalidade.
- `methodology/dfc_methodology.json`: contas de disponibilidades, componentes e regras exatas da DFC direta.
- `methodology/tabela_metodologica_roa.csv`: classificação ROA por código referencial exato ou prefixo oficial.
- `methodology/componentes_roa.csv`: componentes e evidências esperadas por bloco ROA.

## Limites

- Plano referencial oficial descreve o significado formal do `COD_CTA_REF` e nao decide calculo.
- Plano referencial oficial ausente, vazio ou invalido e erro de configuracao do sistema.
- Codigo declarado pela ECD e ausente no plano oficial carregado deve gerar `COD_CTA_REF_NAO_ENCONTRADO_NA_TABELA_OFICIAL`.
- Metodologia interna define tratamentos futuros por finalidade, mas este modelo nao contem regras ativas reais.
- Frontend, Excel e laudo nao devem recalcular regra de negocio a partir destes arquivos.
- A fonte aprovada, seu hash e o contrato de carga estao documentados em
  `docs/methodology/`.
- A conversao reproduzivel e executada por
  `backend/scripts/import_official_reference.py`.

## Regeneracao

Execute somente pelo ambiente oficial:

```text
docker compose --profile test run --rm backend-tests \
  python scripts/import_official_reference.py \
  app/assets/reference/sources/Tabelas-Dinamicas-ECF-Leiaute-11-AC-2024.xlsx \
  app/assets/reference/official_reference_accounts.json
```

O importador rejeita documento com SHA-256 diferente do aprovado.
