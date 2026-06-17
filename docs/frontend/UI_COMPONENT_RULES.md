# CAPAG Analytics - UI Component Rules

## Objetivo

Este arquivo define regras objetivas para componentes do frontend CAPAG Analytics.

Implemente componentes com React, Tailwind CSS e shadcn/ui, usando `frontend/src/styles/globals.css` como fonte de tokens. A referencia visual aprovada esta em `docs/reference/CAPAG Analytics Design System`.

## Regras Gerais

- Tema claro apenas.
- Componentes devem usar CSS variables e classes Tailwind, nao valores soltos.
- Componentes shadcn devem ser adaptados ao visual CAPAG.
- Use `lucide-react` para icones quando o frontend existir.
- Nao copie bundles gerados como codigo fonte.
- Botoes e controles devem ter foco visivel.
- Valores financeiros e percentuais devem usar `.tnum`.
- Textos devem seguir portugues do Brasil, tom tecnico e direto.

## Sidebar

Uso: navegacao fixa do shell administrativo.

Estrutura:

- largura fixa de `--sidebar-width` (`240px`)
- altura total da viewport
- fundo `--sidebar-bg`
- borda direita `1px solid var(--border)`
- topo com marca "CAPAG Analytics"
- lista de itens com `id`, `label`, `icon` e badge opcional
- footer opcional para usuario/conta

Aparencia:

- item ativo usa `--sidebar-active-bg` e `--sidebar-active-fg`
- item normal usa `--sidebar-item`
- hover usa `--sidebar-item-hover`
- icones herdam cor do item
- altura de item: 38px
- radius: `--radius-md`

Itens padrao quando aplicavel:

- Dashboard
- Balanco Patrimonial
- Indicadores CAPAG
- Auditoria
- Importar ECD

Proibicoes:

- Nao usar sidebar escura.
- Nao usar gradiente.
- Nao usar menu com cards internos.
- Nao usar texto promocional.

## Topbar

Uso: barra superior pareada com a Sidebar.

Estrutura:

- altura `--topbar-height` (`60px`)
- fundo `--surface-card`
- borda inferior `1px solid var(--border)`
- titulo a esquerda
- subtitulo ou breadcrumb opcional
- acoes a direita

Aparencia:

- sem sombra
- titulo em `--text-xl`, peso 600
- subtitulo em `--text-sm`, `--text-secondary`
- acoes com gap `--space-3`

Proibicoes:

- Nao transformar topbar em hero.
- Nao colocar cards dentro da topbar.
- Nao usar busca ou acoes que quebrem o alinhamento em telas administrativas.

## Card

Uso: superficie branca para paineis, secoes e blocos de informacao.

Aparencia:

- fundo `--surface-card`
- borda `1px solid var(--border)`
- radius `--radius-lg`
- sombra `--shadow-xs`
- padding padrao `--space-6`

CardHeader:

- titulo em `--text-lg`, peso 600
- subtitulo em `--text-sm`, `--text-secondary`
- action opcional alinhada a direita

Proibicoes:

- Nao usar sombra forte.
- Nao usar borda lateral colorida.
- Nao aninhar cards dentro de cards.
- Nao usar cards para tudo: secoes de pagina devem ser layouts, cards sao itens/painel reais.

## StatCard

Uso: indicadores calculados no topo do dashboard.

Conteudo:

- label curto em uppercase/eyebrow
- valor grande em `--text-2xl`, peso 600
- hint opcional
- icone opcional de apoio

Tons permitidos:

- `neutral`
- `primary`
- `success`
- `warning`
- `danger`

Regra de dominio:

- usar para CAPAG, Liquidez, Endividamento e Poupanca Corrente
- nunca usar para linhas brutas do Balanco Patrimonial

## Button

Uso: comando administrativo.

Variantes:

- `primary`: acao principal da tela
- `secondary`: acao neutra
- `ghost`: toolbar, baixo destaque
- `danger`: destrutiva

Tamanhos:

- `sm`: 32px
- `md`: 38px

Regras:

- usar no maximo um botao `primary` por regiao de decisao
- usar icone a esquerda/direita quando facilitar reconhecimento
- hover do primary escurece para `--primary-hover`
- secondary e ghost usam `--surface-muted` no hover
- disabled usa opacidade reduzida

Proibicoes:

- Nao criar novas variantes sem atualizar este arquivo.
- Nao usar botoes coloridos para status.
- Nao usar texto longo dentro de botao.

## Badge

Uso: status, contadores e categorias curtas.

Variantes:

- `neutral`
- `primary`
- `success`
- `warning`
- `danger`

Aparencia:

- pill com `--radius-full`
- fundo suave + texto solido
- nunca solido saturado
- altura aproximada: 22px
- label de uma ou duas palavras

Exemplos:

- `Incluida`
- `Excluida`
- `CAPAG B`
- `Revisar`
- `18 contas`

## Switch

Uso principal: incluir ou excluir conta dos calculos CAPAG.

Contrato:

- componente controlado
- recebe `checked`
- emite `onChange(next)`
- sempre tem `aria-label`

Tamanhos:

- `sm`: linhas de conta
- `md`: configuracoes pontuais

Tons:

- `solid`: uso geral
- `soft`: linhas repetidas do balanco, com azul translucido

Regra de dominio:

- desligado significa conta fora dos calculos
- linha excluida deve ficar com opacidade aproximada de 55%
- nome e valor da conta devem ficar tachados

## Input

Uso: busca e entrada simples.

Aparencia:

- altura `sm` 32px ou `md` 38px
- fundo `--surface-card`
- borda `--border-strong`
- radius `--radius-md`
- icone opcional a esquerda
- foco com borda `--ring` e halo azul translucido

Uso recomendado:

- busca de conta ou grupo
- busca em auditoria
- filtros textuais simples

Proibicoes:

- Nao usar para formularios longos sem desenhar padrao especifico.
- Nao usar placeholder como unica instrucao critica.

## SegmentedControl

Uso: alternar entre 2 ou 3 modos mutuamente exclusivos.

Uso principal:

- alternar Balanco Patrimonial entre `Duas colunas` e `Livro-razao`

Contrato:

- controlado por `value`
- emite `onChange(id)`
- opcoes tem `id`, `label` e icone opcional

Aparencia:

- wrapper com `--surface-muted`
- borda `--border`
- item selecionado com `--surface-card` e `--shadow-xs`
- labels curtos

## Accordion

Uso: grupo colapsavel generico.

Regras:

- header com chevron
- meta opcional a direita
- `defaultOpen` para uso simples
- `open` + `onToggle` para uso controlado
- para Balanco Patrimonial, preferir `BalanceGroup`

## Dialog

Uso: modal para auditoria, detalhes e fluxos secundarios.

Aparencia:

- scrim `rgba(15, 23, 42, 0.40)`
- blur minimo `blur(1px)`
- painel `--surface-card`
- radius `--radius-xl`
- sombra `--shadow-overlay`
- largura padrao proxima de 720px
- header com titulo e subtitulo
- footer opcional com acoes alinhadas a direita

Comportamento:

- fecha com Escape
- fecha ao clicar no scrim quando apropriado
- botao fechar com `aria-label="Fechar"`

Regra de dominio:

- tabela analitica de auditoria deve aparecer em Dialog ou tela secundaria, nunca como bloco central do dashboard.

## DataTable / Table

Uso: dados analiticos, especialmente auditoria.

Aparencia:

- borda `1px solid var(--border)`
- radius `--radius-lg`
- header com `--surface-inset`
- header uppercase, `--text-xs`, peso 600
- linhas alternadas entre `--surface-card` e `--surface-inset`
- valores numericos com `.tnum`
- colunas monetarias alinhadas a direita

Contrato recomendado:

- `columns`: `key`, `header`, `align`, `width`, `numeric`, `wrap`, `render`
- `rows`: array de objetos
- `emptyText`: padrao `Sem registros.`

Proibicoes:

- Nao usar tabela analitica no centro do dashboard.
- Nao usar tabela para representar o Balanco Patrimonial principal.

## BalanceGroup

Uso: macrogrupo colapsavel do Balanco Patrimonial em duas colunas.

Conteudo:

- nome do grupo
- quantidade de contas
- total formatado
- percentual opcional
- acao de auditoria do grupo
- filhos `AccountRow`

Layout:

- Ativos na coluna esquerda
- Passivos e Patrimonio Liquido na coluna direita
- macrogrupo em uppercase
- fundo do header `--surface-muted`
- corpo com linhas de conta

## AccountRow

Uso: uma conta contabil dentro de `BalanceGroup`.

Conteudo:

- nome da conta
- codigo contabil opcional
- valor formatado
- switch incluir/excluir
- acao `Auditar conta` / `Ver auditoria`

Aparencia:

- linha recuada sob macrogrupo
- valor alinhado a direita
- codigo em fonte pequena e tabular
- hover com `--surface-inset`
- excluida: opacidade aproximada de 55% + tachado em nome e valor

Proibicoes:

- Nao chamar acao de auditoria de filtro.
- Nao usar funil como icone de auditoria.
- Nao esconder conta excluida.

## BalanceLedger

Uso: visao alternativa de Balanco Patrimonial em coluna unica, tipo livro-razao.

Regras:

- renderizar uma secao para Ativos
- renderizar uma secao para Passivos e Patrimonio Liquido
- colunas alinhadas: Conta, %, Valor, Incluir, Auditar
- macrogrupos em uppercase
- contas recuadas como subgrupos
- alternar contra `Duas colunas` usando `SegmentedControl`

Uso recomendado:

- larguras menores
- revisao densa
- comparacao vertical por grupos

## Textos E Nomenclatura

Use:

- `Importar ECD`
- `Exportar CSV`
- `Auditoria`
- `Auditar conta`
- `Ver auditoria`
- `Fechar`
- `Indicadores calculados`
- `Balanco Patrimonial`
- `Aplicacoes`
- `Origens`
- `Sem registros.`

Nao use:

- `filtro` para auditoria
- emojis
- textos promocionais
- explicacoes de feature dentro da interface
