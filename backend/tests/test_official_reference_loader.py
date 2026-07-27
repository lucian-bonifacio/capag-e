from copy import deepcopy
import json
from pathlib import Path

import pytest

from app.assets.reference import (
    OfficialReferenceAssetError,
    load_official_reference_accounts,
)


def test_load_official_reference_accounts_from_governed_asset() -> None:
    accounts = load_official_reference_accounts()

    assert len(accounts) == 1109
    assert {account.reference_code for account in accounts} >= {
        "1.01.01.01.01",
        "2.01.01.01.01",
        "3.01.01.01.01.04",
    }


def test_missing_official_reference_asset_is_configuration_error(tmp_path) -> None:
    with pytest.raises(OfficialReferenceAssetError, match="not found"):
        load_official_reference_accounts(tmp_path / "missing.json")


def test_empty_official_reference_asset_is_configuration_error(tmp_path) -> None:
    payload = _valid_payload()
    payload["records"] = []
    asset_path = _write_payload(tmp_path, payload)

    with pytest.raises(OfficialReferenceAssetError, match="must contain records"):
        load_official_reference_accounts(asset_path)


def test_invalid_official_reference_manifest_is_configuration_error(tmp_path) -> None:
    payload = _valid_payload()
    del payload["source_document_hash"]
    asset_path = _write_payload(tmp_path, payload)

    with pytest.raises(OfficialReferenceAssetError, match="manifest missing fields"):
        load_official_reference_accounts(asset_path)


def test_unpublished_official_reference_asset_is_configuration_error(tmp_path) -> None:
    payload = _valid_payload()
    payload["base_status"] = "em_validacao"
    asset_path = _write_payload(tmp_path, payload)

    with pytest.raises(OfficialReferenceAssetError, match="not published"):
        load_official_reference_accounts(asset_path)


def test_invalid_source_hash_is_configuration_error(tmp_path) -> None:
    payload = _valid_payload()
    payload["source_document_hash"] = "invalid"
    asset_path = _write_payload(tmp_path, payload)

    with pytest.raises(OfficialReferenceAssetError, match="source_document_hash"):
        load_official_reference_accounts(asset_path)


def test_invalid_official_reference_record_is_configuration_error(tmp_path) -> None:
    payload = _valid_payload()
    del payload["records"][0]["official_description"]
    asset_path = _write_payload(tmp_path, payload)

    with pytest.raises(OfficialReferenceAssetError, match="missing fields"):
        load_official_reference_accounts(asset_path)


def test_duplicate_official_reference_record_is_rejected(tmp_path) -> None:
    payload = _valid_payload()
    payload["records"].append(deepcopy(payload["records"][0]))
    payload["source_record_count"] = 2
    payload["asset_record_count"] = 2
    asset_path = _write_payload(tmp_path, payload)

    with pytest.raises(OfficialReferenceAssetError, match="duplicated"):
        load_official_reference_accounts(asset_path)


def test_broken_official_reference_hierarchy_is_rejected(tmp_path) -> None:
    payload = _valid_payload()
    payload["records"][0]["parent_reference_code"] = "9.99"
    payload["records"][0]["level"] = 2
    asset_path = _write_payload(tmp_path, payload)

    with pytest.raises(OfficialReferenceAssetError, match="parent not found"):
        load_official_reference_accounts(asset_path)


def test_invalid_validity_is_rejected(tmp_path) -> None:
    payload = _valid_payload()
    payload["records"][0]["source_valid_to"] = "2014-12-31"
    payload["records"][0]["valid_to"] = 2014
    asset_path = _write_payload(tmp_path, payload)

    with pytest.raises(OfficialReferenceAssetError, match="validity range"):
        load_official_reference_accounts(asset_path)


def test_invalid_status_is_rejected(tmp_path) -> None:
    payload = _valid_payload()
    payload["records"][0]["status"] = "DESCONHECIDA"
    asset_path = _write_payload(tmp_path, payload)

    with pytest.raises(OfficialReferenceAssetError, match="invalid status"):
        load_official_reference_accounts(asset_path)


def test_inconsistent_source_nature_is_rejected(tmp_path) -> None:
    payload = _valid_payload()
    payload["records"][0]["source_nature_code"] = "2"
    asset_path = _write_payload(tmp_path, payload)

    with pytest.raises(OfficialReferenceAssetError, match="inconsistent source nature"):
        load_official_reference_accounts(asset_path)


def test_record_count_mismatch_is_rejected(tmp_path) -> None:
    payload = _valid_payload()
    payload["asset_record_count"] = 2
    asset_path = _write_payload(tmp_path, payload)

    with pytest.raises(OfficialReferenceAssetError, match="asset_record_count"):
        load_official_reference_accounts(asset_path)


def _write_payload(tmp_path: Path, payload: dict) -> Path:
    asset_path = tmp_path / "official-reference.json"
    asset_path.write_text(json.dumps(payload), encoding="utf-8")
    return asset_path


def _valid_payload() -> dict:
    required_fields = [
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
    ]
    return {
        "asset_type": "official_reference_accounts",
        "schema_version": "1.0.0",
        "official_version_id": "test-version",
        "base_status": "publicada",
        "approval_status": "aprovada",
        "methodology_version_id": "metodologia-2024.1",
        "source_document_name": "source.xlsx",
        "source_document_hash": "a" * 64,
        "source_document_date": "2025-11-09",
        "source_url_or_reference": "https://example.test/source.xlsx",
        "source_publisher": "Test publisher",
        "source_system": "ECF",
        "source_layout": "ECF_11",
        "source_calendar_year": 2024,
        "declaration_layout": "ECD_9",
        "entity_type": "PJ_GERAL",
        "source_sheets": ["L100A"],
        "source_record_count": 1,
        "asset_record_count": 1,
        "coverage_status": "completa",
        "required_fields": required_fields,
        "records": [
            {
                "reference_code": "1",
                "official_description": "ATIVO",
                "parent_reference_code": None,
                "level": 1,
                "nature": "ATIVO",
                "valid_from": 2015,
                "valid_to": None,
                "layout": "ECD_9",
                "entity_type": "PJ_GERAL",
                "source": "test-version",
                "status": "ATIVA",
                "methodology_version_id": "metodologia-2024.1",
                "source_sheet": "L100A",
                "source_type": "S",
                "source_nature_code": "1",
                "source_valid_from": "2015-01-01",
                "source_valid_to": None,
                "official_guidance": None,
                "validation_notes": None,
            }
        ],
    }
