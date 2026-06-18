# TASK-001 - Criar indice e convencao de TASKs

## SPEC De Origem

- `specs/SPEC-001-modulo-0-fundacao-governada.md`

## Objetivo

Criar a base documental minima para as TASKs oficiais do CAPAG, estabelecendo um indice inicial, convencao de nomes, campos obrigatorios e rastreabilidade entre `PRD`, arquitetura, SPECs e TASKs.

## Fontes Usadas

- `docs/product/PRD.md`
- `docs/architecture/architecture.md`
- `specs/SPEC-001-modulo-0-fundacao-governada.md`
- `AGENTS.md`

## Escopo Exato

- Criar um documento indice em `tasks/README.md`.
- Definir convencao de numeracao e nomes para TASKs.
- Definir o template obrigatorio de uma TASK conforme contrato da SPEC-001.
- Registrar que TASK nasce apenas de SPEC suficiente.
- Registrar bloqueios para TASKs que tentem decidir arquitetura, API, regra de dominio, formula prudencial, politica de arredondamento, padrao visual ou estrategia critica de teste.
- Registrar a primeira TASK criada neste arquivo no indice.

## Fora De Escopo

- Implementar backend, frontend, banco, migrations, API, engine, exportacao ou laudo.
- Criar endpoints funcionais.
- Criar telas ou componentes visuais.
- Definir regras prudenciais, formulas, arredondamento ou golden cases.
- Usar `docs/reference/` como fonte normativa direta para implementacao.
- Criar todas as TASKs dos modulos funcionais nesta etapa.

## Passos Executaveis

1. Criar `tasks/README.md`.
2. Incluir no README a regra de rastreabilidade `PRD -> Arquitetura -> SPEC -> TASK`.
3. Incluir convencao de nomes: `TASK-NNN-descricao-curta.md`.
4. Incluir template minimo de TASK com os campos exigidos pela SPEC-001.
5. Incluir secao de bloqueios obrigatorios.
6. Registrar `TASK-001` no indice.
7. Validar que `tasks/README.md` e este arquivo existem.
8. Validar que nenhum arquivo de codigo funcional foi criado ou alterado por esta TASK.

## Arquivos Ou Areas Provaveis

- `tasks/README.md`
- `tasks/TASK-001-criar-indice-e-convencao-de-tasks.md`

## Criterios De Aceite

- `tasks/README.md` existe.
- `tasks/README.md` declara que TASK deve nascer de SPEC suficiente.
- `tasks/README.md` declara a rastreabilidade `PRD -> Arquitetura -> SPEC -> TASK`.
- `tasks/README.md` define a convencao `TASK-NNN-descricao-curta.md`.
- `tasks/README.md` contem template com:
  - SPEC de origem;
  - objetivo;
  - escopo exato;
  - fora de escopo;
  - passos executaveis;
  - arquivos ou areas provaveis;
  - criterios de aceite;
  - validacao esperada;
  - riscos;
  - bloqueios pendentes.
- `TASK-001` aparece no indice.
- Nenhuma implementacao funcional e criada nesta TASK.

## Validacao Esperada

- Executar `test -f tasks/README.md`.
- Executar `test -f tasks/TASK-001-criar-indice-e-convencao-de-tasks.md`.
- Executar `git diff --stat` e conferir que as mudancas estao restritas a `tasks/`.

## Riscos

- Risco: o indice virar substituto das SPECs.
  Mitigacao: registrar que a TASK sempre referencia SPEC suficiente e nao redefine contrato.

- Risco: criar TASKs amplas demais depois desta convencao.
  Mitigacao: template exige escopo exato, fora de escopo, criterios verificaveis e bloqueios.

- Risco: TASK funcional tentar decidir regra prudencial.
  Mitigacao: bloqueio explicito no README e nas TASKs derivadas.

## Bloqueios Pendentes

Nao ha bloqueio para executar esta TASK estrutural.

Permanece bloqueado qualquer trabalho que tente implementar funcionalidade, criar contrato de API, alterar regra prudencial, definir formula, definir arredondamento ou criar tela funcional sem SPEC suficiente correspondente.
