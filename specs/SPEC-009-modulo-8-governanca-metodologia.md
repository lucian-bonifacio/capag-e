# SPEC-009 - Modulo 8: Governanca De Metodologia

## 1. Objetivo Tecnico

Especificar a governanca metodologica do CAPAG, garantindo rastreabilidade entre documentos, specs, manuais, assets, codigo, testes, exportacao, laudo e versao metodologica usada em cada resultado.

## 2. Contexto E Problema

O PRD exige que documentos, specs, assets, codigo, testes e laudo permaneçam rastreaveis entre si. A arquitetura define `MethodologyVersion`, assets versionados, validacoes automatizadas e snapshots com versao metodologica.

O problema central e evitar divergencia entre metodologia documentada e comportamento real do sistema, especialmente quando regras prudenciais, assets, testes e laudos evoluirem ao longo do tempo.

## 3. Fontes Usadas

Fontes principais obrigatorias:

- `docs/product/PRD.md`
- `docs/architecture.md`

Fontes de referencia autorizadas pelo usuario:

- `docs/reference/planejamento-modulos/modulo-08-governanca-metodologia/00-visao-geral.md`
- `docs/reference/planejamento-modulos/modulo-08-governanca-metodologia/01-matriz-cobertura-spec-12.md`
- `docs/reference/planejamento-modulos/modulo-08-governanca-metodologia/02-documentos-governados.md`
- `docs/reference/planejamento-modulos/modulo-08-governanca-metodologia/03-matriz-rastreabilidade-metodologica.md`
- `docs/reference/planejamento-modulos/modulo-08-governanca-metodologia/04-regras-atualizacao-manuais-assets.md`
- `docs/reference/planejamento-modulos/modulo-08-governanca-metodologia/05-validacoes-automatizadas-cobertura.md`
- `docs/reference/planejamento-modulos/modulo-08-governanca-metodologia/06-changelog-versao-metodologia.md`
- `docs/reference/planejamento-modulos/modulo-08-governanca-metodologia/07-ui-governanca-metodologica.md`
- `docs/reference/planejamento-modulos/modulo-08-governanca-metodologia/08-testes-governanca.md`
- `docs/reference/planejamento-modulos/modulo-08-governanca-metodologia/09-roadmap-execucao-modulo-8.md`

Fontes frontend governadas:

- `docs/frontend/DESIGN_TOKENS.md`
- `docs/frontend/UI_COMPONENT_RULES.md`
- `docs/frontend/SCREEN_PATTERNS.md`
- `frontend/src/styles/globals.css`

## 4. Escopo

Esta SPEC cobre:

- documentos governados;
- assets metodologicos governados;
- matriz de rastreabilidade metodologica;
- status permitidos;
- regras de atualizacao de manuais;
- regras de atualizacao de assets;
- validacoes automatizadas;
- relatorio de cobertura metodologica;
- changelog metodologico;
- versao metodologica;
- integracao com laudo/exportacao;
- UI opcional de governanca;
- testes de governanca.

## 5. Fora De Escopo

Esta SPEC nao cobre:

- administracao livre de metodologia pelo usuario final;
- edicao de regras de calculo pela interface;
- publicacao formal de manual externo;
- alterar regras prudenciais sem spec/manual/teste;
- atualizar skills e documentos operacionais antes de consolidar os modulos funcionais.

## 6. Decisoes Ja Aprovadas

- Assets metodologicos continuam versionados no repositorio.
- Cada conjunto publicado vira `MethodologyVersion`.
- Resultados e laudos devem carregar versao metodologica usada.
- Mudanca metodologica nao retroage silenciosamente sobre laudos ja emitidos.
- Documentos operacionais e skills devem ser atualizados por ultimo.
- Manual nao deve afirmar como implementado algo que ainda e planejado.
- Mudanca em formula deve atualizar manual, spec e testes.
- Mudanca em nomenclatura deve atualizar API/exportacao quando aplicavel.

## 7. Decisoes Pendentes

Nao ha bloqueio para criar TASKs do Modulo 8 conforme esta SPEC.

Decisoes futuras:

- Quais assets historicos serao migrados primeiro para `MethodologyVersion`.
- Se a UI de governanca sera implementada no MVP ou apenas apos os motores principais.

## 8. Contratos

### 8.1 Documentos Governados

Documentos e artefatos:

- `README.md`;
- `AGENTS.md`;
- `CLAUDE.md`, se existir;
- `docs/product/PRD.md`;
- `docs/architecture.md`;
- `specs/*.md`;
- `docs/reference/manual-plr-capag-ecd-pgfn-v2.md`;
- `docs/reference/manual-motor-operacional-universal-ebitda.md`;
- `docs/frontend/*.md`;
- `frontend/src/styles/globals.css`.

Skills e instrucoes operacionais:

- `.claude/skills`, se existir;
- `.agents/skills`.

Regra: documentos operacionais e skills ficam por ultimo.

### 8.2 Assets Governados

Assets atuais e futuros:

- `tabela_metodologica_plr.csv`;
- `politica_desagios_plr.json`;
- `tabela_metodologica_fco.csv`;
- `componentes_fco_direto.csv`;
- `tabela_metodologica_dfc.csv`;
- `componentes_dfc_direto.csv`;
- `tabela_metodologica_roa.csv`;
- `componentes_roa.csv`;
- mapeamentos comportamentais familia -> referencial.

Toda alteracao em metodologia deve ter:

- justificativa metodologica;
- referencia a spec/manual;
- teste de carregamento;
- teste de regra afetada;
- changelog;
- versao metodologica.

### 8.3 Matriz De Rastreabilidade

Documento alvo:

- `docs/methodology/matriz-rastreabilidade-metodologica.md`

Colunas minimas:

- `tema`;
- `fonte_normativa`;
- `manual`;
- `spec`;
- `asset`;
- `modulo_codigo`;
- `teste`;
- `status`.

Status permitidos:

- `implementado`;
- `parcial`;
- `planejado`;
- `obsoleto`;
- `em_revisao`.

Temas minimos:

- `PLRA`;
- `FCO`;
- `FCA`;
- `ROA`;
- `CAPAG-E`;
- evidencias;
- avaliacao de ativos;
- laudo;
- metodologia PLR;
- metodologia DFC;
- metodologia ROA.

### 8.4 Validacoes Automatizadas

Validacoes recomendadas:

- verificar colunas obrigatorias dos assets;
- verificar tratamentos permitidos;
- verificar componentes referenciados existentes;
- verificar regras sem componente quando deveriam ter;
- listar codigos referenciais com sobreposicao de prefixos;
- detectar regras sem teste associado;
- gerar relatorio de cobertura metodologica.

Relatorio de cobertura deve listar:

- quantidade de regras PLRA;
- quantidade de regras DFC;
- quantidade de regras ROA;
- regras condicionais;
- regras sem politica de desagio;
- componentes sem regra;
- regras sem teste associado.

### 8.5 Changelog Metodologico

Documento alvo:

- `docs/methodology/changelog-metodologico.md`

Cada mudanca deve registrar:

- o que mudou;
- por que mudou;
- impacto esperado;
- risco;
- testes executados;
- se afeta laudo.

Identificador sugerido:

```text
methodology_version = YYYYMMDD-sequencial
```

### 8.6 Integracao Com Laudo E Exportacao

Laudo e exportacao devem informar:

- versao da metodologia;
- data;
- assets usados;
- status de cobertura;
- snapshot suficiente quando nao houver persistencia historica.

### 8.7 UI Opcional

Rotas possiveis:

```text
/governanca/metodologia
/governanca/cobertura
```

A UI pode mostrar:

- versao metodologica atual;
- alertas de asset incompleto;
- status parcial dos motores;
- data da metodologia;
- caminho dos assets usados.

A UI nao pode:

- editar regra critica;
- publicar manual;
- administrar metodologia livremente.

## 9. Responsabilidades Por Camada

### Domain

Modelar `MethodologyVersion`, status de cobertura e referencias de rastreabilidade.

### Engine/Governance

Validar assets, cobertura, prefixos, componentes e regras associadas a testes.

### Application

Publicar metodologia, registrar changelog e associar versao a analises/snapshots.

### API

Expor consulta de versao/cobertura, se UI for implementada.

### Frontend

Exibir versao e cobertura sem permitir edicao de regra critica.

### Export/Report

Serializar versao metodologica e status de cobertura.

## 10. Dados De Entrada E Saida

Entradas:

- docs governados;
- specs;
- assets metodologicos;
- testes;
- snapshots;
- laudos/exportacoes;
- changelog.

Saidas:

- matriz de rastreabilidade;
- `MethodologyVersion`;
- relatorio de cobertura;
- changelog metodologico;
- validacoes automatizadas;
- dados de versao em laudo/exportacao;
- UI opcional de governanca.

## 11. Estados E Erros Relevantes

Estados:

- `implementado`;
- `parcial`;
- `planejado`;
- `obsoleto`;
- `em_revisao`.

Erros e bloqueios:

- asset sem coluna obrigatoria;
- tratamento invalido;
- componente inexistente;
- regra sem teste associado;
- regra sem spec/manual;
- laudo/exportacao sem versao metodologica;
- manual declarando planejado como implementado;
- mudanca metodologica sem changelog;
- tentativa de alterar laudo historico por metodologia nova.

## 12. Criterios De Aceite

- Existe matriz de rastreabilidade planejada.
- Documentos governados estao definidos.
- Assets governados estao definidos.
- Status permitidos estao definidos.
- Regras de atualizacao de manuais e assets estao definidas.
- Validacoes automatizadas estao especificadas.
- Relatorio de cobertura metodologica esta especificado.
- Changelog metodologico esta especificado.
- Laudo/exportacao informam versao metodologica.
- UI de governanca, se existir, nao edita regra critica.
- Documentos operacionais e skills ficam por ultimo.

## 13. Estrategia De Validacao Esperada

Testes obrigatorios:

- validar colunas obrigatorias dos assets PLR/FCO atuais;
- validar que todo componente referenciado existe;
- validar tratamentos permitidos;
- validar regras sem teste associado;
- validar que laudo/exportacao inclui versao metodologica;
- validar que manual/spec de estado atual nao contradiz motores implementados em pontos canonicos;
- validar relatorio de cobertura.

## 14. Riscos E Mitigacoes

- Risco: metodologia mudar sem teste.
  Mitigacao: validacoes e teste de regra afetada obrigatorios.

- Risco: laudo historico mudar por metodologia nova.
  Mitigacao: `MethodologyVersion` em snapshots/laudos e proibicao de retroatividade silenciosa.

- Risco: docs e codigo divergirem.
  Mitigacao: matriz de rastreabilidade e validacao de pontos canonicos.

- Risco: UI permitir edicao critica sem governanca.
  Mitigacao: UI somente leitura para versao/cobertura.

- Risco: skills antigas orientarem agentes incorretamente.
  Mitigacao: atualizar skills apenas apos consolidar arquitetura e specs.

## 15. Bloqueios

Nao ha bloqueio para criar TASKs do Modulo 8 conforme esta SPEC.

Permanece bloqueado qualquer trabalho que tente:

- mudar metodologia sem spec/manual/teste/changelog;
- emitir laudo/exportacao sem versao metodologica;
- editar regra critica pela UI;
- atualizar AGENTS/skills finais antes de consolidar os modulos principais;
- retroagir metodologia sobre laudos ja emitidos.
