# TASK-067 - Estruturar assets ROA

## SPEC De Origem

- `specs/SPEC-007-modulo-6-motor-roa-plra.md`

## Dependencias

- `TASK-018-criar-validacao-assets-metodologicos-minima.md`
- `TASK-054-exportacao-e-testes-contrato-capag-e.md`

## Objetivo

Estruturar assets metodológicos de ROA e componentes ROA, sem calcular resultado nem criar regra prudencial além do contrato da SPEC-007.

## Fontes Usadas

- `docs/product/PRD.md`
- `docs/architecture/architecture.md`
- `specs/SPEC-007-modulo-6-motor-roa-plra.md`

## Escopo Exato

- Criar estrutura para `tabela_metodologica_roa` e `componentes_roa`.
- Registrar colunas mínimas da SPEC-007.
- Validar tratamentos permitidos.

## Fora De Escopo

- Calcular ROA.
- Criar API, UI ou exportação.
- Criar regra por nome livre.

## Passos Executaveis

1. Criar estrutura de assets ROA.
2. Criar validação estrutural.
3. Criar testes de carregamento.

## Arquivos Ou Areas Provaveis

- `backend/app/assets/`
- `backend/tests/`

## Criterios De Aceite

- Assets ROA possuem colunas mínimas.
- Tratamentos permitidos são validados.
- Nome livre não decide classificação.

## Validacao Esperada

- Executar validações via `docker compose`.

## Riscos

- Risco: asset inicial virar regra não aprovada.
  Mitigação: limitar a estrutura governada.

## Bloqueios Pendentes

Bloqueada até validação de assets e contrato CAPAG-E existirem.
