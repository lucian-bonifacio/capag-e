# TASK-062 - Implementar motor DFC direta

## SPEC De Origem

- `specs/SPEC-006-modulo-5-dfc-direta-fca.md`

## Dependencias

- `TASK-061-estruturar-metodologia-dfc-disponibilidades.md`

## Objetivo

Implementar motor DFC direta para classificar fluxos financeiros efetivos com contrapartida em disponibilidades e gerar `DfcAuditRow`.

## Fontes Usadas

- `docs/product/PRD.md`
- `docs/architecture.md`
- `specs/SPEC-006-modulo-5-dfc-direta-fca.md`

## Escopo Exato

- Processar `I200` e `I250`.
- Incluir apenas lançamentos com caixa/disponibilidades.
- Classificar atividade DFC.
- Gerar linhas auditáveis.
- Marcar não classificados e fluxos incompatíveis.

## Fora De Escopo

- Ajustes manuais.
- Evidências materiais.
- API, UI e exportação.
- Motor ROA.

## Passos Executaveis

1. Ler metodologia DFC.
2. Implementar motor e `DfcAuditRow`.
3. Criar testes de fluxo com/sem caixa.
4. Validar status de linha.

## Arquivos Ou Areas Provaveis

- `backend/app/engine/`
- `backend/app/domain/`
- `backend/tests/`

## Criterios De Aceite

- Lançamento sem caixa não entra na DFC.
- Linha não classificada fica auditável.
- Valores usam `Decimal`.

## Validacao Esperada

- Executar testes backend via `docker compose`.

## Riscos

- Risco: incluir fluxo sem caixa.
  Mitigação: teste obrigatório de contrapartida em disponibilidades.

## Bloqueios Pendentes

Bloqueada até metodologia DFC estar estruturada.
