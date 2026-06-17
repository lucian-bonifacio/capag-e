# TASK-045 - Cenario reclassificado e revisao humana

## SPEC De Origem

- `specs/SPEC-003-modulo-2-capag-reclassificada.md`

## Dependencias

- `TASK-038-persistir-snapshots-camada-declarada.md`
- `TASK-044-classificacao-score-salvaguardas-reclassificada.md`

## Objetivo

Criar o cenário reclassificado completo, com persistência de classificações, comparação com camada declarada e revisão humana analítica ou por subgrupo.

## Fontes Usadas

- `docs/product/PRD.md`
- `docs/architecture.md`
- `specs/SPEC-003-modulo-2-capag-reclassificada.md`

## Escopo Exato

- Persistir perfis, classificações e snapshots reclassificados.
- Comparar declarado vs reclassificado.
- Permitir decisão humana sem sobrescrever camada declarada.
- Registrar revisão analítica e por subgrupo.

## Fora De Escopo

- Implementar UI.
- Criar laudo final.
- Implementar evidências formais do módulo 4.
- Recalcular CAPAG-E final sem contrato disponível.

## Passos Executaveis

1. Modelar cenário reclassificado.
2. Criar persistência e migrations.
3. Integrar revisão humana.
4. Criar testes de preservação da camada declarada.

## Arquivos Ou Areas Provaveis

- `backend/app/domain/`
- `backend/app/repositories/`
- `backend/alembic/`
- `backend/tests/`

## Criterios De Aceite

- Cenário reclassificado não sobrescreve declarado.
- Revisões ficam auditáveis.
- Cenário pode ser parcial ou bloqueado com status explícito.

## Validacao Esperada

- Executar migrations e testes via `docker compose`.

## Riscos

- Risco: revisão humana alterar dado declaratório.
  Mitigação: persistir revisão em camada própria.

## Bloqueios Pendentes

Bloqueada até classificação reclassificada e snapshots declarados existirem.
