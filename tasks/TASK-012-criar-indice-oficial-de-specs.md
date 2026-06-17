# TASK-012 - Criar indice oficial de SPECs

## SPEC De Origem

- `specs/SPEC-001-modulo-0-fundacao-governada.md`

## Dependencias

- `TASK-005-auditar-indice-e-rastreabilidade-de-specs.md`

Esta TASK so deve ser executada depois que a TASK-005 auditar todas as SPECs existentes e classificar sua suficiencia para gerar TASKs.

## Objetivo

Criar um indice oficial das SPECs em `specs/`, registrando status, modulo, fontes principais, dependencias, bloqueios e relacao com TASKs, sem alterar o conteudo tecnico das SPECs.

## Fontes Usadas

- `docs/product/PRD.md`
- `docs/architecture.md`
- `specs/SPEC-001-modulo-0-fundacao-governada.md`
- relatorio esperado de `tasks/reports/TASK-005-auditoria-specs.md`

## Escopo Exato

- Criar `specs/README.md`.
- Listar todas as SPECs existentes em `specs/`.
- Para cada SPEC, registrar:
  - codigo;
  - titulo;
  - modulo;
  - status documental;
  - suficiencia para TASK;
  - fontes principais;
  - dependencias conhecidas;
  - bloqueios declarados;
  - TASKs derivadas existentes.
- Registrar regra de que `docs/reference/` nao e fonte normativa direta para TASKs, salvo autorizacao explicita ou incorporacao em documento governado.
- Registrar que SPEC insuficiente nao deve gerar TASK funcional.

## Fora De Escopo

- Alterar qualquer SPEC.
- Resolver bloqueios ou decisoes pendentes.
- Criar TASK funcional.
- Criar ou alterar arquitetura.
- Criar contrato de API.
- Definir regra de dominio, formula prudencial, arredondamento ou golden cases.
- Alterar `tasks/README.md`.
- Implementar codigo.

## Passos Executaveis

1. Ler `tasks/reports/TASK-005-auditoria-specs.md`.
2. Listar as SPECs existentes em `specs/`.
3. Criar `specs/README.md`.
4. Preencher o indice com uma linha por SPEC.
5. Registrar status e bloqueios conforme relatorio da TASK-005.
6. Registrar TASKs derivadas existentes, sem criar novas TASKs nesta execucao.
7. Validar que nenhuma SPEC foi alterada.

## Arquivos Ou Areas Provaveis

- `specs/README.md`
- `specs/` apenas para leitura, exceto o README criado nesta TASK
- `tasks/` apenas para leitura

## Criterios De Aceite

- `specs/README.md` existe.
- O README lista todas as SPECs existentes.
- Cada SPEC possui status documental e suficiencia para TASK.
- Bloqueios declarados sao visiveis no indice.
- TASKs derivadas existentes sao referenciadas quando aplicavel.
- O README declara que SPEC insuficiente nao gera TASK funcional.
- Nenhum arquivo de SPEC e alterado.
- Nenhuma TASK funcional e criada durante esta TASK.

## Validacao Esperada

- Executar `test -f specs/README.md`.
- Executar `git diff --stat` e confirmar que a execucao alterou apenas `specs/README.md`.
- Conferir manualmente que nenhuma SPEC foi alterada.
- Conferir manualmente que o README nao resolve bloqueios nem cria contrato funcional.

## Riscos

- Risco: o indice virar fonte normativa paralela.
  Mitigacao: declarar que o indice resume status e rastreabilidade, mas nao substitui as SPECs.

- Risco: marcar SPEC incompleta como suficiente.
  Mitigacao: usar a classificacao do relatorio da TASK-005 e registrar bloqueios explicitamente.

- Risco: criar TASK funcional a partir do indice sem revisar a SPEC.
  Mitigacao: exigir referencia direta a SPEC suficiente em toda TASK derivada.

## Bloqueios Pendentes

Bloqueada ate a execucao da TASK-005.

Permanece bloqueado qualquer trabalho que tente alterar SPECs, resolver decisoes pendentes, criar TASK funcional ou implementar codigo durante esta TASK.
