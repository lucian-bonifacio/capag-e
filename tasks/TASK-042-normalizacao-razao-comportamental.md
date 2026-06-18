# TASK-042 - Normalizacao e razao comportamental

## SPEC De Origem

- `specs/SPEC-003-modulo-2-capag-reclassificada.md`

## Dependencias

- `TASK-041-exportacao-e-testes-camada-declarada.md`

## Objetivo

Criar a base de normalização comportamental e razão por conta para a camada reclassificada, preservando dados originais e contrapartidas auditáveis.

## Fontes Usadas

- `docs/product/PRD.md`
- `docs/architecture/architecture.md`
- `specs/SPEC-003-modulo-2-capag-reclassificada.md`

## Escopo Exato

- Preservar texto original e criar campos normalizados.
- Agrupar partidas por conta analítica.
- Vincular `I250` a `I200`.
- Identificar contrapartidas simples e compostas.
- Marcar ambiguidade de contrapartida.

## Fora De Escopo

- Classificar família contábil.
- Calcular score.
- Criar revisão humana.
- Criar API, frontend ou exportação.
- Usar palavra-chave isolada como decisão.

## Passos Executaveis

1. Ler contratos de entradas da SPEC-003.
2. Implementar normalização permitida.
3. Montar razão por conta e contrapartidas.
4. Criar testes de lançamentos simples, compostos e ambíguos.

## Arquivos Ou Areas Provaveis

- `backend/app/engine/`
- `backend/app/domain/`
- `backend/tests/`

## Criterios De Aceite

- Dado original é preservado.
- Contrapartidas ambíguas ficam marcadas.
- Normalização textual não decide classificação.
- Valores usam `Decimal`.

## Validacao Esperada

- Executar testes backend via `docker compose`.

## Riscos

- Risco: normalização virar classificação por palavra-chave.
  Mitigação: bloquear decisão de família nesta TASK.

## Bloqueios Pendentes

Bloqueada até camada declarada estar disponível.
