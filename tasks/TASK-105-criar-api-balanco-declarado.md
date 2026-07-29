# TASK-105 - Criar API do balanço declarado

## SPEC De Origem

- `specs/SPEC-012-modulo-1c-balanco-patrimonial-declarado.md`

## Dependencias

- `TASK-039-criar-api-camada-declarada.md`
- `TASK-104-implementar-conciliacao-balanco-declarado.md`

## Objetivo

Substituir o payload genérico atualmente usado pelo balanço por um contrato
específico de Balanço Patrimonial declarado, incluindo estrutura, valores,
estado geral, conciliação e componentes auditáveis.

## Fontes Usadas

- `docs/product/PRD.md`
- `docs/architecture/architecture.md`
- `specs/SPEC-002-modulo-1-camada-declarada.md`
- `specs/SPEC-012-modulo-1c-balanco-patrimonial-declarado.md`
- `tasks/TASK-039-criar-api-camada-declarada.md`
- `tasks/TASK-104-implementar-conciliacao-balanco-declarado.md`

## Escopo Exato

- Criar schemas específicos do balanço conforme a `SPEC-012`.
- Migrar `GET .../declared/balance/accounts` para o novo payload.
- Expor estado geral, bloqueio, período, totais, diferença, linhas e
  limitações.
- Serializar valores monetários como string decimal.
- Expor todos os campos normalizados necessários do `J100`.
- Expor estado e diferença das linhas de detalhe.
- Criar `GET .../balance/accounts/{aggregation_code}/components`.
- Expor contas, centros de custo, saldos e linhas originais componentes.
- Retirar os apontamentos conceitualmente incorretos de comparação direta
  `J100 x I050`.
- Manter a rota de auditoria declarada por conta separada.
- Garantir que endpoints de leitura não persistam snapshots.
- Criar testes de contrato, erros e serialização.

## Fora De Escopo

- Recalcular balanço no schema ou controller.
- Alterar metodologia PLRA/CAPAG-E.
- Criar frontend.
- Expor download do arquivo original.
- Criar switches ou decisões humanas.
- Manter compatibilidade silenciosa com o payload incorreto anterior.

## Passos Executaveis

1. Criar os schemas Pydantic do balanço e dos componentes.
2. Adaptar o serviço de leitura ao motor da `TASK-104`.
3. Migrar o endpoint principal.
4. Criar o endpoint de componentes.
5. Remover warnings baseados em igualdade direta de códigos.
6. Ajustar OpenAPI e respostas de erro.
7. Criar testes de API e ausência de escrita em consultas.

## Arquivos Ou Areas Provaveis

- `backend/app/schemas/declared.py`
- `backend/app/api/declared.py`
- `backend/app/application/declared_service.py`
- `backend/tests/test_declared_api.py`
- `backend/tests/`

## Criterios De Aceite

- Endpoint principal retorna contrato específico de balanço.
- Payload contém estado, totais, diferença e árvore declarada.
- Valores monetários são strings decimais.
- Linha de detalhe informa conciliação e quantidade de componentes.
- Endpoint de componentes retorna `I050/I052/I155` auditáveis.
- Nenhuma resposta compara diretamente `COD_AGL` com `COD_CTA`.
- Auditoria declarada por conta permanece disponível separadamente.
- Consultas não criam ou alteram snapshots.
- OpenAPI representa o contrato aprovado na SPEC.

## Validacao Esperada

- Executar testes backend via `docker compose`.
- Validar OpenAPI e schemas de resposta.
- Testar balanço válido e todos os estados de erro.
- Testar endpoint de componentes.
- Testar ausência de escrita em chamadas GET.
- Conferir ausência de `float` nos arquivos alterados.

## Riscos

- Risco: manter campos antigos com semântica incorreta.
  Mitigação: usar schemas novos e remover a comparação direta.
- Risco: controller recalcular regra.
  Mitigação: consumir objetos prontos do serviço/motor.
- Risco: resposta principal ficar excessivamente pesada.
  Mitigação: carregar componentes sob demanda em endpoint próprio.

## Bloqueios Pendentes

Bloqueada até a conclusão da `TASK-104`.

