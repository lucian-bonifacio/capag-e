# TASK-007 - Auditar documentos operacionais e agentes

## SPEC De Origem

- `specs/SPEC-001-modulo-0-fundacao-governada.md`

## Dependencias

- `TASK-002-auditar-estrutura-minima-repositorio.md`
- `TASK-005-auditar-indice-e-rastreabilidade-de-specs.md`
- `TASK-006-auditar-validacoes-minimas-do-projeto.md`

Esta TASK so deve ser executada depois que a estrutura minima, o estado das SPECs e as validacoes minimas estiverem auditados.

## Objetivo

Auditar documentos operacionais e instrucoes de agentes para identificar desalinhamentos com o PRD, a arquitetura e a SPEC-001, preparando TASKs futuras de refinamento sem alterar esses documentos nesta etapa.

## Fontes Usadas

- `docs/product/PRD.md`
- `docs/architecture/architecture.md`
- `specs/SPEC-001-modulo-0-fundacao-governada.md`
- `AGENTS.md`
- `TODOLIST.md`
- log esperado de `logs/LOG-002-auditar-estrutura-minima-repositorio.md`
- log esperado de `logs/LOG-005-auditar-indice-e-rastreabilidade-de-specs.md`
- log esperado de `logs/LOG-006-auditar-validacoes-minimas-do-projeto.md`

## Escopo Exato

- Auditar documentos operacionais existentes, incluindo:
  - `AGENTS.md`;
  - `TODOLIST.md`;
  - `README.md`, se existir;
  - outros documentos operacionais na raiz, se existirem.
- Verificar se esses documentos refletem:
  - fluxo `PRD -> Arquitetura -> SPEC -> TASK`;
  - proibicao de TASK sem SPEC suficiente;
  - separacao entre frontend, API, application, domain, IO, engine, repositories, export e report;
  - proibicao de regra prudencial no frontend, Excel ou laudo;
  - validacoes esperadas antes de implementacao;
  - necessidade de TASKs pequenas e verificaveis.
- Verificar se documentos operacionais registram Docker/Docker Compose como unico ambiente oficial.
- Verificar se documentos operacionais evitam instrucoes de `.venv`, `node_modules` no host ou instalacao global/local fora de container.
- Registrar lacunas e conflitos em log operacional.
- Propor proximas TASKs pequenas para refinamento de documentos operacionais.

## Fora De Escopo

- Alterar `AGENTS.md`.
- Alterar `TODOLIST.md`.
- Alterar `README.md` ou criar README.
- Alterar skills, plugins, configuracoes do Codex ou instrucoes externas.
- Criar ou alterar SPECs.
- Criar ou executar TASKs funcionais.
- Implementar backend, frontend, testes ou CI.
- Atualizar `tasks/README.md`.

## Passos Executaveis

1. Ler os logs das TASKs 002, 005 e 006.
2. Listar documentos operacionais existentes na raiz.
3. Ler `AGENTS.md` e `TODOLIST.md`.
4. Ler `README.md`, se existir.
5. Comparar os documentos com `docs/product/PRD.md`, `docs/architecture/architecture.md` e `SPEC-001`.
6. Criar log em `logs/LOG-007-auditar-documentos-operacionais-e-agentes.md`.
7. Registrar lacunas, conflitos e pontos defasados sem corrigi-los.
8. Sugerir proximas TASKs pequenas para refinamento documental.
9. Validar que nenhum documento operacional foi alterado durante a execucao.

## Arquivos Ou Areas Provaveis

- `logs/LOG-007-auditar-documentos-operacionais-e-agentes.md`
- `AGENTS.md` apenas para leitura
- `TODOLIST.md` apenas para leitura
- `README.md` apenas para leitura, se existir
- documentos operacionais da raiz apenas para leitura

## Criterios De Aceite

- Existe log em `logs/LOG-007-auditar-documentos-operacionais-e-agentes.md`.
- O log cita a SPEC de origem.
- O log lista os documentos operacionais auditados.
- O log identifica alinhamentos, lacunas e conflitos com PRD, arquitetura e SPEC-001.
- O log identifica se ha lacuna ou conflito sobre ambiente oficial Docker-only.
- O log sugere TASKs futuras pequenas para refinamento.
- Nenhum documento operacional e alterado.
- Nenhuma skill, plugin ou configuracao do Codex e alterada.

## Validacao Esperada

- Executar `test -f logs/LOG-007-auditar-documentos-operacionais-e-agentes.md`.
- Executar `git diff --stat` e confirmar que a execucao alterou apenas `logs/LOG-007-auditar-documentos-operacionais-e-agentes.md`.
- Conferir manualmente que `AGENTS.md`, `TODOLIST.md`, `README.md`, skills, plugins e configs nao foram alterados.

## Riscos

- Risco: auditoria virar refinamento imediato dos documentos.
  Mitigacao: registrar lacunas em log e propor TASKs futuras, sem editar documentos nesta TASK.

- Risco: documentos operacionais contradizerem fontes governadas.
  Mitigacao: registrar conflito e tratar PRD, arquitetura e SPECs como fontes superiores para a proxima TASK.

- Risco: criar uma TASK de refinamento ampla demais.
  Mitigacao: sugerir refinamentos fatiados por documento ou por tipo de regra.

## Bloqueios Pendentes

Bloqueada ate a execucao das TASKs 002, 005 e 006.

Permanece bloqueado qualquer trabalho que tente alterar documentos operacionais, skills, plugins, configuracoes, SPECs ou codigo durante esta auditoria.
