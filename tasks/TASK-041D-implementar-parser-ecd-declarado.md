# TASK-041D - Implementar parser ECD declarado

## SPEC De Origem

- `specs/SPEC-002-modulo-1-camada-declarada.md`

## Dependencias

- `TASK-041C-criar-fixtures-ecd-governadas.md`

## Objetivo

Implementar leitor/parser da ECD para os registros minimos da camada declarada, preservando dados originais e normalizando valores com `Decimal`.

## Fontes Usadas

- `docs/product/PRD.md`
- `docs/architecture/architecture.md`
- `specs/SPEC-002-modulo-1-camada-declarada.md`
- `tasks/TASK-041C-criar-fixtures-ecd-governadas.md`

## Escopo Exato

- Ler arquivo ECD em texto e detectar/aceitar encoding previsto.
- Parsear registros `I050`, `I051`, `I155`, `I200`, `I250` e `J100`.
- Preservar linha original e numero de linha quando aplicavel.
- Normalizar valores contabeis para `Decimal`.
- Retornar estrutura intermediaria sem aplicar metodologia prudencial.
- Criar testes com fixtures governadas.

## Fora De Escopo

- Persistir no banco.
- Executar camada declarada.
- Inferir regra metodologica.
- Reclassificar conta por comportamento.

## Passos Executaveis

1. Criar modulo de parser em `backend/app/io/`.
2. Implementar parsing dos registros minimos.
3. Implementar normalizacao decimal e tratamento de erros.
4. Criar testes por fixture e por registro.

## Arquivos Ou Areas Provaveis

- `backend/app/io/`
- `backend/tests/`
- `backend/tests/fixtures/`

## Criterios De Aceite

- Parser extrai `I050`, `I051`, `I155`, `I200`, `I250` e `J100`.
- Valores sao `Decimal`, nunca `float`.
- Parser nao aplica metodologia nem regra prudencial.

## Validacao Esperada

- Executar testes backend via `docker compose`.
- Conferir ausencia de `float` em parser e testes.

## Riscos

- Risco: misturar parse com regra de dominio.
  Mitigacao: limitar parser a leitura, normalizacao e estrutura intermediaria.

## Bloqueios Pendentes

Bloqueada ate fixtures governadas existirem.
