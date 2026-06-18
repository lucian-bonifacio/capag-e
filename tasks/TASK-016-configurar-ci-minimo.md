# TASK-016 - Configurar CI minimo

## SPEC De Origem

- `specs/SPEC-001-modulo-0-fundacao-governada.md`

## Dependencias

- `TASK-006-auditar-validacoes-minimas-do-projeto.md`
- `TASK-014-configurar-testes-backend-minimos.md`
- `TASK-015-configurar-testes-frontend-minimos.md`

Esta TASK so deve ser executada depois que as validacoes minimas de backend e frontend estiverem configuradas ou explicitamente dispensadas por log.

## Objetivo

Configurar um workflow minimo de CI para executar validacoes basicas do projeto em ambiente isolado, sem introduzir deploy, publicacao, secrets, validacoes prudenciais ou pipelines funcionais amplos.

## Fontes Usadas

- `docs/product/PRD.md`
- `docs/architecture/architecture.md`
- `specs/SPEC-001-modulo-0-fundacao-governada.md`
- log esperado de `logs/LOG-006-auditar-validacoes-minimas-do-projeto.md`

## Escopo Exato

- Criar workflow minimo em `.github/workflows/`.
- Executar validacoes backend minimas quando existirem.
- Executar validacoes frontend minimas quando existirem.
- Usar containers ou ambiente isolado equivalente no CI.
- Manter o workflow restrito a pull requests e pushes locais de branch, conforme convencao definida no projeto.
- Nao usar secrets.
- Nao configurar deploy.
- Nao criar validacoes metodologicas, migrations ou golden tests ainda, salvo se TASK anterior ja tiver criado comando minimo aprovado.

## Fora De Escopo

- Criar deploy.
- Configurar ambiente de producao ou staging.
- Criar secrets ou variaveis sensiveis.
- Criar testes novos.
- Criar migrations ou banco de CI.
- Criar validacao de assets metodologicos.
- Criar golden tests.
- Instalar ou alterar dependencias sem necessidade registrada.
- Usar instalacao global de dependencias no runner.
- Alterar backend ou frontend.
- Atualizar `tasks/README.md`.

## Passos Executaveis

1. Ler `logs/LOG-006-auditar-validacoes-minimas-do-projeto.md`.
2. Confirmar comandos minimos disponiveis para backend e frontend.
3. Criar `.github/workflows/ci.yml`.
4. Configurar jobs apenas para comandos existentes e aprovados pelas TASKs anteriores.
5. Garantir que o workflow nao dependa de secrets.
6. Garantir que o workflow nao execute deploy.
7. Validar sintaxe do YAML.
8. Validar que nenhum codigo backend/frontend/teste foi alterado durante a execucao.

## Arquivos Ou Areas Provaveis

- `.github/workflows/ci.yml`

## Criterios De Aceite

- A TASK-006 foi executada antes desta TASK.
- As TASKs 014 e 015 foram executadas ou explicitamente dispensadas.
- `.github/workflows/ci.yml` existe.
- O workflow executa apenas validacoes minimas ja existentes.
- O workflow nao usa secrets.
- O workflow nao faz deploy.
- O workflow nao depende de instalacao global no runner.
- Nenhum teste, backend, frontend, migration, asset ou golden case e criado nesta TASK.

## Validacao Esperada

- Executar validacao de sintaxe YAML disponivel no ambiente, se houver.
- Executar `git diff --stat` e confirmar que as alteracoes estao restritas a `.github/workflows/ci.yml`.
- Conferir manualmente que o workflow nao usa secrets e nao executa deploy.

## Riscos

- Risco: CI minimo virar pipeline amplo demais.
  Mitigacao: limitar o workflow a comandos ja existentes e aprovados por TASKs anteriores.

- Risco: introduzir secrets ou deploy prematuramente.
  Mitigacao: bloquear secrets, ambientes remotos e publicacao nesta TASK.

- Risco: CI quebrar por depender de estrutura ainda ausente.
  Mitigacao: depender das TASKs 014 e 015 ou registrar dispensa explicita antes de executar.

## Bloqueios Pendentes

Bloqueada ate a execucao da TASK-006 e das TASKs 014 e 015, salvo dispensa explicita documentada.

Permanece bloqueado qualquer trabalho que tente criar deploy, secrets, banco de CI, migrations, validacao metodologica, golden tests, testes novos ou alteracoes funcionais durante esta TASK.
