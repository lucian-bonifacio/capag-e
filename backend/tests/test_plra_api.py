from datetime import date
from decimal import Decimal
from io import BytesIO

from fastapi.testclient import TestClient
from openpyxl import load_workbook
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.pool import StaticPool

from app.api.plra import get_plra_session
from app.domain import ProcessingStatus
from app.main import create_app
from app.repositories import (
    AnalysisModel,
    Base,
    CompanyModel,
    EcdFileModel,
    EcdI050AccountModel,
    EcdI051ReferenceLinkModel,
    EcdI155BalanceModel,
    EcdJ100BalanceRowModel,
    ExerciseModel,
)


BASE_PATH = "/api/v1/analyses/analysis-1/exercises/2024/plra"


def test_plra_api_runs_persists_and_exposes_audit_with_decimal_strings() -> None:
    client = _client()

    response = client.post(f"{BASE_PATH}/run")

    assert response.status_code == 200
    body = response.json()
    assert body["gross_economic_liabilities_value"] == "100000.00"
    assert body["plra_value"] == "-100000.00"
    assert body["plra_status"] == "parcial"
    assert body["methodology_version_id"] == "metodologia-2024.1"
    assert body["balance_status"] == "ESTRUTURA_INVALIDA"
    assert (
        "BALANCO_DECLARADO_NAO_VALIDO:ESTRUTURA_INVALIDA"
        in body["blocking_issues"]
    )

    stored = client.get(BASE_PATH)
    assert stored.status_code == 200
    assert stored.json() == body

    audit = client.get(f"{BASE_PATH}/audit")
    assert audit.status_code == 200
    assert audit.json()["plra_status"] == "parcial"
    assert audit.json()["rows"][0]["base_value"] == "100000.00"
    assert audit.json()["rows"][0]["final_economic_value"] == "100000.00"
    assert audit.json()["rows"][0]["inclusion_status"] == "incluido_passivo"


def test_plra_api_returns_not_found_before_first_run() -> None:
    response = _client().get(BASE_PATH)

    assert response.status_code == 404
    assert response.json()["detail"]["error_code"] == "PLRA_NOT_FOUND"


def test_plra_api_downloads_the_latest_snapshot_workbook() -> None:
    client = _client()
    assert client.post(f"{BASE_PATH}/run").status_code == 200

    response = client.get(f"{BASE_PATH}/export.xlsx")

    assert response.status_code == 200
    assert response.headers["content-type"].startswith(
        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
    assert "capag-plra-analysis-1-2024.xlsx" in response.headers[
        "content-disposition"
    ]
    workbook = load_workbook(BytesIO(response.content))
    assert workbook["plra_resumo"]["G2"].value == "-100000.00"
    assert workbook["plra_memoria"]["K2"].value == "100000.00"


def test_plra_openapi_exposes_governed_paths_and_string_values() -> None:
    schema = create_app().openapi()

    assert "get" in schema["paths"][BASE_PATH.replace("analysis-1", "{analysis_id}").replace("2024", "{year}")]
    assert (
        "post"
        in schema["paths"][
            f"{BASE_PATH.replace('analysis-1', '{analysis_id}').replace('2024', '{year}')}/run"
        ]
    )
    assert (
        "get"
        in schema["paths"][
            f"{BASE_PATH.replace('analysis-1', '{analysis_id}').replace('2024', '{year}')}/audit"
        ]
    )
    assert (
        "get"
        in schema["paths"][
            f"{BASE_PATH.replace('analysis-1', '{analysis_id}').replace('2024', '{year}')}/export.xlsx"
        ]
    )
    response_schema = schema["components"]["schemas"]["PlraCalculationResponse"]
    assert response_schema["properties"]["plra_value"]["type"] == "string"
    audit_schema = schema["components"]["schemas"]["PlraAccountAuditRowResponse"]
    assert audit_schema["properties"]["default_discount_percent"]["anyOf"][0][
        "type"
    ] == "string"


def _client() -> TestClient:
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
            content_hash="sha256:plra-api",
            layout="ECD_9",
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
        session.add_all(
            [
                EcdI050AccountModel(
                    exercise_id=exercise.id,
                    account_code="1725",
                    account_name="Fornecedores nacionais",
                    account_type="A",
                    account_nature="02",
                    level=4,
                    parent_account_code="1700",
                    line_number=2,
                    source_line="|I050|...|",
                ),
                EcdI051ReferenceLinkModel(
                    exercise_id=exercise.id,
                    account_code="1725",
                    reference_code="2.01.01.03.01",
                    line_number=3,
                    source_line="|I051|2.01.01.03.01|",
                ),
                EcdI155BalanceModel(
                    exercise_id=exercise.id,
                    account_code="1725",
                    initial_balance=Decimal("0.00"),
                    initial_balance_indicator="C",
                    debit_amount=Decimal("0.00"),
                    credit_amount=Decimal("100000.00"),
                    final_balance=Decimal("100000.00"),
                    final_balance_indicator="C",
                    line_number=4,
                    source_line="|I155|...|",
                ),
                EcdJ100BalanceRowModel(
                    exercise_id=exercise.id,
                    aggregation_code="1725",
                    aggregation_code_type="D",
                    aggregation_level=1,
                    parent_aggregation_code=None,
                    balance_group="P",
                    description="Fornecedores nacionais",
                    initial_amount=Decimal("0.00"),
                    initial_debit_credit_indicator="C",
                    final_amount=Decimal("100000.00"),
                    final_debit_credit_indicator="C",
                    line_number=5,
                    source_line="|J100|...|",
                ),
            ]
        )
        session.commit()

    app = create_app()

    def override_session():
        with Session(engine) as session:
            yield session

    app.dependency_overrides[get_plra_session] = override_session
    return TestClient(app)
