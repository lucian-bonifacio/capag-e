# Estrutura Do AGENTS.md

Use esta estrutura como baseline para criar ou atualizar o `AGENTS.md` inicial do projeto.

Preserve instruções existentes que continuem válidas, mas organize o documento para deixar claro que seu foco é SPECs e TASKs.

```markdown
# Instruções Para Agentes

## 1. Objetivo

## 2. Fontes Obrigatórias

## 3. Fluxo Obrigatório: PRD -> Arquitetura -> SPEC -> TASK

## 4. Regras Para Criar SPECs

## 5. Lentes Especializadas Para SPECs

## 6. Regras Para Criar TASKs

## 7. Decisões Técnicas E Bloqueios

## 8. Documentos De Frontend Governados

## 9. Domain Engine Específico Do Projeto
```

## 1. Objetivo

Declarar que o arquivo orienta agentes de IA, assistentes de código e ferramentas automatizadas na criação de SPECs e TASKs.

Não declarar nenhuma etapa posterior à criação de TASKs.

## 2. Fontes Obrigatórias

Listar:

- PRD do projeto;
- documento de arquitetura;
- decisões técnicas/ADRs, se existirem;
- documentos governados de frontend, se existirem;
- referências especializadas do projeto.

## 3. Fluxo Obrigatório

Usar explicitamente:

```text
PRD + Arquitetura + Docs governados
        ↓
SPECs especializadas
        ↓
TASKs correspondentes
```

## 4. Regras Para Criar SPECs

Explicar que SPECs devem transformar PRD e arquitetura em visão técnica verificável.

SPECs devem explicitar:

- contexto e problema;
- escopo;
- decisões;
- contratos;
- responsabilidades;
- critérios de aceite;
- riscos;
- bloqueios;
- fora de escopo.

## 5. Lentes Especializadas Para SPECs

Incluir orientação para aplicar lentes:

- arquitetura;
- backend FastAPI;
- frontend React;
- QA;
- domínio/engine específico quando aplicável.

## 6. Regras Para Criar TASKs

Declarar que TASK deriva de SPEC suficiente.

TASK deve conter:

- SPEC de origem;
- objetivo;
- escopo;
- passos executáveis;
- arquivos ou áreas prováveis;
- critérios de aceite;
- validação esperada;
- fora de escopo;
- bloqueios herdados ou pendentes.

## 7. Decisões Técnicas E Bloqueios

Declarar que o agente deve bloquear quando faltar:

- decisão arquitetural;
- contrato de API;
- fonte normativa;
- regra de cálculo;
- critério de aceite verificável;
- estratégia de teste necessária.

## 8. Documentos De Frontend Governados

Quando existirem, referenciar:

- `docs/frontend/DESIGN_TOKENS.md`
- `docs/frontend/UI_COMPONENT_RULES.md`
- `docs/frontend/SCREEN_PATTERNS.md`
- `frontend/src/styles/globals.css`

Esses documentos são fontes para SPECs frontend e TASKs frontend.

## 9. Domain Engine Específico Do Projeto

Incluir somente quando aplicável.

Deixar claro que regras CAPAG de domínio/engine são específicas de projeto e não devem ser generalizadas automaticamente.
