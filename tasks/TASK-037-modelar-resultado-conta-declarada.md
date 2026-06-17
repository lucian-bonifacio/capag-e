# TASK-037 - Modelar resultado por conta declarada

## SPEC De Origem

- `specs/SPEC-002-modulo-1-camada-declarada.md`

## Dependencias

- `TASK-036-implementar-matcher-metodologico-declarado.md`

## Objetivo

Modelar o resultado auditável por conta da camada declarada, preservando `I051`, status metodológico, regra aplicada, versão metodológica e valores em `Decimal`.

## Fontes Usadas

- `docs/product/PRD.md`
- `docs/architecture.md`
- `specs/SPEC-002-modulo-1-camada-declarada.md`

## Escopo Exato

- Criar contratos internos para resultado por conta declarada.
- Registrar código societário, `COD_CTA_REF`, descrição oficial, regra metodológica, status e finalidade.
- Preservar valores como `Decimal`.
- Preparar snapshot sem expor API ainda.

## Fora De Escopo

- Criar endpoint.
- Criar tela.
- Criar exportação Excel.
- Implementar camada reclassificada.
- Criar regra prudencial nova.

## Passos Executaveis

1. Ler contratos da SPEC-002.
2. Modelar entidades/value objects internos.
3. Integrar saída do matcher.
4. Criar testes unitários de serialização interna e status.

## Arquivos Ou Areas Provaveis

- `backend/app/domain/`
- `backend/app/engine/`
- `backend/tests/`

## Criterios De Aceite

- Resultado preserva leitura declarada.
- Status de regra fica explícito.
- Valores financeiros não usam `float`.
- Resultado não altera camada declarada original.

## Validacao Esperada

- Executar testes backend via `docker compose`.
- Revisar ausência de cálculo fora do engine.

## Riscos

- Risco: misturar plano oficial com metodologia interna.
  Mitigação: campos e responsabilidades separados.

## Bloqueios Pendentes

Bloqueada até matcher metodológico declarado existir.
