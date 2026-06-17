# Estrutura De Saida

Use esta estrutura como contrato padrao para projetos sem frontend existente:

```text
project-root/
├── AGENTS.md
├── docs/
│   └── frontend/
│       ├── DESIGN_TOKENS.md
│       ├── UI_COMPONENT_RULES.md
│       └── SCREEN_PATTERNS.md
└── frontend/
    └── src/
        └── styles/
            └── globals.css
```

## AGENTS.md

Criar na raiz do projeto.

Deve conter uma instrucao obrigatoria para qualquer IA ou agente antes de criar ou alterar frontend:

```md
Ao criar ou alterar qualquer tela do frontend, siga obrigatoriamente:

- docs/frontend/DESIGN_TOKENS.md
- docs/frontend/UI_COMPONENT_RULES.md
- docs/frontend/SCREEN_PATTERNS.md
- frontend/src/styles/globals.css

Nao invente nova estetica.
Nao altere cores, fonte, espacamentos, radius, sombras, sidebar, cards, botoes, badges, switches ou padroes de tela sem autorizacao explicita.
Implemente apenas dentro do padrao visual definido.
```

Se ja existir `AGENTS.md`, inserir uma secao de frontend sem remover instrucoes existentes.

## docs/frontend/DESIGN_TOKENS.md

Documentar:

- objetivo e escopo dos tokens
- tema permitido
- cores primitivas e semanticas
- fonte e escala tipografica
- espacamento
- bordas
- radius
- sombras
- focus ring
- estados visuais
- proibicoes
- processo de alteracao autorizado

## docs/frontend/UI_COMPONENT_RULES.md

Documentar regras por componente:

- Sidebar
- Topbar
- Card e StatCard
- Button
- Badge
- Switch
- Input
- Accordion
- Dialog
- Table/DataTable
- componentes de dominio encontrados na referencia

Para cada componente, definir uso, estrutura, aparencia, estados, acessibilidade minima e proibicoes.

## docs/frontend/SCREEN_PATTERNS.md

Documentar como montar telas recorrentes:

- Dashboard
- tela principal de analise
- auditoria
- importacao
- telas de detalhe
- estados vazios, carregando e erro

Para cada tela, definir hierarquia, layout, componentes permitidos, densidade, comportamento e o que nao fazer.

## frontend/src/styles/globals.css

Implementar CSS variables para os tokens documentados.

Quando o projeto ainda nao tiver frontend, criar somente a arvore minima e o arquivo de tokens. Nao criar uma aplicacao inteira sem pedido explicito.
