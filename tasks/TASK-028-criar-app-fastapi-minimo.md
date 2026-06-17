# TASK-028 - Criar app FastAPI minimo

## SPEC De Origem

- `specs/SPEC-001-modulo-0-fundacao-governada.md`

## Dependencias

- `TASK-003-criar-estrutura-backend-minima.md`
- `TASK-025-configurar-dependencias-backend-minimas.md`

## Objetivo

Criar uma aplicacao FastAPI minima para validar bootstrap do backend via container, sem endpoints funcionais de dominio, contratos de modulo, banco, parser, engine, exportacao ou laudo.

## Fontes Usadas

- `docs/architecture.md`
- `specs/SPEC-001-modulo-0-fundacao-governada.md`

## Escopo Exato

- Criar ponto de entrada minimo da aplicacao FastAPI.
- Criar endpoint tecnico de healthcheck se aprovado pela arquitetura.
- Garantir que OpenAPI seja gerado apenas com endpoints tecnicos minimos.

## Fora De Escopo

- Criar endpoints funcionais.
- Criar schemas de negocio.
- Criar autenticacao.
- Criar banco, repositories, migrations, parser ou engines.
- Criar frontend.

## Passos Executaveis

1. Verificar estrutura backend e dependencias.
2. Criar app FastAPI minimo.
3. Criar healthcheck tecnico simples, se aplicavel.
4. Validar import da aplicacao.
5. Confirmar ausencia de logica funcional.

## Arquivos Ou Areas Provaveis

- `backend/app/main.py`
- `backend/app/api/health.py`, se adotado
- teste sentinela de import, se permitido por TASK-014

## Criterios De Aceite

- App FastAPI importa sem erro.
- Validacao oficial executa via Docker/Docker Compose.
- Nao ha endpoint funcional de dominio.
- Healthcheck, se criado, nao acessa banco nem engine.

## Validacao Esperada

- Executar teste/import minimo definido.
- Executar `git diff --stat` e revisar escopo.

## Riscos

- Risco: healthcheck virar contrato funcional.
  Mitigacao: manter resposta tecnica minima.

## Bloqueios Pendentes

Bloqueada ate a execucao das TASKs 003 e 025.
