# CAPAG Analytics - Design Tokens

## Objetivo

Este arquivo e a fonte unica de verdade dos tokens visuais do frontend CAPAG Analytics.

Toda tela em React, Tailwind CSS e shadcn/ui deve usar estes tokens. Nao crie novas cores, fontes, espacamentos, radius, bordas ou sombras sem autorizacao explicita e sem atualizar este arquivo junto com `frontend/src/styles/globals.css`.

Referencia aprovada: `docs/reference/CAPAG Analytics Design System`.

## Stack Visual

- Framework alvo: React.
- Estilizacao alvo: Tailwind CSS.
- Componentes base: shadcn/ui, adaptados ao visual CAPAG.
- Primitivos: Radix UI via shadcn quando aplicavel.
- Tokens runtime: CSS variables em `frontend/src/styles/globals.css`.
- Tema: claro apenas.

## Principios Visuais

- Interface administrativa objetiva, discreta e profissional.
- Sem dark mode.
- Sem gradientes.
- Sem sombras fortes.
- Sem fundos com imagens, texturas, padroes ou efeitos decorativos.
- Cores semanticas apenas para status, alertas e feedback.
- Bordas de 1px fazem a separacao visual principal.
- Numeros financeiros sempre usam figuras tabulares e alinhamento a direita.

## Cores Primitivas

### Slate

| Token | Valor | Uso |
| --- | --- | --- |
| `--slate-50` | `#F8FAFC` | fundo do app, superficies inset |
| `--slate-100` | `#F1F5F9` | superficies muted e hover leve |
| `--slate-200` | `#E2E8F0` | bordas padrao |
| `--slate-300` | `#CBD5E1` | bordas fortes, switch off |
| `--slate-400` | `#94A3B8` | texto muted, placeholders |
| `--slate-500` | `#64748B` | texto secundario |
| `--slate-600` | `#475569` | itens de navegacao |
| `--slate-700` | `#334155` | texto de linhas e contas |
| `--slate-800` | `#1E293B` | texto forte auxiliar |
| `--slate-900` | `#0F172A` | texto principal |

### Blue

| Token | Valor | Uso |
| --- | --- | --- |
| `--blue-50` | `#EFF6FF` | fundo primario suave |
| `--blue-100` | `#DBEAFE` | borda primario suave |
| `--blue-500` | `#3B82F6` | switch soft e apoio visual |
| `--blue-600` | `#2563EB` | acao primaria e foco |
| `--blue-700` | `#1D4ED8` | hover primario e texto primario |

### Semanticas

| Token | Valor | Uso |
| --- | --- | --- |
| `--green-50` | `#F0FDF4` | sucesso suave |
| `--green-600` | `#16A34A` | sucesso |
| `--green-700` | `#15803D` | texto sucesso |
| `--amber-50` | `#FFFBEB` | alerta suave |
| `--amber-500` | `#F59E0B` | alerta |
| `--amber-600` | `#D97706` | texto alerta |
| `--red-50` | `#FEF2F2` | erro suave |
| `--red-600` | `#DC2626` | erro |
| `--red-700` | `#B91C1C` | texto erro |

## Aliases Semanticos

| Token | Valor | Uso |
| --- | --- | --- |
| `--bg-app` | `var(--slate-50)` | canvas da aplicacao |
| `--surface-card` | `#FFFFFF` | cards, paineis, sidebar, topbar |
| `--surface-muted` | `var(--slate-100)` | preenchimentos sutis e hover |
| `--surface-inset` | `var(--slate-50)` | areas internas, cabecalho de tabela |
| `--text-primary` | `var(--slate-900)` | titulos e valores principais |
| `--text-secondary` | `var(--slate-500)` | labels e metadados |
| `--text-muted` | `var(--slate-400)` | placeholder e disabled |
| `--text-on-brand` | `#FFFFFF` | texto sobre primario |
| `--border` | `var(--slate-200)` | divisor padrao |
| `--border-strong` | `var(--slate-300)` | inputs e bordas fortes |
| `--ring` | `var(--blue-600)` | foco |
| `--primary` | `var(--blue-600)` | acao primaria |
| `--primary-hover` | `var(--blue-700)` | hover primario |
| `--primary-soft` | `var(--blue-50)` | estado primario suave |
| `--primary-text` | `var(--blue-700)` | texto primario sobre fundo suave |
| `--success` | `var(--green-600)` | status sucesso |
| `--success-soft` | `var(--green-50)` | badge sucesso |
| `--success-text` | `var(--green-700)` | texto sucesso |
| `--warning` | `var(--amber-500)` | status alerta |
| `--warning-soft` | `var(--amber-50)` | badge alerta |
| `--warning-text` | `var(--amber-600)` | texto alerta |
| `--danger` | `var(--red-600)` | erro e destrutivo |
| `--danger-soft` | `var(--red-50)` | badge erro |
| `--danger-text` | `var(--red-700)` | texto erro |

## Aliases shadcn/ui

`globals.css` tambem deve expor aliases compativeis com shadcn:

- `--background`
- `--foreground`
- `--card`
- `--card-foreground`
- `--popover`
- `--popover-foreground`
- `--primary`
- `--primary-foreground`
- `--secondary`
- `--secondary-foreground`
- `--muted`
- `--muted-foreground`
- `--accent`
- `--accent-foreground`
- `--destructive`
- `--destructive-foreground`
- `--border`
- `--input`
- `--ring`

Esses aliases devem apontar para a paleta CAPAG. O shadcn deve se adaptar ao CAPAG, nao o contrario.

## Tipografia

- Fonte principal: Inter.
- Fonte mono auxiliar: JetBrains Mono.
- Corpo padrao: `0.875rem` (14px).
- Titulo de secao: `1.375rem` (22px), peso 600.
- Titulo de card: `1.125rem` (18px), peso 600.
- Valor de KPI: `1.75rem` (28px), peso 600.
- Micro labels e table meta: `0.75rem` (12px).

| Token | Valor |
| --- | --- |
| `--font-sans` | `"Inter", ui-sans-serif, system-ui, -apple-system, "Segoe UI", Roboto, Helvetica, Arial, sans-serif` |
| `--font-mono` | `"JetBrains Mono", ui-monospace, "SF Mono", Menlo, Consolas, monospace` |
| `--text-xs` | `0.75rem` |
| `--text-sm` | `0.8125rem` |
| `--text-base` | `0.875rem` |
| `--text-md` | `0.9375rem` |
| `--text-lg` | `1.125rem` |
| `--text-xl` | `1.375rem` |
| `--text-2xl` | `1.75rem` |
| `--text-3xl` | `2.25rem` |
| `--weight-normal` | `400` |
| `--weight-medium` | `500` |
| `--weight-semibold` | `600` |
| `--weight-bold` | `700` |
| `--leading-tight` | `1.2` |
| `--leading-snug` | `1.35` |
| `--leading-normal` | `1.5` |
| `--tracking-tight` | `-0.01em` |
| `--tracking-normal` | `0` |
| `--tracking-wide` | `0.04em` |
| `--num-tabular` | `"tnum" 1, "lnum" 1` |

Use `.tnum` em moeda, percentuais, codigos contabeis e totais financeiros.

## Espacamento

A escala e baseada em grid de 4px.

| Token | Valor |
| --- | --- |
| `--space-0` | `0` |
| `--space-1` | `0.25rem` |
| `--space-2` | `0.5rem` |
| `--space-3` | `0.75rem` |
| `--space-4` | `1rem` |
| `--space-5` | `1.25rem` |
| `--space-6` | `1.5rem` |
| `--space-8` | `2rem` |
| `--space-10` | `2.5rem` |
| `--space-12` | `3rem` |
| `--space-16` | `4rem` |

Regras:

- Padding principal de tela: `--space-8`.
- Gap comum entre cards: `--space-4`.
- Padding padrao de card: `--space-6`.
- Nao criar espacamentos arbitrarios quando um token atende.

## Layout

| Token | Valor | Uso |
| --- | --- | --- |
| `--sidebar-width` | `240px` | largura fixa da sidebar |
| `--topbar-height` | `60px` | altura da topbar |
| `--content-max` | `1280px` | largura maxima geral |
| `--content-pad` | `var(--space-8)` | padding de conteudo |

## Radius

| Token | Valor | Uso |
| --- | --- | --- |
| `--radius-sm` | `4px` | elementos pequenos |
| `--radius-md` | `6px` | botoes e inputs |
| `--radius-lg` | `8px` | cards e grupos |
| `--radius-xl` | `12px` | dialogs e paineis grandes |
| `--radius-full` | `9999px` | badges, pills e avatares |

Cards nao devem passar de 8px de radius salvo regra especifica. Dialogs podem usar 12px.

## Sombras

| Token | Valor | Uso |
| --- | --- | --- |
| `--shadow-xs` | `0 1px 2px 0 rgba(15, 23, 42, 0.04)` | cards |
| `--shadow-sm` | `0 1px 3px 0 rgba(15, 23, 42, 0.06), 0 1px 2px -1px rgba(15, 23, 42, 0.04)` | controles leves |
| `--shadow-md` | `0 4px 12px -2px rgba(15, 23, 42, 0.08), 0 2px 6px -2px rgba(15, 23, 42, 0.04)` | uso raro |
| `--shadow-overlay` | `0 12px 32px -8px rgba(15, 23, 42, 0.18), 0 4px 12px -4px rgba(15, 23, 42, 0.10)` | modais |

Nao usar sombras dramaticas.

## Estados

- Hover de botao primario: `--primary-hover`.
- Hover de botao secundario ou ghost: `--surface-muted`.
- Hover de linhas e itens: `--surface-inset` ou `--surface-muted`.
- Foco visivel: anel azul de 2px com `--ring`.
- Input focado: borda `--ring` e halo `0 0 0 3px rgba(37, 99, 235, 0.12)`.
- Conta excluida: opacidade aproximada de 55% na linha e `line-through` no nome e valor.

## Iconografia

- Usar icones de stroke com cerca de 2px, estilo Lucide/Feather.
- Em producao, preferir `lucide-react`.
- Icones herdam `currentColor`.
- Tamanhos usuais: 15px a 18px.
- Auditoria deve usar prancheta com check. Nao usar funil, filtro ou lupa para auditoria.
- Busca pode usar lupa.

## Proibicoes

- Nao criar dark mode.
- Nao usar gradientes.
- Nao usar hero visual, landing page ou estetica de marketing para telas operacionais.
- Nao usar roxo como tema dominante.
- Nao usar sombras fortes.
- Nao usar emoji na interface.
- Nao chamar auditoria de filtro.
- Nao colocar tabela analitica como bloco central do dashboard.
- Nao exibir linhas brutas do balanco no topo do dashboard no lugar de indicadores calculados.

## Processo De Alteracao

Qualquer alteracao visual autorizada deve atualizar, no mesmo trabalho:

- `docs/frontend/DESIGN_TOKENS.md`
- `docs/frontend/UI_COMPONENT_RULES.md`, se afetar componentes
- `docs/frontend/SCREEN_PATTERNS.md`, se afetar telas
- `frontend/src/styles/globals.css`
