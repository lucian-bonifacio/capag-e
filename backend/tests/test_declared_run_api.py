from pathlib import Path

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.api.declared import (
    get_declared_run_session,
    get_methodology_rules,
    get_official_references,
)
from app.application import EcdImportIdentifiers, persist_parsed_ecd
from app.engine.methodology_matcher import MethodologyRule, OfficialReferenceAccount, RuleStatus
from app.io import parse_ecd_file
from app.main import app
from app.repositories import Base


FIXTURES_DIR = Path(__file__).parent / "fixtures" / "ecd"


def test_declared_run_endpoint_creates_snapshots_for_imported_analysis() -> None:
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(engine)
    SessionForTest = sessionmaker(bind=engine)
    with SessionForTest() as session:
        persist_parsed_ecd(
            session,
            parsed_ecd=parse_ecd_file(FIXTURES_DIR / "valid_declared.ecd"),
            identifiers=EcdImportIdentifiers(
                company_id="company-api-run",
                ecd_file_id="ecd-api-run",
                analysis_id="analysis-api-run",
                methodology_version_id="metodologia-2024.1",
                original_filename="valid_declared.ecd",
                content_hash="sha256:api-run",
            ),
        )

    def override_session():
        session = SessionForTest()
        try:
            yield session
        finally:
            session.close()

    app.dependency_overrides[get_declared_run_session] = override_session
    app.dependency_overrides[get_official_references] = lambda: [_official()]
    app.dependency_overrides[get_methodology_rules] = lambda: [_rule()]
    client = TestClient(app)

    response = client.post("/api/v1/analyses/analysis-api-run/exercises/2024/declared/run")

    app.dependency_overrides.clear()
    assert response.status_code == 200
    assert response.json()["status_counts"] == {"MAPEADO": 1}
    assert response.json()["snapshots_created"] == 1


def test_declared_run_endpoint_returns_configuration_error_without_official_table() -> None:
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(engine)
    SessionForTest = sessionmaker(bind=engine)
    with SessionForTest() as session:
        persist_parsed_ecd(
            session,
            parsed_ecd=parse_ecd_file(FIXTURES_DIR / "valid_declared.ecd"),
            identifiers=EcdImportIdentifiers(
                company_id="company-api-run-empty-official",
                ecd_file_id="ecd-api-run-empty-official",
                analysis_id="analysis-api-run-empty-official",
                methodology_version_id="metodologia-2024.1",
                original_filename="valid_declared.ecd",
                content_hash="sha256:api-run-empty-official",
            ),
        )

    def override_session():
        session = SessionForTest()
        try:
            yield session
        finally:
            session.close()

    app.dependency_overrides[get_declared_run_session] = override_session
    app.dependency_overrides[get_official_references] = lambda: []
    app.dependency_overrides[get_methodology_rules] = lambda: [_rule()]
    client = TestClient(app)

    response = client.post(
        "/api/v1/analyses/analysis-api-run-empty-official/exercises/2024/declared/run"
    )

    app.dependency_overrides.clear()
    assert response.status_code == 503
    assert response.json()["detail"]["error_code"] == (
        "OFFICIAL_REFERENCE_CONFIGURATION_UNAVAILABLE"
    )


def _official() -> OfficialReferenceAccount:
    return OfficialReferenceAccount(
        reference_code="2.01.01.07.01",
        official_description="Descricao oficial sintetica",
        parent_reference_code=None,
        level=5,
        nature="PASSIVO",
        valid_from=2020,
        valid_to=None,
        layout="ECD_2024",
        entity_type="PJ_GERAL",
        source="fixture_sintetica",
        status="ATIVA",
        methodology_version_id="metodologia-2024.1",
    )


def _rule() -> MethodologyRule:
    return MethodologyRule(
        reference_code="2.01.01.07.01",
        purpose="FCO",
        methodology_description="Regra sintetica para teste.",
        plra_category=None,
        fco_category="categoria_sintetica",
        capag_category=None,
        flow_nature=None,
        operational_treatment="tratamento_sintetico",
        include_in_calculation=True,
        sign=None,
        rule_status=RuleStatus.ACTIVE,
        valid_from=2020,
        valid_to=None,
        methodology_version_id="metodologia-2024.1",
        observation=None,
    )
