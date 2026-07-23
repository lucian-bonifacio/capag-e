# TASK-092 - Desenhar persistencia e versionamento do plano referencial

## SPEC De Origem

- `specs/SPEC-010-governanca-plano-referencial-oficial.md`

## Dependencias

- `TASK-089-definir-contrato-carga-plano-referencial.md`
- `TASK-091-preparar-asset-completo-plano-referencial.md`

## Objetivo

Desenhar o modelo tecnico de persistencia, versionamento e auditoria do plano referencial oficial, preservando o asset versionado como fonte governada de reproducibilidade.

## Fontes Usadas

- `docs/product/PRD.md`
- `docs/architecture/architecture.md`
- `specs/SPEC-001-modulo-0-fundacao-governada.md`
- `specs/SPEC-002-modulo-1-camada-declarada.md`
- `specs/SPEC-009-modulo-8-governanca-metodologia.md`
- `specs/SPEC-010-governanca-plano-referencial-oficial.md`
- contrato de carga da `TASK-089`
- asset completo da `TASK-091`

## Escopo Exato

- Definir desenho tecnico de tabelas, entidades e repositorios.
- Definir relacao entre asset versionado, carga em banco e versao publicada.
- Definir trilha de auditoria de importacao, publicacao, bloqueio e substituicao.
- Definir regras de idempotencia de carga.
- Definir preservacao de historico e vinculo com analises existentes.
- Registrar proposta sem implementar migration ainda, salvo autorizacao de TASK futura.

## Fora De Escopo

- Criar migrations ou tabelas executivas nesta TASK.
- Implementar carga em banco.
- Implementar API ou CRUD.
- Alterar snapshots historicos.
- Tratar banco como fonte unica sem asset ou hash rastreavel.

## Passos Executaveis

1. Ler arquitetura de dados e `SPEC-010`.
2. Ler contrato de carga e asset completo aprovado.
3. Desenhar entidades e relacionamentos necessarios.
4. Definir estrategia de versionamento e publicacao.
5. Definir eventos de auditoria e dados minimos de trilha.
6. Definir gates para TASK futura de migration/carga.
7. Registrar desenho em documento governado.

## Arquivos Ou Areas Provaveis

- `docs/architecture/`
- `docs/methodology/`
- `specs/SPEC-010-governanca-plano-referencial-oficial.md`, se houver ajuste aprovado
- `backend/app/domain/`, apenas como referencia de desenho
- `backend/app/models/`, apenas como referencia de desenho

## Criterios De Aceite

- Modelo proposto preserva asset versionado e hash.
- Historico de versoes nao pode ser alterado silenciosamente.
- Carga em banco tem criterio de idempotencia.
- Analises podem apontar para versao usada.
- Gates para migration e carga executiva estao claros.

## Validacao Esperada

- Revisar consistencia documental contra PRD, arquitetura e `SPEC-010`.
- Conferir que nenhuma migration ou tabela executiva foi criada.
- Registrar ausencia de testes automatizados quando a entrega for somente desenho tecnico.

## Riscos

- Risco: desenho antecipar complexidade desnecessaria.
  Mitigacao: separar MVP de extensoes futuras.

- Risco: banco substituir rastreabilidade por Git/asset.
  Mitigacao: exigir referencia a fonte, hash e versao governada.

## Bloqueios Pendentes

- Fonte oficial aprovada.
- Contrato de carga aprovado.
- Asset completo validado quando a tarefa evoluir para implementacao executiva.
