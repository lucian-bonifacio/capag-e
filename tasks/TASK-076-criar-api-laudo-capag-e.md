# TASK-076 - Criar API de laudo CAPAG-E

## SPEC De Origem

- `specs/SPEC-008-modulo-7-gerador-laudo-capag-e.md`

## Dependencias

- `TASK-075-gerar-excel-laudo-estruturado.md`

## Objetivo

Criar API de preview, geração e consulta de laudo CAPAG-E, consumindo resultados calculados e exportação estruturada.

## Fontes Usadas

- `docs/product/PRD.md`
- `docs/architecture/architecture.md`
- `specs/SPEC-008-modulo-7-gerador-laudo-capag-e.md`

## Escopo Exato

- Criar endpoint de preview.
- Criar endpoint de geração.
- Criar endpoint de consulta por `report_id`.
- Validar `assessment_method`, `capag_p_value`, responsável e seções preliminares.

## Fora De Escopo

- Criar frontend.
- Gerar DOCX/PDF.
- Recalcular motores.
- Implementar armazenamento definitivo fora do contrato atual.

## Passos Executaveis

1. Criar schemas de request/response.
2. Criar rotas FastAPI.
3. Integrar geração Excel.
4. Criar testes de contrato.

## Arquivos Ou Areas Provaveis

- `backend/app/api/`
- `backend/app/application/`
- `backend/tests/`

## Criterios De Aceite

- Preview mostra seções e bloqueios.
- Geração respeita status do laudo.
- API não recalcula motores.

## Validacao Esperada

- Executar testes backend via `docker compose`.

## Riscos

- Risco: API gerar laudo sem validação.
  Mitigação: geração depende do validador de status.

## Bloqueios Pendentes

Bloqueada até Excel estruturado do laudo existir.
