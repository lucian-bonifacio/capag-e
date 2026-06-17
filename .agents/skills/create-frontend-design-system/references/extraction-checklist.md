# Checklist De Extracao

Use este checklist antes de escrever os arquivos finais.

## Inventario

- Identificar todos os arquivos da pasta de referencia.
- Separar texto, codigo, manifestos, bundles, imagens e assets.
- Ler docs principais antes dos componentes.
- Ler tokens antes de gerar `globals.css`.
- Ler exemplos de tela antes de escrever `SCREEN_PATTERNS.md`.
- Registrar binarios por nome, tipo e papel esperado.

## Tokens

Extrair:

- tema claro/escuro permitido
- paleta primitiva
- aliases semanticos
- cor de fundo
- superficies
- texto
- bordas
- foco
- primario
- sucesso, alerta e erro
- fonte
- escala tipografica
- pesos
- line-height
- letter-spacing
- numerais tabulares
- espacamento
- largura de layout
- radius
- sombras
- transicoes

## Componentes

Para cada componente encontrado, extrair:

- funcao
- quando usar
- estrutura visual
- props/variantes relevantes
- estados
- acessibilidade minima
- texto permitido
- proibicoes
- relacao com componentes de dominio

Componentes comuns:

- Sidebar
- Topbar
- Button
- Badge
- Switch
- Input
- Card
- StatCard
- Accordion
- Dialog
- Table/DataTable
- componentes especificos do dominio

## Telas

Extrair:

- hierarquia de informacao
- layout principal
- componentes permitidos
- densidade
- filtros/busca
- modais
- tabelas
- indicadores
- estados vazios
- estados de erro
- comportamento responsivo quando inferivel

## Qualidade

Antes de finalizar, confirmar:

- os documentos sao prescritivos, nao apenas descritivos
- `globals.css` bate com `DESIGN_TOKENS.md`
- regras de componentes batem com `UI_COMPONENT_RULES.md`
- telas usam apenas componentes e tokens oficiais
- ha instrucao obrigatoria para IA em `AGENTS.md`
- lacunas foram marcadas como premissas
