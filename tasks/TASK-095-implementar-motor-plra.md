# TASK-095 - Implementar motor PLRA

## SPEC De Origem

- `specs/SPEC-011-modulo-1b-motor-plra.md`

## Dependencias

- `TASK-094-estruturar-metodologia-plra.md`

## Objetivo

Implementar dominio e motor PLRA com hierarquia, desagios, consolidacao, auditoria e estados, sem persistencia ou API.

## Fontes Usadas

- `docs/product/PRD.md`
- `docs/architecture/architecture.md`
- `specs/SPEC-011-modulo-1b-motor-plra.md`

## Escopo Exato

- Modelar `PlraCalculation` e `PlraAccountAuditRow`.
- Calcular `PLR bruto` e `PLRA`.
- Aplicar defaults, exclusoes e passivos.
- Resolver pai/filha e pendencias condicionais.
- Rejeitar `float`.

## Fora De Escopo

- Persistir snapshot.
- Criar API, UI ou Excel.
- Implementar avaliacao de ativos da SPEC-005.
- Calcular FCA, ROA ou CAPAG-E.

## Passos Executaveis

1. Modelar contratos de dominio.
2. Implementar selecao anual e hierarquia.
3. Implementar formulas e audit rows.
4. Criar testes unitarios e golden case.

## Arquivos Ou Areas Provaveis

- `backend/app/domain/`
- `backend/app/engine/`
- `backend/tests/`

## Criterios De Aceite

- Formulas seguem SPEC-011.
- Defaults sao auditaveis.
- Pai e filha nao duplicam saldo.
- Conta sem regra segura nao e inferida.
- Valores usam `Decimal`.

## Validacao Esperada

- Executar testes backend via `docker compose`.

## Riscos

- Risco: sinal ou hierarquia distorcer resultado.
  Mitigacao: testes por natureza, pai/filha e reconciliacao.

## Bloqueios Pendentes

Bloqueada ate assets PLRA validados existirem.
