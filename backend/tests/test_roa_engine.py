from decimal import Decimal

from app.assets.methodology import load_roa_methodology
from app.domain import ComponentStatus, RoaAccountInput, RoaRowStatus
from app.engine import build_roa_audit_rows, calculate_roa


METHODOLOGY = load_roa_methodology()


def test_calculates_rol_roa_and_natural_movements_without_netting_closures() -> None:
    rows = build_roa_audit_rows(
        (
            _account("sales", "3.01.01.01.01.04", debit="1000", credit="1000"),
            _account("returns", "3.01.01.01.02.01", debit="50", credit="50"),
            _account("taxes", "3.01.01.01.02.04", debit="100", credit="100"),
            _account("cost", "3.01.01.03.01.01", debit="300", credit="300"),
            _account("expense", "3.01.01.07.01.02", debit="200", credit="200"),
            _account("fin-income", "3.01.01.05.01.05", debit="20", credit="20"),
            _account("fin-expense", "3.01.01.09.01.08", debit="10", credit="10"),
            _account("non-op-income", "3.01.01.11.01.02", debit="30", credit="30"),
            _account("non-op-expense", "3.01.01.11.01.05", debit="5", credit="5"),
        ),
        METHODOLOGY,
    )
    calculation = calculate_roa(
        exercise_year=2024,
        audit_rows=rows,
        methodology=METHODOLOGY,
        j150_available=False,
    )

    assert calculation.gross_revenue == Decimal("1000.00")
    assert calculation.deductions == Decimal("50.00")
    assert calculation.revenue_taxes == Decimal("100.00")
    assert calculation.net_operating_revenue == Decimal("850.00")
    assert calculation.operating_costs == Decimal("300.00")
    assert calculation.operating_expenses == Decimal("200.00")
    assert calculation.financial_result == Decimal("10.00")
    assert calculation.non_operating_result == Decimal("25.00")
    assert calculation.roa_preliminary == Decimal("385.00")
    assert calculation.roa_final == Decimal("385.00")
    assert calculation.status == ComponentStatus.CALCULATED
    assert "J150" in calculation.limitations[0]


def test_excludes_income_taxes_without_changing_roa() -> None:
    rows = build_roa_audit_rows(
        (_account("irpj", "3.02.01.01.01.12", debit="100", credit="100"),),
        METHODOLOGY,
    )

    calculation = calculate_roa(
        exercise_year=2024,
        audit_rows=rows,
        methodology=METHODOLOGY,
        j150_available=True,
    )

    assert rows[0].final_status == RoaRowStatus.EXCLUDED
    assert rows[0].signed_value == Decimal("0.00")
    assert calculation.roa_final == Decimal("0.00")
    assert calculation.status == ComponentStatus.CALCULATED


def test_credit_nature_cost_account_reduces_the_cost_block() -> None:
    rows = build_roa_audit_rows(
        (
            RoaAccountInput(
                account_code="ending-inventory",
                account_name="Estoque final",
                reference_code="3.01.01.03.01.01",
                reference_description="Custo dos produtos vendidos",
                debit_amount=Decimal("500"),
                credit_amount=Decimal("500"),
                line_reference=1,
                balance_nature="C",
            ),
        ),
        METHODOLOGY,
    )

    calculation = calculate_roa(
        exercise_year=2024,
        audit_rows=rows,
        methodology=METHODOLOGY,
        j150_available=True,
    )

    assert calculation.audit_rows[0].signed_value == Decimal("500.00")
    assert calculation.operating_costs == Decimal("-500.00")
    assert calculation.roa_final == Decimal("500.00")


def test_blocks_conditional_account_and_keeps_it_out_of_preliminary_roa() -> None:
    rows = build_roa_audit_rows(
        (_account("other-expense", "3.01.01.09.01.99", debit="40"),),
        METHODOLOGY,
    )

    calculation = calculate_roa(
        exercise_year=2024,
        audit_rows=rows,
        methodology=METHODOLOGY,
        j150_available=True,
    )

    assert rows[0].base_value == Decimal("40.00")
    assert rows[0].signed_value == Decimal("0.00")
    assert rows[0].final_status == RoaRowStatus.PENDING_REVIEW
    assert calculation.roa_final == Decimal("0.00")
    assert calculation.status == ComponentStatus.BLOCKED_BY_PENDING
    assert calculation.pending_groups[0].code == "CONTA_ROA_CONDICIONAL"


def test_blocks_eligible_account_without_reference_rule() -> None:
    rows = build_roa_audit_rows(
        (_account("unknown", None, debit="25"),),
        METHODOLOGY,
    )

    calculation = calculate_roa(
        exercise_year=2024,
        audit_rows=rows,
        methodology=METHODOLOGY,
        j150_available=True,
    )

    assert rows[0].final_status == RoaRowStatus.NO_RULE
    assert rows[0].pending_reason == "conta_sem_codigo_referencial"
    assert calculation.status == ComponentStatus.BLOCKED_BY_PENDING


def test_empty_input_is_not_calculated_and_records_j150_limitation() -> None:
    calculation = calculate_roa(
        exercise_year=2024,
        audit_rows=(),
        methodology=METHODOLOGY,
        j150_available=False,
    )

    assert calculation.status == ComponentStatus.NOT_CALCULATED
    assert calculation.roa_final == Decimal("0.00")
    assert len(calculation.limitations) == 2


def _account(
    code: str,
    reference_code: str | None,
    *,
    debit: str = "0",
    credit: str = "0",
) -> RoaAccountInput:
    return RoaAccountInput(
        account_code=code,
        account_name=code,
        reference_code=reference_code,
        reference_description=reference_code,
        debit_amount=Decimal(debit),
        credit_amount=Decimal(credit),
        line_reference=1,
    )
