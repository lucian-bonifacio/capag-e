# TASK-009 - Auditar assets metodologicos e versionamento

## SPEC De Origem

- `specs/SPEC-001-modulo-0-fundacao-governada.md`

## Dependencias

- `TASK-002-auditar-estrutura-minima-repositorio.md`
- `TASK-005-auditar-indice-e-rastreabilidade-de-specs.md`
- `TASK-006-auditar-validacoes-minimas-do-projeto.md`

Esta TASK so deve ser executada depois que a estrutura minima, o estado das SPECs e as validacoes minimas estiverem auditados.

## Objetivo

Auditar se o projeto possui estrutura, convencao e validacoes previstas para assets metodologicos versionados, sem criar assets, alterar metodologia ou definir regras prudenciais nesta etapa.

## Fontes Usadas

- `docs/product/PRD.md`
- `docs/architecture.md`
- `specs/SPEC-001-modulo-0-fundacao-governada.md`
- relatorio esperado de `tasks/reports/TASK-002-auditoria-estrutura-minima.md`
- relatorio esperado de `tasks/reports/TASK-005-auditoria-specs.md`
- relatorio esperado de `tasks/reports/TASK-006-auditoria-validacoes.md`

## Escopo Exato

- Auditar se existe estrutura para assets metodologicos versionados.
- Auditar se ha convencao documentada para versao metodologica usada em analise, exportacao e laudo.
- Auditar se ha validacao automatizada ou planejada para assets metodologicos.
- Auditar se ha separacao clara entre:
  - documento governado;
  - asset metodologico versionado;
  - dado operacional persistido;
  - dado de auditoria;
  - resultado calculado.
- Registrar lacunas em relatorio documental.
- Propor proximas TASKs pequenas para estruturar assets, convencao de versao ou validacao, quando necessario.

## Fora De Escopo

- Criar assets metodologicos.
- Alterar metodologia.
- Alterar documentos em `docs/`.
- Alterar SPECs.
- Criar modelos de banco para `MethodologyVersion`.
- Criar migracoes.
- Criar validadores automatizados.
- Definir regras prudenciais, formulas, arredondamento ou golden cases.
- Usar `docs/reference/` como fonte normativa direta para implementar regra.
- Atualizar `tasks/README.md`.

## Passos Executaveis

1. Ler os relatorios das TASKs 002, 005 e 006.
2. Verificar se existe diretorio ou convencao para assets metodologicos.
3. Verificar se documentos governados citam versionamento metodologico suficiente para proxima etapa estrutural.
4. Verificar se ha comandos, scripts ou testes de validacao de assets.
5. Criar relatorio em `tasks/reports/TASK-009-auditoria-assets-metodologicos.md`.
6. Registrar lacunas sem corrigi-las.
7. Classificar lacunas como documentais, estruturais, tecnicas ou bloqueadas por SPEC funcional posterior.
8. Sugerir proximas TASKs pequenas para lacunas encontradas.
9. Validar que nenhum asset, documento governado, SPEC, codigo ou teste foi alterado durante a execucao.

## Arquivos Ou Areas Provaveis

- `tasks/reports/TASK-009-auditoria-assets-metodologicos.md`
- raiz do repositorio apenas para leitura
- `docs/` apenas para leitura
- `specs/` apenas para leitura
- diretorios de assets existentes apenas para leitura, se existirem

## Criterios De Aceite

- Existe relatorio em `tasks/reports/TASK-009-auditoria-assets-metodologicos.md`.
- O relatorio cita a SPEC de origem.
- O relatorio identifica se existe estrutura de assets metodologicos versionados.
- O relatorio registra se ha convencao de versao metodologica.
- O relatorio registra se ha validacao automatizada ou lacuna de validacao.
- O relatorio separa lacunas documentais, estruturais, tecnicas e bloqueadas por SPEC posterior.
- O relatorio sugere proximas TASKs pequenas quando houver lacunas.
- Nenhum asset, documento governado, SPEC, codigo ou teste e criado ou alterado.

## Validacao Esperada

- Executar `test -f tasks/reports/TASK-009-auditoria-assets-metodologicos.md`.
- Executar `git diff --stat` e confirmar que a execucao alterou apenas `tasks/reports/TASK-009-auditoria-assets-metodologicos.md`.
- Conferir manualmente que o relatorio nao define regra prudencial, formula, arredondamento, golden case ou contrato funcional.

## Riscos

- Risco: auditoria virar criacao de metodologia.
  Mitigacao: limitar esta TASK a inventario, lacunas e propostas de TASKs futuras.

- Risco: tratar referencia historica como fonte normativa.
  Mitigacao: registrar que `docs/reference/` nao autoriza regra nova sem SPEC governada suficiente.

- Risco: misturar asset versionado com dado operacional ou resultado calculado.
  Mitigacao: exigir classificacao explicita das lacunas e separacao de responsabilidades.

## Bloqueios Pendentes

Bloqueada ate a execucao das TASKs 002, 005 e 006.

Permanece bloqueado qualquer trabalho que tente criar asset metodologico, alterar metodologia, definir regra prudencial, criar migration, criar validador ou estabelecer golden case durante esta TASK.
