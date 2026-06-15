# Modulo 2 - CAPAG Reclassificada

## Nome provisorio

Nome de trabalho:

- **CAPAG Reclassificada**

Nomes alternativos a decidir:

- CAPAG Auditada;
- CAPAG Refeita;
- CAPAG Comportamental;
- CAPAG por Substancia;
- Analise Comportamental da ECD.

## Objetivo

Criar o planejamento completo do modulo que fara uma segunda leitura da ECD, paralela a camada declarada.

Este modulo deve responder:

> O que os movimentos, saldos, historicos, contrapartidas, recorrencia e materialidade mostram que esta conta realmente parece ser?

## Documentos-base

- `docs/reference/nova_spec_nv_modulo.md`
- `docs/reference/novo_modulo_reclass.md`
- `tmp_deu_a_louca/modulo-01-camada-declarada/`

## Matriz de cobertura

A cobertura das secoes dos documentos de referencia esta controlada em:

- `22-matriz-cobertura-doc-referencia.md`

## Decisao conceitual central

O sistema passara a conviver com duas leituras:

1. **Camada declarada**
   - usa `I051` como classificacao referencial declarada;
   - calcula o resultado conforme a ECD entregue e a metodologia vigente;
   - responde o resultado oficial declarado.

2. **Camada reclassificada/comportamental**
   - preserva o `I051` como dado declarado;
   - nao usa o `I051` como verdade decisoria principal na segunda leitura;
   - calcula perfil comportamental;
   - aplica regras deterministicas;
   - gera score, evidencias, justificativas e recomendacoes;
   - compara o resultado reclassificado com o declarado.

## Fronteira importante

Este modulo nao substitui silenciosamente a camada declarada.

Ele tambem nao e uma classificacao por palavra-chave.

A decisao deve vir do conjunto:

- nome da conta;
- hierarquia;
- saldo;
- debitos;
- creditos;
- contrapartidas;
- historicos;
- recorrencia;
- materialidade;
- precedentes, quando existirem e forem permitidos.

Os riscos conceituais e salvaguardas estao detalhados em:

- `24-riscos-conceituais-e-salvaguardas.md`

## Arquitetura vigente e banco de dados

A V2 original trabalhava sem banco de dados. Porem, este modulo tem forte tendencia a precisar de persistencia para:

- perfis comportamentais;
- scores;
- evidencias;
- revisoes humanas;
- precedentes;
- historico comparativo entre analise declarada e reclassificada.

Por isso, a decisao sobre banco de dados deve ser tomada no modulo 0, antes de implementar este modulo:

- `tmp_deu_a_louca/modulo-00-organizacao-arquitetura-design/11-decisao-banco-dados-persistencia.md`

Enquanto a decisao nao for fechada, o planejamento deve separar:

- MVP em memoria, se ainda for necessario;
- arquitetura com banco, se aprovada;
- precedentes temporarios;
- precedentes persistidos;
- regras versionadas;
- resultados operacionais persistidos.

Mesmo com banco, continuam valendo:

- sem CSV como exportacao oficial;
- sem administracao livre de regras pela interface sem governanca;
- sem IA generativa como nucleo decisorio;
- sem regra de negocio duplicada no frontend;
- uso de `Decimal` no backend;
- exportacao oficial em Excel.

## Resultado esperado do modulo

Para cada conta:

- classificacao original declarada;
- familia comportamental sugerida;
- codigo referencial sugerido, se aplicavel;
- score;
- nivel de confianca;
- evidencias positivas;
- evidencias negativas;
- justificativa auditavel;
- acao recomendada: manter, reclassificar, revisar ou sem conclusao;
- impacto potencial em PLR e CAPAG-e.

No consolidado:

- PLR declarado;
- PLR reclassificado;
- CAPAG-e declarada;
- CAPAG-e reclassificada;
- diferenca entre cenarios;
- contas que explicam a diferenca;
- contas automaticamente reclassificadas no cenario comportamental;
- contas enviadas para revisao.
