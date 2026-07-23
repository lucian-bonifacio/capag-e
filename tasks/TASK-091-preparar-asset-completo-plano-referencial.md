# TASK-091 - Preparar asset completo do plano referencial

## SPEC De Origem

- `specs/SPEC-010-governanca-plano-referencial-oficial.md`

## Dependencias

- `TASK-088-pesquisar-fonte-oficial-plano-referencial.md`
- `TASK-089-definir-contrato-carga-plano-referencial.md`
- `TASK-090-ampliar-validacoes-asset-plano-referencial.md`

## Objetivo

Preparar o asset governado completo do plano referencial oficial a partir de fonte aprovada, preservando origem, hash, metadados, cobertura e validacao automatizada antes de uso operacional amplo.

## Fontes Usadas

- `docs/product/PRD.md`
- `docs/architecture/architecture.md`
- `specs/SPEC-002-modulo-1-camada-declarada.md`
- `specs/SPEC-009-modulo-8-governanca-metodologia.md`
- `specs/SPEC-010-governanca-plano-referencial-oficial.md`
- fonte oficial aprovada na `TASK-088`
- contrato de carga da `TASK-089`

## Escopo Exato

- Converter fonte aprovada para o formato governado do asset.
- Registrar metadados de origem, hash, vigencia, leiaute e tipo de entidade.
- Validar cobertura conforme criterio aprovado.
- Executar validacoes automatizadas do asset.
- Registrar lacunas residuais e codigos em revisao quando existirem.
- Manter reproducibilidade por arquivo versionado.

## Fora De Escopo

- Usar fonte nao aprovada.
- Criar ou migrar banco.
- Criar CRUD ou API administrativa.
- Corrigir manualmente fonte oficial sem justificativa governada.
- Alterar metodologia interna ou regra prudencial.
- Inferir codigo alternativo para conta da ECD.

## Passos Executaveis

1. Confirmar que a fonte oficial foi aprovada.
2. Ler contrato de carga e validacoes existentes.
3. Preparar asset completo em formato governado.
4. Registrar metadados, hash e cobertura.
5. Executar validacoes automatizadas.
6. Ajustar apenas erros estruturais permitidos pelo contrato.
7. Registrar pendencias, lacunas e decisao de publicacao pendente.

## Arquivos Ou Areas Provaveis

- `backend/app/assets/reference/`
- `backend/app/assets/README.md`
- `docs/methodology/`
- `backend/tests/`

## Criterios De Aceite

- Asset completo deriva de fonte aprovada.
- Origem, hash e metadados estao registrados.
- Validacoes automatizadas passam ou registram bloqueios objetivos.
- Lacunas de cobertura ficam explicitas.
- O asset nao altera metodologia prudencial.

## Validacao Esperada

- Executar validacoes de asset via `docker compose`.
- Executar testes backend via `docker compose`.
- Validar ECDs de referencia quando a publicacao operacional for pretendida.
- Conferir ausencia de `float` em arquivos alterados.

## Riscos

- Risco: conversao manual introduzir erro.
  Mitigacao: exigir hash, validacoes e revisao de cobertura.

- Risco: asset incompleto virar base operacional.
  Mitigacao: manter status e decisao de publicacao separados.

## Bloqueios Pendentes

- Fonte oficial aprovada.
- Contrato de carga aprovado.
- Criterio de cobertura aprovado.
