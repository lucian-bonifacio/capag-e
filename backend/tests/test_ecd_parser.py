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
    assert row.account_code == "1.1.1.1.01.00001"
    assert row.description == "CAIXA/BANCOS CC/APLIC"
    assert row.amount == Decimal("9327.26")
    assert row.amount_indicator == "D"


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
