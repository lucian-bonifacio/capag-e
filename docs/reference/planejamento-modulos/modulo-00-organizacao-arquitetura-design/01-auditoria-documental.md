# 01 - Auditoria documental

## Objetivo

Auditar a documentacao existente para identificar conflitos, documentos defasados e fontes de verdade concorrentes.

## Ponto de decisao

Decidir qual sera a ordem oficial de precedencia documental.

## Arquivos correlatos

- `README.md`
- `AGENTS.md`
- `CLAUDE.md`
- `docs/product/prd-v2-formulario-unico.md`
- `docs/specs/`
- `docs/reference/`
- `tasks/`
- `.agents/skills/`
- `.claude/skills/`

## Detalhamento

- Identificar divergencias entre `README.md`, `AGENTS.md` e `CLAUDE.md`.
- Identificar specs que descrevem comportamento implementado.
- Identificar specs que descrevem evolucao futura.
- Identificar documentos de `docs/reference/` que precisam virar specs oficiais.
- Identificar tasks que apontam para comportamento superado.
- Registrar se o termo `condicional` ainda aparece como bloqueante em documentos onde isso nao representa mais o estado desejado.

## Entregavel

Um diagnostico de conflitos documentais e recomendacao de precedencia.

## Criterios de sucesso

- O projeto sabe quais documentos obedecer primeiro.
- Documentos conceituais deixam de competir com specs oficiais.
- Nao ha alteracao funcional.

