# 10 - Consolidacao do planejamento temporario

## Objetivo

Consolidar a propria pasta `tmp_deu_a_louca/` para evitar duplicidade entre a primeira versao solta e a organizacao por modulos.

## Ponto de decisao

O planejamento final deve ficar apenas em:

- `tmp_deu_a_louca/00-planejamento-geral.md`;
- subpastas `tmp_deu_a_louca/modulo-*`.

Os arquivos soltos `01` a `13` da primeira versao foram substituidos pelos modulos.

## Arquivos correlatos

- `tmp_deu_a_louca/00-planejamento-geral.md`
- `tmp_deu_a_louca/modulo-00-organizacao-arquitetura-design/`
- `tmp_deu_a_louca/modulo-01-camada-declarada/`
- `tmp_deu_a_louca/modulo-02-capag-reclassificada/`
- `tmp_deu_a_louca/modulo-03-contrato-capag-e-plra-fca-roa/`
- `tmp_deu_a_louca/modulo-04-evidencias-avaliacao-ativos/`
- `tmp_deu_a_louca/modulo-05-dfc-direto-fca/`
- `tmp_deu_a_louca/modulo-06-motor-roa-plra/`
- `tmp_deu_a_louca/modulo-07-gerador-laudo-capag-e/`
- `tmp_deu_a_louca/modulo-08-governanca-metodologia/`

## Detalhamento

- Comparar a primeira leva de arquivos com os modulos novos.
- Migrar qualquer conteudo ainda util para os modulos correspondentes.
- Remover a primeira leva de arquivos soltos.
- Atualizar `00-planejamento-geral.md` para apontar somente para a estrutura escolhida.

## Entregavel

Pasta `tmp_deu_a_louca/` organizada, sem duplicidade operacional.

Estrutura oficial:

- raiz com `00-planejamento-geral.md`;
- tarefas detalhadas apenas dentro de `modulo-*`.

## Criterios de sucesso

- O usuario sabe qual arquivo ler primeiro.
- Cada tarefa fica em um unico lugar.
- A estrutura temporaria nao vira nova fonte de confusao.

## Fora do escopo

- Alterar arquivos fora de `tmp_deu_a_louca/`.
- Criar tasks oficiais em `tasks/`.
