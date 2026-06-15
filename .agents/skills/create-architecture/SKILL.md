---
name: create-architecture
description: Criar documento de arquitetura de software em Markdown a partir de um PRD obrigatório. Use quando o usuário quiser transformar um PRD em arquitetura técnica, blueprint técnico, system design, plano de implementação arquitetural ou estrutura técnica de projeto, considerando preferências fixas de stack, referências opcionais, decisões específicas, estrutura de pastas, riscos, trade-offs, segurança, dados, integrações, deploy e operação.
---

# Criar Arquitetura

## Objetivo

Use esta skill para produzir um documento de arquitetura de software em Markdown puro a partir de um PRD fornecido pelo usuário.

A entrega deve ser específica, acionável e sem ambiguidades operacionais. Não produza recomendações genéricas, listas abertas de possibilidades ou decisões que deixem margem para interpretação.

## Insumo Obrigatório

Exija um PRD antes de gerar o documento de arquitetura.

Se o usuário não fornecer o PRD, peça o PRD e aguarde. Não gere arquitetura sem esse insumo.

## Coleta de Referências

Antes de gerar o documento final, pergunte se existem referências adicionais que devam ser consideradas.

Use uma pergunta simples:

```text
Existe alguma referência que eu deva considerar além do PRD? Pode ser repositório existente, documento técnico, diagrama, decisão arquitetural anterior, restrição de infraestrutura, padrão de UI, requisito de segurança, LGPD, compliance ou qualquer material que ajude.
```

Se o usuário não tiver referências, continue normalmente. Se houver referências, use-as como insumo técnico, sem assumir que substituem o PRD.

## Preferências Tecnológicas Fixas

Sempre considerar estas tecnologias como base da arquitetura:

- Backend: Python com FastAPI
- Frontend: React com Vite
- Banco de dados relacional: PostgreSQL

Use essas tecnologias por padrão. Não substitua nenhuma delas sem justificar conflito claro com o PRD, limitação técnica relevante, risco operacional ou complexidade desnecessária.

Para áreas sem preferência definida, escolha uma solução específica e pragmática com base no PRD, no tamanho do projeto, no custo operacional e na coerência com Python/FastAPI, React/Vite e PostgreSQL.

## Decisões Padrão

Quando o PRD não exigir outra escolha, assuma:

- API: REST com OpenAPI gerado pelo FastAPI
- ORM e migrações: SQLAlchemy 2.x com Alembic
- Validação backend: Pydantic
- Autenticação: JWT com access token e refresh token
- Armazenamento de refresh token: persistido com hash no backend
- Autorização: RBAC simples por papéis
- Cache de dados no frontend: TanStack Query
- Formulários frontend: React Hook Form com Zod
- UI base: Tailwind CSS, salvo se houver design system existente
- Testes backend: pytest
- Testes frontend: Vitest com React Testing Library
- Testes E2E: Playwright quando houver fluxo crítico de usuário
- Containerização local: Docker e Docker Compose
- CI: GitHub Actions
- Logs backend: logging estruturado em JSON
- Observabilidade inicial: logs estruturados, healthcheck e métricas básicas

Registre essas escolhas no documento final quando forem usadas. Se o PRD justificar outra decisão, escolha uma alternativa específica e explique a troca.

## Regra de Especificidade

Produza sempre decisões específicas.

Não escreva:

- "pode usar Redis ou RabbitMQ"
- "implementar autenticação adequada"
- "criar uma camada de serviços"
- "adicionar observabilidade"
- "usar boas práticas de segurança"
- "avaliar banco de dados conforme necessidade"

Escreva:

- tecnologia escolhida
- responsabilidade da tecnologia
- local de uso na arquitetura
- motivo da escolha
- integração com os demais componentes
- impacto operacional
- trade-off assumido

Quando faltar informação, faça perguntas objetivas antes do documento. Se ainda houver lacunas, assuma uma decisão pragmática, registre como premissa e explique o impacto.

## Atribuições Arquiteturais Obrigatórias

Ao criar o documento, exerça obrigatoriamente estas atribuições:

- Extrair drivers arquiteturais do PRD: requisitos funcionais críticos, requisitos não funcionais, volume esperado, disponibilidade, segurança, privacidade, integrações, restrições, riscos e operação.
- Transformar produto em estrutura técnica: módulos, camadas, serviços, componentes, fronteiras de responsabilidade, fluxos e dependências.
- Definir decisões arquiteturais e trade-offs: decisão, justificativa, alternativas descartadas, impacto e risco.
- Validar coerência entre stack, PRD e contexto: respeitar a stack fixa e desafiar preferências apenas quando houver conflito técnico claro.
- Projetar fronteiras e contratos: APIs, eventos, mensagens, payloads relevantes, autenticação, autorização e integrações.
- Pensar dados desde o início: entidades principais, persistência, ownership, migrações, consistência, auditoria, retenção e cache.
- Cobrir segurança e controle de acesso: autenticação, autorização, dados sensíveis, segredos, auditoria e ameaças relevantes.
- Definir implantação e operação: ambiente local, staging, produção, CI/CD, logs, métricas, alertas, backup, rollback e escalabilidade.
- Identificar riscos, hipóteses e perguntas abertas: separar fatos, premissas, riscos e decisões pendentes.
- Gerar plano técnico de implementação: fases, ordem de execução, fundações técnicas, entregáveis, dependências e spikes necessários.
- Definir estrutura física de pastas: diretórios concretos, responsabilidades e relação com os módulos do PRD.

## Estrutura de Pastas

Inclua uma seção obrigatória de estrutura de pastas recomendada.

A estrutura deve ser concreta e compatível com as decisões arquiteturais. Para cada diretório relevante, explique sua responsabilidade.

Use este baseline apenas como ponto de partida e adapte aos domínios identificados no PRD:

```text
<project-root>/
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   ├── routes/
│   │   │   └── dependencies.py
│   │   ├── core/
│   │   │   ├── config.py
│   │   │   ├── security.py
│   │   │   └── logging.py
│   │   ├── db/
│   │   │   ├── session.py
│   │   │   └── migrations/
│   │   ├── models/
│   │   ├── schemas/
│   │   ├── services/
│   │   ├── repositories/
│   │   └── main.py
│   ├── tests/
│   ├── pyproject.toml
│   └── alembic.ini
├── frontend/
│   ├── src/
│   │   ├── app/
│   │   ├── pages/
│   │   ├── components/
│   │   ├── features/
│   │   ├── hooks/
│   │   ├── lib/
│   │   ├── services/
│   │   ├── styles/
│   │   └── main.tsx
│   ├── tests/
│   ├── package.json
│   └── vite.config.ts
├── infra/
│   ├── docker/
│   └── compose.yaml
├── docs/
│   ├── architecture.md
│   └── adr/
├── scripts/
└── README.md
```

Quando o PRD indicar domínios claros, reflita esses domínios em `backend/app/` e em `frontend/src/features/`.

## Saída

Gere o documento final em Markdown puro.

Não use HTML, DOCX, PDF, apresentação, Mermaid, PlantUML ou tabelas complexas, salvo se o usuário pedir explicitamente.

Use listas, subtítulos e blocos de código para árvore de pastas, contratos, payloads, comandos e exemplos técnicos.

## Layout Obrigatório de Saída

Use exatamente este layout. Preserve títulos e ordem, salvo se o usuário pedir explicitamente outro formato.

```markdown
# Documento de Arquitetura - [Nome do Projeto]

## 1. Resumo Executivo

## 2. Contexto e Objetivos

## 3. Insumos Utilizados

## 4. Premissas e Restrições

## 5. Drivers Arquiteturais

## 6. Stack Tecnológica

## 7. Visão Geral da Arquitetura

## 8. Componentes e Responsabilidades

## 9. Fluxos Principais

## 10. Arquitetura de Dados

## 11. APIs, Contratos e Integrações

## 12. Segurança e Controle de Acesso

## 13. Infraestrutura, Deploy e Operação

## 14. Observabilidade

## 15. Decisões Arquiteturais

## 16. Estrutura de Pastas Recomendada

## 17. Plano Técnico de Implementação

## 18. Riscos, Trade-offs e Mitigações

## 19. Perguntas Abertas
```

## Critérios de Qualidade

Antes de finalizar, verifique:

- o PRD foi usado como insumo principal;
- o usuário foi perguntado sobre referências adicionais;
- a stack fixa foi considerada;
- cada tecnologia escolhida tem responsabilidade clara;
- nenhuma seção deixa decisão técnica importante em aberto sem declarar premissa ou pergunta;
- os componentes têm fronteiras e responsabilidades explícitas;
- os fluxos principais estão conectados aos requisitos do PRD;
- dados, segurança, deploy, operação e observabilidade foram cobertos;
- decisões arquiteturais incluem justificativas e trade-offs;
- a estrutura de pastas é concreta e alinhada aos módulos do projeto;
- o plano de implementação possui ordem executável;
- riscos e perguntas abertas não foram escondidos como decisões definitivas.
