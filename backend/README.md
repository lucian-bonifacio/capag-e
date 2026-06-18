# Backend CAPAG

Este diretorio contem a estrutura minima do backend do CAPAG, conforme responsabilidades definidas em `docs/architecture/architecture.md` e `specs/SPEC-001-modulo-0-fundacao-governada.md`.

## Camadas

- `app/api/`: rotas REST, validacao HTTP, autenticacao/autorizacao, OpenAPI e serializacao.
- `app/application/`: casos de uso, transacoes logicas e orquestracao entre parse, motores, persistencia, exportacao e laudo.
- `app/domain/`: entidades, value objects, estados canonicos, invariantes e contratos internos.
- `app/io/`: leitura, parse e normalizacao de ECD, sem regra prudencial.
- `app/engine/`: motores de calculo, classificacao, auditoria metodologica e governanca de assets.
- `app/repositories/`: persistencia via SQLAlchemy e consultas transacionais.
- `app/export/`: serializacao de snapshots e objetos calculados para Excel, sem recalculo de regra.
- `app/report/`: montagem de laudo estruturado a partir de objetos calculados, evidencias, bloqueios e snapshots, sem executar motor.
- `app/assets/`: leitura de assets metodologicos versionados do repositorio.

## Proibicoes Nesta Fundacao

- Nao criar endpoints funcionais sem TASK e SPEC suficientes.
- Nao criar schemas Pydantic funcionais nesta etapa.
- Nao criar modelos SQLAlchemy ou migrations nesta etapa.
- Nao implementar parser ECD, motores prudenciais, exportacao Excel ou laudo nesta etapa.
- Nao duplicar regra prudencial fora de `app/engine/`.
- Nao usar `float` para valores contabeis, fiscais, financeiros ou prudenciais.

## Validacao Minima

Executar testes backend pelo ambiente oficial:

```bash
COMPOSE_DISABLE_ENV_FILE=1 docker compose --profile test run --rm backend-tests
```

O teste atual e apenas sentinela para validar o runner de `pytest`; ele nao define comportamento funcional do CAPAG.
