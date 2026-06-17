# TASK-051 - Persistir assessment CAPAG-E

## SPEC De Origem

- `specs/SPEC-004-modulo-3-contrato-capag-e-plra-fca-roa.md`

## Dependencias

- `TASK-017-configurar-alembic-minimo.md`
- `TASK-050-implementar-motor-contrato-capag-e.md`

## Objetivo

Persistir snapshots de `CapagEAssessment` com método, componentes, status, fórmula, limitações, bloqueios e versão metodológica.

## Fontes Usadas

- `docs/product/PRD.md`
- `docs/architecture.md`
- `specs/SPEC-004-modulo-3-contrato-capag-e-plra-fca-roa.md`

## Escopo Exato

- Criar modelo persistente mínimo para assessment CAPAG-E.
- Criar migration correspondente.
- Preservar valores como string/decimal controlado.
- Registrar metodologia e bloqueios.

## Fora De Escopo

- Criar motores `FCA` ou `ROA`.
- Criar laudo.
- Criar UI.
- Criar exportação.

## Passos Executaveis

1. Ler entidade de domínio.
2. Criar modelo persistente.
3. Criar migration.
4. Criar testes de persistência.

## Arquivos Ou Areas Provaveis

- `backend/app/repositories/`
- `backend/alembic/`
- `backend/tests/`

## Criterios De Aceite

- Assessment persistido carrega método e status.
- Limitações e bloqueios são preservados.
- Migration roda via Docker Compose.

## Validacao Esperada

- Executar migrations e testes via `docker compose`.

## Riscos

- Risco: persistência perder status parcial.
  Mitigação: status e bloqueios obrigatórios no modelo.

## Bloqueios Pendentes

Bloqueada até motor CAPAG-E e Alembic existirem.
