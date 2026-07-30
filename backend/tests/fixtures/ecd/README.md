# Fixtures ECD Sinteticas

Estas fixtures sao sinteticas, governadas e pequenas. Elas existem para validar parser,
importacao, camada declarada e golden cases da `SPEC-002` para nao versionar ECD real ou dado
sensivel do usuario.

Arquivos:

- `valid_declared.ecd`: caso valido com `I010`, `I030`, `I050`, `I051`, `I052`, `I150`, `I155`, `I200`, `I250`, `J005`, `J100` e `J150`.
- `missing_i051.ecd`: conta sem vinculo referencial declarado, com Bloco J sintético válido para importação CAPAG-E.
- `official_reference_missing.ecd`: `COD_CTA_REF` ausente no plano oficial carregado, com Bloco J sintético válido para importação CAPAG-E.
- `methodology_missing.ecd`: codigo oficial sem regra metodologica exata, com Bloco J sintético válido para importação CAPAG-E.
- `blocked_rule.ecd`: codigo com regra metodologica bloqueada, com Bloco J sintético válido para importação CAPAG-E.
- `dangerous_prefix.ecd`: conta `1725` com `2.01.01.07.01`, que nao pode virar fornecedor por prefixo `2.01.01.*`, com Bloco J sintético válido para importação CAPAG-E.
- `balance_declared_valid.ecd`: balanço `J100` válido, com `COD_AGL` diferente de `COD_CTA` e saldos inicial e final distintos.
- `balance_declared_divergent.ecd`: estrutura válida com diferença exata de `0,01` na conciliação.
- `balance_declared_required_absent.ecd`: Bloco J obrigatório sem `J100`.
- `balance_declared_invalid_structure.ecd`: totalizador e lados do `J100` estruturalmente inválidos.
- `balance_declared_not_required.ecd`: encerramento `I030` fora do período, sem obrigação do Bloco J.

Os CNPJs, nomes, codigos e valores sao ficticios.
