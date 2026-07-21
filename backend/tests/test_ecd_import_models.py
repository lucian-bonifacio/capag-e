from datetime import date
from decimal import Decimal

from sqlalchemy import create_engine, inspect, select
from sqlalchemy.orm import Session

from app.domain import ProcessingStatus
from app.repositories import (
    AnalysisModel,
    Base,
    CompanyModel,
    EcdFileModel,
    EcdI050AccountModel,
    EcdI051ReferenceLinkModel,
    EcdI155BalanceModel,
    EcdI200EntryModel,
    EcdI250EntryItemModel,
    EcdJ100BalanceRowModel,
    ExerciseModel,
)


def test_ecd_normalized_models_create_expected_tables() -> None:
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)

    table_names = set(inspect(engine).get_table_names())

    assert {
        "companies",
        "ecd_files",
        "analyses",
        "analysis_exercises",
        "ecd_i050_accounts",
        "ecd_i051_reference_links",
        "ecd_i155_balances",
        "ecd_i200_entries",
        "ecd_i250_entry_items",
        "ecd_j100_balance_rows",
    }.issubset(table_names)


def test_ecd_normalized_models_persist_traceable_records_with_decimal_values() -> None:
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)

    with Session(engine) as session:
        company = CompanyModel(
            id="company-1",
            legal_name="Empresa Sintetica Ltda",
            tax_id="00000000000100",
        )
        ecd_file = EcdFileModel(
            id="ecd-file-1",
            company=company,
            original_filename="fixture-valida.txt",
            content_hash="sha256:abc123",
            layout="ECD_2024",
            period_start=date(2024, 1, 1),
            period_end=date(2024, 12, 31),
        )
        analysis = AnalysisModel(
            id="analysis-1",
            company=company,
            ecd_file=ecd_file,
            methodology_version_id="metodologia-2024.1",
            status=ProcessingStatus.NOT_RUN.value,
        )
        exercise = ExerciseModel(
            analysis=analysis,
            year=2024,
            status=ProcessingStatus.NOT_RUN.value,
            methodology_version_id="metodologia-2024.1",
        )
        session.add_all([company, ecd_file, analysis, exercise])
        session.flush()

        session.add_all(
            [
                EcdI050AccountModel(
                    exercise=exercise,
                    account_code="1725",
                    account_name="Emprestimo - Sicoob",
                    account_type="A",
                    account_nature="C",
                    level=4,
                    parent_account_code="1700",
                    line_number=10,
                    source_line="|I050|01012024|01|A|4|1725|1700|Emprestimo - Sicoob|",
                ),
                EcdI051ReferenceLinkModel(
                    exercise=exercise,
                    account_code="1725",
                    reference_code="2.01.01.07.01",
                    line_number=11,
                    source_line="|I051|1725|2.01.01.07.01|",
                ),
                EcdI155BalanceModel(
                    exercise=exercise,
                    account_code="1725",
                    initial_balance=Decimal("0.00"),
                    initial_balance_indicator="C",
                    debit_amount=Decimal("0.00"),
                    credit_amount=Decimal("100000.00"),
                    final_balance=Decimal("100000.00"),
                    final_balance_indicator="C",
                    line_number=12,
                    source_line="|I155|1725|0,00|C|0,00|100000,00|100000,00|C|",
                ),
                EcdJ100BalanceRowModel(
                    exercise=exercise,
                    account_code="1725",
                    description="Emprestimo - Sicoob",
                    amount=Decimal("100000.00"),
                    amount_indicator="C",
                    line_number=20,
                    source_line="|J100|1725|Emprestimo - Sicoob|100000,00|C|",
                ),
            ]
        )
        entry = EcdI200EntryModel(
            exercise=exercise,
            entry_number="LCTO-1",
            entry_date=date(2024, 1, 31),
            total_amount=Decimal("100000.00"),
            line_number=30,
            source_line="|I200|LCTO-1|31012024|100000,00|",
        )
        session.add(entry)
        session.flush()
        session.add(
            EcdI250EntryItemModel(
                entry=entry,
                account_code="1725",
                counterparty_account_code="1000",
                amount=Decimal("100000.00"),
                debit_credit_indicator="C",
                history="Lancamento sintetico",
                line_number=31,
                source_line="|I250|1725|1000|100000,00|C|Lancamento sintetico|",
            )
        )
        session.commit()

    with Session(engine) as session:
        stored_balance = session.scalars(select(EcdI155BalanceModel)).one()
        stored_item = session.scalars(select(EcdI250EntryItemModel)).one()

    assert stored_balance.final_balance == Decimal("100000.00")
    assert stored_balance.source_line.startswith("|I155|")
    assert stored_item.amount == Decimal("100000.00")
