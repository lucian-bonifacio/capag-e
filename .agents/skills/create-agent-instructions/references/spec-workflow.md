# Workflow De Criação De SPECs

## Regra Central

Toda SPEC deve transformar PRD, arquitetura e documentos governados em uma especificação técnica verificável.

SPEC vem antes da TASK.

Uma SPEC insuficiente não deve virar TASK.

## SPEC Deve Definir

- objetivo técnico;
- contexto e problema;
- escopo;
- fora de escopo;
- fontes usadas;
- decisões já aprovadas;
- decisões pendentes;
- contratos;
- responsabilidades;
- critérios de aceite;
- estratégia de validação esperada;
- riscos e mitigação;
- bloqueios.

## SPEC Não Deve

- esconder decisão pendente;
- deixar contrato para a TASK decidir;
- deixar regra de negócio para a TASK decidir;
- deixar critério de aceite subjetivo;
- transformar execução de trabalho em substituto de decisão técnica;
- duplicar regra de domínio em camada errada.

## Aplicação Das Lentes

Ao criar uma SPEC, identificar quais lentes são aplicáveis:

- arquitetura;
- backend FastAPI;
- frontend React;
- QA;
- domínio/engine específico do projeto.

Use mais de uma lente quando a SPEC atravessar camadas.

## Bloqueios Em SPECs

Registrar bloqueio e perguntar ao usuário quando faltar:

- decisão arquitetural;
- contrato de API;
- regra de domínio;
- fonte normativa;
- política de precisão ou arredondamento;
- comportamento de tela;
- estado de erro/loading/vazio;
- resultado esperado para teste;
- critério de aceite verificável.
