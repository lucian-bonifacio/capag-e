# TASK-020 - Ajustar gitignore minimo

## SPEC De Origem

- `specs/SPEC-001-modulo-0-fundacao-governada.md`

## Dependencias

- `TASK-019-auditar-higiene-repositorio-e-artefatos.md`

Esta TASK so deve ser executada depois que a TASK-019 identificar lacunas objetivas de `.gitignore` ou confirmar que o arquivo esta ausente.

## Objetivo

Criar ou ajustar `.gitignore` minimo para proteger artefatos temporarios, caches, builds, ambientes locais e arquivos sensiveis, sem remover arquivos ja versionados e sem alterar estrutura funcional do projeto.

## Fontes Usadas

- `docs/product/PRD.md`
- `docs/architecture.md`
- `specs/SPEC-001-modulo-0-fundacao-governada.md`
- relatorio esperado de `tasks/reports/TASK-019-auditoria-higiene-repositorio.md`

## Escopo Exato

- Ler o relatorio da TASK-019.
- Criar `.gitignore` se ele estiver ausente e a auditoria indicar necessidade.
- Ajustar `.gitignore` existente apenas com categorias basicas identificadas pela auditoria, como:
  - arquivos `.env` e variantes locais;
  - `.venv` e ambientes virtuais locais;
  - `node_modules` no host;
  - caches Python;
  - ambientes virtuais Python;
  - caches e builds Node/Vite;
  - artefatos de teste;
  - arquivos temporarios de sistema/editor;
  - logs locais;
  - outputs locais de exportacao quando definidos como nao versionaveis.
- Manter excecoes explicitas para arquivos exemplo seguros, se existirem ou forem previstos por TASK futura.

## Fora De Escopo

- Remover arquivos do repositorio.
- Executar `git rm`.
- Criar arquivos `.env`.
- Ler arquivos `.env`.
- Criar exemplos de ambiente.
- Alterar backend, frontend, docs, specs, tasks ou assets.
- Definir politica final de artefatos de exportacao.
- Alterar configuracoes de build, teste ou CI.
- Atualizar `tasks/README.md`.

## Passos Executaveis

1. Ler `tasks/reports/TASK-019-auditoria-higiene-repositorio.md`.
2. Confirmar quais lacunas de `.gitignore` foram registradas.
3. Criar ou editar `.gitignore` apenas para cobrir lacunas aprovadas.
4. Garantir que `.env` e variantes locais estejam protegidos.
5. Garantir que arquivos exemplo seguros nao sejam bloqueados indevidamente quando aplicavel.
6. Validar que nenhum arquivo foi removido, movido ou renomeado.
7. Validar que nenhum arquivo `.env` foi lido, criado ou alterado.

## Arquivos Ou Areas Provaveis

- `.gitignore`

## Criterios De Aceite

- A TASK-019 foi executada antes desta TASK.
- `.gitignore` existe.
- `.gitignore` cobre categorias basicas registradas no relatorio da TASK-019.
- Arquivos `.env` e variantes locais estao ignorados.
- `.venv` e `node_modules` no host estao ignorados.
- Nenhum arquivo `.env` e lido, criado ou alterado.
- Nenhum arquivo versionado e removido, movido ou renomeado.
- Nenhum codigo, documento governado, SPEC, TASK ou asset e alterado.

## Validacao Esperada

- Executar `test -f .gitignore`.
- Executar `git diff --stat` e confirmar que a execucao alterou apenas `.gitignore`.
- Conferir manualmente que `.gitignore` nao bloqueia arquivos governados necessarios.
- Conferir manualmente que nenhum `.env` foi lido, criado ou alterado.

## Riscos

- Risco: bloquear arquivos governados por regra ampla demais.
  Mitigacao: aplicar apenas padroes basicos e lacunas registradas pela TASK-019.

- Risco: tentar limpar arquivos ja versionados durante ajuste.
  Mitigacao: bloquear remocoes nesta TASK.

- Risco: expor segredo durante verificacao.
  Mitigacao: nao ler arquivos `.env`.

## Bloqueios Pendentes

Bloqueada ate a execucao da TASK-019.

Permanece bloqueado qualquer trabalho que tente remover arquivos, executar `git rm`, ler `.env`, criar `.env`, alterar codigo, alterar documentos governados, alterar SPECs, alterar TASKs ou alterar assets durante esta TASK.
