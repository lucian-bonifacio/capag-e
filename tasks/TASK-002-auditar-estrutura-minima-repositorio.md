# TASK-002 - Auditar estrutura minima do repositorio

## SPEC De Origem

- `specs/SPEC-001-modulo-0-fundacao-governada.md`

## Objetivo

Auditar a estrutura atual do repositorio contra o contrato minimo definido na SPEC-001, identificando o que ja existe, o que falta e quais proximas TASKs estruturais devem ser criadas antes de qualquer implementacao funcional.

## Fontes Usadas

- `docs/product/PRD.md`
- `docs/architecture.md`
- `specs/SPEC-001-modulo-0-fundacao-governada.md`
- `AGENTS.md`

## Escopo Exato

- Verificar a existencia dos caminhos minimos definidos pela SPEC-001:
  - `AGENTS.md`;
  - `TODOLIST.md`;
  - `docs/architecture.md`;
  - `docs/product/PRD.md`;
  - `docs/frontend/`;
  - `specs/`;
  - `tasks/`;
  - `backend/`;
  - `frontend/`.
- Registrar lacunas estruturais no log da TASK.
- Classificar cada lacuna como:
  - ausente;
  - existente mas incompleta;
  - existente e suficiente para a proxima etapa.
- Propor proximas TASKs pequenas para lacunas encontradas.
- Confirmar que nenhuma regra funcional, prudencial, API ou tela sera definida nesta auditoria.

## Fora De Escopo

- Criar diretórios faltantes.
- Criar scaffolding de backend ou frontend.
- Alterar configuracao de projeto.
- Implementar FastAPI, React, banco, migrations, CI, engine, exportacao ou laudo.
- Definir contratos finais de endpoints.
- Definir regras prudenciais, formulas, politica de arredondamento ou golden cases.
- Atualizar `tasks/README.md` ou marcar status de outras TASKs.

## Passos Executaveis

1. Listar a raiz do repositorio e os diretorios governados relevantes.
2. Conferir cada caminho minimo previsto na SPEC-001.
3. Registrar evidencias objetivas de existencia ou ausencia.
4. Registrar os achados no log `logs/LOG-002-auditar-estrutura-minima-repositorio.md`.
5. No log, separar achados por caminho auditado.
6. No log, listar lacunas sem corrigi-las.
7. No log, sugerir proximas TASKs pequenas quando houver lacunas.
8. Validar que nenhum arquivo funcional de backend, frontend, engine, banco, exportacao ou laudo foi alterado durante a execucao.

## Arquivos Ou Areas Provaveis

- `logs/LOG-002-auditar-estrutura-minima-repositorio.md`
- raiz do repositorio apenas para leitura
- `docs/` apenas para leitura
- `specs/` apenas para leitura
- `tasks/` apenas para leitura

## Criterios De Aceite

- O log da TASK existe em `logs/LOG-002-auditar-estrutura-minima-repositorio.md`.
- O log cita a SPEC de origem.
- O log lista todos os caminhos minimos previstos pela SPEC-001.
- Cada caminho auditado possui status objetivo.
- Lacunas estruturais sao registradas sem serem corrigidas nesta TASK.
- Proximas TASKs sugeridas sao pequenas e independentes.
- Nenhum arquivo funcional de backend, frontend, engine, banco, exportacao ou laudo e criado ou alterado.

## Validacao Esperada

- Executar `test -f logs/LOG-002-auditar-estrutura-minima-repositorio.md`.
- Executar `test ! -e tasks/reports/TASK-002-auditoria-estrutura-minima.md`.
- Executar `git diff --stat` e confirmar que a execucao nao alterou arquivos funcionais de backend, frontend, engine, banco, exportacao ou laudo.
- Conferir manualmente que o log nao define regra de dominio, API, formula, arredondamento ou padrao visual.

## Riscos

- Risco: transformar auditoria em correcao estrutural.
  Mitigacao: registrar lacunas e propor TASKs futuras, sem executar correcao nesta TASK.

- Risco: gerar uma TASK seguinte ampla demais.
  Mitigacao: sugerir apenas proximas TASKs pequenas, verificaveis e independentes.

- Risco: interpretar ausencia de diretorio como decisao arquitetural nova.
  Mitigacao: tratar ausencias como lacunas frente a SPEC-001, sem alterar o contrato.

## Bloqueios Pendentes

Nao ha bloqueio para executar esta TASK de auditoria documental.

Permanece bloqueado qualquer trabalho que tente corrigir lacunas, criar scaffolding, implementar codigo ou definir contratos funcionais durante esta TASK.
