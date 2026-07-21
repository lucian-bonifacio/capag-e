# TASK-041M - Gerenciar importacoes ECD existentes

## SPEC De Origem

- `specs/SPEC-002-modulo-1-camada-declarada.md`

## Dependencias

- `TASK-041A-modelar-importacao-ecd-status-analise.md`
- `TASK-041B-criar-migrations-ecd-normalizada.md`
- `TASK-041E-persistir-ecd-normalizada.md`
- `TASK-041F-criar-importacao-ecd-oficial.md`
- `TASK-041H-integrar-ui-analise-importada-real.md`
- `TASK-041J-validar-fluxo-end-to-end-declarada.md`

## Objetivo

Permitir que o usuario acesse importacoes ECD ja existentes, abra a analise associada e remova explicitamente uma importacao antes de reenviar o mesmo arquivo.

## Fontes Usadas

- `docs/product/PRD.md`
- `docs/architecture/architecture.md`
- `specs/SPEC-002-modulo-1-camada-declarada.md`
- `tasks/TASK-041F-criar-importacao-ecd-oficial.md`
- `tasks/TASK-041H-integrar-ui-analise-importada-real.md`
- `tasks/TASK-041J-validar-fluxo-end-to-end-declarada.md`

## Escopo Exato

- Detectar tentativa de importar ECD ja existente pelo `content_hash`.
- Retornar erro controlado ou resposta de conflito que informe que o arquivo ja foi importado.
- Expor dados suficientes da importacao existente para abrir a analise associada.
- Criar listagem simples de importacoes/analises existentes com nome original, periodo, status e acao de abrir.
- Criar remocao explicita e controlada de uma importacao ECD existente.
- Ao remover, apagar dados normalizados e snapshots dependentes da analise/importacao de forma transacional.
- Permitir reimportacao apenas depois da remocao explicita.
- Validar com os arquivos reais autorizados `docs/reference/ecd-example/ECD 2024 DATAPACK.txt` e `docs/reference/ecd-example/ECD 2024 INVENTCLOUD.txt` em testes separados.

## Fora De Escopo

- Salvar ou disponibilizar download do arquivo ECD bruto.
- Criar GED, anexos, versionamento de arquivos brutos ou armazenamento externo.
- Criar autenticação, permissões ou multiusuário.
- Alterar metodologia, matcher, plano referencial ou regra prudencial.
- Alterar cálculo da camada declarada.
- Implementar fila assíncrona ou jobs.
- Criar reimportação silenciosa/idempotente.
- Remover dados sem ação explícita do usuário.

## Passos Executaveis

1. Ler contratos de importacao, persistencia e UI ja existentes.
2. Definir contrato de conflito para ECD ja importada.
3. Criar endpoint ou extensão de endpoint para listar importacoes/analises existentes.
4. Criar endpoint de remocao controlada da importacao/analise.
5. Ajustar UI para exibir importacoes existentes, abrir analise e remover importacao.
6. Ajustar fluxo de upload para orientar o usuario quando o arquivo ja existir.
7. Criar testes backend para duplicidade, listagem, remocao transacional e reimportacao apos remocao.
8. Criar ou ajustar testes frontend/E2E para fluxo de arquivo ja importado e remocao.
9. Validar manualmente com `DATAPACK` e `INVENTCLOUD` em execucoes separadas.

## Arquivos Ou Areas Provaveis

- `backend/app/api/imports.py`
- `backend/app/application/ecd_import_service.py`
- `backend/app/repositories/ecd_imports.py`
- `backend/app/schemas/imports.py`
- `backend/tests/`
- `frontend/src/api/declared.ts`
- `frontend/src/routes/ImportEcdPage.tsx`
- `frontend/src/App.tsx`
- `frontend/e2e/`

## Criterios De Aceite

- Enviar ECD ja importada nao gera erro generico de persistencia.
- O usuario recebe informacao clara de que o arquivo ja existe.
- O usuario consegue abrir a analise existente a partir da UI.
- O usuario consegue remover explicitamente a importacao existente.
- A remocao apaga dados normalizados e snapshots dependentes de forma transacional.
- Depois da remocao, o mesmo ECD pode ser importado novamente.
- Nenhum arquivo ECD bruto e salvo ou exposto para download.
- Valores contabeis continuam usando `Decimal`.
- Frontend nao recalcula regra de negocio.

## Validacao Esperada

- Executar testes backend via `docker compose`.
- Executar testes frontend via `docker compose`.
- Executar E2E Playwright via Docker Compose quando aplicavel.
- Validar manualmente, em testes separados, `ECD 2024 DATAPACK.txt` e `ECD 2024 INVENTCLOUD.txt`.
- Conferir ausencia de `float` em arquivos alterados.

## Riscos

- Risco: remocao apagar dados de analise indevidos.
  Mitigacao: escopo transacional por `analysis_id`/`ecd_file_id`, testes de contagem e confirmacao explicita na UI.

- Risco: reimportacao silenciosa esconder estado existente.
  Mitigacao: retornar conflito orientado e exigir remocao explicita antes de novo envio.

- Risco: expor ECD bruta sensivel.
  Mitigacao: manter apenas metadados e dados normalizados ja previstos, sem download do arquivo bruto.

## Bloqueios Pendentes

Nenhum.
