# 15 - Banco de dados e persistencia do modulo reclassificado

## Objetivo

Planejar como o modulo reclassificado usara banco de dados caso a nova arquitetura aprove persistencia.

## Ponto de decisao

Decidir quais dados do modulo reclassificado precisam ser persistidos e quais podem ser recalculados.

## Dependencia arquitetural

Esta tarefa depende de:

- `tmp_deu_a_louca/modulo-00-organizacao-arquitetura-design/11-decisao-banco-dados-persistencia.md`

## Tabelas sugeridas no documento de referencia

- empresas;
- ecd_arquivos;
- contas;
- contas_referenciais_originais;
- lancamentos;
- partidas;
- saldos;
- perfis_conta;
- scores_classificacao;
- classificacoes_sugeridas;
- revisoes_humanas;
- precedentes;
- regras.

## Como tratar no planejamento

- Nao tratar banco como detalhe interno do engine.
- Definir persistencia antes de implementar revisoes humanas e precedentes.
- Separar dados recalculaveis de snapshots historicos.
- Registrar versao das regras e metodologia usadas em cada resultado.
- Definir se precedentes entram no MVP ou fase posterior.
- Definir implicacoes de seguranca, auditoria, deploy, LGPD, multiusuario e testes.

## Entregavel

Modelo de persistencia do modulo reclassificado, condicionado a decisao arquitetural do modulo 0.

## Criterios de sucesso

- O modulo 2 nao decide banco isoladamente.
- Perfis, scores, evidencias, revisoes e precedentes tem destino claro.
- O sistema preserva rastreabilidade entre resultado declarado e reclassificado.
