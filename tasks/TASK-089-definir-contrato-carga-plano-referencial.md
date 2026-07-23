# TASK-089 - Definir contrato de carga do plano referencial

## SPEC De Origem

- `specs/SPEC-010-governanca-plano-referencial-oficial.md`

## Dependencias

- `TASK-088-pesquisar-fonte-oficial-plano-referencial.md`

## Objetivo

Definir o contrato governado de carga do plano referencial oficial, incluindo campos finais, metadados de origem, hash, estados, versionamento e criterios de publicacao.

## Fontes Usadas

- `docs/product/PRD.md`
- `docs/architecture/architecture.md`
- `specs/SPEC-001-modulo-0-fundacao-governada.md`
- `specs/SPEC-002-modulo-1-camada-declarada.md`
- `specs/SPEC-009-modulo-8-governanca-metodologia.md`
- `specs/SPEC-010-governanca-plano-referencial-oficial.md`
- resultado documental da `TASK-088`

## Escopo Exato

- Definir campos obrigatorios e opcionais da carga.
- Definir metadados de fonte, hash, documento, data, vigencia, leiaute e tipo de entidade.
- Definir estados da base, estados por codigo e transicoes permitidas.
- Definir criterio minimo para fonte aprovada, base publicada e base bloqueada.
- Definir manifest ou estrutura equivalente para rastreabilidade.
- Definir erros de validacao e configuracao relacionados a carga.

## Fora De Escopo

- Implementar loader, banco, API ou UI.
- Popular asset completo.
- Aprovar fonte oficial por conta da TASK.
- Alterar regra prudencial ou metodologia interna.
- Criar contrato de CRUD operacional completo.

## Passos Executaveis

1. Ler `SPEC-010`, `SPEC-002` e resultado da pesquisa da `TASK-088`.
2. Consolidar campos minimos e candidatos em contrato final de carga.
3. Definir estrutura de manifest/metadados.
4. Definir estados, transicoes e erros esperados.
5. Registrar gates para carga, publicacao e bloqueio.
6. Atualizar documento governado aplicavel.

## Arquivos Ou Areas Provaveis

- `specs/SPEC-010-governanca-plano-referencial-oficial.md`
- `docs/methodology/`
- `backend/app/assets/README.md`

## Criterios De Aceite

- Contrato de carga esta documentado e rastreavel.
- Campos obrigatorios, metadados, estados e erros estao definidos.
- Hash e origem da fonte sao obrigatorios para publicacao.
- Contrato nao permite publicacao operacional sem fonte aprovada.
- Contrato nao altera metodologia prudencial.

## Validacao Esperada

- Revisar consistencia documental contra `SPEC-010`, PRD e arquitetura.
- Conferir que o contrato nao cria regra prudencial nem contrato de API executivo.
- Registrar ausencia de testes automatizados quando a entrega for somente documental.

## Riscos

- Risco: contrato ficar amplo demais para implementacao.
  Mitigacao: separar campos obrigatorios de campos candidatos.

- Risco: contrato permitir carga sem rastreabilidade.
  Mitigacao: exigir origem, hash e metadados minimos.

## Bloqueios Pendentes

- Fonte oficial aprovada para permitir carga operacional completa.
