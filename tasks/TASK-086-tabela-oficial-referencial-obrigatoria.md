# TASK-086 - Tabela oficial referencial obrigatoria

## SPEC De Origem

- `specs/SPEC-002-modulo-1-camada-declarada.md`

## Dependencias

- `TASK-035-estruturar-assets-camada-declarada.md`
- `TASK-036-implementar-matcher-metodologico-declarado.md`
- `TASK-041A-modelar-importacao-ecd-status-analise.md`
- `TASK-041B-criar-migrations-ecd-normalizada.md`
- `TASK-041J-validar-fluxo-end-to-end-declarada.md`

## Objetivo

Criar, carregar, versionar e tornar obrigatoria a existencia da tabela oficial do plano referencial para o funcionamento da camada declarada.

## Fontes Usadas

- `docs/product/PRD.md`
- `docs/architecture/architecture.md`
- `specs/SPEC-002-modulo-1-camada-declarada.md`
- `tasks/TASK-085-refinar-apresentacao-leitura-declarada.md`

## Escopo Exato

- Definir o formato governado da tabela oficial do plano referencial conforme campos minimos da `SPEC-002`.
- Criar ou organizar asset governado da tabela oficial com `reference_code`, descricao oficial, hierarquia, natureza, vigencia, leiaute, tipo de entidade, fonte, status e versao metodologica.
- Criar carregador/validador da tabela oficial no backend.
- Tornar a existencia da tabela oficial obrigatoria para executar a camada declarada.
- Bloquear execucao da camada declarada quando a tabela oficial estiver ausente, invalida ou vazia.
- Diferenciar erro de configuracao do sistema de pendencia do arquivo ECD.
- Ajustar API para expor erro controlado quando a tabela oficial obrigatoria nao estiver disponivel.
- Ajustar testes para cobrir tabela oficial presente, ausente, invalida e codigo declarado nao encontrado.
- Manter o status `COD_CTA_REF_NAO_ENCONTRADO_NA_TABELA_OFICIAL` apenas para codigos declarados pela ECD que nao existam na tabela oficial carregada.

## Fora De Escopo

- Criar regra metodologica interna completa.
- Alterar classificacao prudencial, matcher exato ou calculo CAPAG-E.
- Inferir codigo referencial alternativo ao declarado no `I051`.
- Corrigir ECD sem vinculo referencial.
- Criar tela administrativa de manutencao livre da tabela oficial.
- Buscar ou consumir fonte externa em tempo real sem asset governado.

## Passos Executaveis

1. Ler contrato do plano referencial oficial na `SPEC-002`.
2. Auditar assets existentes da camada declarada.
3. Definir arquivo governado da tabela oficial e validacoes minimas.
4. Implementar carregador/validador no backend.
5. Integrar carregamento da tabela oficial ao motor da camada declarada.
6. Bloquear execucao declarada quando a tabela oficial estiver ausente, vazia ou invalida.
7. Ajustar contratos de erro da API quando a configuracao obrigatoria estiver indisponivel.
8. Criar testes backend para tabela oficial presente, ausente, invalida e codigo nao encontrado.
9. Validar manualmente com `DATAPACK` e `INVENTCLOUD` em execucoes separadas.

## Arquivos Ou Areas Provaveis

- `backend/app/assets/`
- `backend/app/engine/methodology_matcher/`
- `backend/app/application/declared_run_service.py`
- `backend/app/api/declared.py`
- `backend/app/schemas/declared.py`
- `backend/tests/`
- `docs/`

## Criterios De Aceite

- A camada declarada nao executa sem tabela oficial carregada e valida.
- Falta de tabela oficial retorna erro controlado de configuracao do sistema.
- Codigo referencial declarado mas inexistente na tabela oficial continua retornando `COD_CTA_REF_NAO_ENCONTRADO_NA_TABELA_OFICIAL`.
- A tabela oficial e asset governado e versionavel.
- O frontend nao precisa calcular nem validar a tabela oficial por conta propria.
- Valores contabeis continuam usando `Decimal`.
- Nenhuma regra prudencial ou metodologia interna e inventada nesta TASK.

## Validacao Esperada

- Executar testes backend via `docker compose`.
- Executar testes frontend/E2E impactados via `docker compose`, se contratos de erro afetarem UI.
- Validar manualmente `docs/reference/ecd-example/ECD 2024 DATAPACK.txt`.
- Validar manualmente `docs/reference/ecd-example/ECD 2024 INVENTCLOUD.txt`.
- Conferir ausencia de `float` em arquivos alterados.

## Riscos

- Risco: bloquear a camada declarada por asset oficial incompleto.
  Mitigacao: bloquear apenas ausencia/invalidade da tabela; codigos nao encontrados permanecem como pendencia por conta.

- Risco: confundir tabela oficial com metodologia interna.
  Mitigacao: manter contratos separados conforme `SPEC-002`.

- Risco: inserir fonte oficial incompleta como verdade final.
  Mitigacao: versionar asset, validar campos minimos e manter status por conta para codigo ausente.

## Bloqueios Pendentes

Nenhum.
