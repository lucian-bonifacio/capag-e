# TASK-097 - Criar API e integracao PLRA CAPAG-E

## SPEC De Origem

- `specs/SPEC-011-modulo-1b-motor-plra.md`

## Dependencias

- `TASK-096-persistir-snapshots-plra.md`
- `TASK-052-criar-api-capag-assessment.md`

## Objetivo

Expor execucao e consulta do PLRA e alimentar automaticamente o contrato CAPAG-E com valor, status, limitacoes e bloqueios reais.

## Fontes Usadas

- `docs/product/PRD.md`
- `docs/architecture/architecture.md`
- `specs/SPEC-011-modulo-1b-motor-plra.md`
- `specs/SPEC-004-modulo-3-contrato-capag-e-plra-fca-roa.md`

## Escopo Exato

- Criar schemas e endpoints PLRA.
- Expor resumo, auditoria, pendencias e versao.
- Integrar snapshot ao `CapagEAssessment`.
- Impedir PLRA final informado sem snapshot calculado.

## Fora De Escopo

- Criar UI ou Excel.
- Calcular FCA, ROA ou CAPAG-E fora do motor existente.
- Alterar metodologia por endpoint livre.

## Passos Executaveis

1. Criar schemas Pydantic.
2. Criar rotas e orquestracao.
3. Integrar contrato CAPAG-E.
4. Criar testes de API e propagacao de status.

## Arquivos Ou Areas Provaveis

- `backend/app/api/`
- `backend/app/schemas/`
- `backend/app/application/`
- `backend/tests/`

## Criterios De Aceite

- API serializa decimais como string.
- PLRA calculado alimenta assessment.
- Pendencia ou evidencia bloqueante propaga status.
- OpenAPI reflete o contrato da SPEC.

## Validacao Esperada

- Executar testes backend via `docker compose`.

## Riscos

- Risco: API aceitar status divergente do snapshot.
  Mitigacao: status sempre derivado do caso de uso.

## Bloqueios Pendentes

Bloqueada ate persistencia PLRA e API CAPAG-E existirem.
