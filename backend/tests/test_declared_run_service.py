from pathlib import Path
from decimal import Decimal

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from app.application import EcdImportIdentifiers, persist_parsed_ecd, run_declared_layer
from app.application.declared_service import SqlAlchemyDeclaredSnapshotReader
from app.engine.methodology_matcher import MethodologyRule, OfficialReferenceAccount, RuleStatus
from app.io import parse_ecd_file, parse_ecd_text
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
    assert accounts[0].account_nature == "01"
    assert accounts[0].account_level == 4
    assert accounts[0].parent_account_code == "1700"
    assert accounts[0].account_order is not None
    assert accounts[0].final_status == "MAPEADO"


def test_balance_accounts_use_j100_values_and_i050_hierarchy() -> None:
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)

    with Session(engine) as session:
        persist_parsed_ecd(
            session,
            parsed_ecd=parse_ecd_text(
                "\n".join(
                    [
                        "|0000|ECD_2024|01012024|31122024|EMPRESA SINTETICA|00000000000100|",
                        "|I050|01012024|01|S|1|1||ATIVO|",
                        "|I155|1|0,00|D|0,00|999,00|999,00|D|",
                        "|I050|01012024|01|S|2|1.1|1|ATIVO CIRCULANTE|",
                        "|I155|1.1|0,00|D|0,00|999,00|999,00|D|",
                        "|I050|01012024|01|S|2|1.2|1|ATIVO NAO CIRCULANTE|",
                        "|I155|1.2|0,00|D|0,00|10,00|10,00|D|",
                        "|I050|01012024|02|S|1|2||PASSIVO|",
                        "|I155|2|0,00|C|0,00|90,00|90,00|C|",
                        "|J100|1|ATIVO|999,00|D|",
                        "|J100|2|PASSIVO|999,00|C|",
                        "|J100|1|ATIVO|100,00|D|",
                        "|J100|1.1|ATIVO CIRCULANTE|100,00|D|",
                        "|J100|2|PASSIVO|100,00|C|",
                        "|J100|9.9|CONTA J100 SEM I050|1,00|D|",
                    ]
                )
            ),
            identifiers=_identifiers(analysis_id="analysis-j100", fixture_name="j100.ecd"),
        )
        run_declared_layer(
            session,
            analysis_id="analysis-j100",
            year=2024,
            official_references=[],
            methodology_rules=[],
        )
        reader = SqlAlchemyDeclaredSnapshotReader(session)
        declared_accounts = reader.list_accounts(analysis_id="analysis-j100", year=2024)
        balance_accounts = reader.list_balance_accounts(analysis_id="analysis-j100", year=2024)
        consistency_warnings = reader.list_balance_consistency_warnings(
            analysis_id="analysis-j100",
            year=2024,
        )

    declared_by_code = {account.account_code: account for account in declared_accounts}
    balance_by_code = {account.account_code: account for account in balance_accounts}

    assert declared_by_code["1.1"].base_value == Decimal("999.00")
    assert len(balance_accounts) == 4
    assert balance_by_code["1.1"].base_value == Decimal("100.00")
    assert balance_by_code["1.1"].account_nature == "01"
    assert balance_by_code["1.1"].account_type == "S"
    assert balance_by_code["1.1"].account_level == 2
    assert balance_by_code["1.1"].parent_account_code == "1"
    assert balance_by_code["2"].base_value == Decimal("100.00")
    assert balance_by_code["2"].account_nature == "02"
    assert {
        (warning.warning_code, warning.account_code)
        for warning in consistency_warnings
    } == {
        ("I050_PATRIMONIAL_SEM_J100", "1.2"),
        ("J100_SEM_I050", "9.9"),
    }


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
