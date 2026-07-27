from __future__ import annotations

import csv
from dataclasses import dataclass
from pathlib import Path


DEFAULT_ROA_RULES_ASSET = Path(__file__).with_name("tabela_metodologica_roa.csv")
DEFAULT_ROA_COMPONENTS_ASSET = Path(__file__).with_name("componentes_roa.csv")
ROA_BLOCKS = {
    "receita_bruta",
    "deducoes_receita",
    "tributos_receita",
    "custos_operacionais",
    "despesas_operacionais",
    "resultado_financeiro",
    "resultado_nao_operacional",
    "pressoes_complementares_caixa",
}
ROA_TREATMENTS = {
    "incluir_automaticamente",
    "excluir_automaticamente",
    "condicional",
}
MATCH_MODES = {"exato", "prefixo"}
NATURAL_SIDES = {"credito", "debito", "variavel"}
PRIMARY_RULES = {"somar", "subtrair", "aplicar_sinal_contabil", "excluir"}
METHODOLOGY_VERSION = "metodologia-2024.1"
RULE_FIELDS = (
    "codigo_referencial",
    "modo_correspondencia",
    "grupo_metodologico",
    "macrogrupo",
    "bloco_roa",
    "sinal_natural",
    "tratamento",
    "regra_principal",
    "componente_roa",
    "exige_revisao",
    "motivo_condicional",
    "methodology_version_id",
)
COMPONENT_FIELDS = (
    "componente_roa",
    "bloco_roa",
    "rotulo",
    "required_evidence_type",
    "methodology_version_id",
)


class RoaMethodologyAssetError(RuntimeError):
    pass


@dataclass(frozen=True)
class RoaComponent:
    code: str
    block: str
    label: str
    required_evidence_type: str
    methodology_version_id: str


@dataclass(frozen=True)
class RoaMethodologyRule:
    reference_code: str
    match_mode: str
    methodology_group: str
    macrogroup: str
    block: str
    natural_side: str
    treatment: str
    primary_rule: str
    component_code: str
    requires_review: bool
    conditional_reason: str | None
    methodology_version_id: str

    def matches(self, reference_code: str) -> bool:
        if self.match_mode == "exato":
            return reference_code == self.reference_code
        return reference_code == self.reference_code or reference_code.startswith(
            f"{self.reference_code}."
        )


@dataclass(frozen=True)
class RoaMethodology:
    methodology_version_id: str
    components: tuple[RoaComponent, ...]
    rules: tuple[RoaMethodologyRule, ...]

    def rule_for(self, reference_code: str | None) -> RoaMethodologyRule | None:
        if reference_code is None:
            return None
        matches = [rule for rule in self.rules if rule.matches(reference_code)]
        if not matches:
            return None
        return max(
            matches,
            key=lambda rule: (
                rule.match_mode == "exato",
                len(rule.reference_code),
            ),
        )

    def component(self, component_code: str) -> RoaComponent:
        for component in self.components:
            if component.code == component_code:
                return component
        raise KeyError(component_code)


def load_roa_methodology(
    rules_path: Path = DEFAULT_ROA_RULES_ASSET,
    components_path: Path = DEFAULT_ROA_COMPONENTS_ASSET,
) -> RoaMethodology:
    components = _load_components(components_path)
    rules = _load_rules(rules_path, components)
    return RoaMethodology(
        methodology_version_id=METHODOLOGY_VERSION,
        components=tuple(components.values()),
        rules=tuple(rules),
    )


def _load_components(path: Path) -> dict[str, RoaComponent]:
    rows = _read_csv(path, COMPONENT_FIELDS, "ROA components")
    components: dict[str, RoaComponent] = {}
    for index, row in enumerate(rows, start=2):
        _require_values(row, COMPONENT_FIELDS, "ROA component", index)
        if row["componente_roa"] in components:
            raise RoaMethodologyAssetError(f"ROA component row {index} is duplicated.")
        if row["bloco_roa"] not in ROA_BLOCKS:
            raise RoaMethodologyAssetError(f"ROA component row {index} has invalid block.")
        _require_version(row, "ROA component", index)
        components[row["componente_roa"]] = RoaComponent(
            code=row["componente_roa"],
            block=row["bloco_roa"],
            label=row["rotulo"],
            required_evidence_type=row["required_evidence_type"],
            methodology_version_id=row["methodology_version_id"],
        )
    if {component.block for component in components.values()} != ROA_BLOCKS:
        raise RoaMethodologyAssetError("ROA components do not cover every required block.")
    return components


def _load_rules(
    path: Path,
    components: dict[str, RoaComponent],
) -> list[RoaMethodologyRule]:
    from app.assets.reference import load_official_reference_accounts

    rows = _read_csv(path, RULE_FIELDS, "ROA rules")
    official_codes = {
        account.reference_code for account in load_official_reference_accounts()
    }
    rules: list[RoaMethodologyRule] = []
    seen: set[tuple[str, str]] = set()
    for index, row in enumerate(rows, start=2):
        required = tuple(field for field in RULE_FIELDS if field != "motivo_condicional")
        _require_values(row, required, "ROA rule", index)
        key = (row["codigo_referencial"], row["modo_correspondencia"])
        if key in seen:
            raise RoaMethodologyAssetError(f"ROA rule row {index} is duplicated.")
        if row["codigo_referencial"] not in official_codes:
            raise RoaMethodologyAssetError(
                f"ROA rule row {index} is absent from official reference plan."
            )
        if row["modo_correspondencia"] not in MATCH_MODES:
            raise RoaMethodologyAssetError(
                f"ROA rule row {index} has invalid match mode."
            )
        if row["bloco_roa"] not in ROA_BLOCKS:
            raise RoaMethodologyAssetError(f"ROA rule row {index} has invalid block.")
        if row["sinal_natural"] not in NATURAL_SIDES:
            raise RoaMethodologyAssetError(
                f"ROA rule row {index} has invalid natural side."
            )
        if row["tratamento"] not in ROA_TREATMENTS:
            raise RoaMethodologyAssetError(
                f"ROA rule row {index} has invalid treatment."
            )
        if row["regra_principal"] not in PRIMARY_RULES:
            raise RoaMethodologyAssetError(
                f"ROA rule row {index} has invalid primary rule."
            )
        component = components.get(row["componente_roa"])
        if component is None or component.block != row["bloco_roa"]:
            raise RoaMethodologyAssetError(
                f"ROA rule row {index} has incompatible component."
            )
        requires_review = _parse_bool(row["exige_revisao"], "ROA rule", index)
        conditional_reason = row["motivo_condicional"].strip() or None
        if row["tratamento"] == "condicional" and (
            not requires_review or conditional_reason is None
        ):
            raise RoaMethodologyAssetError(
                f"ROA conditional rule row {index} requires review and reason."
            )
        if row["tratamento"] != "condicional" and conditional_reason is not None:
            raise RoaMethodologyAssetError(
                f"ROA rule row {index} has unexpected conditional reason."
            )
        if row["tratamento"] == "excluir_automaticamente" and (
            row["regra_principal"] != "excluir"
        ):
            raise RoaMethodologyAssetError(
                f"ROA excluded rule row {index} must use excluir."
            )
        _require_version(row, "ROA rule", index)
        seen.add(key)
        rules.append(
            RoaMethodologyRule(
                reference_code=row["codigo_referencial"],
                match_mode=row["modo_correspondencia"],
                methodology_group=row["grupo_metodologico"],
                macrogroup=row["macrogrupo"],
                block=row["bloco_roa"],
                natural_side=row["sinal_natural"],
                treatment=row["tratamento"],
                primary_rule=row["regra_principal"],
                component_code=row["componente_roa"],
                requires_review=requires_review,
                conditional_reason=conditional_reason,
                methodology_version_id=row["methodology_version_id"],
            )
        )
    if not rules:
        raise RoaMethodologyAssetError("ROA rules asset must not be empty.")
    return rules


def _read_csv(path: Path, fields: tuple[str, ...], label: str) -> list[dict[str, str]]:
    if not path.is_file():
        raise RoaMethodologyAssetError(f"{label} asset not found: {path.name}.")
    with path.open(encoding="utf-8", newline="") as source:
        reader = csv.DictReader(source)
        if tuple(reader.fieldnames or ()) != fields:
            raise RoaMethodologyAssetError(f"{label} asset has invalid columns.")
        return list(reader)


def _require_values(
    row: dict[str, str],
    fields: tuple[str, ...],
    label: str,
    index: int,
) -> None:
    if any(not row[field].strip() for field in fields):
        raise RoaMethodologyAssetError(f"{label} row {index} has empty required value.")


def _require_version(row: dict[str, str], label: str, index: int) -> None:
    if row["methodology_version_id"] != METHODOLOGY_VERSION:
        raise RoaMethodologyAssetError(
            f"{label} row {index} has invalid methodology version."
        )


def _parse_bool(value: str, label: str, index: int) -> bool:
    if value not in {"true", "false"}:
        raise RoaMethodologyAssetError(f"{label} row {index} has invalid boolean.")
    return value == "true"
