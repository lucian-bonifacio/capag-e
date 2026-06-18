# Frontend CAPAG

Este diretorio contem a estrutura minima do frontend do CAPAG, conforme responsabilidades definidas em `docs/architecture/architecture.md`, `specs/SPEC-001-modulo-0-fundacao-governada.md` e documentos governados em `docs/frontend/`.

## Estrutura

- `src/components/`: componentes React futuros.
- `src/routes/`: organizacao futura de rotas.
- `src/styles/`: estilos globais e tokens runtime.
- `src/lib/`: utilitarios frontend futuros.
- `src/api/`: camada futura de cliente HTTP.
- `src/types/`: tipos e contratos frontend futuros.

## Fonte Visual Governada

- `frontend/src/styles/globals.css` permanece como fonte de tokens runtime.
- Alteracoes visuais devem seguir `docs/frontend/DESIGN_TOKENS.md`, `docs/frontend/UI_COMPONENT_RULES.md` e `docs/frontend/SCREEN_PATTERNS.md`.

## Proibicoes Nesta Fundacao

- Nao criar telas funcionais sem TASK e SPEC suficientes.
- Nao criar rotas definitivas nesta etapa.
- Nao criar cliente de API funcional nesta etapa.
- Nao recalcular motores prudenciais no frontend.
- Nao aplicar regra prudencial no frontend.
- Nao alterar status retornado pelo backend.
- Nao criar tokens visuais fora dos documentos governados.
- Nao criar ou exigir `node_modules` no host.

## Validacao Minima

Executar testes frontend pelo ambiente oficial:

```bash
COMPOSE_DISABLE_ENV_FILE=1 docker compose --profile test run --rm frontend-tests
```

O teste atual e apenas sentinela para validar o runner de Vitest e React Testing Library; ele nao define comportamento de tela, rota, API ou regra de negocio.
