# TASK-052 - Criar API CAPAG assessment

## SPEC De Origem

- `specs/SPEC-004-modulo-3-contrato-capag-e-plra-fca-roa.md`

## Dependencias

- `TASK-051-persistir-assessment-capag-e.md`

## Objetivo

Criar endpoints para executar e consultar `CapagEAssessment`, expondo método, fórmula, componentes, status, limitações e bloqueios.

## Fontes Usadas

- `docs/product/PRD.md`
- `docs/architecture.md`
- `specs/SPEC-004-modulo-3-contrato-capag-e-plra-fca-roa.md`

## Escopo Exato

- Criar endpoint de execução do assessment.
- Criar endpoint de consulta.
- Criar schemas de request, response e erro.
- Serializar valores monetários como string decimal.

## Fora De Escopo

- Criar frontend.
- Calcular DFC/FCA ou ROA.
- Gerar laudo.
- Criar exportação Excel.

## Passos Executaveis

1. Ler endpoints alvo da SPEC-004.
2. Criar schemas Pydantic.
3. Criar rotas FastAPI.
4. Criar testes de contrato.

## Arquivos Ou Areas Provaveis

- `backend/app/api/`
- `backend/app/application/`
- `backend/tests/`

## Criterios De Aceite

- API retorna método e status final.
- Valores são strings decimais.
- Resultado parcial não é mascarado.
- Erros de contrato são explícitos.

## Validacao Esperada

- Executar testes backend via `docker compose`.
- Revisar OpenAPI.

## Riscos

- Risco: API apresentar CAPAG-E final sem componentes suficientes.
  Mitigação: delegar status ao motor e testar bloqueios.

## Bloqueios Pendentes

Bloqueada até persistência do assessment existir.
