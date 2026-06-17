# TASK-046 - Criar API da camada reclassificada

## SPEC De Origem

- `specs/SPEC-003-modulo-2-capag-reclassificada.md`

## Dependencias

- `TASK-045-cenario-reclassificado-revisao-humana.md`

## Objetivo

Criar API para consultar perfis, classificações, comparação declarado vs reclassificado e registrar revisões humanas, sem recalcular regra no frontend.

## Fontes Usadas

- `docs/product/PRD.md`
- `docs/architecture.md`
- `specs/SPEC-003-modulo-2-capag-reclassificada.md`

## Escopo Exato

- Criar schemas de perfis, classificações, revisão e cenário.
- Criar endpoints de consulta e revisão.
- Serializar valores como string decimal.
- Expor status parcial/bloqueado quando contratos posteriores faltarem.

## Fora De Escopo

- Criar UI.
- Criar exportação.
- Criar laudo.
- Implementar CAPAG-E final.

## Passos Executaveis

1. Ler contratos da SPEC-003.
2. Criar schemas Pydantic.
3. Criar rotas FastAPI.
4. Criar testes de contrato.

## Arquivos Ou Areas Provaveis

- `backend/app/api/`
- `backend/app/application/`
- `backend/tests/`

## Criterios De Aceite

- API expõe cenário reclassificado com status.
- Revisão humana fica auditável.
- Valores decimais trafegam como string.

## Validacao Esperada

- Executar testes backend via `docker compose`.
- Revisar OpenAPI.

## Riscos

- Risco: API aplicar regra comportamental.
  Mitigação: regra fica no engine; API orquestra e serializa.

## Bloqueios Pendentes

Bloqueada até cenário reclassificado persistido existir.
