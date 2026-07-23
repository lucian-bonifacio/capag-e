import json

import pytest

from app.assets.reference import (
    OfficialReferenceAssetError,
    load_official_reference_accounts,
)


def test_load_official_reference_accounts_from_governed_asset() -> None:
    accounts = load_official_reference_accounts()

    assert len(accounts) > 0
    assert {account.reference_code for account in accounts} >= {
        "2.01.01.07.01",
        "1.01.02.03.04",
    }


def test_missing_official_reference_asset_is_configuration_error(tmp_path) -> None:
    with pytest.raises(OfficialReferenceAssetError, match="not found"):
        load_official_reference_accounts(tmp_path / "missing.json")


def test_empty_official_reference_asset_is_configuration_error(tmp_path) -> None:
    asset_path = tmp_path / "empty.json"
    asset_path.write_text(
        json.dumps(
            {
                "asset_type": "official_reference_accounts",
                "records": [],
            }
        ),
        encoding="utf-8",
    )

    with pytest.raises(OfficialReferenceAssetError, match="must contain records"):
        load_official_reference_accounts(asset_path)


def test_invalid_official_reference_asset_is_configuration_error(tmp_path) -> None:
    asset_path = tmp_path / "invalid.json"
    asset_path.write_text(
        json.dumps(
            {
                "asset_type": "official_reference_accounts",
                "records": [
                    {
                        "reference_code": "2.01.01.07.01",
                    }
                ],
            }
        ),
        encoding="utf-8",
    )

    with pytest.raises(OfficialReferenceAssetError, match="missing fields"):
        load_official_reference_accounts(asset_path)
