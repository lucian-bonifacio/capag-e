from decimal import Decimal

from fastapi.testclient import TestClient

from app.api.declared import get_declared_snapshot_reader
from app.application.declared_service import (
    DeclaredAccountSnapshotView,
    DeclaredLayerSummary,
    DeclaredSnapshotsNotFound,
)
from app.main import app


class FakeDeclaredSnapshotReader:
    def get_summary(self, *, analysis_id: str, year: int) -> DeclaredLayerSummary:
        if analysis_id == "missing":
            raise DeclaredSnapshotsNotFound("Declared snapshot not found.")

        return DeclaredLayerSummary(
            analysis_id=analysis_id,
            year=year,
            total_accounts=2,
            status_counts={
                "MAPEADO": 1,
                "NAO_MAPEADO_METODOLOGICAMENTE": 1,
            },
            methodology_version_id="test-version",
        )

    def list_accounts(
        self,
        *,
        analysis_id: str,
        year: int,
    ) -> list[DeclaredAccountSnapshotView]:
        if analysis_id == "missing":
            raise DeclaredSnapshotsNotFound("Declared snapshot not found.")

        return [
            DeclaredAccountSnapshotView(
                account_code="1725",
                account_name="EMPRESTIMO - SICOOB CREDICITRUS - C",
                declared_reference_code="2.01.01.07.01",
                official_description="Emprestimos e financiamentos",
                official_reference_status="ATIVA",
                methodology_rule_applied="2.01.01.07.01",
                methodology_rule_status="ATIVA",
                purpose="FCO",
                treatment="tratamento_financiamento",
                base_value=Decimal("100000.00"),
                considered_value=Decimal("0.00"),
                final_status="MAPEADO",
                observation=None,
                recommended_action=None,
                methodology_version_id="test-version",
            ),
            DeclaredAccountSnapshotView(
                account_code="9999",
                account_name="Conta sem metodologia exata",
                declared_reference_code="9.99.99",
                official_description="Conta oficial de teste",
                official_reference_status="ATIVA",
                methodology_rule_applied=None,
                methodology_rule_status=None,
                purpose="FCO",
                treatment=None,
                base_value=Decimal("50.10"),
                considered_value=Decimal("50.10"),
                final_status="NAO_MAPEADO_METODOLOGICAMENTE",
                observation="Nenhuma regra metodologica exata encontrada.",
                recommended_action="revisar_metodologia",
                methodology_version_id="test-version",
            ),
        ]


def test_declared_accounts_endpoint_serializes_decimal_values_as_strings() -> None:
    app.dependency_overrides[get_declared_snapshot_reader] = FakeDeclaredSnapshotReader
    client = TestClient(app)

    response = client.get("/api/v1/analyses/analysis-1/exercises/2024/declared/accounts")

    app.dependency_overrides.clear()
    assert response.status_code == 200
    payload = response.json()
    assert payload["analysis_id"] == "analysis-1"
    assert payload["year"] == 2024
    assert payload["accounts"][0]["base_value"] == "100000.00"
    assert payload["accounts"][0]["considered_value"] == "0.00"
    assert payload["accounts"][0]["final_status"] == "MAPEADO"
    assert payload["accounts"][1]["final_status"] == "NAO_MAPEADO_METODOLOGICAMENTE"
    assert payload["accounts"][1]["recommended_action"] == "revisar_metodologia"


def test_declared_summary_endpoint_returns_status_counts() -> None:
    app.dependency_overrides[get_declared_snapshot_reader] = FakeDeclaredSnapshotReader
    client = TestClient(app)

    response = client.get("/api/v1/analyses/analysis-1/exercises/2024/declared")

    app.dependency_overrides.clear()
    assert response.status_code == 200
    assert response.json() == {
        "analysis_id": "analysis-1",
        "year": 2024,
        "total_accounts": 2,
        "status_counts": {
            "MAPEADO": 1,
            "NAO_MAPEADO_METODOLOGICAMENTE": 1,
        },
        "methodology_version_id": "test-version",
    }


def test_declared_endpoint_maps_missing_snapshot_to_explicit_error() -> None:
    app.dependency_overrides[get_declared_snapshot_reader] = FakeDeclaredSnapshotReader
    client = TestClient(app)

    response = client.get("/api/v1/analyses/missing/exercises/2024/declared")

    app.dependency_overrides.clear()
    assert response.status_code == 404
    assert response.json()["detail"] == {
        "error_code": "DECLARED_SNAPSHOT_NOT_FOUND",
        "message": "Declared snapshot not found.",
    }


def test_declared_openapi_contains_declared_contracts() -> None:
    paths = app.openapi()["paths"]

    assert "/api/v1/analyses/{analysis_id}/exercises/{year}/declared" in paths
    assert "/api/v1/analyses/{analysis_id}/exercises/{year}/declared/accounts" in paths
    accounts_operation = paths[
        "/api/v1/analyses/{analysis_id}/exercises/{year}/declared/accounts"
    ]["get"]
    assert accounts_operation["responses"]["200"]["description"] == "Successful Response"

