# 05 - API, frontend, exportacao e laudo

## Objetivo

Planejar as superficies de uso da camada de evidencias e avaliacao de ativos.

## API

Endpoints sugeridos pela spec:

- `GET /api/evidence/{year}`
- `POST /api/evidence`
- `PUT /api/evidence/{evidence_id}`
- `DELETE /api/evidence/{evidence_id}`

Endpoints futuros para ativos podem ser agrupados em:

- `GET /api/assets/valuation/{year}`
- `PUT /api/assets/valuation/{assessment_id}`

## Frontend

Telas ou paineis necessarios:

- evidencias por exercicio;
- filtros por componente;
- filtros por status;
- edicao de justificativa;
- selecao de tipo de evidencia;
- resumo de impacto monetario;
- painel de ativos relevantes;
- valor contabil, default e avaliado;
- status de laudo/avaliacao.

## Exportacao

Abas futuras:

- `evidencias_justificativas`
- `avaliacao_ativos`

## Laudo

O laudo deve consumir:

- ajustes materiais;
- justificativas;
- tipo de evidencia exigida;
- status da evidencia;
- ressalvas;
- ativos relevantes ajustados;
- base de avaliacao;
- ausencia ou presenca de laudo externo.

## Rotas explicitas

Rotas provaveis:

- `/evidencias`
- `/evidencias/:exercicio`
- `/ativos/avaliacao`
- `/ativos/avaliacao/:exercicio`

## Criterios de sucesso

- O usuario entende o que falta para um resultado final defensavel.
- As evidencias aparecem em API, UI, Excel e laudo sem recalculo.
- Ajuste material sem justificativa nao passa invisivel.

