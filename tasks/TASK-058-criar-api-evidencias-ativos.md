# TASK-058 - Criar API de evidencias e ativos

## SPEC De Origem

- `specs/SPEC-005-modulo-4-evidencias-justificativas-ativos.md`

## Dependencias

- `TASK-057-persistir-e-integrar-bloqueios-evidencias.md`

## Objetivo

Criar API para consultar, registrar e revisar evidências, materialidade e avaliações de ativos, expondo bloqueios e ressalvas de forma auditável.

## Fontes Usadas

- `docs/product/PRD.md`
- `docs/architecture.md`
- `specs/SPEC-005-modulo-4-evidencias-justificativas-ativos.md`

## Escopo Exato

- Criar schemas de evidência, override e avaliação de ativo.
- Criar endpoints de consulta e atualização controlada.
- Expor bloqueios por componente.
- Serializar valores como string decimal.

## Fora De Escopo

- Upload persistente de anexos.
- Assinatura digital.
- UI.
- Laudo.

## Passos Executaveis

1. Ler contratos da SPEC-005.
2. Criar schemas Pydantic.
3. Criar rotas FastAPI.
4. Criar testes de contrato.

## Arquivos Ou Areas Provaveis

- `backend/app/api/`
- `backend/app/application/`
- `backend/tests/`

## Criterios De Aceite

- API exige justificativa para override.
- Bloqueios e ressalvas ficam explícitos.
- Valores decimais trafegam como string.

## Validacao Esperada

- Executar testes backend via `docker compose`.

## Riscos

- Risco: API permitir dispensa sem justificativa.
  Mitigação: validação obrigatória de justificativa.

## Bloqueios Pendentes

Bloqueada até persistência de evidências e ativos existir.
