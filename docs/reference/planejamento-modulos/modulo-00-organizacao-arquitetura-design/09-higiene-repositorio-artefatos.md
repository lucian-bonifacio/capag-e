# 09 - Higiene do repositorio e artefatos

## Objetivo

Definir o que deve e o que nao deve ficar versionado no repositorio, reduzindo ruido antes das mudancas maiores.

## Ponto de decisao

Decidir a politica de artefatos versionados, temporarios e gerados.

## Arquivos e pastas correlatos

- `.gitignore`
- `web/dist/`
- `web/node_modules/`
- `web/package-lock.json`
- `src/**/__pycache__/`
- `tests/**/__pycache__/`
- `tests/fixtures/`
- `tests/golden/`
- `tests/design-previews/`
- `docs/samples/`
- `worklog/`
- `tmp_deu_a_louca/`
- `src/capag/assets/`

## Detalhamento

- Classificar artefatos:
  - fonte versionada;
  - asset interno versionado;
  - fixture de teste;
  - golden file;
  - preview de design;
  - sample documental;
  - build gerado;
  - cache local;
  - temporario de planejamento.
- Definir politica para:
  - `node_modules`;
  - `dist`;
  - `__pycache__`;
  - arquivos `.pyc`;
  - samples ECD grandes;
  - worklogs;
  - arquivos temporarios.
- Definir se `tmp_deu_a_louca/` sera mantida temporariamente, arquivada depois ou convertida em docs/tasks oficiais.
- Verificar se `.gitignore` precisa ser atualizado em task futura.

## Entregavel

Politica de higiene do repositorio e artefatos.

## Criterios de sucesso

- Fica claro o que pode ser versionado.
- Caches e builds deixam de contaminar revisoes.
- Assets metodologicos e fixtures importantes continuam preservados.

## Fora do escopo

- Apagar arquivos agora.
- Rodar limpeza destrutiva.
- Alterar `.gitignore` agora.

