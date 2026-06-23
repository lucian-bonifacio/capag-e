# Assets Da Camada Declarada

Este diretorio guarda assets metodologicos versionados do repositorio.

Nesta etapa, os arquivos sao modelos seguros para a camada declarada. Eles documentam estrutura e campos obrigatorios previstos pela `SPEC-002`, sem popular plano referencial oficial completo, sem criar regra prudencial real e sem implementar motor.

## Estrutura

- `reference/official_reference_accounts.template.json`: modelo para plano referencial oficial.
- `methodology/internal_methodology_rules.template.json`: modelo para metodologia interna por finalidade.

## Limites

- Plano referencial oficial descreve o significado formal do `COD_CTA_REF` e nao decide calculo.
- Metodologia interna define tratamentos futuros por finalidade, mas este modelo nao contem regras ativas reais.
- Frontend, Excel e laudo nao devem recalcular regra de negocio a partir destes arquivos.
- Qualquer populacao real deve vir de fonte governada e validacao propria.

