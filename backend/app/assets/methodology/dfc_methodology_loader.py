from __future__ import annotations

from dataclasses import dataclass
import json
from pathlib import Path
from typing import Any

DEFAULT_DFC_METHODOLOGY_ASSET = Path(__file__).with_name("dfc_methodology.json")
DFC_ACTIVITIES = {"operacional", "investimento", "financiamento"}
DFC_DIRECTIONS = {"entrada", "saida"}
REQUIRED_COMPONENT_CODES = {
    "recebimentos_clientes",
    "pagamentos_fornecedores",
    "pagamentos_empregados",
    "tributos_operacionais",
    "outros_fluxos_operacionais",
    "compra_imobilizado",
    "venda_imobilizado",
    "aquisicao_participacoes",
    "venda_participacoes",
    "aplicacoes_nao_equivalentes",
    "captacao_emprestimos",
    "amortizacao_principal",
    "juros_financiamento",
    "aumento_reducao_capital",
    "distribuicao_lucros",
}


class DfcMethodologyAssetError(RuntimeError):
    pass


@dataclass(frozen=True)
class DfcComponent:
    code: str
    activity: str
    label: str


@dataclass(frozen=True)
class DfcMethodologyRule:
    rule_id: str
    reference_code: str
    activity: str
    component_by_direction: dict[str, str]
    requires_review: bool
    valid_from: int
    valid_to: int | None

    def component_for(self, direction: str) -> str | None:
        return self.component_by_direction.get(direction)


@dataclass(frozen=True)
class DfcMethodology:
    methodology_version_id: str
    status: str
    source: str
    cash_reference_codes: frozenset[str]
    components: tuple[DfcComponent, ...]
    rules: tuple[DfcMethodologyRule, ...]

    def is_cash_reference(self, reference_code: str | None) -> bool:
        return reference_code in self.cash_reference_codes

    def rule_for(self, reference_code: str | None, year: int) -> DfcMethodologyRule | None:
        if reference_code is None:
            return None
        for rule in self.rules:
            if (
                rule.reference_code == reference_code
                and year >= rule.valid_from
                and (rule.valid_to is None or year <= rule.valid_to)
            ):
                return rule
        return None

    def component(self, component_code: str) -> DfcComponent:
        for component in self.components:
            if component.code == component_code:
                return component
        raise KeyError(component_code)


def load_dfc_methodology(
    asset_path: Path = DEFAULT_DFC_METHODOLOGY_ASSET,
) -> DfcMethodology:
    if not asset_path.is_file():
        raise DfcMethodologyAssetError(
            f"DFC methodology asset not found: {asset_path.name}."
        )
    try:
        payload = json.loads(asset_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise DfcMethodologyAssetError("DFC methodology asset is not valid JSON.") from exc
    return _validate_and_build(payload)


def _validate_and_build(payload: Any) -> DfcMethodology:
    from app.assets.reference import load_official_reference_accounts

    if not isinstance(payload, dict) or payload.get("asset_type") != "dfc_methodology":
        raise DfcMethodologyAssetError("DFC methodology asset has invalid asset_type.")
    for field in {"schema_version", "methodology_version_id", "status", "source"}:
        if not isinstance(payload.get(field), str) or not payload[field].strip():
            raise DfcMethodologyAssetError(f"DFC methodology has invalid {field}.")
    if payload["status"] != "ATIVA":
        raise DfcMethodologyAssetError("DFC methodology is not active.")

    official_codes = {
        account.reference_code for account in load_official_reference_accounts()
    }
    cash_codes = _cash_codes(payload.get("cash_reference_codes"), official_codes)
    components = _components(payload.get("components"))
    component_by_code = {component.code: component for component in components}
    rules = _rules(payload.get("rules"), official_codes, cash_codes, component_by_code)

    return DfcMethodology(
        methodology_version_id=payload["methodology_version_id"].strip(),
        status=payload["status"].strip(),
        source=payload["source"].strip(),
        cash_reference_codes=frozenset(cash_codes),
        components=tuple(components),
        rules=tuple(rules),
    )


def _cash_codes(value: Any, official_codes: set[str]) -> set[str]:
    if not isinstance(value, list) or not value:
        raise DfcMethodologyAssetError("DFC cash reference codes must be a non-empty list.")
    if any(not isinstance(code, str) or not code.strip() for code in value):
        raise DfcMethodologyAssetError("DFC cash reference code is invalid.")
    codes = {code.strip() for code in value}
    if len(codes) != len(value):
        raise DfcMethodologyAssetError("DFC cash reference code is duplicated.")
    if any("*" in code for code in codes):
        raise DfcMethodologyAssetError("DFC cash reference codes must be exact.")
    if not codes.issubset(official_codes):
        raise DfcMethodologyAssetError(
            "DFC cash reference code is absent from official reference plan."
        )
    return codes


def _components(value: Any) -> list[DfcComponent]:
    if not isinstance(value, list) or not value:
        raise DfcMethodologyAssetError("DFC components must be a non-empty list.")
    components: list[DfcComponent] = []
    seen_codes: set[str] = set()
    for index, item in enumerate(value):
        if not isinstance(item, dict) or set(item) != {"code", "activity", "label"}:
            raise DfcMethodologyAssetError(f"DFC component {index} has invalid fields.")
        if any(
            not isinstance(item[field], str) or not item[field].strip()
            for field in item
        ):
            raise DfcMethodologyAssetError(f"DFC component {index} has invalid value.")
        if item["activity"] not in DFC_ACTIVITIES:
            raise DfcMethodologyAssetError(f"DFC component {index} has invalid activity.")
        if item["code"] in seen_codes:
            raise DfcMethodologyAssetError(f"DFC component {index} is duplicated.")
        seen_codes.add(item["code"])
        components.append(DfcComponent(**item))
    if not REQUIRED_COMPONENT_CODES.issubset(seen_codes):
        raise DfcMethodologyAssetError("DFC methodology misses required components.")
    return components


def _rules(
    value: Any,
    official_codes: set[str],
    cash_codes: set[str],
    components: dict[str, DfcComponent],
) -> list[DfcMethodologyRule]:
    if not isinstance(value, list) or not value:
        raise DfcMethodologyAssetError("DFC rules must be a non-empty list.")
    rules: list[DfcMethodologyRule] = []
    seen_ids: set[str] = set()
    seen_codes: set[str] = set()
    required_fields = {
        "rule_id",
        "reference_code",
        "activity",
        "component_by_direction",
        "requires_review",
        "valid_from",
        "valid_to",
    }
    for index, item in enumerate(value):
        if not isinstance(item, dict) or set(item) != required_fields:
            raise DfcMethodologyAssetError(f"DFC rule {index} has invalid fields.")
        rule = _rule(item, index)
        if rule.rule_id in seen_ids or rule.reference_code in seen_codes:
            raise DfcMethodologyAssetError(f"DFC rule {index} is duplicated.")
        if "*" in rule.reference_code:
            raise DfcMethodologyAssetError(f"DFC rule {index} must use exact code.")
        if rule.reference_code not in official_codes:
            raise DfcMethodologyAssetError(
                f"DFC rule {index} is absent from official reference plan."
            )
        if rule.reference_code in cash_codes:
            raise DfcMethodologyAssetError(
                f"DFC rule {index} cannot classify a cash reference as counterparty."
            )
        for direction, component_code in rule.component_by_direction.items():
            component = components.get(component_code)
            if component is None or component.activity != rule.activity:
                raise DfcMethodologyAssetError(
                    f"DFC rule {index} has incompatible component for {direction}."
                )
        seen_ids.add(rule.rule_id)
        seen_codes.add(rule.reference_code)
        rules.append(rule)
    return rules


def _rule(value: dict[str, Any], index: int) -> DfcMethodologyRule:
    for field in {"rule_id", "reference_code", "activity"}:
        if not isinstance(value[field], str) or not value[field].strip():
            raise DfcMethodologyAssetError(f"DFC rule {index} has invalid {field}.")
    if value["activity"] not in DFC_ACTIVITIES:
        raise DfcMethodologyAssetError(f"DFC rule {index} has invalid activity.")
    mapping = value["component_by_direction"]
    if (
        not isinstance(mapping, dict)
        or not mapping
        or not set(mapping).issubset(DFC_DIRECTIONS)
        or any(
            not isinstance(component, str) or not component
            for component in mapping.values()
        )
    ):
        raise DfcMethodologyAssetError(
            f"DFC rule {index} has invalid component_by_direction."
        )
    if not isinstance(value["requires_review"], bool):
        raise DfcMethodologyAssetError(f"DFC rule {index} has invalid requires_review.")
    if not isinstance(value["valid_from"], int) or isinstance(value["valid_from"], bool):
        raise DfcMethodologyAssetError(f"DFC rule {index} has invalid valid_from.")
    if value["valid_to"] is not None and (
        not isinstance(value["valid_to"], int) or isinstance(value["valid_to"], bool)
    ):
        raise DfcMethodologyAssetError(f"DFC rule {index} has invalid valid_to.")
    if value["valid_to"] is not None and value["valid_to"] < value["valid_from"]:
        raise DfcMethodologyAssetError(f"DFC rule {index} has invalid validity.")
    return DfcMethodologyRule(
        rule_id=value["rule_id"].strip(),
        reference_code=value["reference_code"].strip(),
        activity=value["activity"],
        component_by_direction=dict(mapping),
        requires_review=value["requires_review"],
        valid_from=value["valid_from"],
        valid_to=value["valid_to"],
    )
