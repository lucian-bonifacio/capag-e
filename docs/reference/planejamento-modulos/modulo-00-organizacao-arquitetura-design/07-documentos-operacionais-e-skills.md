# 07 - Documentos operacionais e skills

## Objetivo

Planejar o alinhamento de `README.md`, `AGENTS.md`, `CLAUDE.md`, tasks e skills depois que arquitetura, specs, testes, higiene de repositorio e roadmap forem aprovados.

## Ponto de decisao

Decidir a ordem de atualizacao dos documentos operacionais e das skills, mantendo esta etapa como uma das ultimas do modulo 0.

## Arquivos correlatos

- `README.md`
- `AGENTS.md`
- `CLAUDE.md`
- `tasks/`
- `.agents/skills/`
- `.claude/skills/`
- `docs/specs/README.md`, se criado
- specs novas aprovadas no modulo 0
- specs novas aprovadas no modulo 1, quando existirem

## Detalhamento

- Atualizar documentos operacionais somente depois de aprovar:
  - fonte de verdade;
  - indice de specs;
  - arquitetura-alvo;
  - rotas React;
  - organizacao de pastas;
  - design system;
  - estrategia de testes;
  - higiene de repositorio;
  - roadmap.
- Atualizar skills somente depois de atualizar os documentos operacionais.
- Revisar tasks antigas e criar nova sequencia oficial.
- Garantir que skills nao antecipem arquitetura ainda nao aprovada.
- Garantir que `README.md` descreva:
  - objetivo do sistema;
  - stack oficial;
  - decisoes arquiteturais vigentes;
  - estrutura de diretorios;
  - fronteiras de responsabilidade;
  - fluxo local de desenvolvimento;
  - testes;
  - politica de artefatos e assets.
- Garantir que `AGENTS.md` descreva:
  - regras para agentes no repositorio;
  - fonte de verdade;
  - arquitetura vigente;
  - proibicoes;
  - fluxo de execucao;
  - validacao obrigatoria;
  - limite entre planejamento e implementacao.
- Garantir que `CLAUDE.md` fique alinhado com `README.md` e `AGENTS.md`.
- Garantir que skills em `.agents/skills/` e `.claude/skills/`:
  - nao contradigam `README.md`, `AGENTS.md` ou `CLAUDE.md`;
  - saibam quando usar design lab, task creator, task worker e testing;
  - respeitem a decisao arquitetural vigente sobre banco de dados e persistencia;
  - reconhecam rotas React e camada `application/` somente se forem aprovadas.

## Entregavel

Plano de atualizacao documental, tasks e skills.

## Criterios de sucesso

- Agentes e Claude passam a obedecer a mesma arquitetura.
- Tasks novas sao pequenas e cronologicas.
- Skills passam a ser consequencia da arquitetura aprovada.

## Fora do escopo

- Atualizar os arquivos reais antes da conclusao do modulo 0.
- Introduzir banco de dados antes da decisao arquitetural.
- Introduzir persistencia de sessao antes da decisao arquitetural.
