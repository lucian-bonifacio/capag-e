# TASK-063 - Calcular FCA, pendencias e evidencias

## SPEC De Origem

- `specs/SPEC-006-modulo-5-dfc-direta-fca.md`

## Dependencias

- `TASK-057-persistir-e-integrar-bloqueios-evidencias.md`
- `TASK-062-implementar-motor-dfc-direta.md`

## Objetivo

Calcular `DfcCalculation` e `FCA` com status final ou parcial, integrando pendências e evidências materiais.

## Fontes Usadas

- `docs/product/PRD.md`
- `docs/architecture.md`
- `specs/SPEC-006-modulo-5-dfc-direta-fca.md`

## Escopo Exato

- Calcular fluxos operacional, investimento e financiamento.
- Calcular `FCA = operacional + investimento + financiamento + ajustes manuais validados`.
- Gerar pendências por regra ausente, fluxo incompatível e evidência material.
- Tratar `FCO` atual como componente operacional/parcial.

## Fora De Escopo

- Motor ROA.
- Laudo.
- API e UI.
- Ajustes manuais livres sem evidência.

## Passos Executaveis

1. Implementar `DfcCalculation`.
2. Integrar pendências/evidências.
3. Criar testes de status parcial, calculado e bloqueado.

## Arquivos Ou Areas Provaveis

- `backend/app/engine/`
- `backend/app/domain/`
- `backend/tests/`

## Criterios De Aceite

- `FCO` não é apresentado como `FCA` completo.
- Movimentos materiais não classificados bloqueiam final quando aplicável.
- Evidências materiais afetam status, não recalculam valor por si.

## Validacao Esperada

- Executar testes backend via `docker compose`.

## Riscos

- Risco: `FCA parcial` aparecer como final.
  Mitigação: status explícito e testes de bloqueio.

## Bloqueios Pendentes

Bloqueada até motor DFC e evidências existirem.
