# 06 - Motor e auditoria da camada declarada

## Objetivo

Planejar os ajustes necessarios no motor para suportar corretamente a camada declarada e sua auditoria.

## Ponto de decisao

Decidir se os motores atuais precisam apenas de ajustes de assets ou tambem de alteracoes de codigo.

## Arquivos correlatos

- `src/capag/engine/plr.py`
- `src/capag/engine/fco.py`
- `src/capag/engine/capag.py`
- `src/capag/engine/audit.py`
- `src/capag/domain/models.py`
- `src/capag/domain/alerts.py`
- `src/capag/assets/reference/`
- `src/capag/assets/methodology/`

## Detalhamento

- Verificar se o matching por especificidade esta correto.
- Verificar se o motor registra regra aplicada.
- Verificar se auditoria diferencia:
  - codigo sem `I051`;
  - codigo sem descricao oficial;
  - codigo sem regra metodologica;
  - codigo excluido automaticamente;
  - codigo incluido automaticamente;
  - codigo reclassificado manualmente.
- Verificar se alertas precisam de novos codigos centralizados.
- Verificar se memoria de calculo precisa citar descricao oficial e tratamento metodologico.

## Entregavel

Plano de ajuste do motor/auditoria declarados.

## Criterios de sucesso

- A camada declarada fica rastreavel por conta.
- A auditoria mostra o que veio da ECD, o que veio da tabela oficial e o que veio da metodologia.

## Fora do escopo

- Criar score comportamental.
- Fazer julgamento de substancia economica.

