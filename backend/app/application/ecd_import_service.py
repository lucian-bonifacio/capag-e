from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime, timezone
from hashlib import sha256

from sqlalchemy import delete, func, select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.domain import EcdPreparationStatus, ProcessingStatus
from app.io import ParsedEcd
from app.repositories import (
    AnalysisModel,
    CompanyModel,
    DeclaredAccountSnapshot,
    EcdFileModel,
    EcdI010BookkeepingModel,
    EcdI030BookHeaderModel,
    EcdI050AccountModel,
    EcdI051ReferenceLinkModel,
    EcdI052AggregationLinkModel,
    EcdI150BalancePeriodModel,
    EcdI155BalanceModel,
    EcdI200EntryModel,
    EcdI250EntryItemModel,
    EcdJ005StatementModel,
    EcdJ100BalanceRowModel,
    EcdJ150PresenceModel,
    ExerciseModel,
    invalidate_capag_assessments,
    invalidate_dfc_calculations,
    invalidate_plra_calculations,
    invalidate_roa_calculations,
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
    parser_version: str | None
    preparation_status: str
    reprocessed_at: datetime | None


@dataclass(frozen=True)
class RemovedEcdImport:
    ecd_file_id: str
    analysis_id: str


def persist_parsed_ecd(
    session: Session,
    *,
    parsed_ecd: ParsedEcd,
    identifiers: EcdImportIdentifiers,
    original_content: bytes | None = None,
    parser_version: str | None = None,
) -> PersistedEcdImport:
    if original_content is not None:
        expected_hash = f"sha256:{sha256(original_content).hexdigest()}"
        if identifiers.content_hash != expected_hash:
            raise EcdPersistenceError("Persisted ECD bytes do not match the informed SHA-256.")

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
                original_content=original_content,
                content_size=len(original_content) if original_content is not None else None,
                parser_version=parser_version,
                preparation_status=EcdPreparationStatus.READY_FOR_RECONCILIATION.value,
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

            _persist_normalized_records(session, exercise, parsed_ecd)

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


def reprocess_existing_ecd(
    session: Session,
    *,
    parsed_ecd: ParsedEcd,
    existing_import: ExistingEcdImport,
    original_content: bytes,
    parser_version: str,
) -> PersistedEcdImport:
    expected_hash = f"sha256:{sha256(original_content).hexdigest()}"
    if existing_import.content_hash != expected_hash:
        raise EcdPersistenceError("Reprocessed ECD bytes do not match the stored SHA-256.")
    if (
        existing_import.preparation_status
        != EcdPreparationStatus.REIMPORT_REQUIRED.value
    ):
        raise EcdPersistenceError("ECD import is not eligible for controlled reprocessing.")

    try:
        with session.begin():
            ecd_file = session.get(EcdFileModel, existing_import.ecd_file_id)
            analysis = session.get(AnalysisModel, existing_import.analysis_id)
            exercise = session.scalar(
                select(ExerciseModel)
                .where(ExerciseModel.analysis_id == existing_import.analysis_id)
                .where(ExerciseModel.year == existing_import.year)
            )
            company = session.get(CompanyModel, existing_import.company_id)
            if ecd_file is None or analysis is None or exercise is None or company is None:
                raise EcdPersistenceError("Legacy ECD import is incomplete in persistence.")

            _delete_normalized_records(
                session,
                exercise_id=exercise.id,
                analysis_id=analysis.id,
                exercise_year=exercise.year,
            )
            _invalidate_derived_results(session, exercise_id=exercise.id)

            company.legal_name = parsed_ecd.header.legal_name
            ecd_file.original_content = original_content
            ecd_file.content_size = len(original_content)
            ecd_file.parser_version = parser_version
            ecd_file.layout = parsed_ecd.header.layout
            ecd_file.period_start = parsed_ecd.header.period_start
            ecd_file.period_end = parsed_ecd.header.period_end
            ecd_file.reprocessed_at = datetime.now(timezone.utc)
            ecd_file.preparation_status = (
                EcdPreparationStatus.READY_FOR_RECONCILIATION.value
            )
            ecd_file.reprocessing_result = "SUCESSO"
            analysis.status = ProcessingStatus.NOT_RUN.value
            exercise.status = ProcessingStatus.NOT_RUN.value

            _persist_normalized_records(session, exercise, parsed_ecd)

            return PersistedEcdImport(
                company_id=company.id,
                ecd_file_id=ecd_file.id,
                analysis_id=analysis.id,
                exercise_id=exercise.id,
                year=exercise.year,
            )
    except EcdPersistenceError:
        session.rollback()
        raise
    except SQLAlchemyError as exc:
        session.rollback()
        raise EcdPersistenceError("Failed to reprocess legacy ECD import.") from exc


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
                    delete(EcdJ150PresenceModel).where(
                        EcdJ150PresenceModel.exercise_id.in_(exercise_ids)
                    )
                )
                session.execute(
                    delete(EcdJ100BalanceRowModel).where(
                        EcdJ100BalanceRowModel.exercise_id.in_(exercise_ids)
                    )
                )
                session.execute(
                    delete(EcdJ005StatementModel).where(
                        EcdJ005StatementModel.exercise_id.in_(exercise_ids)
                    )
                )
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
                    delete(EcdI150BalancePeriodModel).where(
                        EcdI150BalancePeriodModel.exercise_id.in_(exercise_ids)
                    )
                )
                session.execute(
                    delete(EcdI052AggregationLinkModel).where(
                        EcdI052AggregationLinkModel.exercise_id.in_(exercise_ids)
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
                    delete(EcdI030BookHeaderModel).where(
                        EcdI030BookHeaderModel.exercise_id.in_(exercise_ids)
                    )
                )
                session.execute(
                    delete(EcdI010BookkeepingModel).where(
                        EcdI010BookkeepingModel.exercise_id.in_(exercise_ids)
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
            EcdFileModel.parser_version.label("parser_version"),
            EcdFileModel.preparation_status.label("preparation_status"),
            EcdFileModel.reprocessed_at.label("reprocessed_at"),
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
        parser_version=row["parser_version"],
        preparation_status=row["preparation_status"],
        reprocessed_at=row["reprocessed_at"],
    )


def _persist_normalized_records(
    session: Session,
    exercise: ExerciseModel,
    parsed_ecd: ParsedEcd,
) -> None:
    _persist_bookkeeping(session, exercise, parsed_ecd)
    _persist_book_headers(session, exercise, parsed_ecd)
    account_by_code = _persist_accounts(session, exercise, parsed_ecd)
    _persist_reference_links(session, exercise, parsed_ecd)
    _persist_aggregation_links(session, exercise, account_by_code, parsed_ecd)
    period_by_line = _persist_balance_periods(session, exercise, parsed_ecd)
    _persist_balances(session, exercise, period_by_line, parsed_ecd)
    entry_by_number = _persist_entries(session, exercise, parsed_ecd)
    _persist_entry_items(session, entry_by_number, parsed_ecd)
    statement_by_line = _persist_statements(session, exercise, parsed_ecd)
    _persist_j100_rows(session, exercise, statement_by_line, parsed_ecd)
    _persist_j150_presence(session, exercise, statement_by_line, parsed_ecd)


def _delete_normalized_records(
    session: Session,
    *,
    exercise_id: int,
    analysis_id: str,
    exercise_year: int,
) -> None:
    entry_ids = list(
        session.scalars(
            select(EcdI200EntryModel.id).where(
                EcdI200EntryModel.exercise_id == exercise_id
            )
        )
    )
    if entry_ids:
        session.execute(
            delete(EcdI250EntryItemModel).where(
                EcdI250EntryItemModel.entry_id.in_(entry_ids)
            )
        )
    for model in (
        EcdJ150PresenceModel,
        EcdJ100BalanceRowModel,
        EcdJ005StatementModel,
        EcdI200EntryModel,
        EcdI155BalanceModel,
        EcdI150BalancePeriodModel,
        EcdI052AggregationLinkModel,
        EcdI051ReferenceLinkModel,
        EcdI050AccountModel,
        EcdI030BookHeaderModel,
        EcdI010BookkeepingModel,
    ):
        session.execute(delete(model).where(model.exercise_id == exercise_id))
    session.execute(
        delete(DeclaredAccountSnapshot)
        .where(DeclaredAccountSnapshot.analysis_id == analysis_id)
        .where(DeclaredAccountSnapshot.exercise_year == exercise_year)
    )
    session.flush()


def _invalidate_derived_results(session: Session, *, exercise_id: int) -> None:
    invalidate_plra_calculations(session, exercise_id=exercise_id)
    invalidate_dfc_calculations(session, exercise_id=exercise_id)
    invalidate_roa_calculations(session, exercise_id=exercise_id)
    invalidate_capag_assessments(session, exercise_id=exercise_id)


def _persist_bookkeeping(
    session: Session,
    exercise: ExerciseModel,
    parsed_ecd: ParsedEcd,
) -> None:
    session.add_all(
        [
            EcdI010BookkeepingModel(
                exercise=exercise,
                bookkeeping_form=row.bookkeeping_form,
                bookkeeping_version=row.bookkeeping_version,
                line_number=row.line_number,
                source_line=row.source_line,
            )
            for row in parsed_ecd.bookkeeping_i010
        ]
    )


def _persist_book_headers(
    session: Session,
    exercise: ExerciseModel,
    parsed_ecd: ParsedEcd,
) -> None:
    session.add_all(
        [
            EcdI030BookHeaderModel(
                exercise=exercise,
                closing_date=row.closing_date,
                line_number=row.line_number,
                source_line=row.source_line,
            )
            for row in parsed_ecd.book_headers_i030
        ]
    )


def _persist_accounts(
    session: Session,
    exercise: ExerciseModel,
    parsed_ecd: ParsedEcd,
) -> dict[str, EcdI050AccountModel]:
    account_by_code: dict[str, EcdI050AccountModel] = {}
    for account in parsed_ecd.accounts_i050:
        model = EcdI050AccountModel(
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
        session.add(model)
        account_by_code[account.account_code] = model
    session.flush()
    return account_by_code


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


def _persist_aggregation_links(
    session: Session,
    exercise: ExerciseModel,
    account_by_code: dict[str, EcdI050AccountModel],
    parsed_ecd: ParsedEcd,
) -> None:
    session.add_all(
        [
            EcdI052AggregationLinkModel(
                exercise=exercise,
                account=account_by_code[link.account_code],
                account_code=link.account_code,
                cost_center_code=link.cost_center_code,
                aggregation_code=link.aggregation_code,
                line_number=link.line_number,
                source_line=link.source_line,
            )
            for link in parsed_ecd.aggregation_links_i052
        ]
    )


def _persist_balance_periods(
    session: Session,
    exercise: ExerciseModel,
    parsed_ecd: ParsedEcd,
) -> dict[int, EcdI150BalancePeriodModel]:
    period_by_line: dict[int, EcdI150BalancePeriodModel] = {}
    for period in parsed_ecd.balance_periods_i150:
        model = EcdI150BalancePeriodModel(
            exercise=exercise,
            period_start=period.period_start,
            period_end=period.period_end,
            line_number=period.line_number,
            source_line=period.source_line,
        )
        session.add(model)
        period_by_line[period.line_number] = model
    session.flush()
    return period_by_line


def _persist_balances(
    session: Session,
    exercise: ExerciseModel,
    period_by_line: dict[int, EcdI150BalancePeriodModel],
    parsed_ecd: ParsedEcd,
) -> None:
    session.add_all(
        [
            EcdI155BalanceModel(
                exercise=exercise,
                balance_period=(
                    period_by_line.get(balance.i150_line_number)
                    if balance.i150_line_number is not None
                    else None
                ),
                account_code=balance.account_code,
                cost_center_code=balance.cost_center_code,
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


def _persist_statements(
    session: Session,
    exercise: ExerciseModel,
    parsed_ecd: ParsedEcd,
) -> dict[int, EcdJ005StatementModel]:
    statement_by_line: dict[int, EcdJ005StatementModel] = {}
    for statement in parsed_ecd.statements_j005:
        model = EcdJ005StatementModel(
            exercise=exercise,
            period_start=statement.period_start,
            period_end=statement.period_end,
            statement_id=statement.statement_id,
            statement_header=statement.statement_header,
            line_number=statement.line_number,
            source_line=statement.source_line,
        )
        session.add(model)
        statement_by_line[statement.line_number] = model
    session.flush()
    return statement_by_line


def _persist_j100_rows(
    session: Session,
    exercise: ExerciseModel,
    statement_by_line: dict[int, EcdJ005StatementModel],
    parsed_ecd: ParsedEcd,
) -> None:
    session.add_all(
        [
            EcdJ100BalanceRowModel(
                exercise=exercise,
                statement=(
                    statement_by_line.get(row.j005_line_number)
                    if row.j005_line_number is not None
                    else None
                ),
                aggregation_code=row.aggregation_code,
                aggregation_code_type=row.aggregation_code_type,
                aggregation_level=row.aggregation_level,
                parent_aggregation_code=row.parent_aggregation_code,
                balance_group=row.balance_group,
                description=row.description,
                initial_amount=row.initial_amount,
                initial_debit_credit_indicator=row.initial_debit_credit_indicator,
                final_amount=row.final_amount,
                final_debit_credit_indicator=row.final_debit_credit_indicator,
                explanatory_note_reference=row.explanatory_note_reference,
                line_number=row.line_number,
                source_line=row.source_line,
            )
            for row in parsed_ecd.j100_rows
        ]
    )


def _persist_j150_presence(
    session: Session,
    exercise: ExerciseModel,
    statement_by_line: dict[int, EcdJ005StatementModel],
    parsed_ecd: ParsedEcd,
) -> None:
    session.add_all(
        [
            EcdJ150PresenceModel(
                exercise=exercise,
                statement=(
                    statement_by_line.get(row.j005_line_number)
                    if row.j005_line_number is not None
                    else None
                ),
                line_number=row.line_number,
                source_line=row.source_line,
            )
            for row in parsed_ecd.j150_presence
        ]
    )


def _exercise_year(period_end: date) -> int:
    return period_end.year
