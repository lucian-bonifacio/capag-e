from dataclasses import replace
from datetime import date
from decimal import Decimal

import pytest

from app.domain import (
    BalanceAccount,
    BalanceAccountValue,
    BalanceAggregationLink,
    BalanceLineStatus,
    BalanceStatement,
    BalanceStatementRow,
    DeclaredBalanceInput,
    DeclaredBalanceStatus,
)
from app.engine import calculate_declared_balance


def test_valid_balance_is_built_from_j100_and_reconciled_by_i052_i155() -> None:
    result = calculate_declared_balance(_valid_input())

    assert result.status == DeclaredBalanceStatus.VALIDO
    assert result.is_blocking is False
    assert result.assets_final_amount == Decimal("800.00")
    assert result.liabilities_and_equity_final_amount == Decimal("800.00")
    assert result.difference == Decimal("0.00")
    assert [row.aggregation_code for row in result.rows] == ["A", "P"]
    asset_detail = result.rows[0].children[0]
    assert asset_detail.reconciliation_status == BalanceLineStatus.CONCILIADA
    assert asset_detail.reconciled_amount == Decimal("800.00")
    assert asset_detail.difference == Decimal("0.00")
    assert asset_detail.components[0].account_code == "100"


def test_debit_credit_signs_are_normalized_and_difference_is_exact() -> None:
    source = _valid_input()
    values = tuple(
        replace(value, final_amount=Decimal("799.99"))
        if value.account_code == "100"
        else value
        for value in source.account_values
    )

    result = calculate_declared_balance(replace(source, account_values=values))

    asset_detail = result.rows[0].children[0]
    liability_detail = result.rows[1].children[0]
    assert result.status == DeclaredBalanceStatus.DIVERGENTE
    assert asset_detail.difference == Decimal("0.01")
    assert liability_detail.signed_final_amount == Decimal("-800.00")
    assert liability_detail.reconciled_amount == Decimal("-800.00")


def test_detail_without_i052_is_auditable_and_divergent() -> None:
    source = _valid_input()
    links = tuple(
        link for link in source.aggregation_links if link.aggregation_code != "A.D"
    )

    result = calculate_declared_balance(replace(source, aggregation_links=links))

    asset_detail = result.rows[0].children[0]
    assert result.status == DeclaredBalanceStatus.DIVERGENTE
    assert asset_detail.reconciliation_status == BalanceLineStatus.SEM_I052
    assert asset_detail.component_count == 0


def test_detail_without_matching_i155_preserves_component_evidence() -> None:
    source = _valid_input()
    values = tuple(
        value for value in source.account_values if value.account_code != "100"
    )

    result = calculate_declared_balance(replace(source, account_values=values))

    asset_detail = result.rows[0].children[0]
    assert result.status == DeclaredBalanceStatus.DIVERGENTE
    assert asset_detail.reconciliation_status == BalanceLineStatus.SEM_SALDO_I155
    assert asset_detail.components[0].i052_line_number == 20
    assert asset_detail.components[0].i155_line_number is None


def test_cost_center_must_match_between_i052_and_i155() -> None:
    source = _valid_input()
    values = tuple(
        replace(value, cost_center_code="OUTRO")
        if value.account_code == "100"
        else value
        for value in source.account_values
    )

    result = calculate_declared_balance(replace(source, account_values=values))

    assert (
        result.rows[0].children[0].reconciliation_status
        == BalanceLineStatus.SEM_SALDO_I155
    )


def test_invalid_totalizer_and_unbalanced_sides_invalidate_structure() -> None:
    source = _valid_input()
    statement = source.statements[0]
    rows = tuple(
        replace(row, final_amount=Decimal("900.00"))
        if row.aggregation_code == "A"
        else row
        for row in statement.rows
    )

    result = calculate_declared_balance(
        replace(source, statements=(replace(statement, rows=rows),))
    )

    assert result.status == DeclaredBalanceStatus.ESTRUTURA_INVALIDA
    assert "J100_TOTALIZADOR_DIVERGENTE_A" in result.limitations
    assert "J100_LADOS_DIVERGENTES" in result.limitations


def test_multiple_applicable_j005_is_rejected_without_silent_choice() -> None:
    source = _valid_input()

    result = calculate_declared_balance(
        replace(source, statements=(source.statements[0], source.statements[0]))
    )

    assert result.status == DeclaredBalanceStatus.ESTRUTURA_INVALIDA
    assert result.limitations == ("MULTIPLOS_J005_APLICAVEIS",)


def test_required_absent_and_not_required_have_distinct_states() -> None:
    required_absent = calculate_declared_balance(
        replace(_valid_input(), statements=())
    )
    not_required = calculate_declared_balance(
        replace(
            _valid_input(),
            closing_dates=(date(2023, 12, 31),),
            statements=(),
        )
    )

    assert required_absent.status == DeclaredBalanceStatus.OBRIGATORIO_AUSENTE
    assert not_required.status == DeclaredBalanceStatus.NAO_OBRIGATORIO


def test_engine_rejects_non_decimal_monetary_values() -> None:
    source = _valid_input()
    invalid_value = replace(source.account_values[0], final_amount=800)  # type: ignore[arg-type]

    with pytest.raises(TypeError, match="Decimal"):
        calculate_declared_balance(
            replace(source, account_values=(invalid_value, *source.account_values[1:]))
        )


def _valid_input() -> DeclaredBalanceInput:
    target = date(2024, 12, 31)
    rows = (
        _row("A", "T", 1, None, "A", "Ativo", "800.00", "D", 30),
        _row("A.D", "D", 2, "A", "A", "Caixa", "800.00", "D", 31),
        _row("P", "T", 1, None, "P", "Passivo e PL", "800.00", "C", 32),
        _row("P.D", "D", 2, "P", "P", "Capital", "800.00", "C", 33),
    )
    return DeclaredBalanceInput(
        year=2024,
        ecd_period_start=date(2024, 1, 1),
        ecd_period_end=target,
        bookkeeping_forms=("G",),
        closing_dates=(target,),
        statements=(
            BalanceStatement(
                period_start=date(2024, 1, 1),
                period_end=target,
                statement_id="1",
                line_number=29,
                has_j150=True,
                rows=rows,
            ),
        ),
        accounts=(
            BalanceAccount("100", "Caixa", "A"),
            BalanceAccount("200", "Capital", "A"),
        ),
        aggregation_links=(
            BalanceAggregationLink("100", "CC01", "A.D", 20),
            BalanceAggregationLink("200", None, "P.D", 21),
        ),
        account_values=(
            BalanceAccountValue("100", "CC01", target, Decimal("800.00"), "D", 25),
            BalanceAccountValue("200", None, target, Decimal("800.00"), "C", 26),
        ),
    )


def _row(
    code: str,
    code_type: str,
    level: int,
    parent: str | None,
    group: str,
    description: str,
    amount: str,
    indicator: str,
    line_number: int,
) -> BalanceStatementRow:
    return BalanceStatementRow(
        aggregation_code=code,
        aggregation_code_type=code_type,
        aggregation_level=level,
        parent_aggregation_code=parent,
        balance_group=group,
        description=description,
        initial_amount=Decimal("0.00"),
        initial_debit_credit_indicator=indicator,
        final_amount=Decimal(amount),
        final_debit_credit_indicator=indicator,
        explanatory_note_reference=None,
        line_number=line_number,
    )
