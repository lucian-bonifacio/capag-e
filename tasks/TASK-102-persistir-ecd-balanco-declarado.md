# TASK-102 - Persistir ECD e balanço declarado

## SPEC De Origem

- `specs/SPEC-012-modulo-1c-balanco-patrimonial-declarado.md`

## Dependencias

- `TASK-041B-criar-migrations-ecd-normalizada.md`
- `TASK-041E-persistir-ecd-normalizada.md`
- `TASK-041F-criar-importacao-ecd-oficial.md`
- `TASK-101-ampliar-parser-balanco-declarado.md`

## Objetivo

Criar migrations, modelos e persistência transacional para preservar o arquivo
ECD original e os registros normalizados necessários ao Balanço Patrimonial
declarado.

## Fontes Usadas

- `docs/product/PRD.md`
- `docs/architecture/architecture.md`
- `specs/SPEC-002-modulo-1-camada-declarada.md`
- `specs/SPEC-012-modulo-1c-balanco-patrimonial-declarado.md`
- `tasks/TASK-041B-criar-migrations-ecd-normalizada.md`
- `tasks/TASK-041E-persistir-ecd-normalizada.md`
- `tasks/TASK-041F-criar-importacao-ecd-oficial.md`
- `tasks/TASK-101-ampliar-parser-balanco-declarado.md`

## Escopo Exato

- Adicionar conteúdo binário original, tamanho, versão do parser e data de
  reprocessamento ao `EcdFile`.
- Persistir os bytes exatos usados para calcular o SHA-256.
- Criar tabelas ou estruturas relacionais para `I010`, `I030`, `I052`, `I150`,
  `J005` e presença mínima de `J150`.
- Completar a persistência do `J100` com todos os campos da `SPEC-012`.
- Relacionar `I052` ao `I050`, `I155` ao `I150` e `J100/J150` ao `J005`.
- Renomear o conceito persistido de `J100.COD_AGL` para código de aglutinação.
- Preservar número e texto original das linhas.
- Garantir persistência atômica do arquivo e dos registros normalizados.
- Ajustar exclusão confirmada para remover também o conteúdo original.
- Criar testes de migration, constraints, persistência e rollback.

## Fora De Escopo

- Reprocessar importações antigas.
- Implementar o motor de conciliação.
- Alterar o contrato público da API do balanço.
- Criar frontend.
- Alterar limite de upload.
- Criar download público do arquivo original.
- Criar snapshots de consulta.

## Passos Executaveis

1. Modelar as novas entidades e relacionamentos conforme a SPEC.
2. Criar migration Alembic compatível com os dados existentes.
3. Adaptar repositories e o caso de uso de persistência.
4. Passar os bytes originais ao fluxo transacional de importação.
5. Ajustar a exclusão confirmada da importação.
6. Criar testes de persistência, integridade e rollback.
7. Executar migration em PostgreSQL via Docker Compose.

## Arquivos Ou Areas Provaveis

- `backend/alembic/versions/`
- `backend/app/repositories/ecd_imports.py`
- `backend/app/application/ecd_import_service.py`
- `backend/app/api/imports.py`
- `backend/app/domain/imports.py`
- `backend/app/schemas/imports.py`
- `backend/tests/`

## Criterios De Aceite

- Bytes persistidos reproduzem exatamente o hash da importação.
- `EcdFile` registra tamanho, versão do parser e dados de reprocessamento.
- Novos registros normalizados podem ser consultados por análise e exercício.
- `J100` persiste saldo inicial e final em campos distintos.
- Relacionamentos formais preservam os pais dos registros.
- Migration não fabrica dados ausentes para importações antigas.
- Falha na persistência não deixa arquivo ou registros parciais.
- Exclusão confirmada remove o conteúdo original junto com a importação.
- Valores contábeis usam `Numeric/Decimal`, nunca `float`.

## Validacao Esperada

- Executar migrations em PostgreSQL via `docker compose`.
- Executar testes backend focados e suíte aplicável via `docker compose`.
- Validar rollback transacional.
- Recalcular o hash a partir dos bytes recuperados em teste.
- Conferir ausência de `float` nos arquivos alterados.

## Riscos

- Risco: migration interpretar dados antigos como completos.
  Mitigação: manter campos novos identificáveis e sem inferência.
- Risco: divergência entre bytes persistidos e hash.
  Mitigação: calcular e testar o hash sobre o conteúdo efetivamente salvo.
- Risco: persistência parcial.
  Mitigação: manter uma transação por importação.

## Bloqueios Pendentes

Bloqueada até a conclusão da `TASK-101`.

