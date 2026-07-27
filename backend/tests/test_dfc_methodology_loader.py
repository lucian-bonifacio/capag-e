from copy import deepcopy
import json
from pathlib import Path

import pytest

from app.assets.methodology import DfcMethodologyAssetError, load_dfc_methodology


ASSET_PATH = (
    Path(__file__).resolve().parents[1]
    / "app"
    / "assets"
    / "methodology"
    / "dfc_methodology.json"
)


def test_dfc_methodology_loads_required_components_and_exact_cash_codes() -> None:
    methodology = load_dfc_methodology()

    assert methodology.methodology_version_id == "metodologia-2024.1"
    assert methodology.is_cash_reference("1.01.01.01.01")
    assert methodology.is_cash_reference("1.01.01.02.01")
    assert not methodology.is_cash_reference("1.01.02.02.01")
    assert {
        component.activity for component in methodology.components
    } == {"operacional", "investimento", "financiamento"}
    assert len(methodology.components) == 15
    assert all("*" not in code for code in methodology.cash_reference_codes)
    assert all("*" not in rule.reference_code for rule in methodology.rules)


def test_dfc_methodology_classifies_only_by_reference_code() -> None:
    methodology = load_dfc_methodology()

    rule = methodology.rule_for("2.02.01.01.06", 2024)

    assert rule is not None
    assert rule.activity == "financiamento"
    assert rule.component_for("entrada") == "captacao_emprestimos"
    assert rule.component_for("saida") == "amortizacao_principal"
    assert methodology.rule_for("BANCO BRADESCO", 2024) is None


def test_dfc_methodology_rejects_wildcard_cash_code(tmp_path: Path) -> None:
    payload = _payload()
    payload["cash_reference_codes"][0] = "1.01.01.*"

    with pytest.raises(DfcMethodologyAssetError, match="must be exact"):
        load_dfc_methodology(_write(tmp_path, payload))


def test_dfc_methodology_rejects_unknown_official_rule(tmp_path: Path) -> None:
    payload = _payload()
    payload["rules"][0]["reference_code"] = "9.99.99"

    with pytest.raises(DfcMethodologyAssetError, match="absent from official"):
        load_dfc_methodology(_write(tmp_path, payload))


def test_dfc_methodology_rejects_direction_component_from_other_activity(
    tmp_path: Path,
) -> None:
    payload = _payload()
    payload["rules"][0]["component_by_direction"]["entrada"] = "captacao_emprestimos"

    with pytest.raises(DfcMethodologyAssetError, match="incompatible component"):
        load_dfc_methodology(_write(tmp_path, payload))


def test_dfc_methodology_rejects_duplicate_rule(tmp_path: Path) -> None:
    payload = _payload()
    payload["rules"].append(deepcopy(payload["rules"][0]))

    with pytest.raises(DfcMethodologyAssetError, match="duplicated"):
        load_dfc_methodology(_write(tmp_path, payload))


def _payload() -> dict:
    return json.loads(ASSET_PATH.read_text(encoding="utf-8"))


def _write(tmp_path: Path, payload: dict) -> Path:
    path = tmp_path / "dfc-methodology.json"
    path.write_text(json.dumps(payload), encoding="utf-8")
    return path
