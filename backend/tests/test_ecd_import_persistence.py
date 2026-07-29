from decimal import Decimal
from hashlib import sha256
from pathlib import Path

import pytest
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session

from app.application import EcdImportIdentifiers, EcdPersistenceError, persist_parsed_ecd
from app.io import parse_ecd_file
from app.repositories import (
    AnalysisModel,
    Base,
    EcdFileModel,
    EcdI010BookkeepingModel,
    EcdI030BookHeaderModel,
    EcdI050AccountModel,
    EcdI051ReferenceLinkModel,
    EcdI052AggregationLinkModel,
    EcdI150BalancePeriodModel,
    EcdI155BalanceModel,
    EcdI250EntryItemModel,
    EcdJ005StatementModel,
    EcdJ100BalanceRowModel,
    EcdJ150PresenceModel,
)


FIXTURES_DIR = Path(__file__).parent / "fixtures" / "ecd"


def test_persist_parsed_ecd_stores_normalized_records_by_analysis_and_exercise() -> None:
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    parsed = parse_ecd_file(FIXTURES_DIR / "valid_declared.ecd")

    with Session(engine) as session:
        result = persist_parsed_ecd(
            session,
            parsed_ecd=parsed,
            identifiers=_identifiers(),
        )

    with Session(engine) as session:
        analysis = session.get(AnalysisModel, result.analysis_id)
        account = session.scalars(select(EcdI050AccountModel)).one()
        reference_link = session.scalars(select(EcdI051ReferenceLinkModel)).one()
        balance = session.scalars(select(EcdI155BalanceModel)).one()
        item = session.scalars(select(EcdI250EntryItemModel)).one()

    assert analysis is not None
    assert result.year == 2024
    assert account.account_code == "1725"
    assert account.source_line.startswith("|I050|")
    assert reference_link.reference_code == "2.01.01.07.01"
    assert balance.final_balance == Decimal("100000.00")
    assert item.amount == Decimal("100000.00")


def test_persist_parsed_ecd_rolls_back_when_transaction_fails() -> None:
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    parsed = parse_ecd_file(FIXTURES_DIR / "valid_declared.ecd")

    with Session(engine) as session:
        persist_parsed_ecd(
            session,
            parsed_ecd=parsed,
            identifiers=_identifiers(content_hash="sha256:duplicado"),
        )
        with pytest.raises(EcdPersistenceError):
            persist_parsed_ecd(
                session,
                parsed_ecd=parsed,
                identifiers=_identifiers(
                    company_id="company-2",
                    ecd_file_id="ecd-file-2",
                    analysis_id="analysis-2",
                    content_hash="sha256:duplicado",
                ),
            )

    with Session(engine) as session:
        stored_analyses = session.scalars(select(AnalysisModel)).all()

    assert len(stored_analyses) == 1


def test_persist_parsed_ecd_preserves_original_bytes_and_balance_relationships() -> None:
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    raw = (FIXTURES_DIR / "balance_declared_complete.ecd").read_bytes()
    digest = sha256(raw).hexdigest()
    parsed = parse_ecd_file(FIXTURES_DIR / "balance_declared_complete.ecd")

    with Session(engine) as session:
        persist_parsed_ecd(
            session,
            parsed_ecd=parsed,
            identifiers=_identifiers(
                content_hash=f"sha256:{digest}",
            ),
            original_content=raw,
            parser_version="2.0.0",
        )

    with Session(engine) as session:
        ecd_file = session.scalars(select(EcdFileModel)).one()
        bookkeeping = session.scalars(select(EcdI010BookkeepingModel)).one()
        book_header = session.scalars(select(EcdI030BookHeaderModel)).one()
        link = session.scalars(select(EcdI052AggregationLinkModel)).one()
        period = session.scalars(select(EcdI150BalancePeriodModel)).one()
        balance = session.scalars(select(EcdI155BalanceModel)).one()
        statement = session.scalars(select(EcdJ005StatementModel)).one()
        j100_rows = session.scalars(
            select(EcdJ100BalanceRowModel).order_by(EcdJ100BalanceRowModel.line_number)
        ).all()
        j150 = session.scalars(select(EcdJ150PresenceModel)).one()

    assert ecd_file.original_content == raw
    assert ecd_file.content_size == len(raw)
    assert ecd_file.content_hash == f"sha256:{sha256(ecd_file.original_content).hexdigest()}"
    assert ecd_file.parser_version == "2.0.0"
    assert bookkeeping.exercise_id == book_header.exercise_id
    assert link.account_id is not None
    assert link.cost_center_code == "CC01"
    assert balance.balance_period_id == period.id
    assert balance.cost_center_code == "CC01"
    assert j100_rows[1].statement_id == statement.id
    assert j100_rows[1].initial_amount == Decimal("100.00")
    assert j100_rows[1].final_amount == Decimal("800.00")
    assert j150.statement_id == statement.id


def _identifiers(
    *,
    company_id: str = "company-1",
    ecd_file_id: str = "ecd-file-1",
    analysis_id: str = "analysis-1",
    content_hash: str = "sha256:fixture",
) -> EcdImportIdentifiers:
    return EcdImportIdentifiers(
        company_id=company_id,
        ecd_file_id=ecd_file_id,
        analysis_id=analysis_id,
        methodology_version_id="metodologia-2024.1",
        original_filename="valid_declared.ecd",
        content_hash=content_hash,
    )
