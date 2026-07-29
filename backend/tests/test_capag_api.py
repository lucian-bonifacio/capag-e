from datetime import date, datetime, timezone
from decimal import Decimal

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.pool import StaticPool

from app.api.capag import get_capag_session
from app.domain import (
    ComponentStatus,
    DeclaredBalanceStatus,
    PlraCalculation,
    ProcessingStatus,
)
from app.main import create_app
from app.repositories import (
    AnalysisModel,
    Base,
    CompanyModel,
    EcdFileModel,
    ExerciseModel,
    add_plra_calculation,
)


def test_capag_api_runs_persists_and_returns_canonical_decimal_strings() -> None:
    client = _client()
    response = client.post(
        "/api/v1/analyses/analysis-1/exercises/2024/capag-assessment/run",
        json={
            "method": "fca_plra",
            "fca_value": "120000.00",
            "fca_status": "calculado",
        },
    )

    assert response.status_code == 200
    assert response.json()["capag_e_value"] == "620000.00"
    assert response.json()["capag_e_status"] == "calculado"
    assert response.json()["methodology_formula"] == "CAPAG-E = PLRA + FCA"
    assert response.json()["methodology_version_id"] == "metodologia-2024.1"
    assert response.json()["balance_status"] == "VALIDO"

    stored = client.get(
        "/api/v1/analyses/analysis-1/exercises/2024/capag-assessment"
    )
    assert stored.status_code == 200
    assert stored.json() == response.json()


def test_capag_api_does_not_mask_partial_fco_as_final_fca() -> None:
    client = _client()
    response = client.post(
        "/api/v1/analyses/analysis-1/exercises/2024/capag-assessment/run",
        json={
            "method": "fca_plra",
            "fco_value": "40000.00",
        },
    )

    assert response.status_code == 200
    assert response.json()["fca_status"] == "parcial"
    assert response.json()["capag_e_status"] == "parcial"
    assert response.json()["capag_e_value"] == "540000.00"


def test_capag_api_rejects_json_float_values() -> None:
    client = _client()
    response = client.post(
        "/api/v1/analyses/analysis-1/exercises/2024/capag-assessment/run",
        json={
            "method": "fca_plra",
            "fca_value": 120000.0,
            "fca_status": "calculado",
        },
    )

    assert response.status_code == 422
    assert "string_type" in response.text


def test_capag_api_rejects_client_supplied_plra() -> None:
    response = _client().post(
        "/api/v1/analyses/analysis-1/exercises/2024/capag-assessment/run",
        json={
            "method": "fca_plra",
            "plra_value": "999999.00",
            "plra_status": "calculado",
            "fca_value": "120000.00",
            "fca_status": "calculado",
        },
    )

    assert response.status_code == 422
    assert response.text.count("extra_forbidden") == 2


def test_capag_api_requires_a_persisted_plra_snapshot() -> None:
    response = _client(include_plra=False).post(
        "/api/v1/analyses/analysis-1/exercises/2024/capag-assessment/run",
        json={
            "method": "fca_plra",
            "fca_value": "120000.00",
            "fca_status": "calculado",
        },
    )

    assert response.status_code == 422
    assert response.json()["detail"]["error_code"] == "CAPAG_ASSESSMENT_CONTRACT_ERROR"


def test_capag_api_propagates_plra_blocking_status_and_messages() -> None:
    response = _client(
        plra_status=ComponentStatus.BLOCKED_BY_EVIDENCE
    ).post(
        "/api/v1/analyses/analysis-1/exercises/2024/capag-assessment/run",
        json={
            "method": "fca_plra",
            "fca_value": "120000.00",
            "fca_status": "calculado",
        },
    )

    assert response.status_code == 200
    body = response.json()
    assert body["plra_status"] == "bloqueado_por_evidencia"
    assert body["capag_e_status"] == "bloqueado"
    assert body["capag_e_value"] is None
    assert "EVIDENCIA_CRITICA_PENDENTE" in body["blocking_issues"]
    assert "Avaliacao patrimonial pendente." in body["limitations"]


def test_capag_api_blocks_final_result_from_non_valid_declared_balance() -> None:
    response = _client(
        balance_status=DeclaredBalanceStatus.DIVERGENTE,
    ).post(
        "/api/v1/analyses/analysis-1/exercises/2024/capag-assessment/run",
        json={
            "method": "fca_plra",
            "fca_value": "120000.00",
            "fca_status": "calculado",
        },
    )

    assert response.status_code == 200
    body = response.json()
    assert body["balance_status"] == "DIVERGENTE"
    assert body["capag_e_status"] == "bloqueado"
    assert body["capag_e_value"] is None
    assert "BALANCO_DECLARADO_NAO_VALIDO:DIVERGENTE" in body["blocking_issues"]


def test_capag_openapi_exposes_governed_paths_and_string_values() -> None:
    schema = create_app().openapi()
    base_path = "/api/v1/analyses/{analysis_id}/exercises/{year}/capag-assessment"

    assert "get" in schema["paths"][base_path]
    assert "post" in schema["paths"][f"{base_path}/run"]
    response_schema = schema["components"]["schemas"]["CapagAssessmentResponse"]
    assert response_schema["properties"]["capag_e_value"]["anyOf"][0]["type"] == "string"


def _client(
    *,
    include_plra: bool = True,
    plra_status: ComponentStatus = ComponentStatus.CALCULATED,
    balance_status: DeclaredBalanceStatus = DeclaredBalanceStatus.VALIDO,
) -> TestClient:
    engine = create_engine(
        "sqlite+pysqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(engine)
    with Session(engine) as session:
        company = CompanyModel(
            id="company-1",
            legal_name="Empresa de teste",
            tax_id="00000000000100",
        )
        ecd_file = EcdFileModel(
            id="ecd-1",
            company_id=company.id,
            original_filename="teste.ecd",
            content_hash="sha256:capag-api",
            layout="ECD_2024",
            period_start=date(2024, 1, 1),
            period_end=date(2024, 12, 31),
        )
        analysis = AnalysisModel(
            id="analysis-1",
            company_id=company.id,
            ecd_file_id=ecd_file.id,
            methodology_version_id="metodologia-2024.1",
            status=ProcessingStatus.NOT_RUN.value,
        )
        exercise = ExerciseModel(
            analysis_id=analysis.id,
            year=2024,
            status=ProcessingStatus.NOT_RUN.value,
            methodology_version_id="metodologia-2024.1",
        )
        session.add_all([company, ecd_file, analysis, exercise])
        session.flush()
        if include_plra:
            add_plra_calculation(
                session,
                exercise_id=exercise.id,
                calculation=_plra_calculation(plra_status, balance_status),
            )
        session.commit()

    app = create_app()

    def override_session():
        with Session(engine) as session:
            yield session

    app.dependency_overrides[get_capag_session] = override_session
    return TestClient(app)


def _plra_calculation(
    status: ComponentStatus,
    balance_status: DeclaredBalanceStatus,
) -> PlraCalculation:
    blocked = status != ComponentStatus.CALCULATED
    return PlraCalculation(
        analysis_id="analysis-1",
        exercise_year=2024,
        gross_assets_value=Decimal("700000.00"),
        gross_economic_liabilities_value=Decimal("200000.00"),
        adjusted_assets_value=Decimal("700000.00"),
        plr_gross_value=Decimal("500000.00"),
        plra_value=Decimal("500000.00"),
        plra_status=status,
        calculation_formula=(
            "PLRA = ativos com valor economico final - passivos economicos exigiveis"
        ),
        account_rows=(),
        pending_accounts=("1.2.3",) if blocked else (),
        warnings=(),
        limitations=("Avaliacao patrimonial pendente.",) if blocked else (),
        blocking_issues=("EVIDENCIA_CRITICA_PENDENTE",) if blocked else (),
        balance_status=balance_status,
        methodology_version_id="metodologia-2024.1",
        calculated_at=datetime.now(timezone.utc),
    )
