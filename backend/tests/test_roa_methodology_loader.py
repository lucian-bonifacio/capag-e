from pathlib import Path

import pytest

from app.assets.methodology import (
    ROA_BLOCKS,
    ROA_TREATMENTS,
    RoaMethodologyAssetError,
    load_roa_methodology,
)


def test_roa_methodology_loads_required_columns_blocks_and_treatments() -> None:
    methodology = load_roa_methodology()

    assert methodology.methodology_version_id == "metodologia-2024.1"
    assert {component.block for component in methodology.components} == ROA_BLOCKS
    assert {rule.treatment for rule in methodology.rules} == ROA_TREATMENTS
    assert all(rule.methodology_version_id == "metodologia-2024.1" for rule in methodology.rules)


def test_roa_methodology_uses_exact_rule_before_longer_prefix_without_names() -> None:
    methodology = load_roa_methodology()

    tax_rule = methodology.rule_for("3.01.01.01.02.04")
    financial_rule = methodology.rule_for("3.01.01.09.01.08")
    unknown = methodology.rule_for("DESPESAS BANCARIAS")

    assert tax_rule is not None
    assert tax_rule.block == "tributos_receita"
    assert financial_rule is not None
    assert financial_rule.block == "resultado_financeiro"
    assert unknown is None


def test_roa_methodology_validates_conditional_review_and_reason(tmp_path: Path) -> None:
    rules = _rules_text().replace(
        "3.01.01.05,prefixo,outras_receitas,RESULTADO_NAO_OPERACIONAL,resultado_nao_operacional,credito,condicional,somar,receitas_nao_operacionais,true,",
        "3.01.01.05,prefixo,outras_receitas,RESULTADO_NAO_OPERACIONAL,resultado_nao_operacional,credito,condicional,somar,receitas_nao_operacionais,false,",
    )

    with pytest.raises(RoaMethodologyAssetError, match="requires review and reason"):
        load_roa_methodology(_write(tmp_path, "rules.csv", rules))


def test_roa_methodology_rejects_treatment_outside_contract(tmp_path: Path) -> None:
    rules = _rules_text().replace(
        "incluir_automaticamente",
        "incluir_sem_governanca",
        1,
    )

    with pytest.raises(RoaMethodologyAssetError, match="invalid treatment"):
        load_roa_methodology(_write(tmp_path, "rules.csv", rules))


def _rules_text() -> str:
    from app.assets.methodology import DEFAULT_ROA_RULES_ASSET

    return DEFAULT_ROA_RULES_ASSET.read_text(encoding="utf-8")


def _write(directory: Path, name: str, content: str) -> Path:
    path = directory / name
    path.write_text(content, encoding="utf-8")
    return path
