# TASK-002A - Descontinuar reports em TASKs pendentes

## SPEC De Origem

- `specs/SPEC-001-modulo-0-fundacao-governada.md`

## Dependencias

- `TASK-002 - Auditar estrutura minima do repositorio` concluida.
- Decisao do usuario de descontinuar o fluxo `tasks/reports/` e consolidar achados, auditorias, validacoes e evidencias operacionais em `logs/`.

## Objetivo

Sanear TASKs pendentes e documentos operacionais que ainda referenciam `tasks/reports/`, substituindo esse fluxo descontinuado por registro em `logs/`, sem alterar `AGENTS.md` e sem executar as TASKs saneadas.

## Fontes Usadas

- `docs/product/PRD.md`
- `docs/architecture/architecture.md`
- `specs/SPEC-001-modulo-0-fundacao-governada.md`
- `tasks/README.md`
- `tasks/TASK-002-auditar-estrutura-minima-repositorio.md`
- `logs/LOG-002-auditar-estrutura-minima-repositorio.md`
- `ROADMAP.md`

## Escopo Exato

- Localizar TASKs pendentes e documentos operacionais que citam:
  - `tasks/reports/`;
  - relatorio esperado em `tasks/reports/`;
  - criacao de relatorio como artefato de execucao;
  - validacao por `test -f tasks/reports/...`.
- Atualizar essas referencias para usar logs em `logs/` como artefato operacional.
- Ajustar passos executaveis, criterios de aceite, arquivos provaveis e validacoes esperadas das TASKs afetadas.
- Preservar o escopo funcional original de cada TASK saneada.
- Registrar no log da TASK-002A a lista de arquivos saneados e os padroes substituidos.
- Manter `AGENTS.md` sem alteracao.

## Fora De Escopo

- Executar qualquer TASK saneada.
- Criar relatorios em `tasks/reports/`.
- Alterar `AGENTS.md`.
- Alterar PRD, arquitetura ou SPECs funcionais.
- Alterar codigo de backend, frontend, engine, banco, exportacao ou laudo.
- Marcar TASKs saneadas como concluidas ou em homologacao.
- Definir nova arquitetura, contrato de API, regra de dominio, formula prudencial, fonte normativa, arredondamento ou padrao visual.

## Passos Executaveis

1. Buscar referencias a `tasks/reports/` em `tasks/`, `ROADMAP.md` e documentos operacionais aplicaveis.
2. Separar referencias em:
   - dependencia de artefato anterior;
   - artefato de execucao a criar;
   - criterio de aceite;
   - validacao esperada;
   - texto historico que nao precisa mudar.
3. Atualizar somente referencias de fluxo futuro ou de TASK pendente.
4. Trocar artefatos de auditoria e evidencia operacional para o log correspondente em `logs/LOG-...`.
5. Garantir que nenhuma TASK saneada passe a executar trabalho funcional adicional.
6. Criar ou atualizar `logs/LOG-002A-descontinuar-reports-em-tasks-pendentes.md`.
7. Validar que nao restam referencias ativas a `tasks/reports/` em TASKs pendentes.

## Arquivos Ou Areas Provaveis

- `tasks/*.md`
- `tasks/README.md`
- `ROADMAP.md`
- `logs/LOG-002A-descontinuar-reports-em-tasks-pendentes.md`

## Criterios De Aceite

- Existe log em `logs/LOG-002A-descontinuar-reports-em-tasks-pendentes.md`.
- TASKs pendentes nao instruem mais criar relatorios em `tasks/reports/`.
- TASKs pendentes nao dependem mais de leitura obrigatoria de relatorios em `tasks/reports/`.
- Validacoes esperadas usam logs em `logs/` quando houver artefato operacional.
- `AGENTS.md` permanece inalterado.
- Nenhum arquivo funcional de backend, frontend, engine, banco, exportacao ou laudo e alterado.
- A TASK nao cria, executa ou conclui as TASKs saneadas.

## Validacao Esperada

- Executar `rg -n "tasks/reports/" tasks ROADMAP.md` e justificar qualquer referencia remanescente.
- Executar `test -f logs/LOG-002A-descontinuar-reports-em-tasks-pendentes.md`.
- Executar `git diff --stat` e confirmar que as alteracoes ficaram restritas a documentos operacionais e log.
- Conferir manualmente que `AGENTS.md` nao foi alterado.

## Riscos

- Risco: alterar o escopo funcional de TASKs futuras ao sanear referencias.
  Mitigacao: trocar somente o destino do artefato operacional, preservando objetivo, escopo e criterios substantivos.

- Risco: remover referencia historica necessaria para rastreabilidade.
  Mitigacao: justificar no log qualquer referencia mantida ou removida.

- Risco: transformar saneamento documental em execucao de TASKs pendentes.
  Mitigacao: nao criar codigo, scaffolding, relatorio ou implementacao funcional nesta TASK.

## Bloqueios Pendentes

Nao ha bloqueio para criar esta TASK.

Permanece bloqueada a execucao do saneamento ate que esta TASK seja selecionada pelo fluxo normal do `ROADMAP.md` e autorizada pelo usuario.
