# TASK-049 - Modelar contrato de dominio CAPAG-E

## SPEC De Origem

- `specs/SPEC-004-modulo-3-contrato-capag-e-plra-fca-roa.md`

## Dependencias

- `TASK-037-modelar-resultado-conta-declarada.md`

## Objetivo

Modelar `CapagEAssessment`, métodos permitidos, status de componentes, status final, bloqueios, limitações e warnings, usando `Decimal` e proibindo `float`.

## Fontes Usadas

- `docs/product/PRD.md`
- `docs/architecture.md`
- `specs/SPEC-004-modulo-3-contrato-capag-e-plra-fca-roa.md`

## Escopo Exato

- Criar contratos internos de domínio para `PLRA`, `FCA`, `ROA` e `CAPAG-E`.
- Modelar métodos `fca_plra`, `roa_plra`, `comparativo_fca_roa` e `nao_definido`.
- Modelar status permitidos e bloqueios mínimos.
- Quantizar valores finais em `0.01`.

## Fora De Escopo

- Calcular DFC/FCA completo.
- Calcular ROA.
- Gerar laudo.
- Criar frontend ou exportação.

## Passos Executaveis

1. Ler contratos da SPEC-004.
2. Criar value objects e entidades de domínio.
3. Criar validações contra `float`.
4. Criar testes unitários de status e quantização.

## Arquivos Ou Areas Provaveis

- `backend/app/domain/`
- `backend/tests/`

## Criterios De Aceite

- `CapagEAssessment` contém campos mínimos.
- Métodos e status inválidos são rejeitados.
- `float` gera erro de contrato.
- Valores finais usam `Decimal`.

## Validacao Esperada

- Executar testes backend via `docker compose`.

## Riscos

- Risco: contrato aceitar resultado sem status.
  Mitigação: status obrigatório por componente e resultado final.

## Bloqueios Pendentes

Bloqueada até domínio base da fundação existir.
