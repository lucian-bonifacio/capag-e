# TASK-041G - Executar camada declarada da ECD importada

## SPEC De Origem

- `specs/SPEC-002-modulo-1-camada-declarada.md`

## Dependencias

- `TASK-041F-criar-importacao-ecd-oficial.md`
- `TASK-036-implementar-matcher-metodologico-declarado.md`
- `TASK-038-persistir-snapshots-camada-declarada.md`

## Objetivo

Implementar a execucao da camada declarada a partir da ECD normalizada importada, gerando snapshots automaticamente via endpoint `POST /declared/run`.

## Fontes Usadas

- `docs/product/PRD.md`
- `docs/architecture/architecture.md`
- `specs/SPEC-002-modulo-1-camada-declarada.md`
- `tasks/TASK-041F-criar-importacao-ecd-oficial.md`

## Escopo Exato

- Criar caso de uso `run_declared_layer` a partir de analise/exercicio importado.
- Criar endpoint `POST /api/v1/analyses/{analysis_id}/exercises/{year}/declared/run`.
- Carregar contas, saldos e `COD_CTA_REF` declarado no `I051`.
- Aplicar plano oficial e metodologia por codigo exato, sem fallback por prefixo.
- Gerar snapshots declarados por conta.
- Atualizar status da analise/exercicio para concluido, concluido_com_pendencias, bloqueado ou erro.

## Fora De Escopo

- Criar parser ECD.
- Criar UI de acionamento.
- Criar reclassificacao comportamental.
- Criar regra metodologica nova.

## Passos Executaveis

1. Ler repositories da ECD normalizada e snapshots declarados.
2. Implementar caso de uso de execucao declarada.
3. Criar endpoint `POST /declared/run`.
4. Criar testes de integracao com fixtures.

## Arquivos Ou Areas Provaveis

- `backend/app/application/`
- `backend/app/api/`
- `backend/app/engine/`
- `backend/tests/`

## Criterios De Aceite

- `POST /declared/run` cria snapshots declarados a partir da ECD importada.
- Conta sem `I051` vira `SEM_VINCULO_REFERENCIAL`.
- Codigo ausente no plano oficial vira `COD_CTA_REF_NAO_ENCONTRADO_NA_TABELA_OFICIAL`.
- Codigo oficial sem regra exata vira `NAO_MAPEADO_METODOLOGICAMENTE`.
- Prefixo perigoso nao classifica resultado final.

## Validacao Esperada

- Executar testes backend via `docker compose`.
- Testar fluxo importacao + run + GET declarada.

## Riscos

- Risco: motor declarado recalcular ou inferir por prefixo.
  Mitigacao: reutilizar matcher exato e golden cases da SPEC-002.

## Bloqueios Pendentes

Bloqueada ate importacao ECD oficial existir.
