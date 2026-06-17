# TASK-019 - Auditar higiene de repositorio e artefatos

## SPEC De Origem

- `specs/SPEC-001-modulo-0-fundacao-governada.md`

## Dependencias

- `TASK-002-auditar-estrutura-minima-repositorio.md`
- `TASK-006-auditar-validacoes-minimas-do-projeto.md`
- `TASK-010-auditar-ambiente-local-e-configuracao.md`

Esta TASK so deve ser executada depois que a estrutura minima, as validacoes e o ambiente local estiverem auditados.

## Objetivo

Auditar a higiene do repositorio, identificando artefatos temporarios, gerados, duplicados, sensiveis ou desalinhados com a estrutura governada, sem remover, mover ou alterar arquivos nesta etapa.

## Fontes Usadas

- `docs/product/PRD.md`
- `docs/architecture.md`
- `specs/SPEC-001-modulo-0-fundacao-governada.md`
- relatorio esperado de `tasks/reports/TASK-002-auditoria-estrutura-minima.md`
- relatorio esperado de `tasks/reports/TASK-006-auditoria-validacoes.md`
- relatorio esperado de `tasks/reports/TASK-010-auditoria-ambiente-local.md`

## Escopo Exato

- Auditar arquivos e diretorios da raiz do repositorio.
- Auditar sinais de artefatos temporarios, duplicados ou gerados que nao deveriam ser fonte governada.
- Auditar se existem arquivos sensiveis versionados ou potencialmente sensiveis, sem ler arquivos `.env`.
- Auditar se existem `.venv`, `node_modules` no host ou outros ambientes locais que contrariem o ambiente oficial Docker-only.
- Auditar se `.gitignore` existe e cobre categorias basicas, quando aplicavel.
- Auditar se ha documentos ou pastas historicas que precisam ser classificados como referencia, governados ou obsoletos.
- Registrar achados em relatorio documental.
- Propor proximas TASKs pequenas para limpeza, classificacao ou ajuste de `.gitignore`.

## Fora De Escopo

- Remover arquivos.
- Mover arquivos.
- Renomear arquivos.
- Alterar `.gitignore`.
- Ler arquivos `.env`.
- Alterar documentos governados.
- Alterar `docs/reference/`.
- Alterar SPECs.
- Alterar codigo, testes, configs ou assets.
- Atualizar `tasks/README.md`.

## Passos Executaveis

1. Ler os relatorios das TASKs 002, 006 e 010.
2. Listar arquivos e diretorios da raiz.
3. Verificar existencia de `.gitignore`.
4. Identificar artefatos temporarios, gerados, duplicados ou potencialmente sensiveis sem ler arquivos `.env`.
5. Classificar achados como:
   - manter;
   - revisar;
   - mover para referencia;
   - remover em TASK futura;
   - proteger por `.gitignore`;
   - bloqueado por decisao do usuario.
6. Criar relatorio em `tasks/reports/TASK-019-auditoria-higiene-repositorio.md`.
7. Sugerir proximas TASKs pequenas para cada grupo de achados.
8. Validar que nenhum arquivo auditado foi removido, movido ou alterado durante a execucao.

## Arquivos Ou Areas Provaveis

- `tasks/reports/TASK-019-auditoria-higiene-repositorio.md`
- raiz do repositorio apenas para leitura
- `.gitignore` apenas para leitura, se existir
- `docs/` apenas para leitura
- `specs/` apenas para leitura
- `frontend/` apenas para leitura
- `backend/` apenas para leitura, se existir

## Criterios De Aceite

- Existe relatorio em `tasks/reports/TASK-019-auditoria-higiene-repositorio.md`.
- O relatorio cita a SPEC de origem.
- O relatorio lista categorias de achados com classificacao objetiva.
- O relatorio identifica se `.gitignore` existe e se ha lacunas aparentes.
- O relatorio identifica ambientes locais proibidos, como `.venv` e `node_modules` no host, sem remove-los.
- Arquivos `.env` nao sao lidos.
- Nenhum arquivo e removido, movido, renomeado ou alterado.
- O relatorio sugere TASKs futuras pequenas para limpeza ou classificacao.

## Validacao Esperada

- Executar `test -f tasks/reports/TASK-019-auditoria-higiene-repositorio.md`.
- Executar `git diff --stat` e confirmar que a execucao alterou apenas `tasks/reports/TASK-019-auditoria-higiene-repositorio.md`.
- Conferir manualmente que nenhum arquivo `.env` foi lido e que nenhum arquivo auditado foi alterado.

## Riscos

- Risco: auditoria virar limpeza destrutiva.
  Mitigacao: registrar achados e propor TASKs futuras, sem remover ou mover nada nesta TASK.

- Risco: expor segredo durante auditoria.
  Mitigacao: nao ler arquivos `.env` e tratar nomes suspeitos como achados sem abrir conteudo sensivel.

- Risco: remover referencia historica ainda util.
  Mitigacao: classificar antes de qualquer limpeza e exigir TASK futura especifica.

## Bloqueios Pendentes

Bloqueada ate a execucao das TASKs 002, 006 e 010.

Permanece bloqueado qualquer trabalho que tente remover, mover, renomear, alterar `.gitignore`, ler `.env`, alterar documentos governados, alterar referencia historica, alterar codigo ou alterar configuracoes durante esta TASK.
