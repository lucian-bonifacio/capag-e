# 08 - Testes DFC e FCA

## Testes obrigatorios

1. Classificar fluxo operacional atual como operacional.
2. Classificar compra de imobilizado como investimento.
3. Classificar captacao/amortizacao de emprestimo como financiamento.
4. Ignorar lancamento sem caixa.
5. Registrar pendencia para regra ausente.
6. Calcular `FCA` como soma das tres atividades.
7. Preservar compatibilidade com `FCO`.

## Areas afetadas

- `io`
- `domain`
- `engine`
- `assets`
- `api`
- `export`
- `frontend`

## Criterio de sucesso

O motor nao perde movimentos, nao soma fluxos sem classificacao e nao confunde `FCO` com `FCA`.

