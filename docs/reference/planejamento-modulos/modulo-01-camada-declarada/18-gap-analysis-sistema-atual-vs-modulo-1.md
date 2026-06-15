# 18 - Gap analysis do sistema atual vs Modulo 1

## Objetivo

Comparar o sistema atual com o comportamento desejado no Modulo 1.

## Ponto de decisao

Decidir quais lacunas viram tasks de implementacao e em qual ordem.

## O que ja existe

### Parser e normalizacao

- `src/capag/io/ecd_parser.py` le registros `I051`.
- `src/capag/io/ecd_normalizer.py` monta `referential_map`.
- O normalizador preserva `COD_CTA_REF` mesmo quando nao existe no catalogo local.
- Ja existe teste aceitando codigo referencial sem match no catalogo local.

### Catalogo referencial

- Existe `src/capag/assets/reference/catalogo_referencial.csv`.
- O catalogo atual e simples:
  - `codigo_referencial`;
  - `descricao_referencial`.
- Ele enriquece descricao quando encontra o codigo.
- Ele nao e uma tabela oficial completa com vigencia, leiaute, natureza, status e hierarquia.

### Metodologia PLR

- Existe `src/capag/assets/methodology/tabela_metodologica_plr.csv`.
- Existe matching exato e por prefixo.
- O prefixo mais especifico vence por ordenacao de tamanho.
- Nao ha `status_regra`.
- Nao ha bloqueio formal de prefixo amplo perigoso.

### Metodologia FCO

- Existe `src/capag/assets/methodology/tabela_metodologica_fco.csv`.
- Existe matching exato e por prefixo.
- Existem regras amplas como `1.01.02.*` e `2.01.01.*`.
- Nao ha tratamento robusto para excluir automaticamente fluxos financeiros/tributarios se uma regra ampla conflitar.

### Auditoria/API/exportacao

- Existem `audit_rows` no resultado PLR.
- A API remove objetos pesados e monta payload de apresentacao.
- A exportacao Excel ainda e estruturalmente simples.

## Lacunas principais

1. Tabela oficial completa do plano referencial.
2. Status das regras metodologicas.
3. Bloqueio de prefixo amplo perigoso.
4. Validacoes automaticas da metodologia.
5. Tratamento por finalidade em estrutura clara.
6. Status formais:
   - `NAO_MAPEADO_METODOLOGICAMENTE`;
   - `COD_CTA_REF_NAO_ENCONTRADO_NA_TABELA_OFICIAL`;
   - `REGRA_BLOQUEADA`;
   - `GENERICA_PERIGOSA`.
7. Resultado por conta declarada com descricao oficial, regra aplicada e categorias por finalidade.
8. Testes obrigatorios completos do documento de referencia.
9. Exportacao declarada com rastreabilidade completa.
10. Persistencia/snapshot da camada declarada, se banco for aprovado.

## Ordem sugerida de fechamento dos gaps

1. Decisao de banco/persistencia no Modulo 0.
2. Spec oficial da camada declarada.
3. Plano referencial oficial.
4. Status de regras e bloqueio de prefixo amplo.
5. Algoritmo de match compartilhado.
6. Validacoes automaticas de metodologia.
7. Ajuste PLR.
8. Ajuste FCO.
9. Resultado por conta/payload.
10. Exportacao.
11. Testes e fixtures.

## Criterios de sucesso

- O planejamento reconhece o que o sistema ja faz.
- As lacunas nao viram retrabalho escondido.
- O Modulo 1 e tratado como ajuste do sistema existente.

