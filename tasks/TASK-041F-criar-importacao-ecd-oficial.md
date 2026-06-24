# TASK-041F - Criar importacao ECD oficial

## SPEC De Origem

- `specs/SPEC-002-modulo-1-camada-declarada.md`

## Dependencias

- `TASK-041E-persistir-ecd-normalizada.md`

## Objetivo

Criar o mecanismo oficial de importacao de ECD real via ambiente Docker, expondo endpoint ou comando governado para gerar analise e persistir ECD normalizada.

## Fontes Usadas

- `docs/product/PRD.md`
- `docs/architecture/architecture.md`
- `specs/SPEC-002-modulo-1-camada-declarada.md`
- `tasks/TASK-041E-persistir-ecd-normalizada.md`

## Escopo Exato

- Criar endpoint de upload/importacao ECD ou comando oficial equivalente em Docker.
- Validar tipo/tamanho basico do arquivo, sem registrar conteudo sensivel em log.
- Criar `Analysis`, `EcdFile` e `Exercise` a partir da importacao.
- Registrar hash do conteudo e nome original.
- Retornar identificadores para consulta da analise.
- Criar testes de importacao com fixtures sinteticas.

## Fora De Escopo

- Criar tela frontend completa de upload, salvo se for minimo indispensavel.
- Executar camada declarada automaticamente.
- Gerar Excel.
- Importar ECD real versionada no repositorio.

## Passos Executaveis

1. Definir contrato operacional do endpoint ou comando oficial.
2. Integrar parser e persistencia normalizada.
3. Criar retorno com `analysis_id` e exercicio.
4. Testar importacao valida e erro de arquivo invalido.

## Arquivos Ou Areas Provaveis

- `backend/app/api/`
- `backend/app/application/`
- `backend/app/io/`
- `backend/tests/`

## Criterios De Aceite

- Usuario consegue importar ECD pelo mecanismo oficial em Docker.
- Importacao cria analise consultavel.
- Logs nao exibem conteudo bruto sensivel da ECD.

## Validacao Esperada

- Executar testes backend via `docker compose`.
- Testar importacao com fixture sintetica.

## Riscos

- Risco: endpoint aceitar arquivo invalido e deixar estado inconsistente.
  Mitigacao: validar antes de concluir importacao e usar transacao.

## Bloqueios Pendentes

Bloqueada ate persistencia da ECD normalizada existir.
