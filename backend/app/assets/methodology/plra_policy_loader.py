from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal, InvalidOperation
import json
from pathlib import Path
from typing import Any

DEFAULT_PLRA_POLICY_ASSET = Path(__file__).with_name("plra_policy.json")
EXPECTED_DEFAULT_DISCOUNTS = {
    "caixa": Decimal("0.00"),
    "bancos": Decimal("0.00"),
    "aplicacoes_imediatas": Decimal("0.05"),
    "clientes": Decimal("0.30"),
    "adiantamentos": Decimal("0.50"),
    "estoques": Decimal("0.80"),
    "imobilizado": Decimal("0.80"),
    "intangivel": Decimal("1.00"),
    "creditos_judiciais": Decimal("0.90"),
}
ALLOWED_TREATMENTS = {
    "INCLUIR_ATIVO",
    "EXCLUIR_ATIVO",
    "INCLUIR_PASSIVO",
    "PASSIVO_CONDICIONAL",
    "EXCLUIR_PATRIMONIO_LIQUIDO",
}
ALLOWED_RULE_STATUSES = {"ATIVA", "BLOQUEADA", "EM_REVISAO", "DEPRECIADA"}


class PlraPolicyAssetError(RuntimeError):
    pass


@dataclass(frozen=True)
class PlraRule:
    methodology_rule_id: str
    reference_code: str
    methodology_group: str
    macrogroup: str
    treatment: str
    default_discount_group: str | None
    rule_status: str
    valid_from: int
    valid_to: int | None
    reason: str


@dataclass(frozen=True)
class PlraPolicy:
    methodology_version_id: str
    status: str
    source: str
    default_discounts: dict[str, Decimal]
    rules: tuple[PlraRule, ...]

    def rule_for(self, reference_code: str, year: int) -> PlraRule | None:
        for rule in self.rules:
            if (
                rule.reference_code == reference_code
                and year >= rule.valid_from
                and (rule.valid_to is None or year <= rule.valid_to)
            ):
                return rule
        return None


def load_plra_policy(
    asset_path: Path = DEFAULT_PLRA_POLICY_ASSET,
) -> PlraPolicy:
    if not asset_path.is_file():
        raise PlraPolicyAssetError(f"PLRA policy asset not found: {asset_path.name}.")
    try:
        payload = json.loads(asset_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise PlraPolicyAssetError("PLRA policy asset is not valid JSON.") from exc
    return _validate_and_build(payload)


def _validate_and_build(payload: Any) -> PlraPolicy:
    from app.assets.reference import load_official_reference_accounts

    if not isinstance(payload, dict) or payload.get("asset_type") != "plra_policy":
        raise PlraPolicyAssetError("PLRA policy asset has invalid asset_type.")
    for field in {"schema_version", "methodology_version_id", "status", "source"}:
        if not isinstance(payload.get(field), str) or not payload[field].strip():
            raise PlraPolicyAssetError(f"PLRA policy has invalid {field}.")
    if payload["status"] != "ATIVA":
        raise PlraPolicyAssetError("PLRA policy is not active.")

    discounts_payload = payload.get("default_discounts")
    if not isinstance(discounts_payload, dict):
        raise PlraPolicyAssetError("PLRA policy default_discounts must be an object.")
    discounts = {
        group: _decimal_percent(value, group)
        for group, value in discounts_payload.items()
    }
    if discounts != EXPECTED_DEFAULT_DISCOUNTS:
        raise PlraPolicyAssetError("PLRA policy defaults do not match SPEC-011.")

    rules_payload = payload.get("rules")
    if not isinstance(rules_payload, list) or len(rules_payload) == 0:
        raise PlraPolicyAssetError("PLRA policy must contain rules.")

    official_by_code = {
        account.reference_code: account for account in load_official_reference_accounts()
    }
    seen_codes: set[str] = set()
    seen_ids: set[str] = set()
    rules: list[PlraRule] = []
    for index, raw_rule in enumerate(rules_payload):
        rule = _build_rule(raw_rule, index)
        if rule.reference_code in seen_codes or rule.methodology_rule_id in seen_ids:
            raise PlraPolicyAssetError(f"PLRA policy rule {index} is duplicated.")
        official = official_by_code.get(rule.reference_code)
        if official is None:
            raise PlraPolicyAssetError(
                f"PLRA policy rule {index} is absent from official reference plan."
            )
        _validate_treatment_nature(rule, official.nature, index)
        if rule.default_discount_group is not None:
            if rule.default_discount_group not in discounts:
                raise PlraPolicyAssetError(
                    f"PLRA policy rule {index} has unknown discount group."
                )
        elif rule.treatment == "INCLUIR_ATIVO":
            raise PlraPolicyAssetError(
                f"PLRA policy rule {index} requires default discount group."
            )
        seen_codes.add(rule.reference_code)
        seen_ids.add(rule.methodology_rule_id)
        rules.append(rule)

    return PlraPolicy(
        methodology_version_id=payload["methodology_version_id"].strip(),
        status=payload["status"].strip(),
        source=payload["source"].strip(),
        default_discounts=discounts,
        rules=tuple(rules),
    )


def _build_rule(value: Any, index: int) -> PlraRule:
    required = {
        "methodology_rule_id",
        "reference_code",
        "methodology_group",
        "macrogroup",
        "treatment",
        "default_discount_group",
        "rule_status",
        "valid_from",
        "valid_to",
        "reason",
    }
    if not isinstance(value, dict):
        raise PlraPolicyAssetError(f"PLRA policy rule {index} must be an object.")
    missing = required - set(value)
    if missing:
        raise PlraPolicyAssetError(f"PLRA policy rule {index} missing fields.")
    for field in {
        "methodology_rule_id",
        "reference_code",
        "methodology_group",
        "macrogroup",
        "treatment",
        "rule_status",
        "reason",
    }:
        if not isinstance(value[field], str) or not value[field].strip():
            raise PlraPolicyAssetError(f"PLRA policy rule {index} has invalid {field}.")
    if "*" in value["reference_code"]:
        raise PlraPolicyAssetError(f"PLRA policy rule {index} must use exact code.")
    if value["treatment"] not in ALLOWED_TREATMENTS:
        raise PlraPolicyAssetError(f"PLRA policy rule {index} has invalid treatment.")
    if value["rule_status"] not in ALLOWED_RULE_STATUSES:
        raise PlraPolicyAssetError(f"PLRA policy rule {index} has invalid status.")
    if not isinstance(value["valid_from"], int):
        raise PlraPolicyAssetError(f"PLRA policy rule {index} has invalid valid_from.")
    if value["valid_to"] is not None and not isinstance(value["valid_to"], int):
        raise PlraPolicyAssetError(f"PLRA policy rule {index} has invalid valid_to.")
    if value["valid_to"] is not None and value["valid_to"] < value["valid_from"]:
        raise PlraPolicyAssetError(f"PLRA policy rule {index} has invalid validity.")
    if value["default_discount_group"] is not None and not isinstance(
        value["default_discount_group"], str
    ):
        raise PlraPolicyAssetError(
            f"PLRA policy rule {index} has invalid default_discount_group."
        )
    return PlraRule(**{field: value[field] for field in required})


def _decimal_percent(value: Any, group: str) -> Decimal:
    if not isinstance(value, str):
        raise PlraPolicyAssetError(
            f"PLRA default discount {group} must be a decimal string."
        )
    try:
        parsed = Decimal(value)
    except InvalidOperation as exc:
        raise PlraPolicyAssetError(
            f"PLRA default discount {group} is invalid."
        ) from exc
    if not parsed.is_finite() or parsed < Decimal("0") or parsed > Decimal("1"):
        raise PlraPolicyAssetError(
            f"PLRA default discount {group} must be between zero and one."
        )
    return parsed


def _validate_treatment_nature(rule: PlraRule, nature: str, index: int) -> None:
    expected = {
        "INCLUIR_ATIVO": "ATIVO",
        "EXCLUIR_ATIVO": "ATIVO",
        "INCLUIR_PASSIVO": "PASSIVO",
        "PASSIVO_CONDICIONAL": "PASSIVO",
        "EXCLUIR_PATRIMONIO_LIQUIDO": "PATRIMONIO_LIQUIDO",
    }[rule.treatment]
    if nature != expected:
        raise PlraPolicyAssetError(
            f"PLRA policy rule {index} is incompatible with official nature."
        )
