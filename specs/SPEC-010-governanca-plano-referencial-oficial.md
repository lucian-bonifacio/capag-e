# SPEC-010 - Governanca Do Plano Referencial Oficial

## 1. Objetivo Tecnico

Definir a governanca do plano referencial oficial usado pelo CAPAG para validar e enriquecer o `COD_CTA_REF` declarado na ECD.

Esta SPEC cobre a pesquisa, aprovacao, versionamento, armazenamento, validacao, manutencao controlada e futura administracao do plano referencial oficial, sem transformar essa base em metodologia prudencial ou fonte de reclassificacao.

## 2. Contexto E Problema

A `SPEC-002` define que a camada declarada deve preservar o `COD_CTA_REF` informado no `I051` da ECD e consultar um plano referencial oficial para obter significado formal, hierarquia, natureza, vigencia, leiaute, tipo de entidade, fonte, status e versao metodologica.

A `TASK-086` criou a infraestrutura minima para exigir uma tabela oficial governada. No entanto, ainda nao existe fonte oficial aprovada para alimentar essa base de forma completa.

Sem uma governanca propria, a tabela oficial pode virar:

- um asset incompleto tratado como verdade final;
- uma lista manual sem rastreabilidade de origem;
- uma tabela editavel livremente sem controle de versao;
- uma forma indireta de alterar regra prudencial ou reclassificacao;
- uma fonte persistida no banco sem processo claro de auditoria e aprovacao.

## 3. Fontes Usadas

Fontes principais obrigatorias:

- `docs/product/PRD.md`
- `docs/architecture/architecture.md`
- `specs/SPEC-001-modulo-0-fundacao-governada.md`
- `specs/SPEC-002-modulo-1-camada-declarada.md`
- `specs/SPEC-009-modulo-8-governanca-metodologia.md`
- `tasks/TASK-086-tabela-oficial-referencial-obrigatoria.md`

Fonte operacional relacionada:

- `backend/app/assets/reference/official_reference_accounts.json`

Materiais em `docs/reference/` nao sao fonte normativa direta desta SPEC, salvo quando uma TASK futura autorizar pesquisa e incorporacao controlada.

## 4. Escopo

Esta SPEC cobre:

- processo para pesquisar e selecionar fonte oficial do plano referencial;
- criterios de aceitacao da fonte oficial;
- modelo governado do plano referencial oficial;
- versionamento e rastreabilidade da fonte;
- validacoes automaticas de completude, formato, vigencia e duplicidade;
- relacao entre asset versionado e persistencia em banco;
- estrategia futura para CRUD controlado;
- trilha de auditoria para alteracoes;
- limites entre plano referencial oficial, metodologia interna e camada reclassificada;
- criterios para criar TASKs documentais, de pesquisa, de modelagem, de carga, de persistencia e de interface administrativa.

## 5. Fora De Escopo

Esta SPEC nao cobre:

- escolher agora uma fonte oficial definitiva;
- popular agora o plano referencial oficial completo;
- criar agora migrations, tabelas ou CRUD sem cumprir os gates internos desta SPEC;
- alterar a metodologia interna da camada declarada;
- definir regra prudencial, formula, fonte normativa prudencial ou arredondamento;
- inferir codigo referencial alternativo para conta da ECD;
- reclassificar contas com base em nome, comportamento ou historico;
- permitir edicao livre de classificacao prudencial pela interface.

## 6. Decisoes Ja Aprovadas

- A ECD permanece a fonte declaratoria.
- O `I051` declara o `COD_CTA_REF` usado pela camada declarada.
- O plano referencial oficial descreve e valida o significado formal do codigo declarado.
- O plano referencial oficial nao decide calculo.
- O plano referencial oficial nao escolhe codigo alternativo ao declarado.
- A metodologia interna e separada do plano referencial oficial.
- Ausencia da tabela oficial e erro de configuracao do sistema.
- Codigo declarado pela ECD e ausente na tabela oficial carregada gera `COD_CTA_REF_NAO_ENCONTRADO_NA_TABELA_OFICIAL`.
- A base oficial precisa ser governada, versionada e auditavel antes de ser tratada como fonte operacional ampla.

## 7. Decisoes Pendentes

Decisoes essenciais pendentes:

- qual fonte oficial sera usada para popular o plano referencial;
- qual leiaute, periodo, tipo de entidade e escopo inicial serao cobertos;
- como obter, armazenar e comprovar a origem da fonte;
- quais campos adicionais serao necessarios alem dos campos minimos da `SPEC-002`;
- se a primeira carga completa ficara apenas como asset versionado, banco de dados, ou ambos;
- qual nivel de CRUD sera permitido;
- quem ou qual processo aprova ajustes manuais;
- como tratar correcao de erro na fonte carregada sem alterar historico silenciosamente;
- como publicar nova versao do plano referencial e invalidar/reprocessar analises dependentes quando necessario.

Enquanto essas decisoes nao forem aprovadas, permanecem bloqueadas apenas as TASKs executivas que dependam delas. A propria continuidade governada do ciclo do plano referencial oficial permanece coberta por esta SPEC.

## 7.1 Continuidade Governada

A `SPEC-010` governa a evolucao completa do plano referencial oficial, incluindo:

- pesquisa e aprovacao da fonte oficial;
- contrato de carga, metadados, hash e rastreabilidade;
- asset governado completo;
- validacoes automaticas de fonte e asset;
- persistencia em banco;
- versionamento operacional;
- auditoria de cargas e alteracoes;
- API de consulta e administracao;
- UX/CRUD controlado.

Essas etapas devem ser tratadas como uma cadeia governada. Cada etapa posterior so pode gerar TASK executiva quando seus gates predecessores estiverem satisfeitos.

Gates minimos:

- TASKs de pesquisa e proposta documental podem ser criadas imediatamente.
- TASKs de contrato de carga e validacao podem ser criadas com base nesta SPEC, desde que nao publiquem base operacional completa sem fonte aprovada.
- TASKs de asset completo exigem fonte oficial aprovada e criterio de cobertura definido.
- TASKs de banco exigem fonte oficial aprovada, contrato de carga aprovado, campos finais definidos e estrategia de versionamento aprovada.
- TASKs de CRUD operacional exigem banco/modelo de versionamento aprovados, regras de permissao, auditoria, publicacao e bloqueio definidas.
- TASKs de publicacao operacional ampla exigem validacao automatica, trilha de origem e decisao governada de publicacao.

## 8. Contratos

### 8.1 Papel Do Plano Referencial Oficial

O plano referencial oficial deve:

- validar existencia do `COD_CTA_REF` declarado;
- fornecer descricao oficial;
- fornecer hierarquia oficial;
- fornecer natureza oficial;
- informar vigencia;
- informar leiaute;
- informar tipo de entidade;
- informar fonte;
- informar status;
- informar versao metodologica ou versao da base oficial.

O plano referencial oficial nao pode:

- alterar o codigo declarado pela ECD;
- sugerir codigo alternativo;
- decidir tratamento PLRA, FCO, FCA, ROA ou CAPAG-E;
- substituir metodologia interna;
- substituir revisao humana ou camada reclassificada;
- aplicar regra prudencial por inferencia.

### 8.2 Campos Minimos

Campos minimos herdados da `SPEC-002`:

- `reference_code`;
- `official_description`;
- `parent_reference_code`;
- `level`;
- `nature`;
- `valid_from`;
- `valid_to`;
- `layout`;
- `entity_type`;
- `source`;
- `status`;
- `methodology_version_id`.

Campos candidatos para evolucao desta SPEC, pendentes de aprovacao da fonte:

- `official_version_id`;
- `source_document_name`;
- `source_document_hash`;
- `source_document_date`;
- `source_url_or_reference`;
- `loaded_at`;
- `loaded_by`;
- `approval_status`;
- `approval_notes`;
- `superseded_by`;
- `change_reason`.

### 8.3 Estados Da Base Oficial

Estados permitidos para a base oficial:

- `rascunho`: levantamento inicial, nao operacional;
- `em_validacao`: fonte em revisao documental e tecnica;
- `aprovada`: fonte aprovada para carga operacional;
- `publicada`: versao carregada e disponivel para execucao;
- `substituida`: versao preservada historicamente, mas nao usada em novas analises;
- `bloqueada`: fonte ou versao impedida de uso por erro, suspeita ou decisao governada.

### 8.4 Estados Por Codigo

Estados permitidos por codigo:

- `ATIVA`: codigo valido para validacao declarada no periodo aplicavel;
- `INATIVA`: codigo preservado historicamente, mas nao aplicavel a nova validacao no periodo;
- `EM_REVISAO`: codigo presente, mas com pendencia de fonte ou interpretacao formal;
- `BLOQUEADA`: codigo nao deve ser usado ate decisao governada.

### 8.5 Asset Versionado E Banco De Dados

O asset versionado deve continuar existindo como fonte governada de reproducibilidade.

O banco de dados pode ser introduzido futuramente para:

- consulta operacional eficiente;
- historico de versoes;
- trilha de carga;
- auditoria de alteracoes;
- relacionamento com analises e snapshots;
- administracao controlada.

Se houver banco, a carga no banco deve apontar para uma versao governada do asset ou para uma fonte aprovada com hash e metadados equivalentes. O banco nao pode virar a unica fonte sem rastreabilidade versionada.

### 8.6 CRUD Controlado

Um CRUD futuro para o plano referencial oficial deve ser tratado como administracao governada, nao como editor livre de metodologia.

Operacoes minimas candidatas:

- listar codigos;
- filtrar por codigo, descricao, natureza, vigencia, leiaute, status e versao;
- visualizar detalhe e origem;
- importar nova versao;
- validar pre-publicacao;
- publicar versao;
- bloquear versao ou codigo;
- registrar correcao com justificativa;
- comparar versoes.

Operacoes que exigem regra adicional antes de implementacao:

- editar codigo publicado;
- excluir codigo publicado;
- alterar vigencia retroativamente;
- alterar natureza oficial;
- corrigir descricao oficial com impacto em analise historica;
- republicar versao usada por analise existente.

### 8.7 Auditoria

Toda mudanca operacional relevante deve registrar:

- usuario ou processo;
- data/hora;
- fonte usada;
- hash da fonte quando houver arquivo;
- versao anterior;
- versao nova;
- diferencas principais;
- justificativa;
- status de aprovacao;
- impacto esperado em analises existentes.

## 9. Responsabilidades Por Camada

### Assets

Armazenar fonte governada versionada, manifestos, hashes, metadados e validacoes automatizaveis.

### Domain

Modelar base oficial, versao, codigo, vigencia, status, origem e invariantes.

### Application

Orquestrar importacao, validacao, publicacao, bloqueio e consulta da base oficial.

### Repositories

Persistir versoes, codigos e auditoria quando a etapa de banco for aprovada.

### API

Expor consulta e administracao controlada, diferenciando erro de configuracao, erro de validacao da fonte e pendencia por codigo.

### Frontend

Permitir consulta, revisao e administracao controlada sem recalcular regra prudencial e sem sugerir reclassificacao.

### Engine

Consumir somente versoes publicadas do plano oficial para validar e enriquecer `COD_CTA_REF` declarado.

## 10. Dados De Entrada E Saida

Entradas futuras:

- fonte oficial aprovada;
- arquivo ou documento fonte;
- metadados de origem;
- regras de validade e vigencia;
- decisao de escopo inicial;
- usuario ou processo responsavel pela carga.

Saidas futuras:

- asset governado do plano referencial oficial;
- relatorio de validacao da fonte;
- versao publicada;
- registros persistidos no banco, quando aprovado;
- trilha de auditoria;
- endpoint de consulta;
- tela administrativa controlada, quando aprovada.

## 11. Estados E Erros Relevantes

Erros de configuracao:

- fonte oficial nao aprovada;
- asset ausente;
- asset vazio;
- asset invalido;
- versao nao publicada;
- banco sem carga publicada, quando banco for obrigatorio.

Pendencias por codigo:

- codigo declarado nao encontrado na versao publicada;
- codigo fora de vigencia;
- codigo bloqueado;
- codigo em revisao.

Erros de governanca:

- tentativa de editar codigo publicado sem justificativa;
- tentativa de excluir historico;
- tentativa de usar fonte sem hash ou origem rastreavel;
- tentativa de alterar base usada por analise historica sem nova versao.

## 12. Criterios De Aceite

- A SPEC separa plano referencial oficial, metodologia interna e camada reclassificada.
- A SPEC registra que ainda nao existe fonte oficial aprovada.
- A SPEC governa a continuidade completa do plano referencial oficial, incluindo asset completo, banco, versionamento, auditoria e CRUD controlado.
- A SPEC bloqueia apenas TASKs executivas que ainda nao tenham cumprido seus gates predecessores.
- A SPEC define campos minimos e campos candidatos para evolucao.
- A SPEC define estados da base oficial e dos codigos.
- A SPEC define relacao entre asset versionado e banco de dados futuro.
- A SPEC define limites para CRUD controlado.
- A SPEC preserva que plano oficial nao decide calculo nem sugere codigo alternativo.
- A SPEC permite criar TASKs documentais e de pesquisa para identificar, preparar e validar fonte oficial.

## 13. Estrategia De Validacao Esperada

Para TASKs documentais e de pesquisa:

- registrar fonte analisada;
- registrar criterio de confiabilidade;
- registrar cobertura por leiaute, vigencia e tipo de entidade;
- registrar lacunas e riscos;
- nao popular base operacional sem aprovacao.

Para TASKs futuras de asset:

- validar JSON/manifesto;
- validar campos obrigatorios;
- validar duplicidades por codigo, leiaute, entidade e vigencia;
- validar hierarquia;
- validar vigencia;
- validar status permitidos;
- validar hash e metadados de origem.

Para TASKs futuras de banco:

- validar migrations via Docker Compose;
- validar carga idempotente;
- validar consulta por versao;
- validar bloqueio sem versao publicada;
- validar preservacao de historico.

Para TASKs futuras de UI/CRUD:

- validar permissao e estados;
- validar que edicoes exigem justificativa;
- validar que publicacao cria nova versao;
- validar que frontend nao recalcula nem sugere reclassificacao.

## 14. Riscos E Mitigacoes

- Risco: fonte incompleta virar verdade operacional.
  Mitigacao: exigir aprovacao, validacao de cobertura e status de versao antes de publicar.

- Risco: CRUD virar edicao livre de metodologia.
  Mitigacao: restringir CRUD ao plano oficial, exigir justificativa, auditoria e impedir regra prudencial local.

- Risco: banco substituir rastreabilidade versionada.
  Mitigacao: banco deve apontar para fonte governada, hash, versao e metadados.

- Risco: alteracao retroativa afetar analises historicas.
  Mitigacao: publicar nova versao e preservar vinculo da analise a versao usada.

- Risco: plano oficial ser usado para inferir codigo alternativo.
  Mitigacao: manter proibicao explicita e testes de camada declarada.

## 15. Gates De Execucao

Liberado imediatamente por esta SPEC:

- criar TASKs documentais de pesquisa de fonte oficial;
- criar TASKs de proposta de contrato de carga;
- criar TASKs de validacao automatica de asset;
- criar TASKs de desenho tecnico para persistencia futura;
- criar TASKs de desenho de UX/controle para CRUD futuro, sem implementar CRUD ainda.

Liberado apos aprovacao dos gates predecessores:

- popular o plano referencial oficial completo;
- criar migrations e tabelas de persistencia;
- implementar carga idempotente em banco;
- implementar versionamento operacional;
- implementar API de consulta administrativa;
- implementar CRUD administrativo controlado;
- publicar nova versao operacional ampla.

Permanece proibido:

- usar fonte externa sem aprovacao e registro governado;
- publicar base operacional sem hash, origem e metadados minimos;
- editar ou excluir historico de codigo publicado sem nova versao e auditoria;
- usar o plano referencial para inferir codigo alternativo ou alterar metodologia prudencial.
