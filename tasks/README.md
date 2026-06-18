# TASKs - CAPAG

## Objetivo

Este diretorio contem TASKs oficiais derivadas de SPECs suficientes.

O fluxo obrigatorio e:

```text
PRD + Arquitetura + Docs governados
        ↓
SPECs especializadas
        ↓
TASKs correspondentes
```

TASK nao substitui SPEC, nao decide arquitetura e nao cria regra de dominio.

A rastreabilidade obrigatoria de execucao e:

```text
PRD -> Arquitetura -> SPEC -> TASK
```

## Fontes Obrigatorias

Antes de criar ou revisar TASKs, leia as fontes aplicaveis:

- `docs/product/PRD.md`
- `docs/architecture/architecture.md`
- SPEC de origem em `specs/`
- documentos governados adicionais aplicaveis

Quando a TASK envolver UI, telas, componentes, UX ou visual, leia tambem:

- `docs/frontend/DESIGN_TOKENS.md`
- `docs/frontend/UI_COMPONENT_RULES.md`
- `docs/frontend/SCREEN_PATTERNS.md`
- `frontend/src/styles/globals.css`

## Convencao De Nomes

Use o formato:

```text
TASK-NNN-descricao-curta.md
```

Exemplo:

```text
TASK-001-criar-indice-e-convencao-de-tasks.md
```

## Tamanho Das TASKs

Prefira TASKs curtas, pequenas e verificaveis.

Quando a SPEC de origem for significativa, atravessar mais de uma camada ou tiver varios entregaveis independentes, divida o trabalho em mais de uma TASK. Cada TASK deve manter escopo executavel de forma independente, criterios de aceite proprios e dependencias explicitas.

Evite criar uma unica TASK grande quando o trabalho puder ser fatiado sem perder rastreabilidade.

## Ambiente Oficial

O ambiente oficial do projeto e exclusivamente Docker/Docker Compose.

Regras:

- comandos oficiais devem executar via `docker compose`;
- dependencias Python devem ser instaladas apenas dentro de imagem/container;
- dependencias Node devem ser instaladas apenas dentro de imagem/container;
- PostgreSQL deve rodar em container;
- testes, builds, migrations e validacoes devem rodar via container;
- o host deve exigir apenas Git, Docker e Docker Compose.

Proibicoes:

- nao criar ou exigir `.venv` local;
- nao criar ou exigir `node_modules` no host;
- nao usar `pip install` global;
- nao usar `npm install -g`, `pnpm add -g`, `yarn global` ou equivalente;
- nao exigir Python, Node, npm, pnpm, yarn ou pip instalados no host para operar o projeto.

Qualquer alternativa fora de Docker deve ser tratada como decisao futura explicita, fora do fluxo oficial da fundacao.

## Template Obrigatorio

Toda TASK deve conter:

```markdown
# TASK-NNN - Titulo

## SPEC De Origem

## Dependencias

## Objetivo

## Fontes Usadas

## Escopo Exato

## Fora De Escopo

## Passos Executaveis

## Arquivos Ou Areas Provaveis

## Criterios De Aceite

## Validacao Esperada

## Riscos

## Bloqueios Pendentes
```

## Bloqueios Obrigatorios

Nao crie TASK quando a SPEC de origem ainda tiver decisao essencial pendente.

TASK nao pode decidir:

- arquitetura;
- contrato de API;
- regra de dominio;
- formula prudencial;
- fonte normativa;
- politica de precisao ou arredondamento;
- padrao visual;
- estrategia critica de teste.

Se uma TASK precisar decidir qualquer item acima, a SPEC esta incompleta.

## Indice

| TASK | SPEC | Status | Objetivo |
| --- | --- | --- | --- |
| `TASK-001-criar-indice-e-convencao-de-tasks.md` | `SPEC-001-modulo-0-fundacao-governada.md` | Criada | Criar indice e convencao oficial de TASKs. |
