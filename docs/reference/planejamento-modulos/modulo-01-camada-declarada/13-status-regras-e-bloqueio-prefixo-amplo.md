# 13 - Status das regras e bloqueio de prefixo amplo

## Objetivo

Definir status de regras metodologicas e impedir que prefixos amplos perigosos sejam usados como classificacao final.

## Ponto de decisao

Decidir como representar `status_regra` nas metodologias PLR/FCO/CAPAG-e e como o motor deve reagir a cada status.

## Arquivos correlatos

- `docs/reference/ajuste_modulo_principal.md`
- `src/capag/assets/methodology/tabela_metodologica_plr.csv`
- `src/capag/assets/methodology/tabela_metodologica_fco.csv`
- `src/capag/engine/plr.py`
- `src/capag/engine/fco.py`
- `src/capag/domain/models.py`
- `src/capag/domain/alerts.py`
- `tests/unit/test_engine_plr.py`

## Status propostos

- `ATIVA`: regra valida para classificacao.
- `BLOQUEADA`: regra nao pode ser usada para classificacao final.
- `EM_REVISAO`: regra ainda nao validada metodologicamente.
- `DEPRECIADA`: regra antiga, mantida apenas para historico.
- `GENERICA_SEGURA`: regra ampla permitida porque filhos relevantes possuem o mesmo tratamento economico.
- `GENERICA_PERIGOSA`: regra ampla identificada como potencialmente incorreta.

## Regra de bloqueio de prefixo amplo

Um prefixo amplo nao deve ser usado como regra final quando seus filhos tiverem tratamentos economicos diferentes.

Exemplo:

- `2.01.01.01.*`: fornecedores.
- `2.01.01.07.*`: emprestimos e financiamentos.
- `2.01.01.09.*`: obrigacoes tributarias.
- `2.01.01.15.*`: provisoes.
- `2.01.01.*`: bloqueada ou generica perigosa.

## Comportamento esperado do motor

- Regra `ATIVA`: pode ser aplicada.
- Regra `GENERICA_SEGURA`: pode ser aplicada quando nao houver regra mais especifica.
- Regra `BLOQUEADA`: deve ser ignorada como classificacao final.
- Regra `GENERICA_PERIGOSA`: deve ser ignorada como classificacao final.
- Regra `EM_REVISAO`: nao deve ser usada automaticamente.
- Regra `DEPRECIADA`: nao deve ser usada para novos calculos, salvo regra explicita de historico.

## Impactos

- Assets metodologicos precisam incluir status.
- Loaders de metodologia precisam validar status.
- Motores PLR/FCO precisam pular regras bloqueadas/perigosas/em revisao.
- Auditoria precisa indicar quando nenhuma regra segura foi encontrada.

## Entregavel

Contrato de status das regras e bloqueio de prefixo amplo.

## Criterios de sucesso

- `2.01.01.*` nao classifica emprestimos como fornecedores.
- Regras amplas so sao usadas quando explicitamente seguras.
- Ausencia de regra segura gera status revisavel, nao classificacao indevida.

## Fora do escopo

- Administrar status de regra pela interface.
- Implementar banco antes da decisao arquitetural transversal.

