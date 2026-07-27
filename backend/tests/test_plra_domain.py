from datetime import datetime, timezone
from decimal import Decimal

import pytest

from app.domain import (
    ComponentStatus,
    PlraAccountAuditRow,
    PlraAccountInput,
    PlraCalculation,
    PlraDecisionStatus,
    PlraInclusionStatus,
)


def test_plra_input_rejects_float() -> None:
    with pytest.raises(TypeError, match="Decimal"):
        _input(final_balance=10.0)  # type: ignore[arg-type]


def test_plra_calculation_serializes_decimal_snapshot() -> None:
    row = PlraAccountAuditRow(
        account_code="1",
        account_name="Caixa",
        account_type="A",
        account_level=1,
        parent_account_code=None,
        declared_reference_code="1.01.01.01.01",
        official_description="Caixa Matriz",
        methodology_rule_id="rule",
        methodology_group="caixa",
        macrogroup="ATIVO_REALIZAVEL",
        base_value=Decimal("10"),
        sign="D",
        inclusion_status=PlraInclusionStatus.INCLUDED_ASSET,
        default_discount_percent=Decimal("0"),
        default_economic_value=Decimal("10"),
        valuation_source="default_interno",
        validated_valuation_value=None,
        final_economic_value=Decimal("10"),
        decision_status=PlraDecisionStatus.AUTOMATIC,
        evidence_status=None,
        reason="Default.",
        limitations=(),
        methodology_version_id="metodologia-2024.1",
    )
    calculation = PlraCalculation(
        analysis_id="analysis",
        exercise_year=2024,
        gross_assets_value=Decimal("10"),
        gross_economic_liabilities_value=Decimal("2"),
        adjusted_assets_value=Decimal("10"),
        plr_gross_value=Decimal("8"),
        plra_value=Decimal("8"),
        plra_status=ComponentStatus.CALCULATED,
        calculation_formula="formula",
        account_rows=(row,),
        pending_accounts=(),
        warnings=(),
        limitations=(),
        blocking_issues=(),
        j100_reconciliation_status="disponivel_para_conferencia",
        methodology_version_id="metodologia-2024.1",
        calculated_at=datetime(2024, 12, 31, tzinfo=timezone.utc),
    )

    assert calculation.to_snapshot()["plra_value"] == "8.00"
    assert calculation.to_snapshot()["account_rows"][0]["base_value"] == "10.00"


def _input(*, final_balance: Decimal) -> PlraAccountInput:
    return PlraAccountInput(
        account_code="1",
        account_name="Conta",
        account_type="A",
        account_level=1,
        parent_account_code=None,
        declared_reference_code=None,
        official_description=None,
        official_nature=None,
        final_balance=final_balance,
        final_balance_indicator="D",
    )
