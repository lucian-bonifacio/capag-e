# TASK-041L - Ajustar fluxo de homologacao por grupo

## SPEC De Origem

- `specs/SPEC-001-modulo-0-fundacao-governada.md`

## Dependencias

- `TASK-041-exportacao-e-testes-camada-declarada.md`

## Objetivo

Ajustar exclusivamente a seção `## 5. Fluxo De Trabalho` do `AGENTS.md` para permitir execução governada de grupos ou sequências de TASKs, mantendo execução individual por TASK, validações obrigatórias e homologação consolidada por grupo.

## Fontes Usadas

- `docs/product/PRD.md`
- `docs/architecture/architecture.md`
- `specs/SPEC-001-modulo-0-fundacao-governada.md`
- `AGENTS.md`

## Escopo Exato

- Alterar apenas a seção `## 5. Fluxo De Trabalho` do `AGENTS.md`.
- Preservar o fluxo atual de execução individual de TASKs.
- Definir o conceito de grupo de execução, incluindo sequência contínua, lista explícita ou conjunto definido pelo usuário.
- Definir que cada TASK do grupo continua sendo executada individualmente, com leitura de fontes, autorização aplicável, execução de escopo, validações, log e atualização de ROADMAP.
- Definir que testes e validações previstas são obrigatórios ao final de cada TASK.
- Definir que, quando não houver teste automatizado adequado para o escopo alterado, a execução deve criar teste automatizado focado quando isso couber na TASK e não violar SPEC, TASK, arquitetura ou gates.
- Definir que, quando criar teste automatizado não couber sem ampliar escopo ou violar gate, a limitação deve ser registrada no log e o agente deve pedir decisão governada ou propor nova TASK.
- Alterar a regra de homologação para permitir homologação consolidada por grupo: cada TASK executada no grupo pode ficar em `aguardando_homologacao`, mas o agente não deve parar para homologação individual até concluir ou bloquear o grupo.
- Definir que, ao final do grupo, o usuário homologa o conjunto; se aprovado, todas as TASKs do grupo aprovadas são marcadas como `concluido`.
- Definir comportamento para reprovação parcial, ajuste solicitado ou falha em uma TASK do grupo.

## Fora De Escopo

- Alterar outras seções do `AGENTS.md`.
- Alterar `ROADMAP.md`, exceto se necessário para registrar a própria TASK durante seu planejamento.
- Alterar regras de ambiente Docker/Docker Compose.
- Alterar statuses permitidos do ROADMAP.
- Implementar Playwright.
- Executar qualquer TASK funcional do produto.

## Passos Executaveis

1. Ler a seção `## 5. Fluxo De Trabalho` atual do `AGENTS.md`.
2. Reescrever apenas essa seção para incluir execução por grupo e homologação consolidada.
3. Preservar as regras atuais de execução individual, logs, validações e roadmap.
4. Garantir que o texto não conflite com `## 6. Gates De Exceção` e `## 7. Ambiente Oficial`.
5. Conferir diff restrito ao trecho permitido.

## Arquivos Ou Areas Provaveis

- `AGENTS.md`

## Criterios De Aceite

- Apenas a seção `## 5. Fluxo De Trabalho` do `AGENTS.md` é alterada.
- O fluxo individual por TASK permanece preservado.
- O fluxo por grupo permite executar uma sequência/lista definida pelo usuário sem exigir homologação individual entre TASKs.
- Validações por TASK ficam obrigatórias.
- A regra sobre criação de testes automatizados quando ausentes fica explícita, com respeito aos gates.
- Homologação consolidada por grupo fica clara.
- Reprovação parcial ou ajuste de uma TASK do grupo tem encaminhamento governado.

## Validacao Esperada

- Conferir `git diff -- AGENTS.md`.
- Conferir que somente a seção `## 5. Fluxo De Trabalho` foi alterada.
- Conferir que `ROADMAP.md` preserva statuses permitidos.

## Riscos

- Risco: fluxo por grupo reduzir rastreabilidade por TASK.
  Mitigacao: manter log, validação e status individual por TASK mesmo dentro do grupo.

- Risco: regra de criar testes automatizados ampliar escopo indevidamente.
  Mitigacao: limitar criação de teste ao escopo da TASK e acionar gate quando exigir mudança maior.

## Bloqueios Pendentes

Nenhum.
