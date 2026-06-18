# TASK-027 - Configurar dependencias frontend minimas

## SPEC De Origem

- `specs/SPEC-001-modulo-0-fundacao-governada.md`

## Dependencias

- `TASK-026-auditar-dependencias-frontend.md`

## Objetivo

Configurar dependencias frontend minimas para uso dentro de container conforme arquitetura e documentos visuais governados, sem criar telas, rotas, componentes de negocio ou consumo de API.

## Fontes Usadas

- `docs/architecture/architecture.md`
- `docs/frontend/DESIGN_TOKENS.md`
- `docs/frontend/UI_COMPONENT_RULES.md`
- `docs/frontend/SCREEN_PATTERNS.md`
- `specs/SPEC-001-modulo-0-fundacao-governada.md`
- log esperado de `logs/LOG-026-auditar-dependencias-frontend.md`

## Escopo Exato

- Criar ou ajustar configuracao de dependencias frontend se a auditoria indicar lacuna.
- Incluir apenas stack minima aprovada.
- Preservar tokens e documentos governados como fonte visual.
- Garantir que dependencias frontend sejam instaladas apenas dentro de container.

## Fora De Escopo

- Criar UI.
- Criar rotas funcionais.
- Criar cliente de API.
- Alterar tokens.
- Criar testes funcionais.
- Configurar CI.
- Criar ou exigir `node_modules` no host.
- Instalar dependencias no host ou globalmente.

## Passos Executaveis

1. Ler log da TASK-026.
2. Criar ou ajustar dependencias frontend minimas.
3. Validar instalacao/build apenas se comandos existirem.
4. Confirmar que nenhuma UI funcional foi criada.

## Arquivos Ou Areas Provaveis

- `frontend/package.json`
- lockfile correspondente, se aplicavel
- arquivos de config de tooling apenas se exigidos pela stack minima

## Criterios De Aceite

- Dependencias frontend minimas existem.
- O fluxo oficial de instalacao e execucao e via container.
- Nenhum `node_modules` no host e criado ou exigido.
- Nenhuma dependencia e instalada globalmente ou no host.
- Nenhuma tela, rota funcional, componente de negocio ou cliente de API e criado.

## Validacao Esperada

- Executar comando de instalacao/build definido, se disponivel.
- Executar `git diff --stat` e revisar escopo.

## Riscos

- Risco: dependencia puxar implementacao de UI.
  Mitigacao: limitar a configuracao de tooling.

## Bloqueios Pendentes

Bloqueada ate a execucao da TASK-026.
