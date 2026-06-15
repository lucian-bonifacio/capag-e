# 10 - Classificacao em camadas e mapeamento referencial

## Objetivo

Definir como a familia detectada sera convertida em codigo referencial sugerido.

## Ponto de decisao

Decidir a estrutura da tabela interna de mapeamento.

## Camadas

1. Macroclasse.
2. Grupo.
3. Familia.
4. Subfamilia.
5. Codigo referencial final.

## Regra essencial

O sistema so deve mapear para codigo referencial final quando houver confianca suficiente nas camadas anteriores.

## Tabela de mapeamento prevista

- familia_detectada;
- subfamilia_detectada;
- macroclasse;
- codigo_referencial_sugerido;
- descricao_referencial_sugerida;
- vigencia;
- ano-calendario;
- leiaute;
- tipo de entidade;
- observacoes.

## Arquivos correlatos

- `src/capag/assets/reference/`
- futuro `src/capag/assets/behavioral/mapeamento_familia_referencial.csv`
- futuro `src/capag/engine/behavioral_mapping.py`

## Entregavel

Spec de mapeamento familia -> referencial.

## Criterios de sucesso

- O modulo nao pula direto para o codigo referencial.
- O mapeamento e versionado e auditavel.

## Fora do escopo

- Administrar mapeamento pela UI.

