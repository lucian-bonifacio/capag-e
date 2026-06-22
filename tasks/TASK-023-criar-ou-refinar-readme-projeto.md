# TASK-023 - Criar ou refinar README do projeto

## SPEC De Origem

- `specs/SPEC-001-modulo-0-fundacao-governada.md`

## Dependencias

- `TASK-007-auditar-documentos-operacionais-e-agentes.md`
- `TASK-010-auditar-ambiente-local-e-configuracao.md`
- `TASK-012-criar-indice-oficial-de-specs.md`

Esta TASK so deve ser executada depois que os documentos operacionais, o ambiente local e o indice oficial de SPECs estiverem auditados ou criados.

## Objetivo

Criar ou refinar o `README.md` principal do projeto para orientar leitura inicial, fontes governadas, fluxo de trabalho, setup local e validacoes basicas, sem substituir PRD, arquitetura, SPECs, TASKs ou AGENTS.md.

## Fontes Usadas

- `docs/product/PRD.md`
- `docs/architecture/architecture.md`
- `specs/SPEC-001-modulo-0-fundacao-governada.md`
- `tasks/README.md`
- `AGENTS.md`
- log esperado de `logs/LOG-007-auditar-documentos-operacionais-e-agentes.md`
- log esperado de `logs/LOG-010-auditar-ambiente-local-e-configuracao.md`
- `specs/README.md`, se criado pela TASK-012

## Escopo Exato

- Criar `README.md` se ele estiver ausente e a auditoria indicar necessidade.
- Refinar `README.md` existente se a auditoria indicar desalinhamentos.
- Registrar objetivo do projeto em alto nivel.
- Registrar fontes governadas principais.
- Registrar ordem de leitura recomendada.
- Registrar fluxo `PRD -> Arquitetura -> SPEC -> TASK`.
- Registrar separacao entre criacao de TASKs e execucao de TASKs.
- Registrar comandos de setup, validacao e execucao local apenas se ja definidos por TASKs anteriores.
- Registrar que o setup oficial exige apenas Git, Docker e Docker Compose no host.
- Registrar que comandos oficiais usam `docker compose`.
- Registrar que `.venv`, `node_modules` no host e instalacoes globais nao fazem parte do fluxo oficial.
- Registrar links para documentos oficiais sem duplicar seus contratos.

## Fora De Escopo

- Alterar PRD.
- Alterar arquitetura.
- Alterar SPECs.
- Alterar TASKs.
- Alterar `AGENTS.md`.
- Criar comandos novos de setup ou validacao.
- Documentar fluxo local baseado em `.venv` ou `node_modules` no host.
- Criar configuracoes de Docker, backend, frontend, testes ou CI.
- Implementar codigo.
- Definir regra de dominio, contrato de API, formula, arredondamento ou padrao visual.
- Atualizar `tasks/README.md`.

## Passos Executaveis

1. Ler os logs das TASKs 007 e 010.
2. Ler `README.md` atual, se existir.
3. Ler `specs/README.md`, se existir.
4. Criar ou atualizar `README.md` apenas com informacoes governadas e comandos ja existentes.
5. Garantir que `README.md` aponta para fontes oficiais em vez de duplicar contratos.
6. Garantir que `README.md` nao introduz regra tecnica nova.
7. Validar que nenhum arquivo alem de `README.md` foi alterado.

## Arquivos Ou Areas Provaveis

- `README.md`

## Criterios De Aceite

- As TASKs 007, 010 e 012 foram executadas ou explicitamente dispensadas quando aplicavel.
- `README.md` existe.
- `README.md` aponta para PRD, arquitetura, SPECs, TASKs e AGENTS.md.
- `README.md` deixa claro que TASK nasce de SPEC suficiente.
- `README.md` separa criacao de TASKs e execucao de TASKs.
- `README.md` documenta Docker/Docker Compose como unico ambiente oficial.
- `README.md` nao exige Python, Node, package managers, `.venv` ou `node_modules` no host.
- `README.md` nao substitui documentos governados.
- `README.md` nao cria comandos, contratos, regras ou decisoes novas.
- Nenhum arquivo alem de `README.md` e alterado.

## Validacao Esperada

- Executar `test -f README.md`.
- Executar `git diff -- README.md` e revisar se as mudancas sao apenas orientativas.
- Executar `git diff --stat` e confirmar que a execucao alterou apenas `README.md`.
- Conferir manualmente que `README.md` nao define regra de dominio, contrato funcional, formula, arredondamento, padrao visual ou comando inexistente.

## Riscos

- Risco: `README.md` virar fonte normativa paralela.
  Mitigacao: usar o README como mapa de leitura e comandos, nao como contrato tecnico.

- Risco: documentar comandos ainda inexistentes.
  Mitigacao: incluir apenas comandos criados e validados por TASKs anteriores.

- Risco: esconder bloqueios ou dependencias.
  Mitigacao: apontar para SPECs, TASKs e logs de auditoria correspondentes.

## Bloqueios Pendentes

Bloqueada ate a execucao das TASKs 007 e 010, e ate a execucao ou dispensa explicita da TASK-012.

Permanece bloqueado qualquer trabalho que tente alterar documentos governados, criar comandos novos, configurar ambiente, implementar codigo, criar testes, alterar SPECs, alterar TASKs ou definir regras tecnicas durante esta TASK.
