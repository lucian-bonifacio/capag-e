from pathlib import Path

from fastapi.testclient import TestClient
from sqlalchemy import select
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool

from app.api.imports import get_import_session
from app.application import run_declared_layer
from app.engine.methodology_matcher import MethodologyRule, OfficialReferenceAccount, RuleStatus
from app.main import app
from app.repositories import (
    AnalysisModel,
    Base,
    DeclaredAccountSnapshot,
    EcdFileModel,
    EcdI050AccountModel,
)


FIXTURES_DIR = Path(__file__).parent / "fixtures" / "ecd"


def test_import_ecd_endpoint_creates_analysis_without_exposing_raw_content() -> None:
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(engine)
    SessionForTest = sessionmaker(bind=engine)

    def override_session():
        session = SessionForTest()
        try:
            yield session
        finally:
            session.close()

    app.dependency_overrides[get_import_session] = override_session
    client = TestClient(app)

    content = (FIXTURES_DIR / "valid_declared.ecd").read_bytes()
    response = client.post(
        "/api/v1/ecd/import",
        data={"methodology_version_id": "metodologia-2024.1"},
        files={"file": ("valid_declared.ecd", content, "text/plain")},
    )

    app.dependency_overrides.clear()
    assert response.status_code == 201
    payload = response.json()
    assert payload["analysis_id"].startswith("analysis-")
    assert payload["year"] == 2024
    assert payload["status"] == "nao_executado"
    assert payload["parser_version"] == "2.1.0"
    assert "Lancamento sintetico" not in response.text

    with Session(engine) as session:
        stored_analysis = session.get(AnalysisModel, payload["analysis_id"])
        stored_file = session.get(EcdFileModel, payload["ecd_file_id"])

    assert stored_analysis is not None
    assert stored_file is not None
    assert stored_file.original_content == content


def test_import_ecd_endpoint_rejects_invalid_extension() -> None:
    client = TestClient(app)

    response = client.post(
        "/api/v1/ecd/import",
        files={"file": ("invalid.csv", b"conteudo", "text/csv")},
    )

    assert response.status_code == 400
    assert response.json()["detail"]["error_code"] == "ECD_INVALID_FILENAME"


def test_import_ecd_endpoint_reports_existing_import_without_reimporting() -> None:
    engine, SessionForTest = _create_test_database()
    app.dependency_overrides[get_import_session] = _override_session(SessionForTest)
    client = TestClient(app)
    content = (FIXTURES_DIR / "valid_declared.ecd").read_bytes()

    first_response = _post_valid_import(client, content)
    second_response = _post_valid_import(client, content)

    app.dependency_overrides.clear()
    assert first_response.status_code == 201
    assert second_response.status_code == 409
    payload = second_response.json()["detail"]
    assert payload["error_code"] == "ECD_ALREADY_IMPORTED"
    assert payload["message"] == "Este arquivo ECD ja foi importado."
    assert payload["existing_import"]["analysis_id"] == first_response.json()["analysis_id"]

    with Session(engine) as session:
        assert len(list(session.scalars(select(AnalysisModel)))) == 1


def test_import_ecd_endpoint_rejects_balance_ineligible_ecd_without_persisting() -> None:
    engine, SessionForTest = _create_test_database()
    app.dependency_overrides[get_import_session] = _override_session(SessionForTest)
    client = TestClient(app)
    content = (FIXTURES_DIR / "balance_declared_required_absent.ecd").read_bytes()

    response = client.post(
        "/api/v1/ecd/import",
        data={"methodology_version_id": "metodologia-2024.1"},
        files={
            "file": (
                "balance_declared_required_absent.ecd",
                content,
                "text/plain",
            )
        },
    )

    app.dependency_overrides.clear()
    assert response.status_code == 400
    payload = response.json()["detail"]
    assert payload["error_code"] == "ECD_BALANCE_OBRIGATORIO_AUSENTE"
    assert payload["balance_status"] == "OBRIGATORIO_AUSENTE"
    assert payload["limitations"] == ["J100_OBRIGATORIO_AUSENTE"]
    assert "ECD rejeitada" in payload["message"]

    with Session(engine) as session:
        assert list(session.scalars(select(AnalysisModel))) == []
        assert list(session.scalars(select(EcdFileModel))) == []


def test_list_and_remove_existing_ecd_import_then_reimport() -> None:
    engine, SessionForTest = _create_test_database()
    app.dependency_overrides[get_import_session] = _override_session(SessionForTest)
    client = TestClient(app)
    content = (FIXTURES_DIR / "valid_declared.ecd").read_bytes()

    import_response = _post_valid_import(client, content)
    imported = import_response.json()
    with Session(engine) as session:
        run_declared_layer(
            session,
            analysis_id=imported["analysis_id"],
            year=imported["year"],
            official_references=[
                OfficialReferenceAccount(
                    reference_code="2.01.01.07.01",
                    official_description="Emprestimos",
                    parent_reference_code=None,
                    level=5,
                    nature="D",
                    valid_from=2024,
                    valid_to=None,
                    layout="ECD_2024",
                    entity_type="PJ_GERAL",
                    source="test",
                    status="ATIVA",
                    methodology_version_id="metodologia-2024.1",
                )
            ],
            methodology_rules=[
                MethodologyRule(
                    reference_code="2.01.01.07.01",
                    purpose="FCO",
                    methodology_description="Caixa operacional",
                    plra_category=None,
                    fco_category="operacional",
                    capag_category=None,
                    flow_nature="operacional",
                    operational_treatment="incluir",
                    include_in_calculation=True,
                    sign="+",
                    rule_status=RuleStatus.ACTIVE,
                    valid_from=2024,
                    valid_to=None,
                    methodology_version_id="metodologia-2024.1",
                )
            ],
        )

    list_response = client.get("/api/v1/ecd/imports")
    assert list_response.status_code == 200
    assert list_response.json()["imports"][0]["analysis_id"] == imported["analysis_id"]

    delete_response = client.delete(f"/api/v1/ecd/imports/{imported['ecd_file_id']}")
    assert delete_response.status_code == 200
    assert delete_response.json() == {
        "ecd_file_id": imported["ecd_file_id"],
        "analysis_id": imported["analysis_id"],
        "deleted": True,
    }

    with Session(engine) as session:
        assert session.get(AnalysisModel, imported["analysis_id"]) is None
        assert session.get(EcdFileModel, imported["ecd_file_id"]) is None
        assert list(session.scalars(select(EcdI050AccountModel))) == []
        assert list(session.scalars(select(DeclaredAccountSnapshot))) == []

    reimport_response = _post_valid_import(client, content)
    app.dependency_overrides.clear()
    assert reimport_response.status_code == 201
    assert reimport_response.json()["analysis_id"] == imported["analysis_id"]


def _create_test_database():
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(engine)
    return engine, sessionmaker(bind=engine)


def _override_session(SessionForTest):
    def override_session():
        session = SessionForTest()
        try:
            yield session
        finally:
            session.close()

    return override_session


def _post_valid_import(client: TestClient, content: bytes):
    return client.post(
        "/api/v1/ecd/import",
        data={"methodology_version_id": "metodologia-2024.1"},
        files={"file": ("valid_declared.ecd", content, "text/plain")},
    )
