from datetime import date
from decimal import Decimal

import pytest

from app.assets.methodology import load_dfc_methodology
from app.domain.dfc import (
    CashFlowDirection,
    DfcActivity,
    DfcEntry,
    DfcEntryItem,
    DfcRowStatus,
)
from app.engine.dfc import build_dfc_audit_rows


METHODOLOGY = load_dfc_methodology()


def test_classifies_operational_cash_inflow_by_reference_code() -> None:
    rows = _run(
        _entry(
            _item("cash", "Disponivel", "1.01.01.02.01", "100.00", "D", 2),
            _item("sales", "Venda", "3.01.01.01.01.04", "100.00", "C", 3),
        )
    )

    assert len(rows) == 1
    assert rows[0].cash_flow_direction == CashFlowDirection.INFLOW
    assert rows[0].dfc_activity == DfcActivity.OPERATIONAL
    assert rows[0].dfc_component_code == "recebimentos_clientes"
    assert rows[0].movement_value == Decimal("100.00")
    assert rows[0].included_value == Decimal("100.00")
    assert rows[0].final_status == DfcRowStatus.INCLUDED


def test_classifies_fixed_asset_purchase_as_investment_outflow() -> None:
    rows = _run(
        _entry(
            _item("cash", "Banco", "1.01.01.02.01", "250.00", "C", 2),
            _item("asset", "Maquina", "1.02.03.01.06", "250.00", "D", 3),
        )
    )

    assert rows[0].dfc_activity == DfcActivity.INVESTMENT
    assert rows[0].dfc_component_code == "compra_imobilizado"
    assert rows[0].included_value == Decimal("-250.00")


@pytest.mark.parametrize(
    ("cash_indicator", "loan_indicator", "component", "value"),
    [
        ("D", "C", "captacao_emprestimos", Decimal("500.00")),
        ("C", "D", "amortizacao_principal", Decimal("-500.00")),
    ],
)
def test_classifies_loan_flow_by_cash_direction(
    cash_indicator: str,
    loan_indicator: str,
    component: str,
    value: Decimal,
) -> None:
    rows = _run(
        _entry(
            _item("cash", "Banco", "1.01.01.02.01", "500.00", cash_indicator, 2),
            _item(
                "loan",
                "Emprestimo",
                "2.02.01.01.06",
                "500.00",
                loan_indicator,
                3,
            ),
        )
    )

    assert rows[0].dfc_activity == DfcActivity.FINANCING
    assert rows[0].dfc_component_code == component
    assert rows[0].included_value == value


def test_ignores_entry_without_cash_even_when_account_name_mentions_cash() -> None:
    rows = _run(
        _entry(
            _item("fake", "CAIXA LIVRE", "1.01.02.02.01", "10.00", "D", 2),
            _item("sales", "Venda", "3.01.01.01.01.04", "10.00", "C", 3),
        )
    )

    assert rows == ()


def test_keeps_unknown_reference_auditable_without_including_value() -> None:
    rows = _run(
        _entry(
            _item("cash", "Banco", "1.01.01.02.01", "10.00", "D", 2),
            _item("unknown", "Outros", "1.01.02.03.02", "10.00", "C", 3),
        )
    )

    assert rows[0].final_status == DfcRowStatus.UNCLASSIFIED
    assert rows[0].pending_reason == "codigo_referencial_sem_regra_dfc"
    assert rows[0].included_value == Decimal("0.00")


def test_marks_incompatible_direction_without_including_value() -> None:
    rows = _run(
        _entry(
            _item("cash", "Banco", "1.01.01.02.01", "10.00", "C", 2),
            _item("customer", "Cliente", "1.01.02.02.01", "10.00", "D", 3),
        )
    )

    assert rows[0].final_status == DfcRowStatus.INCOMPATIBLE_FLOW
    assert rows[0].pending_reason == "direcao_incompativel_com_regra_dfc"
    assert rows[0].included_value == Decimal("0.00")


def test_excludes_internal_transfer_between_cash_accounts_once() -> None:
    rows = _run(
        _entry(
            _item("cash-a", "Banco A", "1.01.01.02.01", "75.00", "C", 2),
            _item("cash-b", "Banco B", "1.01.01.02.01", "75.00", "D", 3),
        )
    )

    assert len(rows) == 1
    assert rows[0].final_status == DfcRowStatus.EXCLUDED
    assert rows[0].pending_reason == "transferencia_entre_disponibilidades"
    assert rows[0].included_value == Decimal("0.00")


def _run(*entries: DfcEntry):
    return build_dfc_audit_rows(tuple(entries), METHODOLOGY, year=2024)


def _entry(*items: DfcEntryItem) -> DfcEntry:
    return DfcEntry(
        entry_number="LCTO-1",
        entry_date=date(2024, 1, 31),
        items=tuple(items),
    )


def _item(
    code: str,
    name: str,
    reference: str | None,
    amount: str,
    indicator: str,
    line: int,
) -> DfcEntryItem:
    return DfcEntryItem(
        account_code=code,
        account_name=name,
        reference_code=reference,
        amount=Decimal(amount),
        debit_credit_indicator=indicator,
        history="Historico",
        line_number=line,
    )
