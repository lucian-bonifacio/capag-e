# Fixtures ECD Sinteticas

Estas fixtures sao sinteticas, governadas e pequenas. Elas existem para validar parser,
importacao, camada declarada e golden cases da `SPEC-002` para nao versionar ECD real ou dado
sensivel do usuario.

Arquivos:

- `valid_declared.ecd`: caso valido com `I050`, `I051`, `I155`, `I200`, `I250` e `J100`.
- `missing_i051.ecd`: conta sem vinculo referencial declarado.
- `official_reference_missing.ecd`: `COD_CTA_REF` ausente no plano oficial carregado.
- `methodology_missing.ecd`: codigo oficial sem regra metodologica exata.
- `blocked_rule.ecd`: codigo com regra metodologica bloqueada.
- `dangerous_prefix.ecd`: conta `1725` com `2.01.01.07.01`, que nao pode virar fornecedor por prefixo `2.01.01.*`.

Os CNPJs, nomes, codigos e valores sao ficticios.
