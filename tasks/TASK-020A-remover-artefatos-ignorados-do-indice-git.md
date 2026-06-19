# TASK-020A - Remover artefatos ignorados do indice Git

## SPEC De Origem

- `specs/SPEC-001-modulo-0-fundacao-governada.md`

## Dependencias

- `TASK-019-auditar-higiene-repositorio-e-artefatos.md`
- `TASK-020-ajustar-gitignore-minimo.md`

Esta TASK so deve ser executada depois que a auditoria de higiene identificar artefatos gerados e que o `.gitignore` minimo estiver criado e homologado.

## Objetivo

Remover do indice Git artefatos gerados ou temporarios que ja estejam rastreados e agora estejam cobertos pelo `.gitignore`, sem apagar arquivos do disco, sem alterar codigo funcional e sem alterar o `.gitignore`.

## Fontes Usadas

- `docs/product/PRD.md`
- `docs/architecture/architecture.md`
- `specs/SPEC-001-modulo-0-fundacao-governada.md`
- `logs/LOG-019-auditar-higiene-repositorio-e-artefatos.md`
- `logs/LOG-020-ajustar-gitignore-minimo.md`

## Escopo Exato

- Identificar arquivos rastreados que tambem estejam ignorados pelo `.gitignore`.
- Remover do indice Git apenas artefatos gerados ou temporarios confirmados, como bytecode Python, caches ou equivalentes.
- Preservar os arquivos no disco quando existirem localmente.
- Validar que o conjunto de arquivos rastreados e ignorados foi sanado.
- Registrar a execucao em log operacional.

## Fora De Escopo

- Apagar arquivos do disco.
- Remover arquivos governados do repositorio.
- Alterar `.gitignore`.
- Ler, criar ou alterar arquivos `.env`.
- Alterar codigo, testes, docs, specs, tasks ou assets.
- Alterar configuracoes de build, teste, CI ou Docker.
- Fazer commit, push ou interagir com remoto.
- Atualizar `tasks/README.md`.

## Passos Executaveis

1. Ler `logs/LOG-019-auditar-higiene-repositorio-e-artefatos.md`.
2. Ler `logs/LOG-020-ajustar-gitignore-minimo.md`.
3. Executar `git ls-files -ci --exclude-standard` para identificar arquivos rastreados e ignorados.
4. Confirmar que cada arquivo identificado e artefato gerado ou temporario.
5. Executar remocao apenas do indice Git para os artefatos confirmados.
6. Validar que os arquivos nao permanecem rastreados.
7. Validar que os arquivos nao foram apagados do disco por esta TASK.
8. Registrar log em `logs/LOG-020A-remover-artefatos-ignorados-do-indice-git.md`.

## Arquivos Ou Areas Provaveis

- indice Git
- `logs/LOG-020A-remover-artefatos-ignorados-do-indice-git.md`
- `ROADMAP.md`

## Criterios De Aceite

- A TASK-019 e a TASK-020 foram homologadas antes desta TASK.
- Arquivos rastreados e ignorados sao identificados antes de qualquer remocao do indice.
- Apenas artefatos gerados ou temporarios sao removidos do indice Git.
- Nenhum arquivo governado e removido do indice.
- Nenhum arquivo e apagado do disco por esta TASK.
- `.gitignore` nao e alterado.
- Nenhum arquivo `.env` e lido, criado ou alterado.
- Nao ha commit, push ou alteracao no remoto.

## Validacao Esperada

- Executar `git ls-files -ci --exclude-standard` e confirmar que nao ha artefatos rastreados ainda ignorados.
- Executar `git status --short` e confirmar que a remocao do indice esta restrita aos artefatos aprovados.
- Conferir manualmente que os arquivos removidos do indice sao gerados ou temporarios.
- Conferir manualmente que nenhum arquivo `.env` foi lido, criado ou alterado.

## Riscos

- Risco: remover do indice arquivo governado necessario.
  Mitigacao: revisar explicitamente a lista de `git ls-files -ci --exclude-standard` antes de qualquer remocao do indice.

- Risco: apagar arquivo do disco por engano.
  Mitigacao: usar remocao apenas do indice Git e validar existencia local quando aplicavel.

- Risco: misturar saneamento local com commit/push.
  Mitigacao: bloquear commit, push e qualquer interacao com remoto nesta TASK.

## Bloqueios Pendentes

Bloqueada ate a homologacao da TASK-020.

Permanece bloqueado qualquer trabalho que tente apagar arquivos do disco, remover arquivo governado do indice, alterar `.gitignore`, ler `.env`, criar `.env`, alterar codigo, alterar documentos governados, alterar SPECs, alterar TASKs, alterar assets, fazer commit, push ou interagir com remoto durante esta TASK.
