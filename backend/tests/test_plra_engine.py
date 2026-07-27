from dataclasses import replace
from datetime import datetime, timezone
from decimal import Decimal

from app.assets.methodology import PlraPolicy, PlraRule, load_plra_policy
from app.domain import ComponentStatus, PlraAccountInput, PlraInclusionStatus
from app.engine import calculate_plra


NOW = datetime(2024, 12, 31, tzinfo=timezone.utc)


def test_calculate_plra_golden_case_with_defaults_and_liabilities() -> None:
    result = calculate_plra(
        analysis_id="analysis",
        exercise_year=2024,
        accounts=[
            _account("cash", "1.01.01.01.01", "ATIVO", "100", "D"),
            _account("clients", "1.01.02.02.01", "ATIVO", "100", "D"),
            _account("stock", "1.01.03.02.01", "ATIVO", "100", "D"),
            _account("tax", "1.01.02.03.02", "ATIVO", "30", "D"),
            _account("supplier", "2.01.01.03.01", "PASSIVO", "50", "C"),
        ],
        policy=load_plra_policy(),
        methodology_version_id="metodologia-2024.1",
        j100_available=True,
        calculated_at=NOW,
    )

    assert result.gross_assets_value == Decimal("300.00")
    assert result.adjusted_assets_value == Decimal("190.00")
    assert result.gross_economic_liabilities_value == Decimal("50.00")
    assert result.plr_gross_value == Decimal("250.00")
    assert result.plra_value == Decimal("140.00")
    assert result.plra_status == ComponentStatus.CALCULATED
    tax_row = next(row for row in result.account_rows if row.account_code == "tax")
    assert tax_row.inclusion_status == PlraInclusionStatus.EXCLUDED
    assert tax_row.final_economic_value == Decimal("0.00")


def test_validated_valuation_replaces_default() -> None:
    result = calculate_plra(
        analysis_id="analysis",
        exercise_year=2024,
        accounts=[_account("stock", "1.01.03.02.01", "ATIVO", "100", "D")],
        policy=load_plra_policy(),
        methodology_version_id="metodologia-2024.1",
        validated_valuations={"stock": Decimal("65")},
        calculated_at=NOW,
    )

    row = result.account_rows[0]
    assert row.default_economic_value == Decimal("20.00")
    assert row.final_economic_value == Decimal("65.00")
    assert row.valuation_source == "avaliacao_validada"


def test_parent_and_child_are_not_double_counted() -> None:
    child = _account("child", "1.01.01.01.01", "ATIVO", "100", "D")
    parent = replace(
        _account("parent", "1.01.01.01.01", "ATIVO", "100", "D"),
        account_type="S",
        account_level=4,
    )
    child = replace(child, parent_account_code="parent", account_level=5)

    result = calculate_plra(
        analysis_id="analysis",
        exercise_year=2024,
        accounts=[parent, child],
        policy=load_plra_policy(),
        methodology_version_id="metodologia-2024.1",
        calculated_at=NOW,
    )

    assert result.gross_assets_value == Decimal("100.00")
    assert result.account_rows[0].inclusion_status == PlraInclusionStatus.IGNORED_HIERARCHY


def test_account_without_i051_is_audited_without_blocking() -> None:
    account = replace(
        _account("unlinked", None, None, "25", "D"),
        official_description=None,
    )

    result = calculate_plra(
        analysis_id="analysis",
        exercise_year=2024,
        accounts=[account],
        policy=load_plra_policy(),
        methodology_version_id="metodologia-2024.1",
        calculated_at=NOW,
    )

    assert result.plra_status == ComponentStatus.CALCULATED
    assert result.account_rows[0].inclusion_status == PlraInclusionStatus.NO_REFERENCE


def test_nonzero_patrimonial_account_without_rule_is_partial() -> None:
    result = calculate_plra(
        analysis_id="analysis",
        exercise_year=2024,
        accounts=[_account("uncovered", "1.01.01.01.02", "ATIVO", "25", "D")],
        policy=load_plra_policy(),
        methodology_version_id="metodologia-2024.1",
        calculated_at=NOW,
    )

    assert result.plra_status == ComponentStatus.PARTIAL
    assert result.pending_accounts == ("uncovered",)


def test_conditional_liability_without_decision_blocks() -> None:
    base_policy = load_plra_policy()
    conditional = PlraRule(
        methodology_rule_id="conditional",
        reference_code="2.01.01.03.01",
        methodology_group="fornecedores",
        macrogroup="PASSIVO_EXIGIVEL",
        treatment="PASSIVO_CONDICIONAL",
        default_discount_group=None,
        rule_status="ATIVA",
        valid_from=2024,
        valid_to=None,
        reason="Decisao necessaria.",
    )
    policy = PlraPolicy(
        methodology_version_id=base_policy.methodology_version_id,
        status=base_policy.status,
        source=base_policy.source,
        default_discounts=base_policy.default_discounts,
        rules=(conditional,),
    )

    result = calculate_plra(
        analysis_id="analysis",
        exercise_year=2024,
        accounts=[_account("conditional", "2.01.01.03.01", "PASSIVO", "50", "C")],
        policy=policy,
        methodology_version_id="metodologia-2024.1",
        calculated_at=NOW,
    )

    assert result.plra_status == ComponentStatus.BLOCKED_BY_PENDING
    assert result.pending_accounts == ("conditional",)


def test_critical_evidence_blocks_but_preserves_value() -> None:
    result = calculate_plra(
        analysis_id="analysis",
        exercise_year=2024,
        accounts=[_account("stock", "1.01.03.02.01", "ATIVO", "100", "D")],
        policy=load_plra_policy(),
        methodology_version_id="metodologia-2024.1",
        evidence_statuses={"stock": "pendente_critica"},
        calculated_at=NOW,
    )

    assert result.plra_value == Decimal("20.00")
    assert result.plra_status == ComponentStatus.BLOCKED_BY_EVIDENCE


def test_credit_balance_reduces_asset_and_debit_balance_reduces_liability() -> None:
    result = calculate_plra(
        analysis_id="analysis",
        exercise_year=2024,
        accounts=[
            _account("depreciation", "1.02.03.01.30", "ATIVO", "20", "C"),
            _account("liability_debit", "2.01.01.09.08", "PASSIVO", "5", "D"),
        ],
        policy=load_plra_policy(),
        methodology_version_id="metodologia-2024.1",
        calculated_at=NOW,
    )

    assert result.gross_assets_value == Decimal("-20.00")
    assert result.adjusted_assets_value == Decimal("-4.00")
    assert result.gross_economic_liabilities_value == Decimal("-5.00")
    assert result.plra_value == Decimal("1.00")


def _account(
    code: str,
    reference_code: str | None,
    nature: str | None,
    balance: str,
    indicator: str,
) -> PlraAccountInput:
    return PlraAccountInput(
        account_code=code,
        account_name=f"Conta {code}",
        account_type="A",
        account_level=5,
        parent_account_code=None,
        declared_reference_code=reference_code,
        official_description=f"Referencia {reference_code}" if reference_code else None,
        official_nature=nature,
        final_balance=Decimal(balance),
        final_balance_indicator=indicator,
    )
