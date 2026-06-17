# Insumos Obrigatórios Do Projeto

Antes de criar ou atualizar `AGENTS.md`, obter ou localizar:

## PRD

O PRD é fonte de requisitos de produto.

Usar para extrair:

- objetivos;
- escopo;
- fluxos;
- requisitos funcionais;
- requisitos não funcionais;
- restrições;
- prioridades;
- critérios de produto.

Se não existir PRD, parar e pedir ao usuário.

## Arquitetura

O documento de arquitetura é fonte de decisões técnicas.

Usar para extrair:

- stack;
- camadas;
- fronteiras;
- contratos;
- módulos;
- persistência;
- integrações;
- decisões e trade-offs;
- riscos técnicos;
- estrutura de pastas.

Se não existir arquitetura, parar e pedir ao usuário.

## Documentos Frontend Governados

Quando existirem, ler:

- `docs/frontend/DESIGN_TOKENS.md`
- `docs/frontend/UI_COMPONENT_RULES.md`
- `docs/frontend/SCREEN_PATTERNS.md`
- `frontend/src/styles/globals.css`

Esses documentos não substituem PRD nem arquitetura. Eles orientam SPECs e TASKs que envolvam frontend.

## Decisões Técnicas E ADRs

Quando existirem, ler documentos de decisão relevantes.

Não criar instruções que contradigam ADR aprovado.

## Referências Especializadas

Usar referências especializadas como lentes para criar SPECs, não como substitutas do PRD ou da arquitetura.
