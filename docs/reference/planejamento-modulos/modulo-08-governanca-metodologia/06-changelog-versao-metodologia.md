# 06 - Changelog e versao da metodologia

## Objetivo

Definir como registrar mudancas metodologicas e versoes usadas.

## Changelog metodologico

Documento futuro possivel:

- `docs/methodology/changelog-metodologico.md`

Cada mudanca deve registrar:

- o que mudou;
- por que mudou;
- impacto esperado;
- risco;
- testes executados;
- se afeta laudo.

## Versao da metodologia

Identificador sugerido:

```text
methodology_version = YYYYMMDD-sequencial
```

## Integracao com laudo

O laudo deve informar:

- versao da metodologia;
- data;
- assets usados;
- status de cobertura;
- snapshot suficiente quando nao houver persistencia historica.

## Regra de compatibilidade

Alteracao de metodologia nao deve retroagir silenciosamente sobre laudos ja emitidos.

