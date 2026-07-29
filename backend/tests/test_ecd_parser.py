from decimal import Decimal
from pathlib import Path

import pytest

from app.io import EcdParseError, parse_ecd_file, parse_ecd_text


FIXTURES_DIR = Path(__file__).parent / "fixtures" / "ecd"


def test_parser_extracts_minimum_declared_records_from_valid_fixture() -> None:
    parsed = parse_ecd_file(FIXTURES_DIR / "valid_declared.ecd")

    assert parsed.header.layout == "ECD_2024"
    assert parsed.header.tax_id == "00000000000100"
    assert parsed.accounts_i050[0].account_code == "1725"
    assert parsed.reference_links_i051[0].account_code == "1725"
    assert parsed.reference_links_i051[0].reference_code == "2.01.01.07.01"
    assert parsed.balances_i155[0].final_balance == Decimal("100000.00")
    assert parsed.entries_i200[0].entry_number == "LCTO-1"
    assert parsed.entries_i200[0].items[0].amount == Decimal("100000.00")
    assert parsed.j100_rows[0].source_line.startswith("|J100|")


def test_parser_normalizes_official_lecd_marker_to_applicable_layout() -> None:
    parsed = parse_ecd_text(
        "|0000|LECD|01012024|31122024|EMPRESA REAL|00000000000100|"
    )

    assert parsed.header.layout == "ECD_9"


def test_parser_preserves_missing_i051_as_absence_of_reference_link() -> None:
    parsed = parse_ecd_file(FIXTURES_DIR / "missing_i051.ecd")

    assert parsed.accounts_i050[0].account_code == "3001"
    assert parsed.reference_links_i051 == []


def test_parser_keeps_dangerous_prefix_code_exactly_as_declared() -> None:
    parsed = parse_ecd_file(FIXTURES_DIR / "dangerous_prefix.ecd")

    assert parsed.reference_links_i051[0].reference_code == "2.01.01.07.01"


def test_parser_links_i051_with_empty_cost_center_to_previous_account() -> None:
    parsed = parse_ecd_text(
        "\n".join(
            [
                "|0000|ECD_2024|01012024|31122024|EMPRESA SINTETICA|00000000000100|",
                "|I050|01012024|01|A|5|973|972|APURACAO DE RESULTADO - TRANSITORIA|",
                "|I051||3.01.01.09.01.99|",
            ]
        )
    )

    link = parsed.reference_links_i051[0]
    assert link.account_code == "973"
    assert link.reference_code == "3.01.01.09.01.99"


def test_parser_accepts_i155_with_empty_cost_center_field() -> None:
    parsed = parse_ecd_text(
        "\n".join(
            [
                "|0000|ECD_2024|01012024|31122024|EMPRESA SINTETICA|00000000000100|",
                "|I050|01012024|01|A|5|1.1.1.1.01.0001||Banco sintetico|",
                "|I155|1.1.1.1.01.0001||9327,26|D|635202,75|382514,46|262015,55|D|",
            ]
        )
    )

    balance = parsed.balances_i155[0]
    assert balance.account_code == "1.1.1.1.01.0001"
    assert balance.cost_center_code is None
    assert balance.initial_balance == Decimal("9327.26")
    assert balance.debit_amount == Decimal("635202.75")
    assert balance.credit_amount == Decimal("382514.46")
    assert balance.final_balance == Decimal("262015.55")
    assert balance.final_balance_indicator == "D"


def test_parser_accepts_full_j100_balance_row_layout() -> None:
    parsed = parse_ecd_text(
        "\n".join(
            [
                "|0000|ECD_2024|01012024|31122024|EMPRESA SINTETICA|00000000000100|",
                "|J100|1.1.1.1.01.00001|D|6|1.1.1.1.01|A|CAIXA/BANCOS CC/APLIC|9327,26|D|80182,51|D||",
            ]
        )
    )

    row = parsed.j100_rows[0]
    assert row.aggregation_code == "1.1.1.1.01.00001"
    assert row.aggregation_code_type == "D"
    assert row.aggregation_level == 6
    assert row.parent_aggregation_code == "1.1.1.1.01"
    assert row.balance_group == "A"
    assert row.description == "CAIXA/BANCOS CC/APLIC"
    assert row.initial_amount == Decimal("9327.26")
    assert row.initial_debit_credit_indicator == "D"
    assert row.final_amount == Decimal("80182.51")
    assert row.final_debit_credit_indicator == "D"
    assert not hasattr(row, "account_code")


def test_parser_preserves_balance_context_and_all_required_records() -> None:
    parsed = parse_ecd_file(FIXTURES_DIR / "balance_declared_complete.ecd")

    assert parsed.bookkeeping_i010[0].bookkeeping_form == "G"
    assert parsed.book_headers_i030[0].closing_date.isoformat() == "2024-12-31"
    assert parsed.balance_periods_i150[0].period_start.isoformat() == "2024-01-01"
    assert parsed.statements_j005[0].statement_id == "1"
    assert parsed.j150_presence[0].j005_line_number == parsed.statements_j005[0].line_number

    aggregation_link = parsed.aggregation_links_i052[0]
    assert aggregation_link.account_code == "1.01.01.001"
    assert aggregation_link.cost_center_code == "CC01"
    assert aggregation_link.aggregation_code == "AGL-CAIXA"

    balance = parsed.balances_i155[0]
    assert balance.cost_center_code == "CC01"
    assert balance.period_start == parsed.balance_periods_i150[0].period_start
    assert balance.period_end == parsed.balance_periods_i150[0].period_end
    assert balance.i150_line_number == parsed.balance_periods_i150[0].line_number

    row = parsed.j100_rows[1]
    assert row.aggregation_code == "AGL-CAIXA"
    assert row.j005_line_number == parsed.statements_j005[0].line_number
    assert row.initial_amount == Decimal("100.00")
    assert row.final_amount == Decimal("800.00")
    assert row.explanatory_note_reference == "N1"


def test_parser_reads_closing_date_from_full_official_i030_layout() -> None:
    parsed = parse_ecd_text(
        "\n".join(
            [
                "|0000|LECD|01012024|31122024|EMPRESA SINTETICA|00000000000100|",
                "|I030|TERMO DE ABERTURA|4|LIVRO DIARIO|100|EMPRESA SINTETICA|"
                "123|00000000000100|01012020||SAO PAULO|31122024|",
            ]
        )
    )

    assert parsed.book_headers_i030[0].closing_date.isoformat() == "2024-12-31"


def test_parser_rejects_i051_without_account_context() -> None:
    with pytest.raises(EcdParseError, match="I051 without previous I050"):
        parse_ecd_text(
            "\n".join(
                [
                    "|0000|ECD_2024|01012024|31122024|EMPRESA SINTETICA|00000000000100|",
                    "|I051|2.01.01.07.01|",
                ]
            )
        )
