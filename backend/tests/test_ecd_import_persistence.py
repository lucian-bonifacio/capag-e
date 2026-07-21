from decimal import Decimal
from pathlib import Path

import pytest
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session

from app.application import EcdImportIdentifiers, EcdPersistenceError, persist_parsed_ecd
from app.io import parse_ecd_file
from app.repositories import (
    AnalysisModel,
    Base,
    EcdI050AccountModel,
    EcdI051ReferenceLinkModel,
    EcdI155BalanceModel,
    EcdI250EntryItemModel,
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
