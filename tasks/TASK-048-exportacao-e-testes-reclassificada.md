# TASK-048 - Exportacao e testes da camada reclassificada

## SPEC De Origem

- `specs/SPEC-003-modulo-2-capag-reclassificada.md`

## Dependencias

- `TASK-046-criar-api-camada-reclassificada.md`
- `TASK-047-criar-ui-revisao-reclassificada.md`

## Objetivo

Criar exportação comparativa da camada reclassificada e consolidar testes do módulo, preservando declarado, reclassificado, revisado, evidências, score e limitações.

## Fontes Usadas

- `docs/product/PRD.md`
- `docs/architecture.md`
- `specs/SPEC-003-modulo-2-capag-reclassificada.md`

## Escopo Exato

- Exportar comparação declarado vs reclassificado.
- Incluir score, confiança, revisão humana, status e limitações.
- Criar testes de normalização, perfil, score, salvaguardas, API e exportação.
- Garantir que exportação não recalcula regra.

## Fora De Escopo

- Gerar laudo final.
- Criar evidências formais do módulo 4.
- Calcular CAPAG-E final sem contrato aplicável.

## Passos Executaveis

1. Criar exportador comparativo sem recalculo.
2. Criar testes obrigatórios do módulo.
3. Validar via Docker Compose.

## Arquivos Ou Areas Provaveis

- `backend/app/export/`
- `backend/tests/`
- frontend apenas se ação de exportação já estiver prevista

## Criterios De Aceite

- Exportação preserva declarado e reclassificado.
- Limitações e status ficam visíveis.
- Testes cobrem falso positivo e revisão humana.

## Validacao Esperada

- Executar testes backend e build frontend via `docker compose`.

## Riscos

- Risco: exportação esconder cenário parcial.
  Mitigação: status e limitações obrigatórios.

## Bloqueios Pendentes

Bloqueada até API e UI reclassificadas existirem.
