# TASK-011B - Reorganizar documentacao oficial de arquitetura

## SPEC De Origem

- `specs/SPEC-001-modulo-0-fundacao-governada.md`

## Dependencias

- `TASK-011-auditar-fronteiras-de-camadas.md`

Esta TASK so deve ser executada depois que a auditoria de fronteiras de camadas estiver homologada.

## Objetivo

Reorganizar a documentacao oficial de arquitetura para que a arquitetura principal passe de `docs/architecture.md` para `docs/architecture/architecture.md`, preparando o diretorio de arquitetura para artefatos complementares como fronteiras de camadas e ADRs, sem alterar decisoes tecnicas da arquitetura.

## Fontes Usadas

- `docs/product/PRD.md`
- `docs/architecture.md`
- `specs/SPEC-001-modulo-0-fundacao-governada.md`
- `tasks/README.md`
- `tasks/TASK-011A-criar-artefato-governado-fronteiras-camadas.md`
- `logs/LOG-011-auditar-fronteiras-de-camadas.md`

## Escopo Exato

- Criar o diretorio `docs/architecture/`.
- Mover `docs/architecture.md` para `docs/architecture/architecture.md`.
- Criar o diretorio `docs/architecture/adr/`.
- Atualizar `specs/SPEC-001-modulo-0-fundacao-governada.md` para refletir a nova estrutura documental oficial:
  - `docs/architecture/architecture.md` como documento principal de arquitetura;
  - `docs/architecture/` como diretorio de artefatos arquiteturais;
  - `docs/architecture/adr/` como local para decisoes arquiteturais futuras.
- Revisar e atualizar TASKs que citam `docs/architecture.md`, mantendo rastreabilidade para a nova localizacao.
- Revisar e atualizar documentos governados que citam `docs/architecture.md`, quando a referencia representar caminho oficial vigente.
- Atualizar `tasks/TASK-011A-criar-artefato-governado-fronteiras-camadas.md` para:
  - depender desta TASK;
  - usar `docs/architecture/architecture.md` como arquitetura principal;
  - criar `docs/architecture/layer-boundaries.md` como artefato futuro.
- Atualizar `ROADMAP.md` apenas se necessario para manter a proxima tarefa e a ordem logica.
- Registrar em log quais familias de arquivos foram revisadas.

## Fora De Escopo

- Alterar decisoes arquiteturais.
- Reescrever o conteudo tecnico de `docs/architecture.md` alem do necessario para mover o arquivo e ajustar referencias internas, se existirem.
- Alterar PRD.
- Alterar regras de dominio.
- Alterar contratos de API.
- Definir formula prudencial, fonte normativa, politica de precisao/arredondamento ou golden cases.
- Implementar codigo.
- Criar ou alterar backend, frontend, testes, CI, migrations ou assets.
- Criar o artefato de fronteiras de camadas; isso permanece escopo da `TASK-011A`.
- Reescrever logs historicos apenas para trocar caminhos antigos; logs devem permanecer como evidencia do estado em que foram criados.
- Alterar `AGENTS.md`, salvo aprovacao explicita do usuario durante a execucao.

## Passos Executaveis

1. Ler `docs/architecture.md`.
2. Ler `specs/SPEC-001-modulo-0-fundacao-governada.md`.
3. Ler `tasks/TASK-011A-criar-artefato-governado-fronteiras-camadas.md`.
4. Mapear citacoes de `docs/architecture.md` em documentos governados e TASKs.
5. Criar `docs/architecture/`.
6. Mover `docs/architecture.md` para `docs/architecture/architecture.md`.
7. Criar `docs/architecture/adr/` com arquivo sentinela, se necessario para versionar o diretorio.
8. Atualizar referencias oficiais em `specs/`, `tasks/`, `docs/` e `ROADMAP.md` quando aplicavel.
9. Atualizar `TASK-011A` para apontar o artefato futuro para `docs/architecture/layer-boundaries.md`.
10. Criar log em `logs/LOG-011B-reorganizar-documentacao-oficial-arquitetura.md`.
11. Validar que a reorganizacao nao alterou conteudo tecnico de arquitetura nem executou a `TASK-011A`.

## Arquivos Ou Areas Provaveis

- `docs/architecture.md`
- `docs/architecture/architecture.md`
- `docs/architecture/adr/.gitkeep`
- `specs/SPEC-001-modulo-0-fundacao-governada.md`
- `tasks/TASK-*.md`
- `docs/**/*.md`
- `ROADMAP.md`
- `logs/LOG-011B-reorganizar-documentacao-oficial-arquitetura.md`

## Criterios De Aceite

- `docs/architecture/architecture.md` existe.
- `docs/architecture.md` nao existe mais.
- `docs/architecture/adr/` existe e esta versionavel.
- `SPEC-001` reflete a nova estrutura documental oficial de arquitetura.
- `TASK-011A` aponta para `docs/architecture/layer-boundaries.md`.
- TASKs que citavam `docs/architecture.md` foram revisadas e atualizadas quando a referencia representa o caminho oficial vigente.
- Documentos governados que citavam `docs/architecture.md` foram revisados e atualizados quando a referencia representa o caminho oficial vigente.
- Logs historicos nao foram reescritos apenas para trocar caminhos antigos.
- Nenhuma decisao arquitetural, regra de dominio, contrato de API, formula prudencial, arredondamento, schema, endpoint, classe, teste ou configuracao e criada nesta TASK.

## Validacao Esperada

- Executar `test -f docs/architecture/architecture.md`.
- Executar `test ! -e docs/architecture.md`.
- Executar `test -d docs/architecture/adr`.
- Executar busca por `docs/architecture.md` em `specs/`, `tasks/`, `docs/` e `ROADMAP.md`, excluindo logs historicos, e revisar remanescentes.
- Executar `git diff --stat` e confirmar que as alteracoes estao restritas a reorganizacao documental, referencias governadas, TASK-011A, roadmap e log da TASK.
- Conferir manualmente que o conteudo tecnico da arquitetura nao foi alterado.
- Conferir manualmente que a `TASK-011A` nao foi executada.

## Riscos

- Risco: reorganizacao documental virar mudanca de arquitetura.
  Mitigacao: mover arquivo e atualizar referencias sem alterar decisoes tecnicas.

- Risco: referencias antigas ficarem em TASKs pendentes e confundirem execucoes futuras.
  Mitigacao: mapear e revisar citacoes em `tasks/` e documentos governados.

- Risco: logs historicos serem reescritos e perderem valor de evidencia.
  Mitigacao: nao atualizar logs antigos apenas para trocar caminhos.

- Risco: `TASK-011A` ser executada junto com a reorganizacao.
  Mitigacao: limitar esta TASK a estrutura documental e referencias; manter artefato de fronteiras para execucao posterior.

## Bloqueios Pendentes

Bloqueada ate homologacao da `TASK-011`.

Permanece bloqueado qualquer trabalho que tente alterar decisoes arquiteturais, PRD, regras de dominio, contratos funcionais, formulas prudenciais, arredondamento, schemas, endpoints, classes, codigo, testes, CI, migrations, assets ou executar a `TASK-011A` durante esta TASK.
