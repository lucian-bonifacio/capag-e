from __future__ import annotations

import json
import re
from datetime import date
from pathlib import Path
from typing import Any

from app.engine.methodology_matcher import OfficialReferenceAccount


DEFAULT_OFFICIAL_REFERENCE_ASSET = Path(__file__).with_name("official_reference_accounts.json")

REQUIRED_MANIFEST_FIELDS = {
    "asset_type",
    "schema_version",
    "official_version_id",
    "base_status",
    "approval_status",
    "methodology_version_id",
    "source_document_name",
    "source_document_hash",
    "source_document_date",
    "source_url_or_reference",
    "source_publisher",
    "source_system",
    "source_layout",
    "source_calendar_year",
    "declaration_layout",
    "entity_type",
    "source_sheets",
    "source_record_count",
    "asset_record_count",
    "coverage_status",
    "required_fields",
    "records",
}

REQUIRED_OFFICIAL_REFERENCE_FIELDS = {
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

ALLOWED_BASE_STATUSES = {
    "rascunho",
    "em_validacao",
    "aprovada",
    "publicada",
    "substituida",
    "bloqueada",
}
ALLOWED_APPROVAL_STATUSES = {"pendente", "aprovada", "rejeitada"}
ALLOWED_RECORD_STATUSES = {"ATIVA", "INATIVA", "EM_REVISAO", "BLOQUEADA"}
ALLOWED_NATURES = {"ATIVO", "PASSIVO", "PATRIMONIO_LIQUIDO", "RESULTADO"}
SOURCE_NATURES = {
    "1": "ATIVO",
    "2": "PASSIVO",
    "3": "PATRIMONIO_LIQUIDO",
    "4": "RESULTADO",
}
REFERENCE_CODE_PATTERN = re.compile(r"^[1-9](?:\.\d{2})*$")
SHA256_PATTERN = re.compile(r"^[0-9a-f]{64}$")


class OfficialReferenceAssetError(RuntimeError):
    pass


def load_official_reference_accounts(
    asset_path: Path = DEFAULT_OFFICIAL_REFERENCE_ASSET,
) -> list[OfficialReferenceAccount]:
    if not asset_path.is_file():
        raise OfficialReferenceAssetError(
            f"Official reference asset not found: {asset_path.name}."
        )

    try:
        payload = json.loads(asset_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise OfficialReferenceAssetError("Official reference asset is not valid JSON.") from exc

    _validate_payload(payload)
    return [_record_to_official_reference(record) for record in payload["records"]]


def _validate_payload(payload: Any) -> None:
    if not isinstance(payload, dict):
        raise OfficialReferenceAssetError("Official reference asset must be a JSON object.")

    missing_manifest_fields = REQUIRED_MANIFEST_FIELDS - set(payload)
    if missing_manifest_fields:
        fields = ", ".join(sorted(missing_manifest_fields))
        raise OfficialReferenceAssetError(
            f"Official reference manifest missing fields: {fields}."
        )

    if payload["asset_type"] != "official_reference_accounts":
        raise OfficialReferenceAssetError(
            "Official reference asset has invalid asset_type."
        )

    _validate_manifest(payload)

    records = payload["records"]
    if not isinstance(records, list):
        raise OfficialReferenceAssetError("Official reference asset records must be a list.")

    if len(records) == 0:
        raise OfficialReferenceAssetError("Official reference asset must contain records.")

    if payload["source_record_count"] != len(records):
        raise OfficialReferenceAssetError(
            "Official reference asset source_record_count does not match records."
        )
    if payload["asset_record_count"] != len(records):
        raise OfficialReferenceAssetError(
            "Official reference asset asset_record_count does not match records."
        )

    seen: set[tuple[str, str, str, int, int | None]] = set()
    for index, record in enumerate(records):
        _validate_record(record, index, payload)
        key = (
            record["reference_code"].strip(),
            record["layout"].strip(),
            record["entity_type"].strip(),
            record["valid_from"],
            record["valid_to"],
        )
        if key in seen:
            raise OfficialReferenceAssetError(
                f"Official reference record {index} is duplicated."
            )
        seen.add(key)

    _validate_hierarchy(records)


def _validate_manifest(payload: dict[str, Any]) -> None:
    string_fields = {
        "schema_version",
        "official_version_id",
        "approval_status",
        "methodology_version_id",
        "source_document_name",
        "source_document_date",
        "source_url_or_reference",
        "source_publisher",
        "source_system",
        "source_layout",
        "declaration_layout",
        "entity_type",
        "coverage_status",
    }
    for field in string_fields:
        if not isinstance(payload[field], str) or payload[field].strip() == "":
            raise OfficialReferenceAssetError(
                f"Official reference manifest has invalid {field}."
            )

    if payload["base_status"] not in ALLOWED_BASE_STATUSES:
        raise OfficialReferenceAssetError(
            "Official reference manifest has invalid base_status."
        )
    if payload["base_status"] != "publicada":
        raise OfficialReferenceAssetError(
            "Official reference base is not published."
        )
    if payload["approval_status"] not in ALLOWED_APPROVAL_STATUSES:
        raise OfficialReferenceAssetError(
            "Official reference manifest has invalid approval_status."
        )
    if payload["approval_status"] != "aprovada":
        raise OfficialReferenceAssetError(
            "Official reference source is not approved."
        )
    if not isinstance(payload["source_document_hash"], str) or not SHA256_PATTERN.fullmatch(
        payload["source_document_hash"]
    ):
        raise OfficialReferenceAssetError(
            "Official reference manifest has invalid source_document_hash."
        )

    _parse_iso_date(payload["source_document_date"], "source_document_date")

    if not isinstance(payload["source_calendar_year"], int):
        raise OfficialReferenceAssetError(
            "Official reference manifest has invalid source_calendar_year."
        )

    for field in {"source_record_count", "asset_record_count"}:
        if not isinstance(payload[field], int) or payload[field] < 1:
            raise OfficialReferenceAssetError(
                f"Official reference manifest has invalid {field}."
            )

    source_sheets = payload["source_sheets"]
    if (
        not isinstance(source_sheets, list)
        or len(source_sheets) == 0
        or any(not isinstance(item, str) or item.strip() == "" for item in source_sheets)
    ):
        raise OfficialReferenceAssetError(
            "Official reference manifest has invalid source_sheets."
        )

    required_fields = payload["required_fields"]
    if not isinstance(required_fields, list) or set(required_fields) != REQUIRED_OFFICIAL_REFERENCE_FIELDS:
        raise OfficialReferenceAssetError(
            "Official reference manifest has invalid required_fields."
        )


def _validate_record(record: Any, index: int, manifest: dict[str, Any]) -> None:
    if not isinstance(record, dict):
        raise OfficialReferenceAssetError(
            f"Official reference record {index} must be a JSON object."
        )

    missing_fields = REQUIRED_OFFICIAL_REFERENCE_FIELDS - set(record)
    if missing_fields:
        fields = ", ".join(sorted(missing_fields))
        raise OfficialReferenceAssetError(
            f"Official reference record {index} missing fields: {fields}."
        )

    string_fields = {
        "reference_code",
        "official_description",
        "nature",
        "layout",
        "entity_type",
        "source",
        "status",
        "methodology_version_id",
        "source_sheet",
        "source_type",
        "source_nature_code",
        "source_valid_from",
    }
    for field in string_fields:
        if not isinstance(record[field], str) or record[field].strip() == "":
            raise OfficialReferenceAssetError(
                f"Official reference record {index} has invalid {field}."
            )

    if not REFERENCE_CODE_PATTERN.fullmatch(record["reference_code"].strip()):
        raise OfficialReferenceAssetError(
            f"Official reference record {index} has invalid reference_code."
        )

    if record["parent_reference_code"] is not None and not isinstance(
        record["parent_reference_code"], str
    ):
        raise OfficialReferenceAssetError(
            f"Official reference record {index} has invalid parent_reference_code."
        )
    if isinstance(record["parent_reference_code"], str):
        parent_code = record["parent_reference_code"].strip()
        if parent_code == "" or not REFERENCE_CODE_PATTERN.fullmatch(parent_code):
            raise OfficialReferenceAssetError(
                f"Official reference record {index} has invalid parent_reference_code."
            )

    if not isinstance(record["level"], int) or record["level"] < 1:
        raise OfficialReferenceAssetError(
            f"Official reference record {index} has invalid level."
        )

    if not isinstance(record["valid_from"], int):
        raise OfficialReferenceAssetError(
            f"Official reference record {index} has invalid valid_from."
        )

    if record["valid_to"] is not None and not isinstance(record["valid_to"], int):
        raise OfficialReferenceAssetError(
            f"Official reference record {index} has invalid valid_to."
        )

    if (
        isinstance(record["valid_to"], int)
        and record["valid_to"] < record["valid_from"]
    ):
        raise OfficialReferenceAssetError(
            f"Official reference record {index} has invalid validity range."
        )

    source_valid_from = _parse_iso_date(
        record["source_valid_from"], f"record {index} source_valid_from"
    )
    source_valid_to = (
        _parse_iso_date(record["source_valid_to"], f"record {index} source_valid_to")
        if record["source_valid_to"] is not None
        else None
    )
    if source_valid_to is not None and source_valid_to < source_valid_from:
        raise OfficialReferenceAssetError(
            f"Official reference record {index} has invalid source validity range."
        )
    if source_valid_from.year != record["valid_from"]:
        raise OfficialReferenceAssetError(
            f"Official reference record {index} has inconsistent valid_from."
        )
    if (
        source_valid_to is None
        and record["valid_to"] is not None
        or source_valid_to is not None
        and record["valid_to"] != source_valid_to.year
    ):
        raise OfficialReferenceAssetError(
            f"Official reference record {index} has inconsistent valid_to."
        )

    if record["nature"] not in ALLOWED_NATURES:
        raise OfficialReferenceAssetError(
            f"Official reference record {index} has invalid nature."
        )
    if SOURCE_NATURES.get(record["source_nature_code"]) != record["nature"]:
        raise OfficialReferenceAssetError(
            f"Official reference record {index} has inconsistent source nature."
        )
    if record["status"] not in ALLOWED_RECORD_STATUSES:
        raise OfficialReferenceAssetError(
            f"Official reference record {index} has invalid status."
        )
    if record["source_type"] not in {"A", "S"}:
        raise OfficialReferenceAssetError(
            f"Official reference record {index} has invalid source_type."
        )
    if record["official_guidance"] is not None and not isinstance(
        record["official_guidance"], str
    ):
        raise OfficialReferenceAssetError(
            f"Official reference record {index} has invalid official_guidance."
        )
    if record["validation_notes"] is not None and not isinstance(
        record["validation_notes"], str
    ):
        raise OfficialReferenceAssetError(
            f"Official reference record {index} has invalid validation_notes."
        )
    if record["status"] in {"EM_REVISAO", "BLOQUEADA"} and (
        not isinstance(record["validation_notes"], str)
        or record["validation_notes"].strip() == ""
    ):
        raise OfficialReferenceAssetError(
            f"Official reference record {index} requires validation_notes."
        )

    if record["layout"] != manifest["declaration_layout"]:
        raise OfficialReferenceAssetError(
            f"Official reference record {index} has inconsistent layout."
        )
    if record["entity_type"] != manifest["entity_type"]:
        raise OfficialReferenceAssetError(
            f"Official reference record {index} has inconsistent entity_type."
        )
    if record["source_sheet"] not in manifest["source_sheets"]:
        raise OfficialReferenceAssetError(
            f"Official reference record {index} has invalid source_sheet."
        )
    if record["methodology_version_id"] != manifest["methodology_version_id"]:
        raise OfficialReferenceAssetError(
            f"Official reference record {index} has inconsistent methodology_version_id."
        )


def _validate_hierarchy(records: list[dict[str, Any]]) -> None:
    records_by_code: dict[str, list[dict[str, Any]]] = {}
    for record in records:
        records_by_code.setdefault(record["reference_code"], []).append(record)

    parent_by_code: dict[str, str | None] = {}
    for record in records:
        code = record["reference_code"]
        parent_code = record["parent_reference_code"]
        parent_by_code.setdefault(code, parent_code)
        if parent_by_code[code] != parent_code:
            raise OfficialReferenceAssetError(
                f"Official reference hierarchy has conflicting parents for {code}."
            )
        if parent_code is None:
            continue
        parent_candidates = records_by_code.get(parent_code, [])
        if len(parent_candidates) == 0:
            raise OfficialReferenceAssetError(
                f"Official reference hierarchy parent not found for {code}."
            )
        if (
            all(parent["level"] >= record["level"] for parent in parent_candidates)
            and record["status"] != "EM_REVISAO"
        ):
            raise OfficialReferenceAssetError(
                f"Official reference hierarchy has invalid level for {code}."
            )

    for code in parent_by_code:
        visited: set[str] = set()
        current: str | None = code
        while current is not None:
            if current in visited:
                raise OfficialReferenceAssetError(
                    f"Official reference hierarchy has cycle at {current}."
                )
            visited.add(current)
            current = parent_by_code.get(current)


def _parse_iso_date(value: Any, field: str) -> date:
    if not isinstance(value, str):
        raise OfficialReferenceAssetError(
            f"Official reference asset has invalid {field}."
        )
    try:
        return date.fromisoformat(value)
    except ValueError as exc:
        raise OfficialReferenceAssetError(
            f"Official reference asset has invalid {field}."
        ) from exc


def _record_to_official_reference(record: dict[str, Any]) -> OfficialReferenceAccount:
    return OfficialReferenceAccount(
        reference_code=record["reference_code"].strip(),
        official_description=record["official_description"].strip(),
        parent_reference_code=(
            record["parent_reference_code"].strip()
            if isinstance(record["parent_reference_code"], str)
            else None
        ),
        level=record["level"],
        nature=record["nature"].strip(),
        valid_from=record["valid_from"],
        valid_to=record["valid_to"],
        layout=record["layout"].strip(),
        entity_type=record["entity_type"].strip(),
        source=record["source"].strip(),
        status=record["status"].strip(),
        methodology_version_id=record["methodology_version_id"].strip(),
    )
