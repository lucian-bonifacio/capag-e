# TASK-107 - Integrar validade do balanço ao PLRA e CAPAG-E

## SPEC De Origem

- `specs/SPEC-012-modulo-1c-balanco-patrimonial-declarado.md`

## Dependencias

- `TASK-095-implementar-motor-plra.md`
- `TASK-097-criar-api-integracao-plra-capag-e.md`
- `TASK-105-criar-api-balanco-declarado.md`

## Objetivo

Integrar o estado objetivo do Balanço Patrimonial declarado aos contratos de
PLRA e CAPAG-E, impedindo resultado anual final sobre base inválida sem alterar
fórmulas ou tratamentos prudenciais.

## Fontes Usadas

- `docs/product/PRD.md`
- `docs/architecture/architecture.md`
- `specs/SPEC-004-modulo-3-contrato-capag-e-plra-fca-roa.md`
- `specs/SPEC-011-modulo-1b-motor-plra.md`
- `specs/SPEC-012-modulo-1c-balanco-patrimonial-declarado.md`
- `tasks/TASK-095-implementar-motor-plra.md`
- `tasks/TASK-097-criar-api-integracao-plra-capag-e.md`
- `tasks/TASK-105-criar-api-balanco-declarado.md`

## Escopo Exato

- Substituir o controle informativo antigo por `balance_status`.
- Consumir o estado produzido pelo motor do balanço, sem recalculá-lo no PLRA.
- Permitir resultado final somente com `balance_status = VALIDO`.
- Manter valores intermediários como diagnóstico quando houver bloqueio.
- Expor bloqueio e limitação nos contratos PLRA e CAPAG-E.
- Impedir `CapagEAssessment` final dependente de balanço inválido.
- Invalidar resultados dependentes quando reprocessamento alterar a base.
- Ajustar persistência e serialização dos campos afetados.
- Ajustar API, UI PLRA e exportação somente para refletir o novo estado.
- Criar testes de integração para todos os estados do balanço.

## Fora De Escopo

- Alterar fórmula do PLRA ou CAPAG-E.
- Alterar regras de inclusão, exclusão ou deságio.
- Criar switches ou decisões humanas.
- Usar valores do `J100` como fonte analítica do PLRA.
- Recalcular o balanço no frontend, Excel ou laudo.
- Criar snapshot do balanço por consulta.

## Passos Executaveis

1. Migrar o contrato PLRA de reconciliação informativa para `balance_status`.
2. Integrar o estado do balanço ao motor e à persistência PLRA.
3. Propagar bloqueio e limitações ao assessment CAPAG-E.
4. Ajustar schemas, API, UI e exportação afetados.
5. Integrar invalidação após reprocessamento.
6. Criar testes de diagnóstico permitido e resultado final bloqueado.
7. Validar que fórmulas e políticas permanecem inalteradas.

## Arquivos Ou Areas Provaveis

- `backend/app/domain/plra.py`
- `backend/app/engine/plra.py`
- `backend/app/application/plra_service.py`
- `backend/app/repositories/plra_calculations.py`
- `backend/app/schemas/plra.py`
- `backend/app/domain/capag.py`
- `backend/app/engine/capag.py`
- `backend/app/application/capag_service.py`
- `frontend/src/routes/PlraPage.tsx`
- `backend/app/export/plra_excel.py`
- `backend/tests/`
- `frontend/src/test/`

## Criterios De Aceite

- `balance_status` vem do motor do balanço declarado.
- Apenas `VALIDO` permite PLRA/CAPAG-E anual final.
- Estado inválido preserva valores intermediários como diagnóstico bloqueado.
- Bloqueio e limitação aparecem na API, UI e exportação afetadas.
- Reprocessamento invalida resultados dependentes.
- `J100` continua fora da fonte analítica primária do PLRA.
- Fórmulas, deságios e regras por conta permanecem inalterados.
- Nenhum frontend ou exportador recalcula o estado.

## Validacao Esperada

- Executar testes backend via `docker compose`.
- Executar testes frontend e build via `docker compose` quando afetados.
- Testar cada `balance_status` no PLRA e CAPAG-E.
- Testar invalidação após reprocessamento.
- Conferir ausência de `float` nos arquivos alterados.

## Riscos

- Risco: confundir bloqueio de base com mudança metodológica.
  Mitigação: preservar cálculos intermediários e fórmulas existentes.
- Risco: motor PLRA recalcular o balanço.
  Mitigação: consumir apenas o estado oficial produzido pela camada declarada.
- Risco: resultado final antigo permanecer válido após reprocessamento.
  Mitigação: integrar invalidação de dependências.

## Bloqueios Pendentes

Bloqueada até a conclusão das `TASK-095`, `TASK-097` e `TASK-105`.

