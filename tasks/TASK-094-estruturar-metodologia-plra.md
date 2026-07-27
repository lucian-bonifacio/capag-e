# TASK-094 - Estruturar metodologia PLRA

## SPEC De Origem

- `specs/SPEC-011-modulo-1b-motor-plra.md`

## Dependencias

- `TASK-041M-gerenciar-importacoes-ecd-existentes.md`
- `TASK-091-preparar-asset-completo-plano-referencial.md`

## Objetivo

Criar assets versionados de grupos, regras exatas e desagios default do PLRA, incorporando a politica aprovada sem implementar o motor.

## Fontes Usadas

- `docs/product/PRD.md`
- `docs/architecture/architecture.md`
- `specs/SPEC-011-modulo-1b-motor-plra.md`

## Escopo Exato

- Criar schema e asset de politica PLRA.
- Registrar os nove defaults aprovados.
- Mapear grupos e tratamentos por codigo referencial exato.
- Validar cobertura, percentuais, duplicidades e versao.

## Fora De Escopo

- Calcular PLRA.
- Criar API, UI, persistencia ou Excel.
- Inferir codigo ou criar regra fora da SPEC.

## Passos Executaveis

1. Criar assets PLRA versionados.
2. Implementar loader e validacao estrutural.
3. Cruzar regras com plano oficial.
4. Criar testes de defaults e cobertura.

## Arquivos Ou Areas Provaveis

- `backend/app/assets/methodology/`
- `backend/app/assets/`
- `backend/tests/`

## Criterios De Aceite

- Defaults correspondem a SPEC-011.
- Toda regra usa codigo exato e versao.
- Asset rejeita percentual invalido e duplicidade.
- Regra ausente permanece pendencia, sem inferencia.

## Validacao Esperada

- Executar validacoes e testes backend via `docker compose`.

## Riscos

- Risco: asset interno divergir do plano oficial.
  Mitigacao: validacao cruzada obrigatoria.

## Bloqueios Pendentes

Bloqueada ate o plano referencial completo estar preparado.
