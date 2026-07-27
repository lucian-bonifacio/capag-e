from copy import deepcopy
from decimal import Decimal
import json
from pathlib import Path

import pytest

from app.assets.methodology import (
    EXPECTED_DEFAULT_DISCOUNTS,
    PlraPolicyAssetError,
    load_plra_policy,
)


POLICY_PATH = (
    Path(__file__).resolve().parents[1]
    / "app"
    / "assets"
    / "methodology"
    / "plra_policy.json"
)


def test_plra_policy_loads_approved_defaults_and_exact_rules() -> None:
    policy = load_plra_policy()

    assert policy.default_discounts == EXPECTED_DEFAULT_DISCOUNTS
    assert policy.default_discounts["intangivel"] == Decimal("1.00")
    assert len(policy.rules) == 34
    assert all("*" not in rule.reference_code for rule in policy.rules)
    assert policy.rule_for("1.01.03.02.01", 2024) is not None
    assert policy.rule_for("9.99.99", 2024) is None


def test_plra_policy_rejects_float_discount(tmp_path) -> None:
    payload = _payload()
    payload["default_discounts"]["clientes"] = 0.30

    with pytest.raises(PlraPolicyAssetError, match="decimal string"):
        load_plra_policy(_write(tmp_path, payload))


def test_plra_policy_rejects_out_of_range_discount(tmp_path) -> None:
    payload = _payload()
    payload["default_discounts"]["clientes"] = "1.01"

    with pytest.raises(PlraPolicyAssetError, match="between zero and one"):
        load_plra_policy(_write(tmp_path, payload))


def test_plra_policy_rejects_duplicate_exact_code(tmp_path) -> None:
    payload = _payload()
    payload["rules"].append(deepcopy(payload["rules"][0]))

    with pytest.raises(PlraPolicyAssetError, match="duplicated"):
        load_plra_policy(_write(tmp_path, payload))


def test_plra_policy_rejects_code_absent_from_official_plan(tmp_path) -> None:
    payload = _payload()
    payload["rules"][0]["reference_code"] = "9.99.99"

    with pytest.raises(PlraPolicyAssetError, match="absent from official"):
        load_plra_policy(_write(tmp_path, payload))


def test_plra_policy_rejects_wildcard_code(tmp_path) -> None:
    payload = _payload()
    payload["rules"][0]["reference_code"] = "1.01.*"

    with pytest.raises(PlraPolicyAssetError, match="exact code"):
        load_plra_policy(_write(tmp_path, payload))


def _payload() -> dict:
    return json.loads(POLICY_PATH.read_text(encoding="utf-8"))


def _write(tmp_path: Path, payload: dict) -> Path:
    path = tmp_path / "plra-policy.json"
    path.write_text(json.dumps(payload), encoding="utf-8")
    return path
