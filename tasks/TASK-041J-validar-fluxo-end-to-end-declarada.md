# TASK-041J - Validar fluxo end-to-end da camada declarada

## SPEC De Origem

- `specs/SPEC-002-modulo-1-camada-declarada.md`

## Dependencias

- `TASK-041F-criar-importacao-ecd-oficial.md`
- `TASK-041G-executar-camada-declarada-ecd-importada.md`
- `TASK-041H-integrar-ui-analise-importada-real.md`
- `TASK-041I-criar-exportacao-excel-acionavel-analise.md`
- `TASK-041K-configurar-playwright-e2e-camada-declarada.md`

## Objetivo

Consolidar validacoes end-to-end da camada declarada, cobrindo importacao ECD, parser, persistencia, execucao declarada, API, UI e Excel.

## Fontes Usadas

- `docs/product/PRD.md`
- `docs/architecture/architecture.md`
- `specs/SPEC-002-modulo-1-camada-declarada.md`

## Escopo Exato

- Criar teste end-to-end automatizado ou integracao equivalente em Docker.
- Cobrir ECD valida.
- Cobrir ECD sem `I051`.
- Cobrir codigo referencial ausente no plano oficial.
- Cobrir regra metodologica ausente.
- Cobrir regra bloqueada.
- Cobrir prefixo perigoso.
- Validar que API, UI e Excel refletem snapshots, sem recalcular fora do backend.

## Fora De Escopo

- Criar novas regras metodologicas reais.
- Criar reclassificacao comportamental.
- Criar laudo final.
- Usar ECD real sensivel no repositorio.

## Passos Executaveis

1. Orquestrar ambiente Docker para teste e2e.
2. Importar fixtures governadas.
3. Executar camada declarada.
4. Validar endpoints, UI e Excel.
5. Registrar limitacoes operacionais restantes, se existirem.

## Arquivos Ou Areas Provaveis

- `backend/tests/`
- `frontend/src/test/`
- `docker-compose.yml`
- `logs/`

## Criterios De Aceite

- Fluxo ECD fixture -> importacao -> run declarado -> consulta UI/API -> Excel e validado.
- Golden cases da SPEC-002 passam.
- Nenhuma etapa usa `float`.
- Frontend e Excel nao recalculam regra.

## Validacao Esperada

- Executar testes backend via `docker compose`.
- Executar testes/build frontend via `docker compose`.
- Executar teste e2e ou roteiro automatizado equivalente em Docker.

## Riscos

- Risco: teste e2e ficar fragil por maturidade inicial do produto.
  Mitigacao: manter fixture pequena, deterministica e focada nos contratos da SPEC-002.

## Bloqueios Pendentes

Bloqueada ate importacao, run declarado, UI real e exportacao acionavel existirem.
