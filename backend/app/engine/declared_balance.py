from __future__ import annotations

from collections import defaultdict
from dataclasses import replace
from datetime import date
from decimal import Decimal, ROUND_HALF_UP

from app.domain.declared_balance import (
    BalanceAccountValue,
    BalanceComponent,
    BalanceLineStatus,
    BalanceRowStructuralStatus,
    BalanceStatement,
    BalanceStatementRow,
    DeclaredBalance,
    DeclaredBalanceInput,
    DeclaredBalanceRow,
    DeclaredBalanceStatus,
)


CENT = Decimal("0.01")
REQUIRED_BOOKKEEPING_FORMS = frozenset({"G", "R", "B"})


def calculate_declared_balance(source: DeclaredBalanceInput) -> DeclaredBalance:
    obligation_error = _obligation_error(source)
    if obligation_error is not None:
        return _empty_result(
            source.year,
            DeclaredBalanceStatus.ESTRUTURA_INVALIDA,
            obligation_error,
        )

    if not _is_block_j_required(source):
        return _empty_result(
            source.year,
            DeclaredBalanceStatus.NAO_OBRIGATORIO,
            "BLOCO_J_NAO_OBRIGATORIO",
        )

    target_end = date(source.year, 12, 31)
    applicable = tuple(
        statement
        for statement in source.statements
        if statement.period_end == target_end and statement.statement_id == "1"
    )
    if not applicable:
        return _empty_result(
            source.year,
            DeclaredBalanceStatus.OBRIGATORIO_AUSENTE,
            "J100_OBRIGATORIO_AUSENTE",
        )
    if len(applicable) > 1:
        return _empty_result(
            source.year,
            DeclaredBalanceStatus.ESTRUTURA_INVALIDA,
            "MULTIPLOS_J005_APLICAVEIS",
        )

    statement = applicable[0]
    if not statement.rows:
        return _empty_result(
            source.year,
            DeclaredBalanceStatus.OBRIGATORIO_AUSENTE,
            "J100_OBRIGATORIO_AUSENTE",
            statement=statement,
        )
    if not statement.has_j150:
        return _empty_result(
            source.year,
            DeclaredBalanceStatus.ESTRUTURA_INVALIDA,
            "J150_OBRIGATORIO_AUSENTE",
            statement=statement,
        )

    return _calculate_statement(source, statement)


def _calculate_statement(
    source: DeclaredBalanceInput,
    statement: BalanceStatement,
) -> DeclaredBalance:
    limitations: list[str] = []
    invalid_codes: set[str] = set()
    rows_by_code: dict[str, BalanceStatementRow] = {}

    for row in statement.rows:
        code = row.aggregation_code
        if not code:
            limitations.append(f"J100_COD_AGL_AUSENTE_LINHA_{row.line_number}")
            continue
        if code in rows_by_code:
            limitations.append(f"J100_COD_AGL_DUPLICADO_{code}")
            invalid_codes.add(code)
            continue
        rows_by_code[code] = row

    for code, row in rows_by_code.items():
        if row.aggregation_code_type not in {"T", "D"}:
            limitations.append(f"J100_TIPO_INVALIDO_{code}")
            invalid_codes.add(code)
        if row.aggregation_level is None or row.aggregation_level < 1:
            limitations.append(f"J100_NIVEL_INVALIDO_{code}")
            invalid_codes.add(code)
        if row.balance_group not in {"A", "P"}:
            limitations.append(f"J100_GRUPO_INVALIDO_{code}")
            invalid_codes.add(code)
        if row.final_amount is None:
            limitations.append(f"J100_VALOR_FINAL_AUSENTE_{code}")
            invalid_codes.add(code)
        if row.initial_debit_credit_indicator not in {"D", "C"}:
            limitations.append(f"J100_SINAL_INICIAL_INVALIDO_{code}")
            invalid_codes.add(code)
        if row.final_debit_credit_indicator not in {"D", "C"}:
            limitations.append(f"J100_SINAL_FINAL_INVALIDO_{code}")
            invalid_codes.add(code)

    roots = [
        row
        for row in rows_by_code.values()
        if row.aggregation_level == 1 and row.parent_aggregation_code is None
    ]
    if len(roots) != 2 or {row.balance_group for row in roots} != {"A", "P"}:
        limitations.append("J100_RAIZES_INVALIDAS")
        invalid_codes.update(
            row.aggregation_code for row in roots if row.aggregation_code is not None
        )

    if not any(row.aggregation_code_type == "D" for row in rows_by_code.values()):
        limitations.append("J100_SEM_LINHA_DETALHE")

    children_by_parent: dict[str | None, list[BalanceStatementRow]] = defaultdict(list)
    for code, row in rows_by_code.items():
        if row.aggregation_level == 1:
            if row.parent_aggregation_code is not None:
                limitations.append(f"J100_RAIZ_COM_PAI_{code}")
                invalid_codes.add(code)
            children_by_parent[None].append(row)
            continue

        parent = rows_by_code.get(row.parent_aggregation_code or "")
        if parent is None:
            limitations.append(f"J100_PAI_AUSENTE_{code}")
            invalid_codes.add(code)
            continue
        if (
            row.aggregation_level is None
            or parent.aggregation_level is None
            or row.aggregation_level != parent.aggregation_level + 1
        ):
            limitations.append(f"J100_NIVEL_INCOMPATIVEL_{code}")
            invalid_codes.update({code, parent.aggregation_code or ""})
        if row.balance_group != parent.balance_group:
            limitations.append(f"J100_GRUPO_INCOMPATIVEL_{code}")
            invalid_codes.update({code, parent.aggregation_code or ""})
        children_by_parent[parent.aggregation_code].append(row)

    for code, row in rows_by_code.items():
        children = children_by_parent.get(code, [])
        if row.aggregation_code_type == "D" and children:
            limitations.append(f"J100_DETALHE_COM_FILHOS_{code}")
            invalid_codes.add(code)
        if row.aggregation_code_type != "T":
            continue
        if not children:
            limitations.append(f"J100_TOTALIZADOR_SEM_FILHOS_{code}")
            invalid_codes.add(code)
            continue
        if not _row_can_be_signed(row) or any(not _row_can_be_signed(child) for child in children):
            continue
        child_total = _money(sum((_signed_row_final(child) for child in children), Decimal("0")))
        if _signed_row_final(row) != child_total:
            limitations.append(f"J100_TOTALIZADOR_DIVERGENTE_{code}")
            invalid_codes.add(code)

    accounts = {account.account_code: account for account in source.accounts}
    links_by_aggregation: dict[str, list] = defaultdict(list)
    for link in source.aggregation_links:
        account = accounts.get(link.account_code)
        if account is not None and account.account_type == "A":
            links_by_aggregation[link.aggregation_code].append(link)

    values_by_key: dict[tuple[str, str | None], list[BalanceAccountValue]] = defaultdict(list)
    for value in source.account_values:
        if value.period_end == statement.period_end:
            values_by_key[(value.account_code, value.cost_center_code)].append(value)

    reconciliations: dict[
        str,
        tuple[BalanceLineStatus, Decimal, Decimal, tuple[BalanceComponent, ...]],
    ] = {}
    for code, row in rows_by_code.items():
        if row.aggregation_code_type != "D" or not _row_can_be_signed(row):
            continue
        unique_links = {
            (link.account_code, link.cost_center_code): link
            for link in links_by_aggregation.get(code, [])
        }
        if not unique_links:
            declared = _signed_row_final(row)
            reconciliations[code] = (
                BalanceLineStatus.SEM_I052,
                Decimal("0.00"),
                declared,
                (),
            )
            continue

        components: list[BalanceComponent] = []
        reconciled = Decimal("0.00")
        missing_balance = False
        for key, link in sorted(
            unique_links.items(),
            key=lambda item: (item[1].line_number, item[0][0], item[0][1] or ""),
        ):
            balances = values_by_key.get(key, [])
            account = accounts[link.account_code]
            if not balances:
                missing_balance = True
                components.append(
                    BalanceComponent(
                        account_code=account.account_code,
                        account_name=account.account_name,
                        cost_center_code=link.cost_center_code,
                        final_amount=None,
                        final_debit_credit_indicator=None,
                        signed_final_amount=None,
                        i052_line_number=link.line_number,
                        i155_line_number=None,
                    )
                )
                continue
            for balance in sorted(balances, key=lambda item: item.line_number):
                if balance.final_debit_credit_indicator not in {"D", "C"}:
                    limitations.append(f"I155_SINAL_INVALIDO_LINHA_{balance.line_number}")
                    invalid_codes.add(code)
                    missing_balance = True
                    components.append(
                        BalanceComponent(
                            account_code=account.account_code,
                            account_name=account.account_name,
                            cost_center_code=link.cost_center_code,
                            final_amount=_money(balance.final_amount),
                            final_debit_credit_indicator=(
                                balance.final_debit_credit_indicator
                            ),
                            signed_final_amount=None,
                            i052_line_number=link.line_number,
                            i155_line_number=balance.line_number,
                        )
                    )
                    continue
                signed = _signed(balance.final_amount, balance.final_debit_credit_indicator)
                reconciled = _money(reconciled + signed)
                components.append(
                    BalanceComponent(
                        account_code=account.account_code,
                        account_name=account.account_name,
                        cost_center_code=link.cost_center_code,
                        final_amount=_money(balance.final_amount),
                        final_debit_credit_indicator=balance.final_debit_credit_indicator,
                        signed_final_amount=signed,
                        i052_line_number=link.line_number,
                        i155_line_number=balance.line_number,
                    )
                )

        difference = _money(_signed_row_final(row) - reconciled)
        if missing_balance:
            line_status = BalanceLineStatus.SEM_SALDO_I155
        elif difference == Decimal("0.00"):
            line_status = BalanceLineStatus.CONCILIADA
        else:
            line_status = BalanceLineStatus.DIVERGENTE
        reconciliations[code] = (
            line_status,
            reconciled,
            difference,
            tuple(components),
        )

    roots_output = tuple(
        _build_row(
            row,
            children_by_parent,
            invalid_codes,
            reconciliations,
        )
        for row in sorted(children_by_parent.get(None, []), key=lambda item: item.line_number)
        if _row_can_be_rendered(row)
    )

    asset_root = next((row for row in roots if row.balance_group == "A"), None)
    liability_root = next((row for row in roots if row.balance_group == "P"), None)
    assets = (
        abs(_signed_row_final(asset_root))
        if asset_root is not None and _row_can_be_signed(asset_root)
        else None
    )
    liabilities = (
        abs(_signed_row_final(liability_root))
        if liability_root is not None and _row_can_be_signed(liability_root)
        else None
    )
    side_difference = (
        _money(assets - liabilities)
        if assets is not None and liabilities is not None
        else None
    )
    if side_difference is not None and side_difference != Decimal("0.00"):
        limitations.append("J100_LADOS_DIVERGENTES")
        if asset_root is not None and asset_root.aggregation_code:
            invalid_codes.add(asset_root.aggregation_code)
        if liability_root is not None and liability_root.aggregation_code:
            invalid_codes.add(liability_root.aggregation_code)

    if limitations:
        status = DeclaredBalanceStatus.ESTRUTURA_INVALIDA
    elif any(
        reconciliation[0] != BalanceLineStatus.CONCILIADA
        for reconciliation in reconciliations.values()
    ):
        status = DeclaredBalanceStatus.DIVERGENTE
    else:
        status = DeclaredBalanceStatus.VALIDO

    if invalid_codes:
        roots_output = tuple(_mark_structural_status(row, invalid_codes) for row in roots_output)

    return DeclaredBalance(
        year=source.year,
        status=status,
        is_blocking=status != DeclaredBalanceStatus.VALIDO,
        j005_period_start=statement.period_start,
        j005_period_end=statement.period_end,
        assets_final_amount=_money(assets) if assets is not None else None,
        liabilities_and_equity_final_amount=(
            _money(liabilities) if liabilities is not None else None
        ),
        difference=side_difference,
        rows=roots_output,
        limitations=tuple(dict.fromkeys(limitations)),
    )


def _build_row(
    row: BalanceStatementRow,
    children_by_parent: dict[str | None, list[BalanceStatementRow]],
    invalid_codes: set[str],
    reconciliations: dict[
        str,
        tuple[BalanceLineStatus, Decimal, Decimal, tuple[BalanceComponent, ...]],
    ],
) -> DeclaredBalanceRow:
    code = row.aggregation_code or ""
    reconciliation = reconciliations.get(code)
    components = reconciliation[3] if reconciliation is not None else ()
    return DeclaredBalanceRow(
        aggregation_code=code,
        aggregation_code_type=row.aggregation_code_type or "",
        aggregation_level=row.aggregation_level or 0,
        parent_aggregation_code=row.parent_aggregation_code,
        balance_group=row.balance_group or "",
        description=row.description,
        initial_amount=_money(row.initial_amount),
        initial_debit_credit_indicator=row.initial_debit_credit_indicator or "",
        signed_initial_amount=(
            _signed(row.initial_amount, row.initial_debit_credit_indicator)
            if row.initial_debit_credit_indicator in {"D", "C"}
            else None
        ),
        final_amount=_money(row.final_amount or Decimal("0")),
        final_debit_credit_indicator=row.final_debit_credit_indicator or "",
        signed_final_amount=(
            _signed_row_final(row) if _row_can_be_signed(row) else None
        ),
        explanatory_note_reference=row.explanatory_note_reference,
        line_number=row.line_number,
        structural_status=(
            BalanceRowStructuralStatus.INVALIDA
            if code in invalid_codes
            else BalanceRowStructuralStatus.VALIDA
        ),
        reconciliation_status=reconciliation[0] if reconciliation is not None else None,
        reconciled_amount=reconciliation[1] if reconciliation is not None else None,
        difference=reconciliation[2] if reconciliation is not None else None,
        component_count=len(components),
        components=components,
        children=tuple(
            _build_row(child, children_by_parent, invalid_codes, reconciliations)
            for child in sorted(children_by_parent.get(code, []), key=lambda item: item.line_number)
            if _row_can_be_rendered(child)
        ),
    )


def _mark_structural_status(
    row: DeclaredBalanceRow,
    invalid_codes: set[str],
) -> DeclaredBalanceRow:
    return replace(
        row,
        structural_status=(
            BalanceRowStructuralStatus.INVALIDA
            if row.aggregation_code in invalid_codes
            else row.structural_status
        ),
        children=tuple(_mark_structural_status(child, invalid_codes) for child in row.children),
    )


def _obligation_error(source: DeclaredBalanceInput) -> str | None:
    forms = {form.strip().upper() for form in source.bookkeeping_forms if form.strip()}
    closings = set(source.closing_dates)
    if len(forms) != 1:
        return "I010_AUSENTE_OU_AMBIGUO"
    if len(closings) != 1:
        return "I030_AUSENTE_OU_AMBIGUO"
    return None


def _is_block_j_required(source: DeclaredBalanceInput) -> bool:
    form = source.bookkeeping_forms[0].strip().upper()
    closing = source.closing_dates[0]
    return (
        form in REQUIRED_BOOKKEEPING_FORMS
        and source.ecd_period_start <= closing <= source.ecd_period_end
    )


def _row_can_be_rendered(row: BalanceStatementRow) -> bool:
    return (
        bool(row.aggregation_code)
        and row.aggregation_level is not None
        and row.final_amount is not None
    )


def _row_can_be_signed(row: BalanceStatementRow) -> bool:
    return (
        row.final_amount is not None
        and row.final_debit_credit_indicator in {"D", "C"}
    )


def _signed_row_final(row: BalanceStatementRow) -> Decimal:
    return _signed(
        row.final_amount or Decimal("0"),
        row.final_debit_credit_indicator or "D",
    )


def _signed(amount: Decimal, indicator: str) -> Decimal:
    if not isinstance(amount, Decimal):
        raise TypeError("monetary amount must be Decimal")
    normalized = _money(amount)
    if indicator == "D":
        return normalized
    if indicator == "C":
        return _money(-normalized)
    raise ValueError("debit/credit indicator must be D or C")


def _money(value: Decimal) -> Decimal:
    if not isinstance(value, Decimal):
        raise TypeError("monetary amount must be Decimal")
    return value.quantize(CENT, rounding=ROUND_HALF_UP)


def _empty_result(
    year: int,
    status: DeclaredBalanceStatus,
    limitation: str,
    *,
    statement: BalanceStatement | None = None,
) -> DeclaredBalance:
    return DeclaredBalance(
        year=year,
        status=status,
        is_blocking=status != DeclaredBalanceStatus.VALIDO,
        j005_period_start=statement.period_start if statement is not None else None,
        j005_period_end=statement.period_end if statement is not None else None,
        assets_final_amount=None,
        liabilities_and_equity_final_amount=None,
        difference=None,
        rows=(),
        limitations=(limitation,),
    )
