from __future__ import annotations

from hashlib import sha256
from pathlib import Path

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool

from app.api.declared import get_declared_run_session
from app.api.imports import get_import_session
from app.domain import DeclaredBalanceStatus, EcdPreparationStatus
from app.main import app
from app.repositories import Base, EcdFileModel


ECD_DIRECTORY = Path("/workspace/docs/reference/ecd-example")


@pytest.mark.parametrize(
    ("filename", "expected_status"),
    [
        ("ECD 2024 DATAPACK.txt", DeclaredBalanceStatus.VALIDO),
        ("ECD 2024 INVENTCLOUD.txt", DeclaredBalanceStatus.DIVERGENTE),
    ],
)
def test_real_ecd_reimport_and_declared_balance_are_evaluated_separately(
    filename: str,
    expected_status: DeclaredBalanceStatus,
) -> None:
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(engine)
    SessionForTest = sessionmaker(bind=engine)

    def override_session():
        with SessionForTest() as session:
            yield session

    app.dependency_overrides[get_import_session] = override_session
    app.dependency_overrides[get_declared_run_session] = override_session
    client = TestClient(app)
    source = ECD_DIRECTORY / filename
    original = source.read_bytes()

    try:
        first_import = client.post(
            "/api/v1/ecd/import",
            data={"methodology_version_id": "metodologia-2024.1"},
            files={"file": (filename, original, "text/plain")},
        )
        assert first_import.status_code == 201, first_import.text
        imported = first_import.json()

        with Session(engine) as session:
            ecd_file = session.get(EcdFileModel, imported["ecd_file_id"])
            assert ecd_file is not None
            ecd_file.preparation_status = EcdPreparationStatus.REIMPORT_REQUIRED.value
            session.commit()

        reimport = client.post(
            "/api/v1/ecd/import",
            data={"methodology_version_id": "metodologia-2024.1"},
            files={"file": (filename, original, "text/plain")},
        )
        assert reimport.status_code == 200
        assert reimport.json()["reprocessed"] is True
        assert reimport.json()["analysis_id"] == imported["analysis_id"]
        assert reimport.json()["ecd_file_id"] == imported["ecd_file_id"]

        balance = client.get(
            f"/api/v1/analyses/{imported['analysis_id']}/"
            f"exercises/{imported['year']}/declared/balance/accounts"
        )
        assert balance.status_code == 200
        balance_payload = balance.json()
        assert balance_payload["balance_status"] == expected_status.value
        assert balance_payload["is_blocking"] is (
            expected_status != DeclaredBalanceStatus.VALIDO
        )
        detail_statuses = _detail_statuses(balance_payload["rows"])
        if expected_status == DeclaredBalanceStatus.VALIDO:
            assert set(detail_statuses) == {"CONCILIADA"}
        else:
            assert any(status != "CONCILIADA" for status in detail_statuses)

        with Session(engine) as session:
            stored = session.scalar(select(EcdFileModel))
            assert stored is not None
            assert stored.original_content == original
            assert stored.content_size == len(original)
            assert stored.content_hash == f"sha256:{sha256(original).hexdigest()}"
            assert (
                stored.preparation_status
                == EcdPreparationStatus.READY_FOR_RECONCILIATION.value
            )
    finally:
        app.dependency_overrides.clear()


def _detail_statuses(rows: list[dict]) -> list[str]:
    statuses: list[str] = []
    for row in rows:
        if row["reconciliation_status"] is not None:
            statuses.append(row["reconciliation_status"])
        statuses.extend(_detail_statuses(row["children"]))
    return statuses
