# TASK-090 - Ampliar validacoes do asset referencial

## SPEC De Origem

- `specs/SPEC-010-governanca-plano-referencial-oficial.md`

## Dependencias

- `TASK-089-definir-contrato-carga-plano-referencial.md`

## Objetivo

Ampliar as validacoes automatizadas do asset do plano referencial oficial, preparando o sistema para validar fonte, campos, duplicidades, hierarquia, vigencia, status e metadados antes de publicacao operacional.

## Fontes Usadas

- `docs/product/PRD.md`
- `docs/architecture/architecture.md`
- `specs/SPEC-002-modulo-1-camada-declarada.md`
- `specs/SPEC-009-modulo-8-governanca-metodologia.md`
- `specs/SPEC-010-governanca-plano-referencial-oficial.md`
- `tasks/TASK-086-tabela-oficial-referencial-obrigatoria.md`
- `tasks/TASK-089-definir-contrato-carga-plano-referencial.md`

## Escopo Exato

- Validar campos obrigatorios definidos no contrato de carga.
- Validar duplicidades por codigo, leiaute, entidade e vigencia.
- Validar hierarquia e referencias parentais.
- Validar vigencia e status permitidos.
- Validar metadados de origem e hash quando aplicavel.
- Criar testes automatizados focados nas validacoes.
- Manter bloqueio controlado quando o asset estiver ausente, vazio ou invalido.

## Fora De Escopo

- Popular base oficial completa.
- Criar banco, migrations, API administrativa ou CRUD.
- Aprovar fonte oficial.
- Alterar regra prudencial ou inferir codigo referencial.
- Substituir a camada declarada ou o matcher metodologico.

## Passos Executaveis

1. Ler loader e testes criados na `TASK-086`.
2. Ler contrato de carga definido na `TASK-089`.
3. Expandir validador do asset referencial.
4. Criar fixtures pequenas e deterministicas para casos validos e invalidos.
5. Criar testes de duplicidade, hierarquia, vigencia, status e metadados.
6. Validar que erros continuam controlados e rastreaveis.

## Arquivos Ou Areas Provaveis

- `backend/app/assets/reference/`
- `backend/app/assets/README.md`
- `backend/tests/test_official_reference_loader.py`
- `backend/tests/test_assets_structure.py`

## Criterios De Aceite

- Asset invalido falha com erro controlado.
- Duplicidades relevantes sao rejeitadas.
- Hierarquia quebrada e detectada.
- Status e vigencias invalidas sao rejeitados.
- Metadados de fonte/hash sao validados quando exigidos pelo contrato.
- Testes automatizados cobrem os principais erros.

## Validacao Esperada

- Executar testes backend via `docker compose`.
- Conferir ausencia de `float` em arquivos alterados.
- Registrar limitacoes se alguma validacao depender de fonte oficial ainda nao aprovada.

## Riscos

- Risco: validador ficar acoplado ao asset minimo atual.
  Mitigacao: usar contrato de carga como referencia, nao exemplos pontuais.

- Risco: validacao rejeitar casos historicos validos.
  Mitigacao: separar regras obrigatorias de regras condicionadas a fonte aprovada.

## Bloqueios Pendentes

- Nenhum para validacoes estruturais.
- Validacoes dependentes de cobertura completa ficam condicionadas a fonte oficial aprovada.
