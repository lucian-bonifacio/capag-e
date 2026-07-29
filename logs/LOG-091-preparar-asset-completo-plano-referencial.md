# LOG - TASK-091 - Preparar asset completo do plano referencial

## Referencia

- Task: `tasks/TASK-091-preparar-asset-completo-plano-referencial.md`
- SPEC: `specs/SPEC-010-governanca-plano-referencial-oficial.md`
- Status: concluido

## Fontes Consultadas

- `specs/SPEC-002-modulo-1-camada-declarada.md`
- `specs/SPEC-010-governanca-plano-referencial-oficial.md`
- `docs/methodology/pesquisa-fonte-oficial-plano-referencial.md`
- `docs/methodology/contrato-carga-plano-referencial.md`
- XLSX oficial SPED/RFB aprovado.

## Execucao

- Data: 2026-07-24
- Acao: conversao e publicacao do asset governado completo.
- Resumo: preservada a fonte oficial com SHA-256 aprovado e gerado asset reproduzivel com 1.109 registros das abas `L100A` e `L300A`.
- Resumo: a divergencia oficial de nivel da conta `3.11.05.01.01.01` foi preservada e marcada `EM_REVISAO`, sem correcao local.
- Resumo: o marcador real `LECD` passou a ser normalizado para o leiaute governado `ECD_9` nos periodos aplicaveis.

## Arquivos Alterados

- `backend/app/assets/reference/sources/Tabelas-Dinamicas-ECF-Leiaute-11-AC-2024.xlsx`
- `backend/app/assets/reference/official_reference_accounts.json`
- `backend/scripts/import_official_reference.py`
- `backend/app/io/ecd_parser.py`
- `backend/tests/test_assets_structure.py`
- `backend/tests/test_ecd_parser.py`
- `docs/methodology/pesquisa-fonte-oficial-plano-referencial.md`
- `docs/methodology/contrato-carga-plano-referencial.md`
- `logs/LOG-091-preparar-asset-completo-plano-referencial.md`
- `ROADMAP.md`

## Validacoes

- Comando: testes backend completos via `docker compose`.
  - Resultado: 110 testes aprovados.
- Comando: testes focados de asset, loader e parser via `docker compose`.
  - Resultado: 28 testes aprovados, incluindo reproducao exata do asset pela fonte versionada.
- Validacao: cobertura do `ECD 2024 DATAPACK.txt`.
  - Resultado: 58 de 58 codigos `I051` distintos encontrados; nenhuma ausencia.
- Validacao: integridade da fonte.
  - Resultado: SHA-256 `0c66a19ce859cdc7a1eee137896243100cbaa26239ffa8ed3044762f3e359397`.

## Pendencias Ou Bloqueios

- Uma conta oficial permanece `EM_REVISAO` por divergencia de nivel na propria fonte; ela nao integra os codigos usados pelo DATAPACK.

## Homologacao

- Status: aprovada
- Data: 2026-07-29
- Decisao do usuario: todas as TASKs pendentes foram homologadas.
- Observacao: entrega homologada conforme o escopo e as fontes vigentes. A compatibilidade com a nova camada declarada sera revisada, quando aplicavel, nas `TASK-101` a `TASK-108`; ajustes transversais de status e resultado final concentram-se nas `TASK-107` e `TASK-108`.
