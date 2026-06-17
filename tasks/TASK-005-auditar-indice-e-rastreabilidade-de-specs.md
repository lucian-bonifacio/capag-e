# TASK-005 - Auditar indice e rastreabilidade de SPECs

## SPEC De Origem

- `specs/SPEC-001-modulo-0-fundacao-governada.md`

## Dependencias

- `TASK-002-auditar-estrutura-minima-repositorio.md`

Esta TASK so deve ser executada depois que a TASK-002 registrar o estado geral da estrutura minima do repositorio.

## Objetivo

Auditar as SPECs existentes em `specs/`, verificar se cada uma possui fontes, escopo, criterios e bloqueios explicitos, e preparar a base para um indice oficial de rastreabilidade entre PRD, arquitetura, SPECs e TASKs.

## Fontes Usadas

- `docs/product/PRD.md`
- `docs/architecture.md`
- `specs/SPEC-001-modulo-0-fundacao-governada.md`
- arquivos existentes em `specs/`
- relatorio esperado de `tasks/reports/TASK-002-auditoria-estrutura-minima.md`

## Escopo Exato

- Listar todas as SPECs existentes em `specs/`.
- Verificar se cada SPEC declara:
  - objetivo tecnico;
  - fontes usadas;
  - escopo;
  - fora de escopo;
  - decisoes pendentes;
  - contratos;
  - criterios de aceite;
  - validacao esperada;
  - riscos;
  - bloqueios.
- Classificar cada SPEC quanto a suficiencia para gerar TASKs:
  - suficiente para TASK;
  - suficiente com restricoes;
  - bloqueada;
  - precisa revisao documental.
- Registrar lacunas em relatorio documental.
- Sugerir proximas TASKs pequenas para criar ou ajustar indice oficial de SPECs.

## Fora De Escopo

- Alterar qualquer arquivo em `specs/`.
- Criar ou revisar conteudo tecnico das SPECs.
- Criar TASKs funcionais derivadas das SPECs auditadas.
- Resolver decisoes pendentes.
- Definir contratos de API.
- Definir regra de dominio, formula prudencial, arredondamento ou golden cases.
- Atualizar `tasks/README.md`.

## Passos Executaveis

1. Ler `tasks/reports/TASK-002-auditoria-estrutura-minima.md`.
2. Listar arquivos em `specs/`.
3. Para cada SPEC, conferir a presenca dos campos exigidos pela SPEC-001.
4. Registrar achados em `tasks/reports/TASK-005-auditoria-specs.md`.
5. Classificar cada SPEC quanto a suficiencia para gerar TASKs.
6. Registrar bloqueios sem tentar resolve-los.
7. Sugerir proximas TASKs pequenas para lacunas encontradas.
8. Validar que nenhum arquivo em `specs/` foi alterado durante a execucao.

## Arquivos Ou Areas Provaveis

- `tasks/reports/TASK-005-auditoria-specs.md`
- `specs/` apenas para leitura
- `docs/product/PRD.md` apenas para leitura
- `docs/architecture.md` apenas para leitura

## Criterios De Aceite

- Existe relatorio em `tasks/reports/TASK-005-auditoria-specs.md`.
- O relatorio lista todas as SPECs existentes em `specs/`.
- Cada SPEC listada possui classificacao objetiva de suficiencia para TASK.
- Lacunas e bloqueios sao registrados sem correcao nesta TASK.
- O relatorio nao altera, reinterpreta ou substitui contratos das SPECs.
- Nenhum arquivo em `specs/` e alterado.
- Nenhuma TASK funcional e criada durante esta auditoria.

## Validacao Esperada

- Executar `test -f tasks/reports/TASK-005-auditoria-specs.md`.
- Executar `git diff --stat` e confirmar que a execucao alterou apenas `tasks/reports/TASK-005-auditoria-specs.md`.
- Conferir manualmente que nenhum arquivo em `specs/` foi alterado.
- Conferir manualmente que o relatorio nao decide regra de dominio, contrato de API, formula prudencial ou politica de arredondamento.

## Riscos

- Risco: auditoria virar revisao tecnica das SPECs.
  Mitigacao: limitar a TASK a presenca de campos, suficiencia documental e bloqueios declarados.

- Risco: classificar SPEC incompleta como suficiente por conveniencia.
  Mitigacao: exigir bloqueio quando faltar contrato, criterio verificavel ou decisao essencial.

- Risco: criar TASK funcional antes da rastreabilidade estar clara.
  Mitigacao: sugerir TASKs futuras pequenas e manter esta TASK apenas documental.

## Bloqueios Pendentes

Bloqueada ate a execucao da TASK-002.

Permanece bloqueado qualquer trabalho que tente alterar SPECs, resolver decisoes pendentes ou criar TASK funcional durante esta auditoria.
