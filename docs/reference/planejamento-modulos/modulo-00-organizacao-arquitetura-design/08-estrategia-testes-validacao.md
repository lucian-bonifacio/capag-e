# 08 - Estrategia de testes e validacao

## Objetivo

Definir uma estrategia oficial de testes e validacao para a nova organizacao do sistema.

## Ponto de decisao

Decidir quais validacoes serao obrigatorias por tipo de mudanca.

## Arquivos correlatos

- `tests/unit/`
- `tests/integration/`
- `tests/golden/`
- `tests/fixtures/`
- `tests/design-previews/`
- `web/package.json`
- `pyproject.toml`
- `docs/specs/spec-02-ingestao-validacao-normalizacao-ecd.md`
- `docs/specs/spec-04-motor-calculo-plr-capag-auditoria-pendencias.md`
- `docs/specs/spec-05-exportacao-excel.md`
- `.agents/skills/testing/SKILL.md`
- `.claude/skills/testing/SKILL.md`

## Detalhamento

- Definir testes por camada:
  - `io`: parser, reader, normalizador e fixtures ECD;
  - `domain`: estados, invariantes, FCO, sessoes;
  - `engine`: PLR, FCO, CAPAG, auditoria, metodologia;
  - `api`: contratos, rotas, serializacao e erros;
  - `export`: workbook Excel e golden tests;
  - `frontend`: build, navegacao, componentes criticos e validacao visual;
  - `docs`: consistencia de estrutura quando aplicavel.
- Definir comandos padrao:
  - `.venv/bin/python -m pytest`;
  - `.venv/bin/python -m pytest <tests relevantes>`;
  - `cd web && npm run build`.
- Definir quando validacao visual e obrigatoria:
  - mudancas em layout;
  - rotas React;
  - grids;
  - drill-downs;
  - estados vazios/erro.
- Definir quando previews em `tests/design-previews/` devem ser criados.
- Definir que ausencia de teste deve ser justificada na task/worklog.

## Entregavel

Spec ou documento de estrategia de testes e validacao.

## Criterios de sucesso

- Cada tipo de mudanca tem validacao proporcional definida.
- Tasks futuras nao ficam ambiguas sobre quais testes rodar.
- Skills de testing podem ser atualizadas com base nesse documento.

## Fora do escopo

- Criar testes agora.
- Rodar suite completa agora.
- Alterar codigo funcional.

