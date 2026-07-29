# TASK-104 - Implementar conciliação do balanço declarado

## SPEC De Origem

- `specs/SPEC-012-modulo-1c-balanco-patrimonial-declarado.md`

## Dependencias

- `TASK-103-reprocessar-importacoes-ecd-legadas.md`

## Objetivo

Implementar o motor determinístico que verifica a obrigatoriedade do Bloco J,
constrói a árvore do `J100`, valida totalizadores e concilia linhas de detalhe
por `I050 + I052 + I155`.

## Fontes Usadas

- `docs/product/PRD.md`
- `docs/architecture/architecture.md`
- `specs/SPEC-002-modulo-1-camada-declarada.md`
- `specs/SPEC-012-modulo-1c-balanco-patrimonial-declarado.md`
- `docs/methodology/pesquisa-oficial-balanco-patrimonial-ecd.md`
- `tasks/TASK-103-reprocessar-importacoes-ecd-legadas.md`

## Escopo Exato

- Determinar a obrigatoriedade do Bloco J por `0000`, `I010` e `I030`.
- Selecionar o `J005` anual aplicável conforme período e `ID_DEM = 1`.
- Rejeitar múltiplos `J005` igualmente aplicáveis.
- Construir a árvore exclusivamente por `COD_AGL`, `COD_AGL_SUP` e
  `NIVEL_AGL`.
- Validar raízes, grupos, pais, níveis, totalizadores e fechamento dos lados.
- Conciliar linhas de detalhe pela relação `I050 -> I052 -> J100`.
- Respeitar conta e centro de custo na seleção do saldo `I155`.
- Normalizar sinais de débito e crédito em `Decimal`.
- Calcular valores declarados, conciliados e diferenças exatas em centavos.
- Produzir um estado geral do balanço e um estado por linha de detalhe.
- Disponibilizar as contas componentes de cada linha.
- Não persistir snapshot em consultas ou cálculos do balanço.
- Criar testes unitários e de integração do motor.

## Fora De Escopo

- Alterar metodologia ou fórmula PLRA/CAPAG-E.
- Usar `I051` para construir o balanço.
- Criar API ou frontend.
- Criar decisão humana ou switch.
- Corrigir a ECD importada.
- Persistir snapshots do balanço.

## Passos Executaveis

1. Modelar os objetos de balanço, linha e componente.
2. Implementar o avaliador de obrigatoriedade.
3. Implementar a seleção do `J005`.
4. Implementar e validar a árvore do `J100`.
5. Implementar a conciliação das linhas de detalhe.
6. Consolidar estados conforme a precedência da SPEC.
7. Criar testes para todos os estados e diferenças.

## Arquivos Ou Areas Provaveis

- `backend/app/domain/`
- `backend/app/engine/`
- `backend/app/application/`
- `backend/app/repositories/`
- `backend/tests/`

## Criterios De Aceite

- Obrigatoriedade do Bloco J é determinada sem heurística.
- `J005` anual correto é selecionado de forma determinística.
- Árvore usa somente a estrutura do `J100`.
- Totalizadores são validados pela soma assinada dos filhos imediatos.
- Linhas de detalhe são conciliadas por `I052 + I155`.
- Centro de custo é respeitado quando declarado.
- Diferença igual a `0.00` produz `CONCILIADA`.
- Estados `SEM_I052` e `SEM_SALDO_I155` são auditáveis.
- Balanço produz somente os estados definidos na SPEC.
- Nenhum valor usa `float`.
- Consultar ou calcular o balanço não grava snapshot.

## Validacao Esperada

- Executar testes backend focados via `docker compose`.
- Executar a suíte backend aplicável via `docker compose`.
- Cobrir balanço válido, divergente, ausente, inválido e não obrigatório.
- Cobrir centro de custo, totalizadores e sinais de débito/crédito.
- Conferir ausência de `float` nos arquivos alterados.

## Riscos

- Risco: dupla contagem de conta e centro de custo.
  Mitigação: chave explícita e testes de composição.
- Risco: validar árvore pelo prefixo do código.
  Mitigação: usar apenas campos formais do `J100`.
- Risco: confundir consistência interna com tratamento prudencial.
  Mitigação: manter o motor sem `I051` e sem metodologia PLRA.

## Bloqueios Pendentes

Bloqueada até a conclusão da `TASK-103`.

