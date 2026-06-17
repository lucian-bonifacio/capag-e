---
name: create-agent-instructions
description: Criar ou atualizar o AGENTS.md inicial de um projeto para orientar agentes na criação de SPECs e TASKs a partir de PRD, arquitetura e documentos governados. Use quando o usuário quiser definir instruções para agentes de IA, assistentes de código ou ferramentas automatizadas criarem SPECs especializadas e TASKs correspondentes, aplicando lentes de arquitetura, backend FastAPI, frontend React, QA e domínio específico quando aplicável.
---

# Criar Instruções Para Agentes

## Objetivo

Criar ou atualizar `AGENTS.md` na raiz do projeto como guia operacional para agentes criarem SPECs e TASKs.

A saída esperada governa apenas:

- criação de SPECs;
- criação de TASKs correspondentes;
- decisões técnicas e bloqueios que precisam aparecer antes de uma TASK.

## Insumos Obrigatórios

Antes de gerar ou atualizar `AGENTS.md`, exija:

- PRD existente;
- documento de arquitetura existente;
- documentos governados de frontend, quando existirem;
- referências especializadas disponíveis no projeto.

Leia `references/required-project-inputs.md` antes de avaliar os insumos.

Se PRD ou arquitetura não forem fornecidos e não puderem ser localizados, peça o caminho ao usuário e aguarde.

## Workflow

1. Localizar ou confirmar PRD e arquitetura.
2. Localizar documentos governados de frontend quando existirem.
3. Ler referências especializadas aplicáveis.
4. Ler `references/agents-output-structure.md`.
5. Ler `references/spec-workflow.md`.
6. Ler `references/spec-specialty-lenses.md`.
7. Ler `references/task-creation-rules.md`.
8. Ler `references/capag-domain-engine-lens.md` apenas quando o projeto for CAPAG, tiver domínio prudencial/contábil equivalente ou o usuário pedir adaptação explícita.
9. Criar ou atualizar `AGENTS.md`, preservando instruções úteis já existentes.
10. Validar que o documento final não descreve nenhuma etapa posterior à criação de TASKs.

## Regras Centrais

- `AGENTS.md` deve orientar PRD + Arquitetura + Docs governados -> SPECs -> TASKs.
- SPEC vem antes da TASK.
- TASK nasce de SPEC suficiente.
- SPEC deve declarar decisões, contratos, critérios de aceite, riscos, bloqueios e fora de escopo.
- TASK não deve decidir arquitetura, regra, contrato ou critério metodológico que faltou na SPEC.
- Se faltar decisão, fonte ou contrato, registrar bloqueio ou pergunta; não preencher com chute.
- Não criar instruções para etapas posteriores às TASKs nesta primeira versão.

## Referências Especializadas

Use as referências internas como lentes para escrever as instruções do `AGENTS.md`:

- `references/spec-specialty-lenses.md`: arquitetura, backend FastAPI, frontend React e QA.
- `references/capag-domain-engine-lens.md`: lente específica CAPAG para domínio/engine prudencial-contábil.

As lentes especializadas servem para orientar criação de SPECs. Elas não são SPECs prontas nem TASKs prontas.

## Saída

Criar ou atualizar:

```text
AGENTS.md
```

O documento final deve ser Markdown puro, objetivo, prescritivo e em português do Brasil quando o projeto estiver em português.

## Validação

Antes de finalizar, confirme:

- `AGENTS.md` existe na raiz.
- O documento exige PRD e arquitetura como fontes base.
- O documento orienta criação de SPECs.
- O documento orienta criação de TASKs correspondentes.
- O documento inclui lentes especializadas para SPECs.
- O documento marca domain-engine CAPAG como específico do projeto, não genérico.
- O documento não descreve nenhuma etapa posterior à criação de TASKs.
