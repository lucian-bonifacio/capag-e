# TASK-057 - Persistir e integrar bloqueios de evidencias

## SPEC De Origem

- `specs/SPEC-005-modulo-4-evidencias-justificativas-ativos.md`

## Dependencias

- `TASK-051-persistir-assessment-capag-e.md`
- `TASK-096-persistir-snapshots-plra.md`
- `TASK-055-modelar-evidencias-materialidade.md`
- `TASK-056-modelar-avaliacao-ativos.md`

## Objetivo

Persistir evidências, avaliações de ativos, bloqueios e ressalvas, integrando-os aos componentes afetados sem recalcular motores fora do backend.

## Fontes Usadas

- `docs/product/PRD.md`
- `docs/architecture/architecture.md`
- `specs/SPEC-005-modulo-4-evidencias-justificativas-ativos.md`

## Escopo Exato

- Criar modelos persistentes e migrations.
- Persistir status de evidência e avaliação.
- Integrar avaliacoes e bloqueios aos snapshots PLRA e ao contrato CAPAG-E.
- Preservar versão metodológica.

## Fora De Escopo

- Upload de anexos.
- Laudo narrativo.
- UI e API.
- Criar motor DFC ou ROA.

## Passos Executaveis

1. Criar modelos de persistência.
2. Criar migrations.
3. Integrar avaliacoes e bloqueios com PLRA e assessment.
4. Criar testes de persistência e propagação de status.

## Arquivos Ou Areas Provaveis

- `backend/app/repositories/`
- `backend/alembic/`
- `backend/tests/`

## Criterios De Aceite

- Evidências críticas pendentes bloqueiam ou ressalvam conforme regra.
- Avaliações de ativos preservam status.
- PLRA e contrato CAPAG-E recebem bloqueios sem recalcular evidencia fora dos motores.

## Validacao Esperada

- Executar migrations e testes via `docker compose`.

## Riscos

- Risco: bloquear componente errado.
  Mitigação: escopo e componente metodológico obrigatórios.

## Bloqueios Pendentes

Bloqueada ate modelos de evidencia, ativos, snapshots PLRA e assessment existirem.
