# TASK-096 - Persistir snapshots PLRA

## SPEC De Origem

- `specs/SPEC-011-modulo-1b-motor-plra.md`

## Dependencias

- `TASK-095-implementar-motor-plra.md`

## Objetivo

Persistir calculos e audit rows PLRA por analise, exercicio e versao metodologica, com invalidacao de dependentes.

## Fontes Usadas

- `docs/product/PRD.md`
- `docs/architecture/architecture.md`
- `specs/SPEC-011-modulo-1b-motor-plra.md`

## Escopo Exato

- Criar modelos SQLAlchemy e migration.
- Persistir snapshot e memoria por conta.
- Recuperar ultima execucao aplicavel.
- Invalidar assessment CAPAG-E dependente quando PLRA mudar.

## Fora De Escopo

- Criar API, UI ou Excel.
- Persistir anexos.
- Recalcular fora do engine.

## Passos Executaveis

1. Criar modelos persistentes.
2. Criar migration Alembic.
3. Implementar repositorio e caso de uso.
4. Testar atomicidade, versao e invalidacao.

## Arquivos Ou Areas Provaveis

- `backend/app/repositories/`
- `backend/app/application/`
- `backend/alembic/versions/`
- `backend/tests/`

## Criterios De Aceite

- Snapshot preserva metodologia e auditoria.
- Reprocessamento nao altera snapshot historico.
- Assessment dependente e invalidado.
- Migration chega ao `head`.

## Validacao Esperada

- Executar migration e testes backend via `docker compose`.

## Riscos

- Risco: PLRA novo coexistir com CAPAG-E obsoleto.
  Mitigacao: invalidacao transacional de dependentes.

## Bloqueios Pendentes

Bloqueada ate o motor PLRA existir.
