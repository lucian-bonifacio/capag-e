# Modulo 1 - Camada declarada

## Objetivo

Organizar e corrigir a camada declarada do sistema.

Camada declarada significa:

```text
ECD entregue
  -> I050/I051/I155/I200/I250/J100
  -> COD_CTA_REF declarado no I051
  -> plano referencial oficial
  -> metodologia interna versionada
  -> PLR/FCO/CAPAG-e declarados
  -> auditoria/exportacao/frontend
```

## Origem do modulo

Este modulo nasce do problema descrito em:

- `docs/reference/ajuste_modulo_principal.md`

A matriz de cobertura do documento esta em:

- `12-matriz-cobertura-ajuste-modulo-principal.md`

O ponto central e que o sistema atual usa o `COD_CTA_REF` declarado na ECD, mas a metodologia interna pode estar interpretando codigos amplos demais por prefixo.

Exemplo do problema:

- ECD declara `2.01.01.07.01`.
- A tabela metodologica usa `2.01.01.*`.
- O sistema pode classificar emprestimos/financiamentos como fornecedores.

## Decisao conceitual

A ECD continua sendo a fonte declaratoria.

O sistema nao deve adivinhar a classificacao principal pelo nome livre da conta.

O sistema deve separar:

- descricao oficial do codigo referencial;
- tratamento metodologico interno para PLR, FCO, CAPAG-e e auditoria.

## O que este modulo nao e

Este modulo nao e a analise comportamental.

Ele nao confronta a ECD com substancia economica observada para criar uma segunda leitura.

Ele organiza o resultado oficial declarado baseado no `I051` e nos artefatos metodologicos versionados.

## Impacto esperado

Este modulo afeta muita coisa:

- `README.md`;
- specs;
- assets referenciais;
- assets metodologicos;
- parser/normalizador, se houver lacuna de dados necessarios;
- motor PLR;
- motor FCO;
- auditoria;
- API/presentation;
- frontend;
- exportacao Excel;
- testes unitarios e integracao;
- tasks;
- skills.

Por isso ele foi quebrado em varias tarefas.

## Relacao com o sistema atual

Como este modulo ajusta funcionalidades ja existentes, toda tarefa deve considerar o gap analysis:

- `18-gap-analysis-sistema-atual-vs-modulo-1.md`

## Banco de dados

Inicialmente a V2 trabalhava sem banco de dados. Na nova organizacao, a camada declarada provavelmente precisara considerar persistencia para:

- plano referencial oficial;
- metodologia versionada;
- snapshots de analise declarada;
- auditoria e memoria de calculo;
- historico por empresa e exercicio, se aprovado;
- rastreabilidade entre ECD importada, resultado calculado e exportacao.

Essa decisao nao deve ser tomada isoladamente dentro do modulo 1.

Ela depende da tarefa:

- `tmp_deu_a_louca/modulo-00-organizacao-arquitetura-design/11-decisao-banco-dados-persistencia.md`

Enquanto essa decisao nao for fechada, as tarefas do modulo 1 devem indicar claramente quando assumem arquitetura em memoria e quando dependem da arquitetura futura com banco.
