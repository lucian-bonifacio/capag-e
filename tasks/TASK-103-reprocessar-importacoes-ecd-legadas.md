# TASK-103 - Reprocessar importações ECD legadas

## SPEC De Origem

- `specs/SPEC-012-modulo-1c-balanco-patrimonial-declarado.md`

## Dependencias

- `TASK-041M-gerenciar-importacoes-ecd-existentes.md`
- `TASK-102-persistir-ecd-balanco-declarado.md`

## Objetivo

Implementar o reenvio e reprocessamento controlado de importações anteriores
que não preservaram o arquivo original ou os registros exigidos pela
`SPEC-012`, sem fabricar dados nem perder identificadores.

## Fontes Usadas

- `docs/product/PRD.md`
- `docs/architecture/architecture.md`
- `specs/SPEC-012-modulo-1c-balanco-patrimonial-declarado.md`
- `tasks/TASK-041M-gerenciar-importacoes-ecd-existentes.md`
- `tasks/TASK-102-persistir-ecd-balanco-declarado.md`

## Escopo Exato

- Identificar importações anteriores incompletas como
  `REIMPORTACAO_NECESSARIA`.
- Permitir reenvio do mesmo arquivo quando o hash corresponder a uma
  importação incompleta.
- Manter `409 ECD_ALREADY_IMPORTED` para importação já completa.
- Persistir o arquivo original e os novos registros somente após parse válido.
- Substituir os dados normalizados antigos de forma atômica.
- Preservar identificadores da empresa, arquivo, análise e exercício.
- Registrar `parser_version`, data e resultado do reprocessamento.
- Invalidar resultados derivados da versão normalizada anterior.
- Retornar `200` e `reprocessed = true` no reprocessamento bem-sucedido.
- Preservar `201` e `reprocessed = false` para arquivo novo.
- Criar testes de sucesso, conflito e rollback.

## Fora De Escopo

- Inferir registros ausentes sem reenvio.
- Alterar manualmente o arquivo original.
- Criar o motor do balanço.
- Alterar metodologia PLRA/CAPAG-E.
- Criar interface específica de reprocessamento.
- Alterar limite de upload.

## Passos Executaveis

1. Definir a detecção objetiva de importação anterior incompleta.
2. Ajustar o caso de uso de importação para o mesmo hash elegível.
3. Implementar substituição transacional dos dados normalizados.
4. Invalidar resultados derivados conforme contratos existentes.
5. Ajustar resposta e conflitos da API de importação.
6. Criar testes de reprocessamento e rollback.
7. Validar que importação completa continua protegida contra duplicidade.

## Arquivos Ou Areas Provaveis

- `backend/app/api/imports.py`
- `backend/app/application/ecd_import_service.py`
- `backend/app/repositories/`
- `backend/app/schemas/imports.py`
- `backend/tests/`

## Criterios De Aceite

- Importação antiga incompleta é identificada sem inferência.
- Mesmo hash incompleto pode ser completado por reenvio.
- Mesmo hash completo continua retornando conflito.
- Identificadores existentes são preservados.
- Dados antigos só são substituídos após sucesso integral.
- Erro de parse ou persistência mantém a versão anterior intacta.
- Resultados derivados ficam invalidados após reprocessamento.
- Resposta distingue importação nova de reprocessamento.
- Nenhum snapshot é criado por consulta.

## Validacao Esperada

- Executar testes backend via `docker compose`.
- Validar reprocessamento bem-sucedido e rollback.
- Validar conflito de importação completa.
- Validar invalidação de resultados derivados.
- Conferir ausência de `float` nos arquivos alterados.

## Riscos

- Risco: perder análise existente durante o reprocessamento.
  Mitigação: substituir dados somente dentro de transação concluída.
- Risco: aceitar arquivo diferente como reprocessamento.
  Mitigação: exigir igualdade exata do SHA-256.
- Risco: manter resultado calculado sobre dados antigos.
  Mitigação: invalidar dependências na mesma transação.

## Bloqueios Pendentes

Bloqueada até a conclusão da `TASK-102`.

