from decimal import Decimal

from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session

from app.domain import DeclaredAccountResult
from app.application.declared_service import SqlAlchemyDeclaredSnapshotReader
from app.engine.methodology_matcher import (
    MatchRequest,
    MethodologyRule,
    OfficialReferenceAccount,
    RuleStatus,
    match_declared_methodology,
)
from app.repositories import Base, DeclaredAccountSnapshot, add_declared_account_snapshot


def test_declared_account_snapshot_persists_methodology_version_and_status() -> None:
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    result = _declared_result()

    with Session(engine) as session:
        snapshot = add_declared_account_snapshot(
            session,
            analysis_id="analysis-1",
            exercise_year=2024,
            result=result,
        )
        session.commit()
        snapshot_id = snapshot.id

    with Session(engine) as session:
        stored = session.get(DeclaredAccountSnapshot, snapshot_id)

    assert stored is not None
    assert stored.analysis_id == "analysis-1"
    assert stored.exercise_year == 2024
    assert stored.account_code == "1725"
    assert stored.declared_reference_code == "2.01.01.07.01"
    assert stored.methodology_version_id == "test-version"
    assert stored.final_status == "MAPEADO"
    assert stored.observation is None
    assert stored.snapshot_json["methodology_version_id"] == "test-version"


def test_declared_account_snapshot_keeps_multiple_runs_without_overwriting() -> None:
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)

    with Session(engine) as session:
        add_declared_account_snapshot(
            session,
            analysis_id="analysis-1",
            exercise_year=2024,
            result=_declared_result(methodology_version_id="version-1"),
        )
        add_declared_account_snapshot(
            session,
            analysis_id="analysis-1",
            exercise_year=2024,
            result=_declared_result(methodology_version_id="version-2"),
        )
        session.commit()

        stored_versions = session.scalars(
            select(DeclaredAccountSnapshot.methodology_version_id).order_by(
                DeclaredAccountSnapshot.id
            )
        ).all()

    assert stored_versions == ["version-1", "version-2"]


def test_sqlalchemy_declared_snapshot_reader_returns_summary_and_accounts() -> None:
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)

    with Session(engine) as session:
        add_declared_account_snapshot(
            session,
            analysis_id="analysis-1",
            exercise_year=2024,
            result=_declared_result(methodology_version_id="version-1"),
        )
        session.commit()

        reader = SqlAlchemyDeclaredSnapshotReader(session)
        summary = reader.get_summary(analysis_id="analysis-1", year=2024)
        accounts = reader.list_accounts(analysis_id="analysis-1", year=2024)

    assert summary.total_accounts == 1
    assert summary.status_counts == {"MAPEADO": 1}
    assert summary.methodology_version_id == "version-1"
    assert accounts[0].account_code == "1725"
    assert accounts[0].base_value == Decimal("100000.00")


def _declared_result(methodology_version_id: str = "test-version") -> DeclaredAccountResult:
    match_result = match_declared_methodology(
        request=MatchRequest(
            reference_code="2.01.01.07.01",
            year=2024,
            layout="ECD_2024",
            entity_type="PJ_GERAL",
            purpose="FCO",
        ),
        official_references=[
            OfficialReferenceAccount(
                reference_code="2.01.01.07.01",
                official_description="Descricao oficial de teste",
                parent_reference_code=None,
                level=5,
                nature="PASSIVO",
                valid_from=2020,
                valid_to=None,
                layout="ECD_2024",
                entity_type="PJ_GERAL",
                source="fixture_unitaria",
                status="ATIVA",
                methodology_version_id=methodology_version_id,
            )
        ],
        methodology_rules=[
            MethodologyRule(
                reference_code="2.01.01.07.01",
                purpose="FCO",
                methodology_description="Regra de teste sem valor metodologico real.",
                plra_category=None,
                fco_category="categoria_teste",
                capag_category=None,
                flow_nature=None,
                operational_treatment="tratamento_teste",
                include_in_calculation=True,
                sign=None,
                rule_status=RuleStatus.ACTIVE,
                valid_from=2020,
                valid_to=None,
                methodology_version_id=methodology_version_id,
                observation=None,
            )
        ],
    )
    return DeclaredAccountResult.from_match(
        account_code="1725",
        account_name="Conta de teste",
        declared_reference_code="2.01.01.07.01",
        purpose="FCO",
        base_value=Decimal("100000.00"),
        considered_value=Decimal("0.00"),
        methodology_version_id=methodology_version_id,
        match_result=match_result,
    )
