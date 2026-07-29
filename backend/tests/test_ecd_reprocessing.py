from datetime import date, datetime, timezone
from decimal import Decimal
from hashlib import sha256
from pathlib import Path

from fastapi.testclient import TestClient
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool

from app.api.imports import get_import_session
from app.domain import EcdPreparationStatus, ProcessingStatus
from app.main import app
from app.repositories import (
    AnalysisModel,
    Base,
    CompanyModel,
    EcdFileModel,
    EcdI050AccountModel,
    EcdI052AggregationLinkModel,
    ExerciseModel,
    PlraCalculationModel,
)


FIXTURES_DIR = Path(__file__).parent / "fixtures" / "ecd"


def test_same_hash_reprocesses_legacy_import_and_invalidates_results() -> None:
    engine, SessionForTest = _database()
    raw = (FIXTURES_DIR / "balance_declared_complete.ecd").read_bytes()
    digest = sha256(raw).hexdigest()
    _seed_legacy_import(SessionForTest, content_hash=f"sha256:{digest}")
    app.dependency_overrides[get_import_session] = _override(SessionForTest)

    response = TestClient(app).post(
        "/api/v1/ecd/import",
        files={"file": ("balance_declared_complete.ecd", raw, "text/plain")},
    )

    app.dependency_overrides.clear()
    assert response.status_code == 200
    assert response.json()["reprocessed"] is True
    assert response.json()["analysis_id"] == "analysis-legacy"
    assert response.json()["ecd_file_id"] == "ecd-legacy"

    with Session(engine) as session:
        ecd_file = session.get(EcdFileModel, "ecd-legacy")
        exercise = session.scalar(
            select(ExerciseModel).where(ExerciseModel.analysis_id == "analysis-legacy")
        )
        accounts = session.scalars(select(EcdI050AccountModel)).all()
        links = session.scalars(select(EcdI052AggregationLinkModel)).all()
        plra = session.scalars(select(PlraCalculationModel)).one()

    assert ecd_file is not None
    assert exercise is not None
    assert ecd_file.original_content == raw
    assert ecd_file.parser_version == "2.1.0"
    assert ecd_file.reprocessed_at is not None
    assert (
        ecd_file.preparation_status
        == EcdPreparationStatus.READY_FOR_RECONCILIATION.value
    )
    assert exercise.id == 1
    assert [account.account_code for account in accounts] == ["1.01.01.001"]
    assert links[0].aggregation_code == "AGL-CAIXA"
    assert plra.invalidated_at is not None


def test_invalid_reimport_keeps_legacy_data_untouched() -> None:
    engine, SessionForTest = _database()
    raw = b"|0000|LECD|invalid|"
    digest = sha256(raw).hexdigest()
    _seed_legacy_import(SessionForTest, content_hash=f"sha256:{digest}")
    app.dependency_overrides[get_import_session] = _override(SessionForTest)

    response = TestClient(app).post(
        "/api/v1/ecd/import",
        files={"file": ("invalid.ecd", raw, "text/plain")},
    )

    app.dependency_overrides.clear()
    assert response.status_code == 400
    with Session(engine) as session:
        ecd_file = session.get(EcdFileModel, "ecd-legacy")
        accounts = session.scalars(select(EcdI050AccountModel)).all()

    assert ecd_file is not None
    assert ecd_file.original_content is None
    assert (
        ecd_file.preparation_status
        == EcdPreparationStatus.REIMPORT_REQUIRED.value
    )
    assert [account.account_code for account in accounts] == ["LEGACY"]


def _database():
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(engine)
    return engine, sessionmaker(bind=engine)


def _override(SessionForTest):
    def override_session():
        with SessionForTest() as session:
            yield session

    return override_session


def _seed_legacy_import(SessionForTest, *, content_hash: str) -> None:
    with SessionForTest() as session:
        company = CompanyModel(
            id="company-legacy",
            legal_name="Empresa Balanço",
            tax_id="00000000000100",
        )
        ecd_file = EcdFileModel(
            id="ecd-legacy",
            company=company,
            original_filename="legacy.ecd",
            content_hash=content_hash,
            original_content=None,
            content_size=None,
            parser_version=None,
            preparation_status=EcdPreparationStatus.REIMPORT_REQUIRED.value,
            layout="ECD_9",
            period_start=date(2024, 1, 1),
            period_end=date(2024, 12, 31),
        )
        analysis = AnalysisModel(
            id="analysis-legacy",
            company=company,
            ecd_file=ecd_file,
            methodology_version_id="metodologia-2024.1",
            status=ProcessingStatus.COMPLETED.value,
        )
        exercise = ExerciseModel(
            id=1,
            analysis=analysis,
            year=2024,
            status=ProcessingStatus.COMPLETED.value,
            methodology_version_id="metodologia-2024.1",
        )
        session.add_all([company, ecd_file, analysis, exercise])
        session.flush()
        session.add(
            EcdI050AccountModel(
                exercise=exercise,
                account_code="LEGACY",
                account_name="Conta legada",
                account_type="A",
                account_nature="01",
                level=1,
                parent_account_code=None,
                line_number=1,
                source_line="|I050|LEGACY|",
            )
        )
        session.add(
            PlraCalculationModel(
                exercise_id=exercise.id,
                analysis_id=analysis.id,
                exercise_year=2024,
                gross_assets_value=Decimal("1.00"),
                gross_economic_liabilities_value=Decimal("0.00"),
                adjusted_assets_value=Decimal("1.00"),
                plr_gross_value=Decimal("1.00"),
                plra_value=Decimal("1.00"),
                plra_status="calculado",
                calculation_formula="teste",
                pending_accounts_json=[],
                warnings_json=[],
                limitations_json=[],
                blocking_issues_json=[],
                balance_status="VALIDO",
                methodology_version_id="metodologia-2024.1",
                snapshot_json={},
                calculated_at=datetime(2024, 12, 31, tzinfo=timezone.utc),
            )
        )
        session.commit()
