# 01 - Nome, escopo e linguagem do modulo

## Objetivo

Escolher o nome correto do modulo e estabelecer linguagem tecnica segura.

## Ponto de decisao

Escolher entre:

- CAPAG Reclassificada;
- CAPAG Auditada;
- CAPAG Refeita;
- CAPAG Comportamental;
- Analise Comportamental da ECD.

## Arquivos correlatos

- `docs/reference/nova_spec_nv_modulo.md`
- `docs/reference/novo_modulo_reclass.md`
- `README.md`
- `docs/specs/`
- futuro frontend React;
- futura exportacao Excel/laudo.

## Detalhamento

- Evitar dizer que o sistema "ignora o I051" de forma absoluta.
- Usar linguagem preferencial:
  - o modulo preserva o `I051` como classificacao declarada;
  - o modulo nao usa o `I051` como verdade decisoria principal na segunda analise;
  - o modulo confronta a classificacao declarada com a substancia economica observada.
- Definir se o termo "reclassificada" pode passar a impressao de resultado final obrigatorio.
- Definir se o termo "auditada" comunica melhor que existe revisao/evidencia.
- Definir como o nome aparecera:
  - em tela;
  - no Excel;
  - no futuro laudo;
  - nas specs;
  - nas tasks.

## Entregavel

Decisao de nomenclatura e glossario basico.

## Criterios de sucesso

- O nome nao confunde camada declarada com camada comportamental.
- A linguagem preserva rastreabilidade.
- O modulo nao parece substituir automaticamente a ECD.

## Fora do escopo

- Implementar telas.
- Alterar docs oficiais fora de `tmp_deu_a_louca/`.

