# 07 - API, frontend, exportacao e laudo da DFC

## API

Endpoints sugeridos:

- `GET /api/dfc/{year}`
- `POST /api/dfc/decision`
- `POST /api/dfc/recalculate`

Payload deve conter:

- resumo por atividade;
- componentes;
- linhas de auditoria;
- pendencias;
- valor `FCA`;
- status `FCA`.

## Frontend

Tela de `DFC direta` com:

- resumo por atividade;
- tabela de movimentos;
- filtros por atividade;
- filtros por status;
- pendencias;
- fluxos nao classificados;
- resumo `FCA`.

## Exportacao

Abas futuras:

- `dfc_resumo`
- `dfc_auditoria`

## Laudo

O laudo deve informar:

- DFC reconstruida por metodo direto;
- separacao operacional, investimento e financiamento;
- movimentos nao classificados;
- status final ou parcial do `FCA`.

## Rotas explicitas

- `/dfc`
- `/dfc/:exercicio`
- `/dfc/auditoria`

