# TASK-018 - Criar validacao de assets metodologicos minima

## SPEC De Origem

- `specs/SPEC-001-modulo-0-fundacao-governada.md`

## Dependencias

- `TASK-006-auditar-validacoes-minimas-do-projeto.md`
- `TASK-009-auditar-assets-metodologicos-e-versionamento.md`

Esta TASK so deve ser executada depois que a auditoria de assets metodologicos indicar estrutura ou convencao suficiente para uma validacao minima, sem depender de regras prudenciais funcionais.

## Objetivo

Criar uma validacao minima via Docker Compose para inventario e formato basico de assets metodologicos versionados, sem validar conteudo prudencial, formulas, arredondamento, golden cases ou regras de negocio.

## Fontes Usadas

- `docs/product/PRD.md`
- `docs/architecture.md`
- `specs/SPEC-001-modulo-0-fundacao-governada.md`
- log esperado de `logs/LOG-006-auditar-validacoes-minimas-do-projeto.md`
- log esperado de `logs/LOG-009-auditar-assets-metodologicos-e-versionamento.md`

## Escopo Exato

- Ler a auditoria de assets metodologicos antes de criar qualquer validacao.
- Criar validacao minima apenas se houver estrutura de assets definida ou lacuna explicitamente preparada por TASK anterior.
- Validar somente aspectos estruturais basicos, como:
  - existencia de diretorio esperado;
  - nomes de arquivos conforme convencao;
  - presenca de metadados minimos de versao quando definidos;
  - ausencia de arquivos temporarios indevidos.
- Integrar comando de validacao local somente se a TASK-006 indicar local apropriado.
- Documentar o comando de validacao via `docker compose`, se necessario.

## Fora De Escopo

- Criar assets metodologicos.
- Alterar assets existentes.
- Validar regras prudenciais.
- Validar formulas.
- Validar arredondamento.
- Criar golden cases.
- Criar fixtures contabeis.
- Criar motor de calculo.
- Criar modelos de banco para metodologia.
- Criar migration.
- Criar `.venv` ou `node_modules` no host.
- Instalar dependencias no host.
- Alterar SPECs ou documentos governados.
- Atualizar `tasks/README.md`.

## Passos Executaveis

1. Ler `logs/LOG-006-auditar-validacoes-minimas-do-projeto.md`.
2. Ler `logs/LOG-009-auditar-assets-metodologicos-e-versionamento.md`.
3. Confirmar que ha convencao suficiente para validacao estrutural minima.
4. Criar script ou teste de validacao estrutural minima.
5. Documentar comando de execucao quando necessario.
6. Validar que a validacao nao interpreta conteudo prudencial.
7. Validar que nenhum asset, SPEC, documento governado, migration, modelo ou engine foi alterado.

## Arquivos Ou Areas Provaveis

- script de validacao em local definido por auditoria anterior
- configuracao de teste ou comando minimo, se indicado pela TASK-006
- documentacao local de comando, se indicada pela auditoria

## Criterios De Aceite

- As TASKs 006 e 009 foram executadas antes desta TASK.
- Existe comando ou script de validacao estrutural minima de assets.
- A validacao nao cria nem altera assets.
- A validacao nao interpreta regra prudencial, formula, arredondamento ou golden case.
- O comando de validacao esta documentado quando necessario.
- O comando oficial usa `docker compose`.
- Nenhuma SPEC, documento governado, migration, modelo, engine ou fixture contabil e criado ou alterado.

## Validacao Esperada

- Executar o comando de validacao criado pela TASK.
- Executar `git diff --stat` e confirmar que as alteracoes estao restritas ao script/configuracao/documentacao minima permitida.
- Conferir manualmente que a validacao e estrutural e nao prudencial.

## Riscos

- Risco: validador estrutural virar validador metodologico sem SPEC funcional.
  Mitigacao: limitar a validacao a existencia, nomes e metadados basicos.

- Risco: criar ou modificar assets durante validacao.
  Mitigacao: validar em modo somente leitura.

- Risco: introduzir golden cases prematuramente.
  Mitigacao: bloquear golden cases ate SPEC funcional correspondente.

## Bloqueios Pendentes

Bloqueada ate a execucao das TASKs 006 e 009.

Permanece bloqueado qualquer trabalho que tente criar assets, alterar metodologia, validar regra prudencial, validar formula, definir arredondamento, criar golden cases, criar fixtures contabeis, criar migration ou criar engine durante esta TASK.
