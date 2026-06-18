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
- Se a TASK estiver em `aguardando_homologacao` e houver ajuste, orientar retorno ao status `pendente` via `roadmap-manager` após confirmação.
