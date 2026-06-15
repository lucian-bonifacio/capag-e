# 16 - API e contratos backend

## Objetivo

Planejar endpoints e contratos necessarios para expor o modulo reclassificado.

## Ponto de decisao

Decidir quais endpoints entram no MVP em memoria.

## Endpoints sugeridos pelo documento de referencia

- importar ECD;
- normalizar;
- montar razao;
- gerar perfis;
- classificar;
- listar contas analisadas;
- retornar perfil;
- retornar classificacao sugerida;
- revisar classificacao;
- gerar relatorio consolidado.

## Adaptacao conforme decisao de persistencia

Se a implementacao inicial ainda for em memoria, endpoints baseados em `{id_ecd}` persistido precisam ser adaptados para sessao ativa.

Possiveis endpoints V2:

- `POST /api/behavioral/run`;
- `GET /api/behavioral/exercises/{year}`;
- `GET /api/behavioral/exercises/{year}/accounts/{account_code}`;
- `POST /api/behavioral/exercises/{year}/review`;
- `GET /api/behavioral/exercises/{year}/report`.

Se banco de dados for aprovado, os contratos podem usar identificadores persistidos de:

- empresa;
- arquivo ECD;
- exercicio;
- analise;
- conta;
- classificacao sugerida;
- revisao humana;
- precedente.

## Arquivos correlatos

- `src/capag/api/routes.py`
- `src/capag/api/schemas.py`
- `src/capag/api/presentation.py`
- futura camada `src/capag/application/`
- futuro `src/capag/engine/behavioral*.py`

## Entregavel

Contrato de API do modulo reclassificado.

## Criterios de sucesso

- API nao contem regra de negocio.
- Contratos respeitam sessao em memoria.

## Fora do escopo

- Criar contratos definitivos antes da decisao de persistencia.
