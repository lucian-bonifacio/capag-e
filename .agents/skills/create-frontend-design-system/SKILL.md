---
name: create-frontend-design-system
description: Criar uma fonte unica de verdade visual para frontend a partir de uma pasta completa de referencia de design system, UI kit, tokens, componentes, exemplos, HTML, CSS, React ou imagens. Use quando o usuario quiser transformar uma referencia visual aprovada em docs oficiais de frontend, tokens CSS, contratos React/Tailwind/shadcn, regras para IA e estrutura inicial de frontend do projeto.
---

# Criar Frontend Design System

## Objetivo

Transformar uma pasta de referencia visual aprovada em uma fonte unica de verdade para o frontend do projeto.

A entrega deve permitir que outra IA crie ou altere telas sem inventar estetica, respeitando tokens, componentes, padroes de tela e contrato tecnico.

## Insumo Principal

Exija uma pasta de referencia visual antes de gerar a entrega.

Aceite como referencia:

- design system exportado
- UI kit
- tokens CSS/JSON
- componentes React/HTML/CSS
- screenshots, imagens e assets
- documentos de guidelines
- bundles ou manifestos gerados

Se o caminho nao existir, localize uma pasta equivalente antes de concluir que esta faltando.

## Workflow

1. Ler a pasta de referencia inteira como contexto.
2. Identificar arquivos textuais, binarios, bundles gerados, manifests, componentes, exemplos, tokens e guidelines.
3. Ler os arquivos textuais relevantes; para binarios, registrar tipo, nome e papel esperado sem despejar bytes.
4. Extrair as decisoes visuais aprovadas: cores, fonte, escala, espacamento, bordas, radius, sombras, layout, iconografia, estados e proibicoes.
5. Identificar a stack alvo. Quando o usuario nao disser outra coisa, usar React + Tailwind CSS + shadcn/ui.
6. Gerar ou atualizar a estrutura oficial do projeto.
7. Validar que os arquivos finais nao deixam margem para nova estetica arbitraria.

## Estrutura De Saida

Leia `references/output-structure.md` antes de criar arquivos no projeto.

Por padrao, gerar:

```text
AGENTS.md

docs/frontend/
├── DESIGN_TOKENS.md
├── UI_COMPONENT_RULES.md
└── SCREEN_PATTERNS.md

frontend/
└── src/
    └── styles/
        └── globals.css
```

Se arquivos existentes ja cobrirem parte dessa funcao, preserve conteudo valido e atualize de forma incremental.

## Contrato Tecnico

Leia `references/react-tailwind-shadcn-contract.md` quando a entrega envolver React, Tailwind ou shadcn/ui.

Formalize nos arquivos gerados:

- framework alvo
- padrao de estilização
- estrategia de tokens
- componentes base
- regras de proibicao
- como alterar o sistema visual com autorizacao explicita

## Checklist De Extracao

Leia `references/extraction-checklist.md` antes de escrever os documentos finais.

Use o checklist para garantir que a pasta de referencia foi convertida em regras objetivas, nao apenas resumida.

## Regras De Escrita

- Escrever documentos em Markdown claro, objetivo e acionavel.
- Usar portugues do Brasil quando o projeto ou usuario estiver em portugues.
- Separar regra visual, regra de componente e padrao de tela nos arquivos corretos.
- Nao inventar tokens que contradigam a referencia.
- Quando houver lacuna, assumir uma decisao minima, marcar como premissa e manter compatibilidade com a referencia.
- Nao copiar componentes demonstrativos como implementacao final sem adaptar ao contrato tecnico do projeto.
- Nao tratar bundle gerado como fonte primaria se houver componentes e tokens legiveis.

## Validacao

Antes de finalizar:

- Confirmar que `AGENTS.md` instrui IAs a seguir os arquivos oficiais antes de mexer no frontend.
- Confirmar que `globals.css` implementa CSS variables para os tokens documentados.
- Confirmar que `DESIGN_TOKENS.md`, `UI_COMPONENT_RULES.md` e `SCREEN_PATTERNS.md` existem e sao consistentes entre si.
- Confirmar que a stack React + Tailwind + shadcn/ui esta formalizada quando aplicavel.
- Confirmar que proibicoes visuais e processo de alteracao estao explicitos.
