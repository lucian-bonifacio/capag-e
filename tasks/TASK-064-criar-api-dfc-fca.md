# TASK-064 - Criar API DFC/FCA

## SPEC De Origem

- `specs/SPEC-006-modulo-5-dfc-direta-fca.md`

## Dependencias

- `TASK-063-calcular-fca-pendencias-evidencias.md`

## Objetivo

Criar API para executar e consultar DFC direta, `FCA`, linhas de auditoria, pendências, evidências e status.

## Fontes Usadas

- `docs/product/PRD.md`
- `docs/architecture.md`
- `specs/SPEC-006-modulo-5-dfc-direta-fca.md`

## Escopo Exato

- Criar schemas para `DfcCalculation` e `DfcAuditRow`.
- Criar endpoints de execução e consulta.
- Expor pendências e status.
- Serializar valores como string decimal.

## Fora De Escopo

- Criar UI.
- Criar exportação.
- Criar laudo.
- Calcular ROA.

## Passos Executaveis

1. Ler contratos da SPEC-006.
2. Criar schemas e rotas.
3. Criar testes de contrato.

## Arquivos Ou Areas Provaveis

- `backend/app/api/`
- `backend/app/application/`
- `backend/tests/`

## Criterios De Aceite

- API expõe linhas auditáveis.
- Status `FCA` fica explícito.
- Valores são strings decimais.

## Validacao Esperada

- Executar testes backend via `docker compose`.

## Riscos

- Risco: API esconder movimentos não classificados.
  Mitigação: pendências e audit rows obrigatórias.

## Bloqueios Pendentes

Bloqueada até cálculo de FCA existir.
