# TASK-035 - Estruturar assets da camada declarada

## SPEC De Origem

- `specs/SPEC-002-modulo-1-camada-declarada.md`

## Dependencias

- `TASK-032-auditar-prontidao-fundacao-governada.md`

## Objetivo

Criar a estrutura governada para assets da camada declarada, separando plano referencial oficial e metodologia interna versionada, sem popular regras prudenciais reais nem implementar motor.

## Fontes Usadas

- `docs/product/PRD.md`
- `docs/architecture/architecture.md`
- `specs/SPEC-002-modulo-1-camada-declarada.md`

## Escopo Exato

- Criar estrutura de diretórios para assets da camada declarada.
- Criar schemas ou arquivos-modelo vazios/seguros para plano referencial oficial e metodologia interna.
- Documentar campos obrigatórios previstos na SPEC-002.
- Garantir que assets reais completos não sejam inventados.

## Fora De Escopo

- Popular plano referencial oficial completo.
- Criar regras metodológicas reais.
- Implementar matcher, parser, engine, API, frontend ou Excel.
- Definir regra prudencial nova.

## Passos Executaveis

1. Ler a SPEC-002.
2. Criar estrutura de assets conforme arquitetura.
3. Criar modelos de arquivo sem regras reais.
4. Documentar campos obrigatórios.
5. Validar que nenhum cálculo ou regra funcional foi criado.

## Arquivos Ou Areas Provaveis

- `backend/app/assets/`
- documentação local de assets, se necessário

## Criterios De Aceite

- Estrutura de assets da camada declarada existe.
- Plano oficial e metodologia interna ficam separados.
- Nenhuma regra prudencial real é inventada.
- Nenhum motor ou API é implementado.

## Validacao Esperada

- Executar validação estrutural dos arquivos criados.
- Conferir `git diff --stat` e confirmar escopo restrito a assets/documentação permitida.

## Riscos

- Risco: criar regra metodológica sem fonte suficiente.
  Mitigação: permitir apenas estrutura e modelos vazios/seguros.

## Bloqueios Pendentes

Bloqueada até a fundação governada estar pronta.
