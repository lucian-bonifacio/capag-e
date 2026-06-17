# TASK-039 - Criar API da camada declarada

## SPEC De Origem

- `specs/SPEC-002-modulo-1-camada-declarada.md`

## Dependencias

- `TASK-028-criar-app-fastapi-minimo.md`
- `TASK-038-persistir-snapshots-camada-declarada.md`

## Objetivo

Criar endpoints da camada declarada para consultar resultado por conta, status metodológico e auditoria mínima, serializando valores financeiros como string decimal.

## Fontes Usadas

- `docs/product/PRD.md`
- `docs/architecture.md`
- `specs/SPEC-002-modulo-1-camada-declarada.md`

## Escopo Exato

- Criar schemas Pydantic da camada declarada.
- Criar endpoint de consulta do resultado declarado.
- Mapear erros e status sem esconder bloqueios.
- Garantir serialização decimal como string.

## Fora De Escopo

- Criar frontend.
- Criar exportação.
- Criar reclassificação.
- Criar parser ECD.
- Criar regra metodológica nova.

## Passos Executaveis

1. Ler contratos da SPEC-002.
2. Criar schemas de response e erro.
3. Criar rota FastAPI.
4. Criar testes de contrato via Docker Compose.

## Arquivos Ou Areas Provaveis

- `backend/app/api/`
- `backend/app/application/`
- `backend/tests/`

## Criterios De Aceite

- API retorna status por conta.
- Valores financeiros são strings decimais.
- Erros de metodologia ficam explícitos.
- OpenAPI reflete o contrato.

## Validacao Esperada

- Executar testes backend via `docker compose`.
- Revisar OpenAPI gerado.

## Riscos

- Risco: API decidir regra de domínio.
  Mitigação: API apenas serializa resultado calculado pelo backend.

## Bloqueios Pendentes

Bloqueada até app FastAPI mínimo e snapshots declarados existirem.
