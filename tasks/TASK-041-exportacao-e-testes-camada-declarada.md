# TASK-041 - Exportacao e testes da camada declarada

## SPEC De Origem

- `specs/SPEC-002-modulo-1-camada-declarada.md`

## Dependencias

- `TASK-039-criar-api-camada-declarada.md`
- `TASK-040-criar-ui-camada-declarada.md`

## Objetivo

Implementar exportação Excel da camada declarada e consolidar testes obrigatórios do módulo, sem recalcular regra de negócio fora do backend.

## Fontes Usadas

- `docs/product/PRD.md`
- `docs/architecture/architecture.md`
- `specs/SPEC-002-modulo-1-camada-declarada.md`

## Escopo Exato

- Criar exportação Excel declarada a partir de snapshots/objetos calculados.
- Incluir status, limitações e versão metodológica.
- Criar testes de matcher, API, exportação e casos de prefixo amplo perigoso.
- Garantir que Excel não recalcula valores.

## Fora De Escopo

- Exportar camada reclassificada.
- Gerar laudo.
- Criar regra metodológica nova.
- Alterar frontend além de acionamento/consumo permitido.

## Passos Executaveis

1. Ler contrato de resultado declarado.
2. Criar exportador Excel sem recalculo.
3. Criar testes de regressão do módulo.
4. Validar via Docker Compose.

## Arquivos Ou Areas Provaveis

- `backend/app/export/`
- `backend/tests/`
- frontend apenas se houver botão/ação já prevista

## Criterios De Aceite

- Excel reflete snapshots declarados.
- Exportação inclui status e versão metodológica.
- Testes cobrem prefixo amplo perigoso.
- Nenhum recálculo ocorre no Excel.

## Validacao Esperada

- Executar testes backend e build frontend via `docker compose`, quando aplicável.
- Conferir planilha gerada por teste sem regra duplicada.

## Riscos

- Risco: exportação recalcular resultado.
  Mitigação: consumir apenas objetos calculados.

## Bloqueios Pendentes

Bloqueada até API e UI da camada declarada existirem.
