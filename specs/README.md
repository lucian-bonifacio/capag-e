# SPECs - CAPAG

## Objetivo

Este indice registra as SPECs oficiais do CAPAG, seu status documental, suficiencia para gerar TASKs, dependencias, bloqueios declarados e TASKs derivadas existentes.

Este documento e um indice de rastreabilidade. Ele nao substitui as SPECs, nao altera contratos tecnicos, nao resolve bloqueios e nao cria regra de dominio, contrato de API, formula prudencial, politica de arredondamento ou golden case.

## Regras De Uso

- Toda TASK funcional deve apontar diretamente para uma SPEC suficiente.
- SPEC insuficiente nao deve gerar TASK funcional.
- `docs/reference/` nao e fonte normativa direta para TASKs, salvo autorizacao explicita do usuario ou incorporacao previa em documento governado.
- Em caso de divergencia entre este indice e uma SPEC, prevalece a SPEC.
- Mudancas tecnicas devem ocorrer nas SPECs correspondentes, nao neste indice.

## Resumo

| SPEC | Modulo | Status documental | Suficiencia para TASK | Fontes principais | Dependencias conhecidas | Bloqueios declarados | TASKs derivadas existentes |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `SPEC-001-modulo-0-fundacao-governada.md` | Modulo 0 - Fundacao Governada | suficiente_para_task | Suficiente para TASKs estruturais e documentais de fundacao. | `docs/product/PRD.md`; `docs/architecture/architecture.md`; docs frontend governados quando aplicavel. | PRD e arquitetura aprovados. | Nao ha bloqueio para TASKs estruturais; permanecem bloqueadas TASKs funcionais de dominio prudencial sem SPEC especifica suficiente. | `TASK-001` a `TASK-034`, incluindo `TASK-002A`, `TASK-011A`, `TASK-011B` e `TASK-021A`. |
| `SPEC-002-modulo-1-camada-declarada.md` | Modulo 1 - Camada Declarada | suficiente_para_task | Suficiente para TASKs da camada declarada. | `docs/product/PRD.md`; `docs/architecture/architecture.md`; `SPEC-001`. | Fundacao governada; fronteiras de camadas; metodologia declarada conforme SPEC. | Nao ha bloqueio para TASKs da camada declarada; permanecem bloqueadas alteracoes fora dos limites da SPEC. | `TASK-035` a `TASK-041`. |
| `SPEC-003-modulo-2-capag-reclassificada.md` | Modulo 2 - CAPAG Reclassificada | suficiente_para_task | Suficiente para TASKs da camada reclassificada. | `docs/product/PRD.md`; `docs/architecture/architecture.md`; `SPEC-001`; SPECs relacionadas quando houver integracao. | Camada declarada; contratos posteriores para resultado, evidencias e laudo quando necessarios. | Nao ha bloqueio para TASKs do Modulo 2; cenarios podem ser parciais ou bloqueados ate contratos posteriores existirem. | `TASK-042` a `TASK-048`. |
| `SPEC-004-modulo-3-contrato-capag-e-plra-fca-roa.md` | Modulo 3 - Contrato CAPAG-E, PLRA, FCA e ROA | suficiente_para_task | Suficiente para TASKs do contrato CAPAG-E. | `docs/product/PRD.md`; `docs/architecture/architecture.md`; `SPEC-001`; SPECs de componentes quando aplicavel. | Componentes `PLRA`, `FCA` e `ROA`; modulos de evidencias e laudo para integracoes especificas. | Nao ha bloqueio para TASKs do contrato; componentes ausentes, parciais ou bloqueados devem ser representados sem esconder limitacoes. | `TASK-049` a `TASK-054`; `TASK-070`. |
| `SPEC-005-modulo-4-evidencias-justificativas-ativos.md` | Modulo 4 - Evidencias, Justificativas e Avaliacao de Ativos | suficiente_para_task | Suficiente para TASKs de evidencias, materialidade, bloqueios e ativos. | `docs/product/PRD.md`; `docs/architecture/architecture.md`; `SPEC-001`; contratos afetados quando houver integracao. | Contrato CAPAG-E e laudo para consumo de bloqueios e ressalvas. | Nao ha bloqueio para TASKs do Modulo 4; permanece bloqueado emitir resultado/laudo final ignorando evidencia critica pendente. | `TASK-055` a `TASK-060`. |
| `SPEC-006-modulo-5-dfc-direta-fca.md` | Modulo 5 - DFC Direta Completa e FCA | suficiente_para_task | Suficiente para TASKs de DFC direta e FCA. | `docs/product/PRD.md`; `docs/architecture/architecture.md`; `SPEC-001`; contratos CAPAG-E quando houver integracao. | Camada declarada, dados normalizados, evidencias e contrato CAPAG-E. | Nao ha bloqueio para TASKs do Modulo 5; permanecem bloqueadas simplificacoes que apresentem componente parcial como FCA final. | `TASK-061` a `TASK-066`. |
| `SPEC-007-modulo-6-motor-roa-plra.md` | Modulo 6 - Motor ROA + PLRA | suficiente_para_task | Suficiente para TASKs do motor ROA + PLRA. | `docs/product/PRD.md`; `docs/architecture/architecture.md`; `SPEC-001`; contrato CAPAG-E quando houver integracao. | Camada declarada, evidencias e contrato CAPAG-E. | Nao ha bloqueio para TASKs do Modulo 6; resultados finais dependem de componentes e bloqueios do contrato CAPAG-E. | `TASK-067` a `TASK-072`. |
| `SPEC-008-modulo-7-gerador-laudo-capag-e.md` | Modulo 7 - Gerador de Laudo CAPAG-E | suficiente_para_task | Suficiente para TASKs do laudo CAPAG-E. | `docs/product/PRD.md`; `docs/architecture/architecture.md`; `SPEC-001`; contrato CAPAG-E e evidencias quando aplicavel. | Resultados calculados, evidencias, bloqueios, snapshots e versao metodologica. | Nao ha bloqueio para TASKs do Modulo 7; permanece bloqueado recalcular motores, esconder limitacoes ou ignorar evidencias criticas pendentes. | `TASK-073` a `TASK-078`. |
| `SPEC-009-modulo-8-governanca-metodologia.md` | Modulo 8 - Governanca de Metodologia | suficiente_para_task | Suficiente para TASKs de governanca metodologica. | `docs/product/PRD.md`; `docs/architecture/architecture.md`; `SPEC-001`; documentos metodologicos governados quando incorporados. | Assets metodologicos, `MethodologyVersion`, validacoes e rastreabilidade entre documentos, codigo, testes e laudo. | Nao ha bloqueio para TASKs do Modulo 8; permanece bloqueado tratar `docs/reference/` como fonte normativa direta sem governanca. | `TASK-079` a `TASK-084`. |

## Detalhamento Por SPEC

### SPEC-001 - Modulo 0: Fundacao Governada

- Arquivo: `SPEC-001-modulo-0-fundacao-governada.md`
- Status documental: `suficiente_para_task`
- Suficiencia: TASKs estruturais e documentais de fundacao.
- Dependencias: PRD e arquitetura aprovados.
- Bloqueios: nao ha bloqueio para TASKs estruturais; TASKs funcionais de dominio prudencial exigem SPEC propria suficiente.
- TASKs derivadas: `TASK-001` a `TASK-034`, incluindo `TASK-002A`, `TASK-011A`, `TASK-011B` e `TASK-021A`.

### SPEC-002 - Modulo 1: Camada Declarada

- Arquivo: `SPEC-002-modulo-1-camada-declarada.md`
- Status documental: `suficiente_para_task`
- Suficiencia: TASKs da camada declarada.
- Dependencias: fundacao governada e fronteiras de camadas.
- Bloqueios: permanecem bloqueadas mudancas que extrapolem os limites da SPEC.
- TASKs derivadas: `TASK-035` a `TASK-041`.

### SPEC-003 - Modulo 2: CAPAG Reclassificada

- Arquivo: `SPEC-003-modulo-2-capag-reclassificada.md`
- Status documental: `suficiente_para_task`
- Suficiencia: TASKs da camada reclassificada.
- Dependencias: camada declarada e contratos posteriores para resultado, evidencias e laudo quando aplicavel.
- Bloqueios: cenarios podem permanecer parciais ou bloqueados ate contratos posteriores existirem.
- TASKs derivadas: `TASK-042` a `TASK-048`.

### SPEC-004 - Modulo 3: Contrato CAPAG-E, PLRA, FCA E ROA

- Arquivo: `SPEC-004-modulo-3-contrato-capag-e-plra-fca-roa.md`
- Status documental: `suficiente_para_task`
- Suficiencia: TASKs do contrato CAPAG-E.
- Dependencias: componentes `PLRA`, `FCA`, `ROA`, evidencias e laudo conforme integracao.
- Bloqueios: componentes ausentes, parciais ou bloqueados devem permanecer explicitos.
- TASKs derivadas: `TASK-049` a `TASK-054`; `TASK-070`.

### SPEC-005 - Modulo 4: Evidencias, Justificativas E Avaliacao De Ativos

- Arquivo: `SPEC-005-modulo-4-evidencias-justificativas-ativos.md`
- Status documental: `suficiente_para_task`
- Suficiencia: TASKs de evidencias, materialidade, bloqueios e ativos.
- Dependencias: contrato CAPAG-E e laudo para consumo de bloqueios e ressalvas.
- Bloqueios: resultado/laudo final nao pode ignorar evidencia critica pendente.
- TASKs derivadas: `TASK-055` a `TASK-060`.

### SPEC-006 - Modulo 5: DFC Direta Completa E FCA

- Arquivo: `SPEC-006-modulo-5-dfc-direta-fca.md`
- Status documental: `suficiente_para_task`
- Suficiencia: TASKs de DFC direta e FCA.
- Dependencias: camada declarada, dados normalizados, evidencias e contrato CAPAG-E.
- Bloqueios: componente parcial nao deve ser apresentado como FCA final.
- TASKs derivadas: `TASK-061` a `TASK-066`.

### SPEC-007 - Modulo 6: Motor ROA + PLRA

- Arquivo: `SPEC-007-modulo-6-motor-roa-plra.md`
- Status documental: `suficiente_para_task`
- Suficiencia: TASKs do motor ROA + PLRA.
- Dependencias: camada declarada, evidencias e contrato CAPAG-E.
- Bloqueios: resultado final depende dos componentes e bloqueios do contrato CAPAG-E.
- TASKs derivadas: `TASK-067` a `TASK-072`.

### SPEC-008 - Modulo 7: Gerador De Laudo CAPAG-E

- Arquivo: `SPEC-008-modulo-7-gerador-laudo-capag-e.md`
- Status documental: `suficiente_para_task`
- Suficiencia: TASKs do laudo CAPAG-E.
- Dependencias: resultados calculados, evidencias, bloqueios, snapshots e versao metodologica.
- Bloqueios: laudo nao recalcula motores, nao esconde limitacoes e nao ignora evidencias criticas pendentes.
- TASKs derivadas: `TASK-073` a `TASK-078`.

### SPEC-009 - Modulo 8: Governanca De Metodologia

- Arquivo: `SPEC-009-modulo-8-governanca-metodologia.md`
- Status documental: `suficiente_para_task`
- Suficiencia: TASKs de governanca metodologica.
- Dependencias: assets metodologicos, `MethodologyVersion`, validacoes e rastreabilidade.
- Bloqueios: `docs/reference/` nao pode ser tratado como fonte normativa direta sem governanca.
- TASKs derivadas: `TASK-079` a `TASK-084`.
