from pathlib import Path
import json

from scripts.import_official_reference import build_payload


ASSETS_ROOT = Path(__file__).resolve().parents[1] / "app" / "assets"
REFERENCE_TEMPLATE = ASSETS_ROOT / "reference" / "official_reference_accounts.template.json"
REFERENCE_ASSET = ASSETS_ROOT / "reference" / "official_reference_accounts.json"
REFERENCE_SOURCE = (
    ASSETS_ROOT
    / "reference"
    / "sources"
    / "Tabelas-Dinamicas-ECF-Leiaute-11-AC-2024.xlsx"
)
METHODOLOGY_TEMPLATE = ASSETS_ROOT / "methodology" / "internal_methodology_rules.template.json"
DFC_METHODOLOGY_ASSET = ASSETS_ROOT / "methodology" / "dfc_methodology.json"
ROA_RULES_ASSET = ASSETS_ROOT / "methodology" / "tabela_metodologica_roa.csv"
ROA_COMPONENTS_ASSET = ASSETS_ROOT / "methodology" / "componentes_roa.csv"
TEMPORARY_NAMES = {
    ".DS_Store",
    "Thumbs.db",
}
TEMPORARY_SUFFIXES = {
    ".bak",
    ".orig",
    ".tmp",
}


def test_assets_package_exists() -> None:
    assert ASSETS_ROOT.is_dir()
    assert (ASSETS_ROOT / "__init__.py").is_file()


def test_declared_layer_assets_are_separated() -> None:
    assert (ASSETS_ROOT / "reference" / "__init__.py").is_file()
    assert (ASSETS_ROOT / "methodology" / "__init__.py").is_file()
    assert REFERENCE_ASSET.is_file()
    assert REFERENCE_TEMPLATE.is_file()
    assert METHODOLOGY_TEMPLATE.is_file()
    assert DFC_METHODOLOGY_ASSET.is_file()
    assert ROA_RULES_ASSET.is_file()
    assert ROA_COMPONENTS_ASSET.is_file()


def test_assets_tree_has_no_temporary_files() -> None:
    temporary_files = [
        path.relative_to(ASSETS_ROOT)
        for path in ASSETS_ROOT.rglob("*")
        if path.is_file()
        and (
            path.name in TEMPORARY_NAMES
            or path.suffix.lower() in TEMPORARY_SUFFIXES
            or path.name.endswith("~")
        )
    ]

    assert temporary_files == []


def test_official_reference_template_is_empty_and_documents_required_fields() -> None:
    payload = json.loads(REFERENCE_TEMPLATE.read_text(encoding="utf-8"))

    assert payload["asset_type"] == "official_reference_accounts"
    assert payload["records"] == []
    assert set(payload["required_fields"]) == {
        "reference_code",
        "official_description",
        "parent_reference_code",
        "level",
        "nature",
        "valid_from",
        "valid_to",
        "layout",
        "entity_type",
        "source",
        "status",
        "methodology_version_id",
        "source_sheet",
        "source_type",
        "source_nature_code",
        "source_valid_from",
        "source_valid_to",
        "official_guidance",
        "validation_notes",
    }


def test_official_reference_asset_is_governed_and_non_empty() -> None:
    payload = json.loads(REFERENCE_ASSET.read_text(encoding="utf-8"))

    assert payload["asset_type"] == "official_reference_accounts"
    assert payload["schema_version"] == "1.0.0"
    assert payload["methodology_version_id"] == "metodologia-2024.1"
    assert payload["base_status"] == "publicada"
    assert payload["approval_status"] == "aprovada"
    assert payload["source_document_hash"] == (
        "0c66a19ce859cdc7a1eee137896243100cbaa26239ffa8ed3044762f3e359397"
    )
    assert payload["source_record_count"] == 1109
    assert payload["asset_record_count"] == 1109
    assert len(payload["records"]) == 1109
    for record in payload["records"]:
        assert set(payload["required_fields"]).issubset(record)


def test_official_reference_asset_is_reproducible_from_approved_source() -> None:
    checked_in_payload = json.loads(REFERENCE_ASSET.read_text(encoding="utf-8"))

    assert build_payload(REFERENCE_SOURCE) == checked_in_payload


def test_internal_methodology_template_is_empty_and_documents_required_fields() -> None:
    payload = json.loads(METHODOLOGY_TEMPLATE.read_text(encoding="utf-8"))

    assert payload["asset_type"] == "internal_methodology_rules"
    assert payload["rules"] == []
    assert set(payload["required_fields"]) == {
        "reference_code",
        "purpose",
        "methodology_description",
        "plra_category",
        "fco_category",
        "capag_category",
        "flow_nature",
        "operational_treatment",
        "include_in_calculation",
        "sign",
        "rule_status",
        "valid_from",
        "valid_to",
        "methodology_version_id",
        "observation",
    }
    assert set(payload["allowed_rule_statuses"]) == {
        "ATIVA",
        "BLOQUEADA",
        "EM_REVISAO",
        "DEPRECIADA",
    }
