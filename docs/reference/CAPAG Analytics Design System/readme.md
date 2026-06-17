# CAPAG Analytics — Design System

Sistema de design para o **CAPAG Analytics**, um sistema administrativo interno que importa arquivos **ECD**, estrutura dados contábeis, exibe o **Balanço Patrimonial**, calcula indicadores **CAPAG** (Capacidade de Pagamento) e apoia a **auditoria analítica** das contas.

O objetivo deste design system é dar regras visuais objetivas para o desenvolvimento frontend — sem depender de interpretação subjetiva de prints. Base técnica: **shadcn/ui + Tailwind CSS + React + Inter**, tema claro.

## Sources
Este design system foi especificado a partir de um **brief textual** (não houve codebase nem Figma anexados). Toda a paleta, tipografia e regras de componentes derivam diretamente desse brief. Se um codebase ou Figma existir, anexe-o para alinhar os componentes ao código real.

---

## Princípios

1. **Objetivo e discreto.** Tela administrativa limpa e profissional. Sem gradientes, sem sombras fortes, sem excesso de cores.
2. **Indicadores antes de números crus.** O topo do dashboard mostra valores *calculados* (CAPAG, Liquidez, Endividamento, Poupança Corrente), nunca linhas brutas do balanço.
3. **Balanço em duas visualizações.** O usuário alterna (via `SegmentedControl`) entre **Duas colunas** (Ativos à esquerda; Passivos e PL à direita, grupos colapsáveis) e **Livro-razão** (coluna única, colunas alinhadas — melhor em larguras menores). Nunca tabela como bloco central.
4. **Inclusão/exclusão por switch.** Cada conta tem um switch que a inclui ou exclui dos cálculos.
5. **Auditoria fora do dashboard.** A tabela analítica só aparece em modal/dialog ou tela secundária. O ícone que a abre chama-se "Auditar conta" / "Ver auditoria" — **nunca** "filtrar".
6. **A paleta é fixa.** Não alterar sem solicitação explícita.

---

## CONTENT FUNDAMENTALS

**Idioma:** Português do Brasil. Terminologia contábil/pública (ECD, Balanço Patrimonial, Ativo Circulante, Patrimônio Líquido, CAPAG, RCL).

**Tom:** Técnico, neutro, direto. É uma ferramenta de trabalho para analistas e auditores — sem marketing, sem entusiasmo, sem exclamações.

**Pessoa:** Impessoal. Rótulos são substantivos ("Indicadores calculados", "Balanço Patrimonial", "Auditoria"). Ações são verbos no infinitivo ("Importar ECD", "Exportar CSV", "Auditar conta", "Fechar").

**Casing:** Title Case suave nos títulos de tela e grupos ("Balanço Patrimonial", "Ativo Circulante"). Rótulos *eyebrow* em MAIÚSCULAS com tracking largo ("INDICADORES CALCULADOS"). Sentence case no corpo.

**Números:** Moeda em formato BR — `R$ 4.210.500,00` (ponto de milhar, vírgula decimal). Percentuais com vírgula — `42,6%`. Sempre alinhados à direita e em **figuras tabulares** (classe `.tnum`).

**Nomenclatura proibida:** Nunca chamar o ícone de auditoria de "filtro". Usar "Auditar conta", "Ver detalhes" ou "Ver auditoria".

**Emoji:** Não. Nenhum emoji na interface.

**Exemplos de copy:**
- Botões: "Importar ECD", "Exportar CSV", "Auditoria", "Fechar"
- Eyebrows: "INDICADORES CALCULADOS", "APLICAÇÕES", "ORIGENS"
- Estado: "5 contas excluídas dos cálculos", "Capacidade de pagamento boa"
- Vazio: "Sem registros."

---

## VISUAL FOUNDATIONS

**Cores.** Paleta Slate (neutros) + Blue (primário), com acentos semânticos verde/âmbar/vermelho usados **apenas** para status. Nada saturado em superfícies grandes.
- Fundo app `#F8FAFC` · Card `#FFFFFF` · Texto principal `#0F172A` · Texto secundário `#64748B` · Borda `#E2E8F0`
- Primário `#2563EB`, hover `#1D4ED8` · Sucesso `#16A34A` · Alerta `#F59E0B` · Erro `#DC2626`
- Acentos semânticos aparecem como *soft fill + texto sólido* (ex.: badge sucesso = fundo `#F0FDF4`, texto `#15803D`), nunca como blocos sólidos saturados.

**Tipografia.** **Inter** para tudo. Pesos 400/500/600/700. Títulos de KPI em 28px/600 com tracking `-0.01em`. Corpo 14px. Valores financeiros sempre em figuras tabulares (`font-variant-numeric: tabular-nums`).

**Espaçamento.** Grade base de 4px, generosa. Padding de card `24px`; gap entre cards `16px`; conteúdo principal com padding `32px` e largura máxima `1280px` centralizada.

**Fundos.** Lisos. Fundo do app em slate-50; superfícies em branco puro. **Sem** imagens de fundo, **sem** gradientes, **sem** texturas ou padrões.

**Cantos.** Suaves: inputs/botões `6px`, cards `8px`, modais `12px`, pills/badges totalmente arredondados.

**Bordas.** 1px sólida em `#E2E8F0` (`--border`) é o divisor padrão — é o que separa cards, linhas de conta e cabeçalhos de tabela. Bordas fazem o trabalho que sombras fortes fariam em outros sistemas.

**Sombras.** Mínimas. Cards usam apenas `--shadow-xs` (quase imperceptível). A sombra mais forte permitida é a do modal (`--shadow-overlay`), ainda suave. Nunca sombras dramáticas.

**Cards.** Branco, borda 1px slate-200, raio 8px, `shadow-xs`. Sem borda colorida à esquerda, sem destaque de cor — apenas a superfície limpa.

**Animação.** Discreta e curta. Transições de 100–140ms em `ease` para hover de botão/linha, posição do knob do switch e rotação do chevron. Sem bounce, sem animações decorativas em loop.

**Hover.** Botão primário escurece para o azul-700; secundário/ghost recebem fundo `--surface-muted`; linhas de conta e itens de sidebar recebem fundo `--surface-inset`/`--surface-muted`. O botão de auditoria fica azul-soft no hover.

**Press / foco.** Sem "shrink". Foco visível = anel azul de 2px (`:focus-visible`), e inputs mostram um halo azul translúcido (`0 0 0 3px rgba(37,99,235,.12)`).

**Estado excluído.** Uma conta excluída dos cálculos é sinalizada por **opacidade ~55%** na linha inteira **+ texto tachado** (nome e valor com `line-through`); o switch fica cinza. Reforça visualmente que está fora dos cálculos, sem esconder a linha.

**Transparência/blur.** Uso mínimo. Apenas o scrim do modal (`rgba(15,23,42,.40)` + `backdrop-filter: blur(1px)`).

**Layout fixo.** Sidebar fixa de 240px à esquerda; topbar de 60px; área principal com rolagem e largura fluida até 1280px.

---

## ICONOGRAPHY

- **Estilo:** ícones de traço (stroke) ~2px, cantos arredondados — estilo **Lucide / Feather**. Combinam com a estética shadcn.
- **Implementação:** SVGs inline desenhados no estilo Lucide (sem dependência de fonte de ícone). Em produção, recomenda-se `lucide-react` para manter consistência exata.
- **Cor:** ícones herdam `currentColor`; em repouso usam `--text-muted`/`--text-secondary`, e a cor ativa/primária quando o item está selecionado ou em hover.
- **Tamanhos:** 15–18px dentro de botões e linhas; 16px nos KPIs.
- **Auditoria:** representada por uma **prancheta com check** (clipboard-check, estilo Lucide) — comunica "revisar/auditar conta". O botão é discreto (ghost): sem moldura em repouso, ganha fundo `--primary-soft` e borda `--blue-100` no hover. **Nunca** usar lupa (essa fica só na busca) nem funil/filtro para auditoria.
- **Switch das contas:** usa o tom `soft` (azul translúcido ~45%), menos chamativo que o switch sólido padrão, já que aparece repetido em muitas linhas.
- **Alternador de visualização:** `SegmentedControl` com ícones de colunas (duas colunas) e linhas (livro-razão).
- **Emoji / Unicode como ícone:** não usar.

> Substituição sinalizada: como nenhum codebase foi fornecido, os ícones são recriações no estilo Lucide. Se o produto usa um set específico, anexe-o e troco as recriações pelos assets reais.

---

## Index — conteúdo deste design system

**Foundations**
- `styles.css` — ponto de entrada (apenas `@import`s). Consumidores linkam este arquivo.
- `tokens/colors.css` · `tokens/typography.css` · `tokens/spacing.css` · `tokens/fonts.css` · `tokens/base.css`
- `guidelines/*.card.html` — specimens (cores, tipo, espaçamento, raio/sombra) exibidos na aba Design System.

**Components** (`components/`)
- `core/` — **Button**, **Badge**, **Switch** (tons `solid`/`soft`), **Input**, **Card** / **CardHeader** / **StatCard**
- `navigation/` — **Sidebar**, **Topbar**, **SegmentedControl** (alternador de visualização)
- `composite/` — **Accordion** (+ Chevron), **Dialog**, **DataTable**
- `balance/` — **BalanceGroup** + **AccountRow** (visão Duas colunas), **BalanceLedger** (visão Livro-razão), **AuditButton** (botão de auditoria compartilhado)

**UI Kits** (`ui_kits/`)
- `dashboard/` — recriação interativa do dashboard CAPAG Analytics: indicadores calculados, Balanço Patrimonial alternável entre **Duas colunas** e **Livro-razão** com switches de inclusão/exclusão, e auditoria analítica em modal.l.

**Outros**
- `SKILL.md` — torna este DS utilizável como Agent Skill.
- Cada componente tem `.d.ts` (contrato de props) e `.prompt.md` (uso) ao lado do `.jsx`.

> Arquivos gerados automaticamente pelo compilador (não editar): `_ds_bundle.js`, `_ds_manifest.json`, `_adherence.oxlintrc.json`.
