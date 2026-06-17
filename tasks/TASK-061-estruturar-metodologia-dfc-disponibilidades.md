# TASK-061 - Estruturar metodologia DFC e disponibilidades

## SPEC De Origem

- `specs/SPEC-006-modulo-5-dfc-direta-fca.md`

## Dependencias

- `TASK-035-estruturar-assets-camada-declarada.md`
- `TASK-054-exportacao-e-testes-contrato-capag-e.md`

## Objetivo

Estruturar metodologia DFC direta e identificação de contas de disponibilidades, sem calcular `FCA` final.

## Fontes Usadas

- `docs/product/PRD.md`
- `docs/architecture.md`
- `specs/SPEC-006-modulo-5-dfc-direta-fca.md`

## Escopo Exato

- Criar estrutura de assets DFC.
- Definir componentes operacionais, investimento, financiamento e não classificados.
- Identificar contas de disponibilidades por código referencial.
- Bloquear classificação por nome livre como critério principal.

## Fora De Escopo

- Calcular DFC.
- Criar API, UI ou exportação.
- Criar regra prudencial não prevista.

## Passos Executaveis

1. Ler contratos da SPEC-006.
2. Criar estrutura de assets DFC.
3. Criar validação estrutural mínima.
4. Criar testes de identificação de disponibilidades.

## Arquivos Ou Areas Provaveis

- `backend/app/assets/`
- `backend/tests/`

## Criterios De Aceite

- Componentes DFC mínimos existem.
- Nome livre não decide classificação.
- Disponibilidades são identificadas por regra governada.

## Validacao Esperada

- Executar validações/testes via `docker compose`.

## Riscos

- Risco: nome de conta virar critério principal.
  Mitigação: código referencial é fonte principal.

## Bloqueios Pendentes

Bloqueada até assets declarados e contrato CAPAG-E existirem.
