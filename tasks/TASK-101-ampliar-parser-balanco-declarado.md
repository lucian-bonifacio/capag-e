# TASK-101 - Ampliar parser do balanço declarado

## SPEC De Origem

- `specs/SPEC-012-modulo-1c-balanco-patrimonial-declarado.md`

## Dependencias

- `TASK-041C-criar-fixtures-ecd-governadas.md`
- `TASK-041D-implementar-parser-ecd-declarado.md`

## Objetivo

Ampliar o parser da ECD para normalizar todos os registros e campos necessários
à obrigatoriedade, construção e conciliação do Balanço Patrimonial declarado,
sem persistir dados nem aplicar regra prudencial.

## Fontes Usadas

- `docs/product/PRD.md`
- `docs/architecture/architecture.md`
- `specs/SPEC-002-modulo-1-camada-declarada.md`
- `specs/SPEC-012-modulo-1c-balanco-patrimonial-declarado.md`
- `docs/methodology/pesquisa-oficial-balanco-patrimonial-ecd.md`
- `tasks/TASK-041C-criar-fixtures-ecd-governadas.md`
- `tasks/TASK-041D-implementar-parser-ecd-declarado.md`

## Escopo Exato

- Parsear `I010`, `I030`, `I052`, `I150`, `J005` e presença de `J150`.
- Preservar os campos necessários do `0000`, incluindo período.
- Associar `I052` à conta `I050` pai.
- Associar `I155` ao período `I150` e preservar `COD_CCUS`.
- Associar `J100` e `J150` ao `J005` pai.
- Normalizar todos os campos do `J100` definidos na `SPEC-012`.
- Separar explicitamente saldo inicial e saldo final do `J100`.
- Usar nomes de domínio próprios para `COD_AGL`, sem tratá-lo como código de
  conta.
- Preservar número e texto original de cada linha.
- Manter valores contábeis em `Decimal`.
- Criar fixtures sintéticas focadas nos novos registros e campos.

## Fora De Escopo

- Criar migration ou persistência.
- Salvar o arquivo ECD original.
- Determinar obrigatoriedade do Bloco J.
- Construir ou conciliar o balanço.
- Alterar API ou frontend.
- Inferir `I051`, `I052`, hierarquia ou código.
- Aplicar metodologia PLRA/CAPAG-E.

## Passos Executaveis

1. Refinar os contratos intermediários do parser.
2. Implementar o contexto de registros pais `I050`, `I150` e `J005`.
3. Implementar o parsing dos novos registros.
4. Corrigir o parsing completo do `J100`.
5. Preservar centro de custo e períodos aplicáveis.
6. Criar fixtures de casos válidos e inválidos.
7. Criar testes unitários por registro e por encadeamento.

## Arquivos Ou Areas Provaveis

- `backend/app/io/ecd_parser.py`
- `backend/app/io/`
- `backend/tests/`
- `backend/tests/fixtures/`

## Criterios De Aceite

- Parser retorna `I010`, `I030`, `I052`, `I150`, `J005`, `J100` e presença
  de `J150`.
- `I052` preserva conta pai, `COD_CCUS` e `COD_AGL`.
- `I155` preserva período e centro de custo.
- `J100` preserva hierarquia, grupo, tipo, valores inicial/final e indicadores.
- `VL_CTA_FIN` não é confundido com `VL_CTA_INI`.
- `COD_AGL` não é exposto como `account_code`.
- Linhas originais continuam auditáveis.
- Nenhum valor contábil usa `float`.
- Parser não executa regra prudencial.

## Validacao Esperada

- Executar testes backend focados via `docker compose`.
- Executar a suíte backend aplicável via `docker compose`.
- Validar fixtures com saldo inicial diferente do final.
- Validar fixture com `COD_AGL` diferente de `COD_CTA`.
- Conferir ausência de `float` nos arquivos alterados.

## Riscos

- Risco: perder o vínculo entre registros filhos e pais.
  Mitigação: manter contexto explícito e testes de encadeamento.
- Risco: preservar a nomenclatura incorreta do parser atual.
  Mitigação: separar contratos de conta contábil e código de aglutinação.
- Risco: misturar parsing e validação de domínio.
  Mitigação: limitar a TASK à leitura e normalização.

## Bloqueios Pendentes

Nenhum.

