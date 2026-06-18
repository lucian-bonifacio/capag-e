# TASK-038 - Persistir snapshots da camada declarada

## SPEC De Origem

- `specs/SPEC-002-modulo-1-camada-declarada.md`

## Dependencias

- `TASK-017-configurar-alembic-minimo.md`
- `TASK-037-modelar-resultado-conta-declarada.md`

## Objetivo

Persistir snapshots da camada declarada com versão metodológica e rastreabilidade por análise, exercício e conta, sem substituir a ECD original e sem criar reclassificação comportamental.

## Fontes Usadas

- `docs/product/PRD.md`
- `docs/architecture/architecture.md`
- `specs/SPEC-002-modulo-1-camada-declarada.md`

## Escopo Exato

- Criar modelos persistentes mínimos para snapshot declarado.
- Criar migration correspondente.
- Preservar `methodology_version_id`.
- Registrar status e limitações por conta.

## Fora De Escopo

- Criar parser ECD.
- Criar reclassificação.
- Criar endpoints.
- Criar tela.
- Criar exportação.

## Passos Executaveis

1. Ler modelo de resultado declarado.
2. Criar modelos SQLAlchemy mínimos.
3. Criar migration via Alembic.
4. Criar testes de persistência via Docker Compose.

## Arquivos Ou Areas Provaveis

- `backend/app/repositories/`
- `backend/alembic/`
- `backend/tests/`

## Criterios De Aceite

- Snapshots declarados persistem versão metodológica.
- Dados declarados originais não são sobrescritos.
- Migration roda via container.

## Validacao Esperada

- Executar Alembic e testes backend via `docker compose`.
- Conferir ausência de regra prudencial nova.

## Riscos

- Risco: persistência virar modelagem ampla demais.
  Mitigação: limitar ao snapshot declarado previsto na SPEC-002.

## Bloqueios Pendentes

Bloqueada até Alembic mínimo e resultado declarado existirem.
