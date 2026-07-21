from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from app.application import EcdImportIdentifiers, persist_parsed_ecd, run_declared_layer
from app.application.declared_service import SqlAlchemyDeclaredSnapshotReader
from app.engine.methodology_matcher import MethodologyRule, OfficialReferenceAccount, RuleStatus
from app.io import parse_ecd_file
from app.repositories import Base


FIXTURES_DIR = Path(__file__).parent / "fixtures" / "ecd"


def test_run_declared_layer_creates_snapshots_from_imported_ecd() -> None:
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)

    with Session(engine) as session:
        persist_parsed_ecd(
            session,
            parsed_ecd=parse_ecd_file(FIXTURES_DIR / "valid_declared.ecd"),
            identifiers=_identifiers(),
        )
        result = run_declared_layer(
            session,
            analysis_id="analysis-1",
            year=2024,
            official_references=[_official("2.01.01.07.01")],
            methodology_rules=[_rule("2.01.01.07.01")],
        )
        reader = SqlAlchemyDeclaredSnapshotReader(session)
        accounts = reader.list_accounts(analysis_id="analysis-1", year=2024)

    assert result.snapshots_created == 1
    assert result.status_counts == {"MAPEADO": 1}
    assert accounts[0].account_code == "1725"
    assert accounts[0].account_type == "A"
    assert accounts[0].account_level == 4
    assert accounts[0].parent_account_code == "1700"
    assert accounts[0].account_order is not None
    assert accounts[0].final_status == "MAPEADO"


def test_run_declared_layer_maps_missing_i051_to_specific_status() -> None:
    result = _run_fixture("missing_i051.ecd", "analysis-sem-i051")

    assert result.status_counts == {"SEM_VINCULO_REFERENCIAL": 1}


def test_run_declared_layer_maps_missing_official_reference_to_specific_status() -> None:
    result = _run_fixture(
        "official_reference_missing.ecd",
        "analysis-ref-ausente",
        methodology_rules=[_rule("9.99.99.99.99")],
    )

    assert result.status_counts == {"COD_CTA_REF_NAO_ENCONTRADO_NA_TABELA_OFICIAL": 1}


def test_run_declared_layer_maps_missing_methodology_to_specific_status() -> None:
    result = _run_fixture(
        "methodology_missing.ecd",
        "analysis-metodo-ausente",
        official_references=[_official("1.01.02.03.04")],
    )

    assert result.status_counts == {"NAO_MAPEADO_METODOLOGICAMENTE": 1}


def test_run_declared_layer_maps_blocked_rule_to_specific_status() -> None:
    result = _run_fixture(
        "blocked_rule.ecd",
        "analysis-bloqueada",
        official_references=[_official("2.99.99.99.99")],
        methodology_rules=[_rule("2.99.99.99.99", rule_status=RuleStatus.BLOCKED)],
    )

    assert result.status_counts == {"REGRA_BLOQUEADA": 1}


def test_run_declared_layer_does_not_classify_dangerous_prefix_rule() -> None:
    result = _run_fixture(
        "dangerous_prefix.ecd",
        "analysis-prefixo",
        official_references=[_official("2.01.01.07.01")],
        methodology_rules=[_rule("2.01.01.*")],
    )

    assert result.status_counts == {"NAO_MAPEADO_METODOLOGICAMENTE": 1}


def _run_fixture(
    fixture_name: str,
    analysis_id: str,
    official_references: list[OfficialReferenceAccount] | None = None,
    methodology_rules: list[MethodologyRule] | None = None,
):
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    with Session(engine) as session:
        persist_parsed_ecd(
            session,
            parsed_ecd=parse_ecd_file(FIXTURES_DIR / fixture_name),
            identifiers=_identifiers(analysis_id=analysis_id, fixture_name=fixture_name),
        )
        return run_declared_layer(
            session,
            analysis_id=analysis_id,
            year=2024,
            official_references=official_references or [],
            methodology_rules=methodology_rules or [],
        )


def _identifiers(
    analysis_id: str = "analysis-1",
    fixture_name: str = "valid_declared.ecd",
) -> EcdImportIdentifiers:
    return EcdImportIdentifiers(
        company_id=f"company-{analysis_id}",
        ecd_file_id=f"ecd-{analysis_id}",
        analysis_id=analysis_id,
        methodology_version_id="metodologia-2024.1",
        original_filename=fixture_name,
        content_hash=f"sha256:{analysis_id}",
    )


def _official(reference_code: str) -> OfficialReferenceAccount:
    return OfficialReferenceAccount(
        reference_code=reference_code,
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


def _rule(
    reference_code: str,
    rule_status: RuleStatus = RuleStatus.ACTIVE,
) -> MethodologyRule:
    return MethodologyRule(
        reference_code=reference_code,
        purpose="FCO",
        methodology_description="Regra sintetica para teste.",
        plra_category=None,
        fco_category="categoria_sintetica",
        capag_category=None,
        flow_nature=None,
        operational_treatment="tratamento_sintetico",
        include_in_calculation=True,
        sign=None,
        rule_status=rule_status,
        valid_from=2020,
        valid_to=None,
        methodology_version_id="metodologia-2024.1",
        observation=None,
    )
