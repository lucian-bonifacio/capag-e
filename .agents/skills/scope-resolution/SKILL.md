---
name: scope-resolution
description: Classificar dúvidas, sugestões, ajustes, reprovações de homologação e mudanças de escopo no CAPAG. Use quando a resposta do usuário não for autorização clara para executar, quando houver pedido de ajuste, dúvida sobre a TASK, sugestão de complemento ou possível necessidade de nova TASK ou SPEC.
---

# Scope Resolution

Use esta skill para classificar interações do usuário que possam alterar execução, escopo ou homologação.

Esta skill não implementa, não cria TASK, não altera roadmap e não edita arquivos de produto. Ela classifica e recomenda encaminhamento.

## Categorias

Classifique a interação em uma categoria:

- `esclarecimento_sem_mudanca`: pergunta ou dúvida que não muda escopo.
- `ajuste_da_task_atual`: ajuste cabe na TASK atual, na SPEC e nos critérios existentes.
- `nova_task`: solicitação válida, mas fora do escopo da TASK atual.
- `nova_spec`: falta SPEC suficiente para sustentar a solicitação.
- `conflito_governado`: solicitação conflita com PRD, arquitetura, SPEC, TASK ou regra obrigatória.

## Homologação

Durante homologação, classifique a interação sem alterar status por conta própria:

- problema relacionado ao escopo, critérios de aceite ou validação esperada da TASK em homologação: classifique como `ajuste_da_task_atual`;
- problema não relacionado ao escopo da TASK em homologação, mas válido e suportado por SPEC suficiente: classifique como `nova_task`;
- problema não relacionado sem SPEC suficiente: classifique como `nova_spec`;
- aprovação clara sem ajuste: não crie nova classificação de ajuste; oriente o fluxo de homologação do `AGENTS.md`.

Em homologação de TASK individual, quando a classificação for `nova_task`, peça autorização para criar a nova TASK e informe que essa autorização também homologa a TASK atual, conforme o `AGENTS.md`.

Em homologação de grupo, identifique o grupo autorizado e diferencie ajustes relacionados ao grupo de mudanças fora do grupo. Ajustes relacionados devem seguir o flow de homologação do grupo definido no `AGENTS.md`, sem criar nova TASK por padrão.

## Encaminhamentos

- Para `esclarecimento_sem_mudanca`, responda objetivamente e pergunte se pode seguir.
- Para `ajuste_da_task_atual`, explique o enquadramento e peça confirmação antes de executar ajuste.
- Para `nova_task`, explique por que é nova TASK e peça confirmação antes de usar `task-planner`.
- Para `nova_spec`, bloqueie implementação e oriente criação ou ajuste de SPEC.
- Para `conflito_governado`, explique o conflito e peça decisão expressa se o usuário quiser alterar a fonte governada.

## Regras

- Sempre pedir confirmação antes de criar TASK, alterar roadmap ou executar ajuste.
- Não tratar silêncio, dúvida ou comentário ambíguo como autorização.
- Não implementar durante a classificação.
- Não ampliar escopo de TASK em execução por conveniência.
- Se a TASK estiver em `aguardando_homologacao` e a classificação for `ajuste_da_task_atual`, orientar retorno ao status `pendente` via `roadmap-manager` após confirmação.
