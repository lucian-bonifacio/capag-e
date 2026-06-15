# 08 - API, frontend, exportacao e laudo do ROA

## API

Endpoints sugeridos:

- `GET /api/roa/{year}`
- `POST /api/roa/decision`
- `POST /api/roa/recalculate`

Payload deve incluir:

- resumo do ROA;
- componentes;
- auditoria;
- pendencias;
- status;
- valor de `CAPAG-E` por metodo `roa_plra`, quando disponivel.

## Frontend

Tela de `ROA` com:

- resumo por bloco;
- tabela de contas de resultado;
- pendencias de despesas/receitas condicionais;
- comparativo com `FCA`, quando existir;
- status de evidencias.

## Exportacao

Abas futuras:

- `roa_resumo`
- `roa_auditoria`
- `roa_pressoes_caixa`

## Laudo

Quando o metodo for `ROA + PLRA`, o laudo deve apresentar:

- formula do `ROA`;
- blocos de receita/custo/despesa;
- pressoes complementares;
- justificativas de despesas materiais;
- valor final de `ROA`;
- combinacao com `PLRA`.

## Rotas explicitas

- `/roa`
- `/roa/:exercicio`
- `/roa/auditoria`

