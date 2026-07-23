from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from app.engine.methodology_matcher import OfficialReferenceAccount


DEFAULT_OFFICIAL_REFERENCE_ASSET = Path(__file__).with_name("official_reference_accounts.json")

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
}


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

    if payload.get("asset_type") != "official_reference_accounts":
        raise OfficialReferenceAssetError(
            "Official reference asset has invalid asset_type."
        )

    records = payload.get("records")
    if not isinstance(records, list):
        raise OfficialReferenceAssetError("Official reference asset records must be a list.")

    if len(records) == 0:
        raise OfficialReferenceAssetError("Official reference asset must contain records.")

    for index, record in enumerate(records):
        _validate_record(record, index)


def _validate_record(record: Any, index: int) -> None:
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
    }
    for field in string_fields:
        if not isinstance(record[field], str) or record[field].strip() == "":
            raise OfficialReferenceAssetError(
                f"Official reference record {index} has invalid {field}."
            )

    if record["parent_reference_code"] is not None and not isinstance(
        record["parent_reference_code"], str
    ):
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
