# TASK-022 - Refinar TODOLIST.md

## SPEC De Origem

- `specs/SPEC-001-modulo-0-fundacao-governada.md`

## Dependencias

- `TASK-007-auditar-documentos-operacionais-e-agentes.md`
- `TASK-012-criar-indice-oficial-de-specs.md`

Esta TASK so deve ser executada depois que os documentos operacionais forem auditados e o indice oficial de SPECs estiver criado ou explicitamente dispensado.

## Objetivo

Refinar `TODOLIST.md` para refletir o estado governado do projeto, separando marcos documentais, criacao de TASKs, execucao de TASKs, implementacao, testes, revisao e entrega sem misturar configuracoes locais ou notas temporarias.

## Fontes Usadas

- `docs/product/PRD.md`
- `docs/architecture/architecture.md`
- `specs/SPEC-001-modulo-0-fundacao-governada.md`
- `tasks/README.md`
- log esperado de `logs/LOG-007-auditar-documentos-operacionais-e-agentes.md`
- `specs/README.md`, se criado pela TASK-012

## Escopo Exato

- Atualizar `TODOLIST.md` apenas como checklist operacional de alto nivel.
- Separar claramente:
  - documentos governados concluidos;
  - criacao de TASKs;
  - execucao de TASKs;
  - implementacao;
  - testes;
  - revisao;
  - entrega;
  - aprendizados.
- Remover ou mover para TASK futura notas de configuracao local que nao pertencem ao `TODOLIST.md`, se a auditoria indicar essa lacuna.
- Registrar que a criacao de TASKs nao implica execucao.
- Registrar que execucao deve seguir TASKs pequenas e dependencias explicitas.

## Fora De Escopo

- Alterar `AGENTS.md`.
- Alterar `tasks/README.md`.
- Alterar SPECs.
- Alterar PRD ou arquitetura.
- Alterar configuracao real do Codex.
- Criar ou executar TASKs.
- Implementar codigo.
- Criar testes, CI, backend, frontend, assets ou migrations.
- Resolver pendencias tecnicas.

## Passos Executaveis

1. Ler `logs/LOG-007-auditar-documentos-operacionais-e-agentes.md`.
2. Ler `TODOLIST.md` atual.
3. Identificar conteudo que deve permanecer como checklist operacional.
4. Identificar conteudo que deve sair do `TODOLIST.md` por ser configuracao local, nota historica ou material temporario.
5. Atualizar `TODOLIST.md` de forma restrita.
6. Garantir que o arquivo nao passa a decidir arquitetura, regras ou contratos.
7. Validar que nenhum arquivo alem de `TODOLIST.md` foi alterado.

## Arquivos Ou Areas Provaveis

- `TODOLIST.md`

## Criterios De Aceite

- A TASK-007 foi executada antes desta TASK.
- `TODOLIST.md` apresenta checklist operacional claro.
- `TODOLIST.md` separa criacao de TASKs e execucao de TASKs.
- `TODOLIST.md` nao contem configuracao local sensivel ou instrucoes tecnicas que pertençam a documento proprio.
- `TODOLIST.md` nao substitui PRD, arquitetura, SPECs, TASKs ou `AGENTS.md`.
- Nenhum arquivo alem de `TODOLIST.md` e alterado.

## Validacao Esperada

- Executar `git diff -- TODOLIST.md` e revisar se as mudancas sao apenas organizacionais.
- Executar `git diff --stat` e confirmar que a execucao alterou apenas `TODOLIST.md`.
- Conferir manualmente que `TODOLIST.md` nao define regra tecnica, contrato funcional, configuracao secreta ou decisao arquitetural.

## Riscos

- Risco: `TODOLIST.md` virar fonte normativa paralela.
  Mitigacao: manter apenas checklist de estado e proximos marcos.

- Risco: remover nota historica ainda util sem rastreabilidade.
  Mitigacao: mover somente quando a auditoria indicar destino ou TASK futura.

- Risco: confundir criacao de TASK com execucao de TASK.
  Mitigacao: declarar separacao explicita entre esses marcos.

## Bloqueios Pendentes

Bloqueada ate a execucao da TASK-007 e ate a execucao ou dispensa explicita da TASK-012.

Permanece bloqueado qualquer trabalho que tente alterar documentos governados, configs reais, SPECs, TASKs, codigo, testes, CI, backend, frontend, assets ou migrations durante esta TASK.
