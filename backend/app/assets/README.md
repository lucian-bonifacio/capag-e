# Assets Da Camada Declarada

Este diretorio guarda assets metodologicos versionados do repositorio.

Nesta etapa, os arquivos documentam estrutura e campos obrigatorios previstos pela `SPEC-002` e incluem um plano referencial oficial governado inicial, de cobertura minima, para validar a camada declarada sem criar regra prudencial real.

## Estrutura

- `reference/official_reference_accounts.json`: plano referencial oficial governado inicial, obrigatorio para executar a camada declarada.
- `reference/official_reference_accounts.template.json`: modelo vazio para estrutura do plano referencial oficial.
- `methodology/internal_methodology_rules.template.json`: modelo para metodologia interna por finalidade.

## Limites

- Plano referencial oficial descreve o significado formal do `COD_CTA_REF` e nao decide calculo.
- Plano referencial oficial ausente, vazio ou invalido e erro de configuracao do sistema.
- Codigo declarado pela ECD e ausente no plano oficial carregado deve gerar `COD_CTA_REF_NAO_ENCONTRADO_NA_TABELA_OFICIAL`.
- Metodologia interna define tratamentos futuros por finalidade, mas este modelo nao contem regras ativas reais.
- Frontend, Excel e laudo nao devem recalcular regra de negocio a partir destes arquivos.
- Qualquer populacao real deve vir de fonte governada e validacao propria.
