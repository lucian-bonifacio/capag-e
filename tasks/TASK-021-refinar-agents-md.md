# TASK-021 - Refinar AGENTS.md

## SPEC De Origem

- `specs/SPEC-001-modulo-0-fundacao-governada.md`

## Dependencias

- `TASK-005-auditar-indice-e-rastreabilidade-de-specs.md`
- `TASK-006-auditar-validacoes-minimas-do-projeto.md`
- `TASK-007-auditar-documentos-operacionais-e-agentes.md`

Esta TASK so deve ser executada depois que os documentos operacionais forem auditados e houver log indicando ajustes necessarios no `AGENTS.md`.

## Objetivo

Refinar `AGENTS.md` para refletir o fluxo governado do projeto, as fontes obrigatorias, as regras de criacao de SPECs e TASKs, as validacoes esperadas e as proibicoes de implementacao sem SPEC suficiente.

## Fontes Usadas

- `docs/product/PRD.md`
- `docs/architecture/architecture.md`
- `specs/SPEC-001-modulo-0-fundacao-governada.md`
- `tasks/README.md`
- log esperado de `logs/LOG-005-auditar-indice-e-rastreabilidade-de-specs.md`
- log esperado de `logs/LOG-006-auditar-validacoes-minimas-do-projeto.md`
- log esperado de `logs/LOG-007-auditar-documentos-operacionais-e-agentes.md`

## Escopo Exato

- Atualizar `AGENTS.md` apenas com regras ja aprovadas em PRD, arquitetura, SPEC-001 e logs das TASKs dependentes.
- Reforcar o fluxo `PRD -> Arquitetura -> SPEC -> TASK`.
- Registrar que TASK nao deve ser implementada durante o processo de criacao de TASKs.
- Registrar que TASK deve ser pequena, verificavel e derivada de SPEC suficiente.
- Registrar que o ambiente oficial e exclusivamente Docker/Docker Compose.
- Registrar proibicao de `.venv`, `node_modules` no host e instalacao global/local fora de container.
- Registrar fontes obrigatorias para SPECs e TASKs.
- Registrar documentos governados de frontend quando o escopo envolver UI.
- Registrar bloqueios para regra prudencial, contrato de API, formula, arredondamento, padrao visual e estrategia critica de teste sem SPEC suficiente.
- Registrar validacoes esperadas conforme maturidade do projeto.

## Fora De Escopo

- Alterar PRD.
- Alterar arquitetura.
- Alterar SPECs.
- Alterar TASKs existentes.
- Alterar `tasks/README.md`.
- Alterar skills, plugins ou configuracoes do Codex.
- Criar ou executar codigo.
- Criar testes, CI, backend, frontend, assets ou migrations.
- Definir nova regra de dominio, formula, arredondamento ou contrato de API.

## Passos Executaveis

1. Ler os logs das TASKs 005, 006 e 007.
2. Ler `AGENTS.md` atual.
3. Identificar desalinhamentos registrados no log da TASK-007.
4. Atualizar `AGENTS.md` de forma restrita aos pontos aprovados.
5. Garantir que as instrucoes nao contradizem PRD, arquitetura, SPEC-001 ou `tasks/README.md`.
6. Garantir que `AGENTS.md` nao cria regra tecnica nova.
7. Validar que nenhum arquivo alem de `AGENTS.md` foi alterado.

## Arquivos Ou Areas Provaveis

- `AGENTS.md`

## Criterios De Aceite

- As TASKs 005, 006 e 007 foram executadas antes desta TASK.
- `AGENTS.md` reflete o fluxo `PRD -> Arquitetura -> SPEC -> TASK`.
- `AGENTS.md` declara que criacao de TASK nao implica execucao da TASK.
- `AGENTS.md` exige TASKs pequenas, verificaveis e derivadas de SPEC suficiente.
- `AGENTS.md` registra ambiente oficial Docker-only.
- `AGENTS.md` proibe `.venv`, `node_modules` no host e instalacao global/local fora de container.
- `AGENTS.md` cita fontes obrigatorias aplicaveis.
- `AGENTS.md` preserva bloqueios para decisoes tecnicas, contratos, regras prudenciais, formulas, arredondamento, padroes visuais e testes criticos.
- Nenhum arquivo alem de `AGENTS.md` e alterado.
- Nenhuma regra nova e introduzida sem fonte governada.

## Validacao Esperada

- Executar `git diff -- AGENTS.md` e revisar se as mudancas sao apenas instrucionais.
- Executar `git diff --stat` e confirmar que a execucao alterou apenas `AGENTS.md`.
- Conferir manualmente que `AGENTS.md` nao contradiz PRD, arquitetura, SPEC-001 ou `tasks/README.md`.

## Riscos

- Risco: `AGENTS.md` virar fonte normativa acima das SPECs.
  Mitigacao: declarar que ele orienta agentes, mas nao substitui PRD, arquitetura ou SPECs.

- Risco: introduzir regra tecnica nova por conveniencia.
  Mitigacao: limitar alteracoes a regras ja aprovadas ou lacunas registradas nos logs.

- Risco: agentes voltarem a implementar TASKs durante a criacao.
  Mitigacao: incluir regra explicita separando criacao de TASK e execucao de TASK.

## Bloqueios Pendentes

Bloqueada ate a execucao das TASKs 005, 006 e 007.

Permanece bloqueado qualquer trabalho que tente alterar PRD, arquitetura, SPECs, TASKs, skills, plugins, configs, codigo, testes, CI, backend, frontend, assets ou migrations durante esta TASK.
