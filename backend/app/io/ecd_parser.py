from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date
from decimal import Decimal, InvalidOperation
from pathlib import Path


class EcdParseError(ValueError):
    pass


@dataclass(frozen=True)
class ParsedLine:
    line_number: int
    source_line: str


@dataclass(frozen=True)
class ParsedEcdHeader(ParsedLine):
    layout: str
    period_start: date
    period_end: date
    legal_name: str
    tax_id: str


@dataclass(frozen=True)
class ParsedI050Account(ParsedLine):
    account_code: str
    account_name: str
    account_type: str | None
    account_nature: str | None
    level: int | None
    parent_account_code: str | None


@dataclass(frozen=True)
class ParsedI051ReferenceLink(ParsedLine):
    account_code: str
    reference_code: str


@dataclass(frozen=True)
class ParsedI155Balance(ParsedLine):
    account_code: str
    initial_balance: Decimal
    initial_balance_indicator: str
    debit_amount: Decimal
    credit_amount: Decimal
    final_balance: Decimal
    final_balance_indicator: str


@dataclass(frozen=True)
class ParsedI200Entry(ParsedLine):
    entry_number: str
    entry_date: date | None
    total_amount: Decimal | None
    items: list[ParsedI250EntryItem] = field(default_factory=list)


@dataclass(frozen=True)
class ParsedI250EntryItem(ParsedLine):
    entry_number: str
    account_code: str
    counterparty_account_code: str | None
    amount: Decimal
    debit_credit_indicator: str | None
    history: str | None


@dataclass(frozen=True)
class ParsedJ100BalanceRow(ParsedLine):
    account_code: str | None
    description: str
    amount: Decimal
    amount_indicator: str | None


@dataclass(frozen=True)
class ParsedEcd:
    header: ParsedEcdHeader
    accounts_i050: list[ParsedI050Account]
    reference_links_i051: list[ParsedI051ReferenceLink]
    balances_i155: list[ParsedI155Balance]
    entries_i200: list[ParsedI200Entry]
    items_i250: list[ParsedI250EntryItem]
    j100_rows: list[ParsedJ100BalanceRow]


def parse_ecd_file(path: Path) -> ParsedEcd:
    raw = path.read_bytes()
    return parse_ecd_bytes(raw)


def parse_ecd_bytes(raw: bytes) -> ParsedEcd:
    for encoding in ("utf-8-sig", "latin-1"):
        try:
            return parse_ecd_text(raw.decode(encoding))
        except UnicodeDecodeError:
            continue

    raise EcdParseError("Unable to decode ECD file with supported encodings.")


def parse_ecd_text(content: str) -> ParsedEcd:
    header: ParsedEcdHeader | None = None
    accounts: list[ParsedI050Account] = []
    reference_links: list[ParsedI051ReferenceLink] = []
    balances: list[ParsedI155Balance] = []
    entries: list[ParsedI200Entry] = []
    items: list[ParsedI250EntryItem] = []
    j100_rows: list[ParsedJ100BalanceRow] = []

    current_account_code: str | None = None
    current_entry_number: str | None = None

    for line_number, raw_line in enumerate(content.splitlines(), start=1):
        source_line = raw_line.strip()
        if source_line == "":
            continue

        fields = _split_ecd_line(source_line)
        record_type = fields[0]

        if record_type == "0000":
            header = _parse_header(fields, line_number, source_line)
        elif record_type == "I050":
            account = _parse_i050(fields, line_number, source_line)
            accounts.append(account)
            current_account_code = account.account_code
        elif record_type == "I051":
            if current_account_code is None:
                raise EcdParseError(f"I051 without previous I050 at line {line_number}.")
            reference_links.append(_parse_i051(fields, current_account_code, line_number, source_line))
        elif record_type == "I155":
            balances.append(_parse_i155(fields, line_number, source_line))
        elif record_type == "I200":
            entry = _parse_i200(fields, line_number, source_line)
            entries.append(entry)
            current_entry_number = entry.entry_number
        elif record_type == "I250":
            if current_entry_number is None:
                raise EcdParseError(f"I250 without previous I200 at line {line_number}.")
            items.append(_parse_i250(fields, current_entry_number, line_number, source_line))
        elif record_type == "J100":
            j100_rows.append(_parse_j100(fields, line_number, source_line))

    if header is None:
        raise EcdParseError("ECD header record 0000 not found.")

    entries_with_items = [
        ParsedI200Entry(
            line_number=entry.line_number,
            source_line=entry.source_line,
            entry_number=entry.entry_number,
            entry_date=entry.entry_date,
            total_amount=entry.total_amount,
            items=[item for item in items if item.entry_number == entry.entry_number],
        )
        for entry in entries
    ]

    return ParsedEcd(
        header=header,
        accounts_i050=accounts,
        reference_links_i051=reference_links,
        balances_i155=balances,
        entries_i200=entries_with_items,
        items_i250=items,
        j100_rows=j100_rows,
    )


def _split_ecd_line(source_line: str) -> list[str]:
    fields = source_line.split("|")
    if fields and fields[0] == "":
        fields = fields[1:]
    if fields and fields[-1] == "":
        fields = fields[:-1]
    if not fields:
        raise EcdParseError("Empty ECD record.")
    return fields


def _parse_header(fields: list[str], line_number: int, source_line: str) -> ParsedEcdHeader:
    _require_fields(fields, 6, line_number)
    return ParsedEcdHeader(
        line_number=line_number,
        source_line=source_line,
        layout=fields[1],
        period_start=_parse_date(fields[2], line_number),
        period_end=_parse_date(fields[3], line_number),
        legal_name=fields[4],
        tax_id=fields[5],
    )


def _parse_i050(fields: list[str], line_number: int, source_line: str) -> ParsedI050Account:
    _require_fields(fields, 8, line_number)
    return ParsedI050Account(
        line_number=line_number,
        source_line=source_line,
        account_type=_none_if_empty(fields[3]),
        account_nature=_none_if_empty(fields[2]),
        level=_parse_int_or_none(fields[4], line_number),
        account_code=fields[5],
        parent_account_code=_none_if_empty(fields[6]),
        account_name=fields[7] if len(fields) > 7 else fields[5],
    )


def _parse_i051(
    fields: list[str],
    current_account_code: str,
    line_number: int,
    source_line: str,
) -> ParsedI051ReferenceLink:
    _require_fields(fields, 2, line_number)
    if len(fields) >= 3:
        account_code = _none_if_empty(fields[1]) or current_account_code
        reference_code = fields[2]
    else:
        account_code = current_account_code
        reference_code = fields[1]
    return ParsedI051ReferenceLink(
        line_number=line_number,
        source_line=source_line,
        account_code=account_code,
        reference_code=reference_code,
    )


def _parse_i155(fields: list[str], line_number: int, source_line: str) -> ParsedI155Balance:
    _require_fields(fields, 8, line_number)
    value_offset = 3 if len(fields) >= 9 else 2
    return ParsedI155Balance(
        line_number=line_number,
        source_line=source_line,
        account_code=fields[1],
        initial_balance=_parse_decimal(fields[value_offset], line_number),
        initial_balance_indicator=fields[value_offset + 1],
        debit_amount=_parse_decimal(fields[value_offset + 2], line_number),
        credit_amount=_parse_decimal(fields[value_offset + 3], line_number),
        final_balance=_parse_decimal(fields[value_offset + 4], line_number),
        final_balance_indicator=fields[value_offset + 5],
    )


def _parse_i200(fields: list[str], line_number: int, source_line: str) -> ParsedI200Entry:
    _require_fields(fields, 3, line_number)
    return ParsedI200Entry(
        line_number=line_number,
        source_line=source_line,
        entry_number=fields[1],
        entry_date=_parse_date(fields[2], line_number) if fields[2] else None,
        total_amount=_parse_decimal(fields[3], line_number) if len(fields) > 3 and fields[3] else None,
    )


def _parse_i250(
    fields: list[str],
    current_entry_number: str,
    line_number: int,
    source_line: str,
) -> ParsedI250EntryItem:
    _require_fields(fields, 4, line_number)
    return ParsedI250EntryItem(
        line_number=line_number,
        source_line=source_line,
        entry_number=current_entry_number,
        account_code=fields[1],
        counterparty_account_code=_none_if_empty(fields[2]),
        amount=_parse_decimal(fields[3], line_number),
        debit_credit_indicator=_none_if_empty(fields[4]) if len(fields) > 4 else None,
        history=_none_if_empty(fields[5]) if len(fields) > 5 else None,
    )


def _parse_j100(fields: list[str], line_number: int, source_line: str) -> ParsedJ100BalanceRow:
    _require_fields(fields, 4, line_number)
    if len(fields) >= 10:
        return ParsedJ100BalanceRow(
            line_number=line_number,
            source_line=source_line,
            account_code=_none_if_empty(fields[1]),
            description=fields[6],
            amount=_parse_decimal(fields[7], line_number),
            amount_indicator=_none_if_empty(fields[8]),
        )

    return ParsedJ100BalanceRow(
        line_number=line_number,
        source_line=source_line,
        account_code=_none_if_empty(fields[1]),
        description=fields[2],
        amount=_parse_decimal(fields[3], line_number),
        amount_indicator=_none_if_empty(fields[4]) if len(fields) > 4 else None,
    )


def _require_fields(fields: list[str], minimum: int, line_number: int) -> None:
    if len(fields) < minimum:
        raise EcdParseError(f"Record {fields[0]} at line {line_number} has too few fields.")


def _parse_decimal(raw_value: str, line_number: int) -> Decimal:
    normalized = raw_value.strip().replace(".", "").replace(",", ".")
    try:
        return Decimal(normalized)
    except InvalidOperation as exc:
        raise EcdParseError(f"Invalid decimal value at line {line_number}.") from exc


def _parse_date(raw_value: str, line_number: int) -> date:
    if len(raw_value) != 8:
        raise EcdParseError(f"Invalid date value at line {line_number}.")
    try:
        day = int(raw_value[0:2])
        month = int(raw_value[2:4])
        year = int(raw_value[4:8])
        return date(year, month, day)
    except ValueError as exc:
        raise EcdParseError(f"Invalid date value at line {line_number}.") from exc


def _parse_int_or_none(raw_value: str, line_number: int) -> int | None:
    value = _none_if_empty(raw_value)
    if value is None:
        return None
    try:
        return int(value)
    except ValueError as exc:
        raise EcdParseError(f"Invalid integer value at line {line_number}.") from exc


def _none_if_empty(raw_value: str) -> str | None:
    value = raw_value.strip()
    return value if value else None
