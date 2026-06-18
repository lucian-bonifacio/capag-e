# TASK-084 - Testes de governanca e documentos operacionais finais

## SPEC De Origem

- `specs/SPEC-009-modulo-8-governanca-metodologia.md`

## Dependencias

- `TASK-081-validacoes-cobertura-metodologica.md`
- `TASK-082-criar-changelog-metodologico.md`
- `TASK-083-criar-ui-governanca-metodologica.md`

## Objetivo

Consolidar testes de governança metodológica e atualizar documentos operacionais e skills apenas ao final do ciclo, conforme a SPEC-009.

## Fontes Usadas

- `docs/product/PRD.md`
- `docs/architecture/architecture.md`
- `specs/SPEC-009-modulo-8-governanca-metodologia.md`
- `AGENTS.md`
- `README.md`
- `TODOLIST.md`

## Escopo Exato

- Testar validações de assets e cobertura.
- Testar matriz e changelog.
- Atualizar documentos operacionais finais quando o ciclo funcional estiver consolidado.
- Atualizar skills/instruções apenas se houver decisão explícita e fonte governada.

## Fora De Escopo

- Alterar metodologia sem SPEC/manual/teste.
- Editar regras pela UI.
- Atualizar documentos operacionais antes dos módulos funcionais.
- Criar nova funcionalidade de domínio.

## Passos Executaveis

1. Executar testes de governança.
2. Conferir cobertura metodológica.
3. Atualizar documentos operacionais finais conforme evidência.
4. Atualizar skills apenas quando autorizado.

## Arquivos Ou Areas Provaveis

- `backend/tests/`
- `docs/methodology/`
- `README.md`
- `AGENTS.md`
- `TODOLIST.md`
- `.agents/skills/`, se autorizado

## Criterios De Aceite

- Testes de governança passam via Docker Compose.
- Documentos operacionais refletem comportamento real.
- Skills só são alteradas com autorização e fonte governada.

## Validacao Esperada

- Executar testes/validações via `docker compose`.
- Revisar diff de documentos operacionais.

## Riscos

- Risco: atualizar instruções antes da implementação real.
  Mitigação: dependência explícita dos módulos e evidência de comportamento.

## Bloqueios Pendentes

Bloqueada até validações, changelog e UI de governança existirem, e até decisão explícita para atualização de skills.
