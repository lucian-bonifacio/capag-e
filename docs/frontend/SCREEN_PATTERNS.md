# CAPAG Analytics - Screen Patterns

## Objetivo

Este arquivo define como montar telas do CAPAG Analytics sem inventar estetica.

Todas as telas devem usar os tokens de `docs/frontend/DESIGN_TOKENS.md`, os componentes de `docs/frontend/UI_COMPONENT_RULES.md` e as CSS variables de `frontend/src/styles/globals.css`.

## Shell Administrativo

Estrutura padrao:

```text
Viewport
├── Sidebar fixa (240px)
└── Area principal
    ├── Topbar fixa no topo (60px)
    └── Main com rolagem
```

Regras:

- Sidebar sempre a esquerda em desktop.
- Topbar sempre branca, com borda inferior e sem sombra.
- Main usa fundo `--bg-app`.
- Padding de main: `--space-8`.
- Conteudo pode ter largura maxima `--content-max`, salvo telas que exigem densidade menor.
- Nao criar landing page ou hero; a primeira tela deve ser uma ferramenta operacional.

## Dashboard

Objetivo: mostrar estado calculado do CAPAG e dar entrada para Balanco, Auditoria e Importacao.

Hierarquia:

1. Topbar com titulo da area e contexto do exercicio/entidade.
2. Bloco de indicadores calculados.
3. Balanco Patrimonial em duas visualizacoes.
4. Acoes de auditoria em modal ou tela secundaria.

Indicadores obrigatorios quando houver dados:

- Indicador CAPAG
- Liquidez Corrente
- Endividamento
- Poupanca Corrente

Regras:

- O topo do dashboard deve exibir indicadores calculados, nunca linhas brutas do balanco.
- Usar `StatCard` para indicadores.
- Usar `Badge warning` para informar contas excluidas dos calculos.
- Incluir busca por conta/grupo quando houver lista de contas.
- A acao `Auditoria` abre dialog ou tela secundaria.

Proibicoes:

- Nao colocar tabela analitica como bloco central.
- Nao usar graficos decorativos sem necessidade operacional.
- Nao misturar dados brutos e calculados sem rotulo claro.

## Balanco Patrimonial

Objetivo: revisar contas, alternar inclusao/exclusao e abrir auditoria.

Visualizacoes:

1. `Duas colunas`
   - Ativos a esquerda.
   - Passivos e Patrimonio Liquido a direita.
   - Grupos colapsaveis com `BalanceGroup`.
   - Contas com `AccountRow`.

2. `Livro-razao`
   - Coluna unica.
   - Colunas alinhadas: Conta, %, Valor, Incluir, Auditar.
   - Macrogrupos em uppercase.
   - Contas recuadas.

Controle:

- Usar `SegmentedControl` para alternar visualizacao.
- Labels: `Duas colunas` e `Livro-razao`.
- Icones: colunas e linhas, estilo Lucide.

Regras de conta:

- Cada conta deve ter switch de inclusao/exclusao.
- Conta excluida permanece visivel, com opacidade e tachado.
- Cada conta deve ter acao de auditoria.
- Grupos podem ter auditoria de grupo.

Proibicoes:

- Nao representar o Balanco Patrimonial principal como tabela central.
- Nao esconder contas excluidas.
- Nao chamar auditoria de filtro.

## Auditoria

Objetivo: exibir lancamentos, evidencias e detalhes analiticos sem poluir o dashboard.

Padroes permitidos:

- Dialog aberto a partir de conta, grupo ou acao geral.
- Tela secundaria de auditoria quando o volume for grande.

Dialog de auditoria:

- Titulo: `Auditoria - [Conta ou Grupo]`.
- Subtitulo: codigo, grupo, quantidade de contas ou total, quando disponivel.
- Mini indicadores no topo quando uteis: lancamentos, total debitos, total creditos.
- `DataTable` com colunas analiticas.
- Footer com `Fechar` e acao secundaria como `Exportar CSV`.

Tabela:

- Datas a esquerda.
- Historico com wrap.
- Documento com largura controlada.
- Debito e Credito alinhados a direita e com `.tnum`.
- Estado vazio: `Sem registros.`

Proibicoes:

- Nao abrir auditoria inline no dashboard.
- Nao usar funil ou termo `filtro` para auditoria.
- Nao saturar a tela com cores semanticas por linha.

## Importacao ECD

Objetivo: permitir entrada de arquivos ECD e orientar validacao/importacao.

Padrao de tela:

- Topbar com titulo `Importar ECD`.
- Card principal com area de selecao/upload.
- Card ou bloco secundario com status de processamento.
- Lista de validacoes em tabela simples ou lista de eventos.
- Acoes: `Selecionar arquivo`, `Importar ECD`, `Cancelar`, `Ver erros`.

Estados:

- Inicial: area vazia, instrucao objetiva e botao de selecao.
- Processando: indicar etapa atual sem animacao decorativa.
- Sucesso: badge `success`, resumo objetivo.
- Alerta: badge `warning`, itens revisaveis.
- Erro: badge `danger`, mensagem especifica e acao para detalhes.

Regras:

- Nao usar hero de upload.
- Nao usar ilustracoes decorativas.
- Nao esconder validacoes tecnicas.
- Usar linguagem impessoal e direta.

## Analise CAPAG

Objetivo: apresentar calculos, metodologia e status das contas consideradas.

Padrao:

- Indicadores calculados no topo.
- Secoes por indicador/metrica.
- Cards para resumo e status.
- Tabelas apenas para detalhes ou auditoria.
- Badges para status metodologico.

Conteudo esperado:

- CAPAG calculado.
- Liquidez.
- Endividamento.
- Poupanca Corrente.
- Contas incluidas/excluidas.
- Bloqueios ou pendencias.
- Link/acao para auditoria.

Regras:

- Separar resultado calculado de dado bruto.
- Usar `.tnum` em valores e percentuais.
- Sinalizar pendencias com `warning`, sem exagero de cor.
- Manter metodologia em tela secundaria, accordion ou detalhe, nao como texto longo no dashboard.

## Telas De Detalhe

Use quando uma entidade, conta, grupo, importacao ou indicador precisar de contexto adicional.

Padrao:

- Topbar com titulo especifico.
- Breadcrumb opcional.
- Cards de resumo no topo.
- Conteudo em secoes claras.
- Tabelas dentro de cards ou area secundaria.

Regras:

- Titulo deve ser substantivo claro.
- Acoes principais ficam na Topbar ou no header da secao.
- Evitar textos longos explicativos dentro da interface.

## Estados Vazios

Texto padrao: `Sem registros.`

Regras:

- Estado vazio deve ser discreto.
- Quando houver acao natural, exibir um botao claro.
- Nao usar ilustracoes grandes.
- Nao usar tom promocional.

Exemplos:

- `Sem contas importadas.`
- `Sem lancamentos para auditoria.`
- `Nenhuma pendencia encontrada.`

## Estados De Erro

Regras:

- Usar `Badge danger` ou texto `--danger-text`.
- Mensagem deve explicar o problema de forma objetiva.
- Oferecer acao recuperavel quando existir.
- Nao usar telas vermelhas ou blocos saturados grandes.

## Estados De Carregamento

Regras:

- Preferir skeletons discretos em `--surface-muted`.
- Evitar spinners grandes.
- Nao bloquear a tela inteira se apenas uma secao esta carregando.

## Responsividade

Como premissa inicial:

- Desktop e larguras medias sao prioridade operacional.
- Em larguras menores, usar `BalanceLedger` em vez de duas colunas.
- Topbar deve preservar titulo e acoes essenciais.
- Controles repetidos devem manter dimensoes estaveis.

## Conteudo E Linguagem

Use:

- Portugues do Brasil.
- Tom tecnico, neutro e direto.
- Acoes no infinitivo.
- Labels curtos.
- Title Case suave em titulos.
- Eyebrows em uppercase.

Nao use:

- emojis
- entusiasmo promocional
- texto explicando como usar a interface quando o componente e autoexplicativo
- termos ambiguos para auditoria

## Governanca

Novos padroes de tela so podem ser criados quando:

- nao houver padrao existente aplicavel
- a decisao for documentada neste arquivo
- os componentes e tokens usados estiverem documentados
- `globals.css` for atualizado se novos tokens forem autorizados
