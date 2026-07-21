from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime

from sqlalchemy import delete, func, select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.domain import ProcessingStatus
from app.io import ParsedEcd
from app.repositories import (
    AnalysisModel,
    CompanyModel,
    DeclaredAccountSnapshot,
    EcdFileModel,
    EcdI050AccountModel,
    EcdI051ReferenceLinkModel,
    EcdI155BalanceModel,
    EcdI200EntryModel,
    EcdI250EntryItemModel,
    EcdJ100BalanceRowModel,
    ExerciseModel,
)


class EcdPersistenceError(RuntimeError):
    pass


class EcdImportNotFound(LookupError):
    pass


class EcdImportRemovalError(RuntimeError):
    pass


@dataclass(frozen=True)
class PersistedEcdImport:
    company_id: str
    ecd_file_id: str
    analysis_id: str
    exercise_id: int
    year: int


@dataclass(frozen=True)
class EcdImportIdentifiers:
    company_id: str
    ecd_file_id: str
    analysis_id: str
    methodology_version_id: str
    original_filename: str
    content_hash: str


@dataclass(frozen=True)
class ExistingEcdImport:
    analysis_id: str
    company_id: str
    ecd_file_id: str
    original_filename: str
    content_hash: str
    layout: str
    period_start: date
    period_end: date
    imported_at: datetime
    year: int
    methodology_version_id: str
    status: str


@dataclass(frozen=True)
class RemovedEcdImport:
    ecd_file_id: str
    analysis_id: str


def persist_parsed_ecd(
    session: Session,
    *,
    parsed_ecd: ParsedEcd,
    identifiers: EcdImportIdentifiers,
) -> PersistedEcdImport:
    try:
        with session.begin():
            company = CompanyModel(
                id=identifiers.company_id,
                legal_name=parsed_ecd.header.legal_name,
                tax_id=parsed_ecd.header.tax_id,
            )
            ecd_file = EcdFileModel(
                id=identifiers.ecd_file_id,
                company=company,
                original_filename=identifiers.original_filename,
                content_hash=identifiers.content_hash,
                layout=parsed_ecd.header.layout,
                period_start=parsed_ecd.header.period_start,
                period_end=parsed_ecd.header.period_end,
            )
            analysis = AnalysisModel(
                id=identifiers.analysis_id,
                company=company,
                ecd_file=ecd_file,
                methodology_version_id=identifiers.methodology_version_id,
                status=ProcessingStatus.NOT_RUN.value,
            )
            exercise = ExerciseModel(
                analysis=analysis,
                year=_exercise_year(parsed_ecd.header.period_end),
                status=ProcessingStatus.NOT_RUN.value,
                methodology_version_id=identifiers.methodology_version_id,
            )
            session.add_all([company, ecd_file, analysis, exercise])
            session.flush()

            _persist_accounts(session, exercise, parsed_ecd)
            _persist_reference_links(session, exercise, parsed_ecd)
            _persist_balances(session, exercise, parsed_ecd)
            entry_by_number = _persist_entries(session, exercise, parsed_ecd)
            _persist_entry_items(session, entry_by_number, parsed_ecd)
            _persist_j100_rows(session, exercise, parsed_ecd)

            return PersistedEcdImport(
                company_id=company.id,
                ecd_file_id=ecd_file.id,
                analysis_id=analysis.id,
                exercise_id=exercise.id,
                year=exercise.year,
            )
    except SQLAlchemyError as exc:
        session.rollback()
        raise EcdPersistenceError("Failed to persist normalized ECD import.") from exc


def get_existing_ecd_import_by_hash(
    session: Session,
    *,
    content_hash: str,
) -> ExistingEcdImport | None:
    row = (
        session.execute(
            _existing_imports_statement().where(EcdFileModel.content_hash == content_hash)
        )
        .mappings()
        .first()
    )
    return _existing_import_from_row(row) if row is not None else None


def list_existing_ecd_imports(session: Session) -> list[ExistingEcdImport]:
    return [
        _existing_import_from_row(row)
        for row in session.execute(_existing_imports_statement()).mappings()
    ]


def remove_ecd_import(session: Session, *, ecd_file_id: str) -> RemovedEcdImport:
    try:
        with session.begin():
            ecd_file = session.get(EcdFileModel, ecd_file_id)
            if ecd_file is None:
                raise EcdImportNotFound("ECD import not found.")

            analysis = session.scalar(
                select(AnalysisModel).where(AnalysisModel.ecd_file_id == ecd_file_id)
            )
            if analysis is None:
                raise EcdImportNotFound("Analysis for ECD import not found.")

            company_id = ecd_file.company_id
            exercise_ids = list(
                session.scalars(
                    select(ExerciseModel.id).where(ExerciseModel.analysis_id == analysis.id)
                )
            )
            entry_ids = list(
                session.scalars(
                    select(EcdI200EntryModel.id).where(
                        EcdI200EntryModel.exercise_id.in_(exercise_ids)
                    )
                )
            )

            session.execute(
                delete(DeclaredAccountSnapshot).where(
                    DeclaredAccountSnapshot.analysis_id == analysis.id
                )
            )
            if entry_ids:
                session.execute(
                    delete(EcdI250EntryItemModel).where(
                        EcdI250EntryItemModel.entry_id.in_(entry_ids)
                    )
                )
            if exercise_ids:
                session.execute(
                    delete(EcdI200EntryModel).where(
                        EcdI200EntryModel.exercise_id.in_(exercise_ids)
                    )
                )
                session.execute(
                    delete(EcdI155BalanceModel).where(
                        EcdI155BalanceModel.exercise_id.in_(exercise_ids)
                    )
                )
                session.execute(
                    delete(EcdI051ReferenceLinkModel).where(
                        EcdI051ReferenceLinkModel.exercise_id.in_(exercise_ids)
                    )
                )
                session.execute(
                    delete(EcdI050AccountModel).where(
                        EcdI050AccountModel.exercise_id.in_(exercise_ids)
                    )
                )
                session.execute(
                    delete(EcdJ100BalanceRowModel).where(
                        EcdJ100BalanceRowModel.exercise_id.in_(exercise_ids)
                    )
                )
                session.execute(
                    delete(ExerciseModel).where(ExerciseModel.id.in_(exercise_ids))
                )

            session.execute(delete(AnalysisModel).where(AnalysisModel.id == analysis.id))
            session.execute(delete(EcdFileModel).where(EcdFileModel.id == ecd_file_id))

            remaining_company_refs = session.scalar(
                select(func.count())
                .select_from(EcdFileModel)
                .where(EcdFileModel.company_id == company_id)
            )
            if remaining_company_refs == 0:
                session.execute(delete(CompanyModel).where(CompanyModel.id == company_id))

            return RemovedEcdImport(ecd_file_id=ecd_file_id, analysis_id=analysis.id)
    except EcdImportNotFound:
        raise
    except SQLAlchemyError as exc:
        session.rollback()
        raise EcdImportRemovalError("Failed to remove ECD import.") from exc


def _existing_imports_statement():
    return (
        select(
            AnalysisModel.id.label("analysis_id"),
            CompanyModel.id.label("company_id"),
            EcdFileModel.id.label("ecd_file_id"),
            EcdFileModel.original_filename.label("original_filename"),
            EcdFileModel.content_hash.label("content_hash"),
            EcdFileModel.layout.label("layout"),
            EcdFileModel.period_start.label("period_start"),
            EcdFileModel.period_end.label("period_end"),
            EcdFileModel.imported_at.label("imported_at"),
            ExerciseModel.year.label("year"),
            AnalysisModel.methodology_version_id.label("methodology_version_id"),
            AnalysisModel.status.label("status"),
        )
        .join(EcdFileModel, AnalysisModel.ecd_file_id == EcdFileModel.id)
        .join(CompanyModel, AnalysisModel.company_id == CompanyModel.id)
        .join(ExerciseModel, ExerciseModel.analysis_id == AnalysisModel.id)
        .order_by(EcdFileModel.imported_at.desc(), AnalysisModel.id)
    )


def _existing_import_from_row(row) -> ExistingEcdImport:
    return ExistingEcdImport(
        analysis_id=row["analysis_id"],
        company_id=row["company_id"],
        ecd_file_id=row["ecd_file_id"],
        original_filename=row["original_filename"],
        content_hash=row["content_hash"],
        layout=row["layout"],
        period_start=row["period_start"],
        period_end=row["period_end"],
        imported_at=row["imported_at"],
        year=row["year"],
        methodology_version_id=row["methodology_version_id"],
        status=row["status"],
    )


def _persist_accounts(session: Session, exercise: ExerciseModel, parsed_ecd: ParsedEcd) -> None:
    session.add_all(
        [
            EcdI050AccountModel(
                exercise=exercise,
                account_code=account.account_code,
                account_name=account.account_name,
                account_type=account.account_type,
                account_nature=account.account_nature,
                level=account.level,
                parent_account_code=account.parent_account_code,
                line_number=account.line_number,
                source_line=account.source_line,
            )
            for account in parsed_ecd.accounts_i050
        ]
    )


def _persist_reference_links(session: Session, exercise: ExerciseModel, parsed_ecd: ParsedEcd) -> None:
    session.add_all(
        [
            EcdI051ReferenceLinkModel(
                exercise=exercise,
                account_code=link.account_code,
                reference_code=link.reference_code,
                line_number=link.line_number,
                source_line=link.source_line,
            )
            for link in parsed_ecd.reference_links_i051
        ]
    )


def _persist_balances(session: Session, exercise: ExerciseModel, parsed_ecd: ParsedEcd) -> None:
    session.add_all(
        [
            EcdI155BalanceModel(
                exercise=exercise,
                account_code=balance.account_code,
                initial_balance=balance.initial_balance,
                initial_balance_indicator=balance.initial_balance_indicator,
                debit_amount=balance.debit_amount,
                credit_amount=balance.credit_amount,
                final_balance=balance.final_balance,
                final_balance_indicator=balance.final_balance_indicator,
                line_number=balance.line_number,
                source_line=balance.source_line,
            )
            for balance in parsed_ecd.balances_i155
        ]
    )


def _persist_entries(
    session: Session,
    exercise: ExerciseModel,
    parsed_ecd: ParsedEcd,
) -> dict[str, EcdI200EntryModel]:
    entry_by_number: dict[str, EcdI200EntryModel] = {}
    for entry in parsed_ecd.entries_i200:
        entry_model = EcdI200EntryModel(
            exercise=exercise,
            entry_number=entry.entry_number,
            entry_date=entry.entry_date,
            total_amount=entry.total_amount,
            line_number=entry.line_number,
            source_line=entry.source_line,
        )
        session.add(entry_model)
        entry_by_number[entry.entry_number] = entry_model

    session.flush()
    return entry_by_number


def _persist_entry_items(
    session: Session,
    entry_by_number: dict[str, EcdI200EntryModel],
    parsed_ecd: ParsedEcd,
) -> None:
    session.add_all(
        [
            EcdI250EntryItemModel(
                entry=entry_by_number[item.entry_number],
                account_code=item.account_code,
                counterparty_account_code=item.counterparty_account_code,
                amount=item.amount,
                debit_credit_indicator=item.debit_credit_indicator,
                history=item.history,
                line_number=item.line_number,
                source_line=item.source_line,
            )
            for item in parsed_ecd.items_i250
        ]
    )


def _persist_j100_rows(session: Session, exercise: ExerciseModel, parsed_ecd: ParsedEcd) -> None:
    session.add_all(
        [
            EcdJ100BalanceRowModel(
                exercise=exercise,
                account_code=row.account_code,
                description=row.description,
                amount=row.amount,
                amount_indicator=row.amount_indicator,
                line_number=row.line_number,
                source_line=row.source_line,
            )
            for row in parsed_ecd.j100_rows
        ]
    )


def _exercise_year(period_end: date) -> int:
    return period_end.year
