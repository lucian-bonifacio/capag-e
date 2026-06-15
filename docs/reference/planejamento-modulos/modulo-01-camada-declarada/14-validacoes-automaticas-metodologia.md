# 14 - Validacoes automaticas da metodologia

## Objetivo

Definir validacoes automaticas para impedir que tabelas metodologicas perigosas entrem em uso.

## Ponto de decisao

Decidir se as validacoes rodam em testes, no startup da API, no carregamento do motor ou em todos esses pontos.

## Arquivos correlatos

- `docs/reference/ajuste_modulo_principal.md`
- `src/capag/assets/reference/`
- `src/capag/assets/methodology/tabela_metodologica_plr.csv`
- `src/capag/assets/methodology/tabela_metodologica_fco.csv`
- `src/capag/engine/plr.py`
- `src/capag/engine/fco.py`
- `src/capag/domain/alerts.py`
- `tests/unit/`
- `tests/integration/`

## Validacoes obrigatorias

1. Existem prefixos amplos ativos que possuem filhos com tratamentos diferentes?
2. Existem regras duplicadas para o mesmo codigo/padrao/finalidade?
3. Existe conflito entre regra exata e regra por prefixo?
4. Existem codigos metodologicos que nao existem na tabela oficial?
5. Existem codigos oficiais relevantes sem metodologia?
6. Existem regras vencidas sendo usadas?
7. Existem regras bloqueadas sendo aplicadas?
8. Existem tratamentos iguais sendo aplicados a naturezas oficiais diferentes sem justificativa?
9. Existem categorias FCO incompatíveis com a natureza oficial?
10. Existem codigos de divida sendo tratados como fornecedor?

## Testes de regressao obrigatorios

- Emprestimo nao pode virar fornecedor:
  - `2.01.01.07.01` nao pode virar `pagamentos_fornecedores`.
- Fornecedor pode virar fornecedor:
  - codigo claro de fornecedor continua fornecedor.
- Tributo a recuperar nao pode virar cliente:
  - `1.01.02.03.*` nao pode virar recebimento de clientes.
- Prefixo bloqueado nao pode classificar:
  - se so houver `2.01.01.*` bloqueada, resultado deve ser `NAO_MAPEADO_METODOLOGICAMENTE`.
- Regra mais especifica vence:
  - `2.01.01.07.*` vence `2.01.01.*`.

## Entregavel

Plano de validacao automatica das tabelas metodologicas.

## Criterios de sucesso

- Erros de metodologia ampla sao detectados antes de afetar resultado.
- Testes impedem regressao da conta `1725`.
- FCO e PLR sao validados por finalidade.

## Fora do escopo

- Corrigir todas as regras metodologicas nesta tarefa.
- Criar UI de administracao de metodologia.

