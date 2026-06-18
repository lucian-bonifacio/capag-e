---
name: roadmap-manager
description: Criar e atualizar o ROADMAP.md vivo do CAPAG. Use quando for necessário manter a próxima tarefa, listar TASKs, alterar status entre pendente, aguardando_homologacao e concluido, inserir TASK já criada ou recalcular a próxima tarefa após homologação.
---

# Roadmap Manager

Use esta skill para criar e manter `ROADMAP.md`, o painel operacional vivo do CAPAG.

O roadmap não substitui TASKs, logs, SPECs, PRD ou arquitetura. Ele aponta para os artefatos corretos e mostra o estado da execução.

## Estrutura Obrigatória

```markdown
# ROADMAP

## Instruções De Uso

## Próxima Tarefa

## Lista De Tarefas
```

## Status Permitidos

Use somente:

- `pendente`
- `aguardando_homologacao`
- `concluido`

## Formato Da Próxima Tarefa

```markdown
ID: TASK-NNN
Título: Título da tarefa
Status: pendente
Task: `tasks/TASK-NNN-descricao.md`
Log: `logs/LOG-NNN-descricao.md`
```

## Formato Da Lista

```markdown
1. [ ] Título da tarefa
   - Status: pendente
   - Task: `tasks/TASK-NNN-descricao.md`
   - Log: `logs/LOG-NNN-descricao.md`
```

Use `[x]` somente quando o status for `concluido`.

## Regras

- Listar todas as TASKs planejadas.
- Não incluir SPEC no roadmap; a TASK já referencia a SPEC.
- Não incluir campo de observação.
- Não criar seção de tarefas candidatas.
- Não criar seção de bloqueios ativos.
- Não registrar log de terminal, decisões técnicas longas ou detalhes de execução.
- Inserir novas TASKs já criadas por `task-planner` na posição lógica.
- Não avançar automaticamente se existir TASK em `aguardando_homologacao`, salvo pedido expresso do usuário.
- Recalcular `## Próxima Tarefa` somente quando o fluxo do `AGENTS.md` permitir.
