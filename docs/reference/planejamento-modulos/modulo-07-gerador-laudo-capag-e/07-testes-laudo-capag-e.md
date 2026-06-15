# 07 - Testes do laudo CAPAG-E

## Testes obrigatorios

1. Gerar laudo final com `FCA + PLRA`.
2. Gerar laudo final com `ROA + PLRA`.
3. Bloquear laudo sem metodo.
4. Bloquear laudo sem `PLRA`.
5. Gerar laudo preliminar com `FCA parcial`.
6. Incluir evidencias materiais.
7. Incluir ressalvas por evidencia pendente.
8. Garantir que o laudo nao recalcula motores.

## Areas afetadas

- `domain`
- `engine` ou futuro `report`
- `export`
- `api`
- `frontend`

## Criterio de sucesso

O laudo deve ser reprodutivel e auditavel a partir dos resultados existentes.

