---
name: execution-log
description: Criar ou atualizar logs objetivos de execução em logs/ para TASKs do CAPAG. Use quando uma TASK for iniciada, executada, validada, enviada para homologação, ajustada ou homologada, e quando for necessário registrar evidência operacional curta sem duplicar a TASK.
---

# Execution Log

Use esta skill para criar ou atualizar logs operacionais de TASKs do CAPAG.

O log é evidência operacional. Não registre raciocínio interno, logs longos de terminal, conteúdo duplicado da TASK ou decisões extensas.

## Nome Do Arquivo

Crie logs em `logs/` usando o padrão:

```text
logs/LOG-NNN-descricao-curta.md
logs/LOG-NNNA-descricao-curta.md
```

O sufixo deve acompanhar a TASK correspondente:

```text
tasks/TASK-002A-ajustar-roadmap.md
logs/LOG-002A-ajustar-roadmap.md
```

## Template Obrigatório

```markdown
# LOG - TASK-NNN - Título

## Referência

- Task: `tasks/TASK-NNN-nome.md`
- SPEC: `specs/SPEC-NNN-nome.md`
- Status: pendente | aguardando_homologacao | concluido

## Fontes Consultadas

- `docs/product/PRD.md`
- `docs/architecture.md`
- `specs/SPEC-NNN-nome.md`

## Execução

- Data:
- Ação:
- Resumo:

## Arquivos Alterados

- `caminho/do/arquivo`

## Validações

- Comando:
  - Resultado:

## Pendências Ou Bloqueios

- Nenhum.

## Homologação

- Status: nao_enviada | aguardando_homologacao | aprovada | ajuste_solicitado
- Data:
- Decisão do usuário:
- Observação:
```

## Regras

- Manter o log curto e verificável.
- Registrar comandos executados apenas quando forem relevantes para validação.
- Resumir resultados; não colar saídas extensas.
- Registrar erro como sintoma, causa objetiva quando conhecida e correção aplicada.
- Registrar transições relevantes de status da TASK: `pendente`, `aguardando_homologacao` e `concluido`.
- Registrar ajuste solicitado pelo usuário em `Homologação` ou `Pendências Ou Bloqueios`.
- Quando houver ajuste em TASK já executada, registrar o ajuste como novo evento em `Execução`, registrar validações correspondentes em `Validações` e atualizar `Homologação` conforme o estado atual.
- Atualizar o status do log em sincronia com o `ROADMAP.md`.
- Não substituir TASK, SPEC, PRD, arquitetura ou ADR.
