# Contrato React + Tailwind + shadcn/ui

Use este contrato quando o usuario escolher React, Tailwind CSS e shadcn/ui, ou quando nao houver stack frontend definida.

## Stack Padrao

- Framework: React
- Build futuro recomendado: Vite, salvo decisao diferente do projeto
- Estilizacao: Tailwind CSS
- Componentes base: shadcn/ui
- Primitivos: Radix UI via shadcn quando aplicavel
- Tokens: CSS variables em `frontend/src/styles/globals.css`
- Fonte: derivada da referencia; se a referencia nao definir, usar Inter

## Interpretacao Da Referencia

Uma pasta de referencia pode estar em HTML, CSS inline, JSX demonstrativo ou bundle gerado. Isso nao significa que a implementacao final deve copiar esse formato.

Converter:

- tokens CSS/JSON para CSS variables e documentacao
- componentes JSX/HTML demonstrativos para regras shadcn/Tailwind
- guidelines visuais para docs oficiais
- telas de exemplo para padroes de tela

Nao transformar bundle gerado em codigo fonte de producao.

## shadcn/ui

Ao formalizar componentes:

- assumir componentes em `frontend/src/components/ui/` quando o frontend existir
- usar variantes previsiveis para Button, Badge e similares
- usar classes Tailwind ligadas a CSS variables
- manter radius, bordas, sombras e cores da referencia
- adaptar o shadcn ao design aprovado, nao o contrario

Componentes como Dialog, Accordion, Switch e Table devem usar primitivos shadcn/Radix quando implementados no frontend real.

## Tailwind

`globals.css` deve expor tokens com CSS variables.

Preferir nomes estaveis e semanticos:

```css
:root {
  --background: ...;
  --foreground: ...;
  --card: ...;
  --card-foreground: ...;
  --primary: ...;
  --primary-foreground: ...;
  --border: ...;
  --ring: ...;
}
```

Se a referencia tiver tokens proprios, manter tambem aliases explicitos quando isso ajudar:

```css
:root {
  --capag-blue-600: ...;
  --capag-slate-900: ...;
}
```

## Regras De Governanca

Documentar que novas telas devem usar os tokens e componentes oficiais.

Mudancas visuais so podem ocorrer com autorizacao explicita e devem atualizar:

- `docs/frontend/DESIGN_TOKENS.md`
- `docs/frontend/UI_COMPONENT_RULES.md`
- `docs/frontend/SCREEN_PATTERNS.md`, se afetar telas
- `frontend/src/styles/globals.css`
