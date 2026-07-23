from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal

from sqlalchemy import delete, select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.domain import DeclaredAccountResult, ProcessingStatus
from app.engine.methodology_matcher import (
    MatchFinalStatus,
    MatchRequest,
    MethodologyRule,
    OfficialReferenceAccount,
    match_declared_methodology,
)
from app.repositories import (
    AnalysisModel,
    DeclaredAccountSnapshot,
    EcdFileModel,
    EcdI050AccountModel,
    EcdI051ReferenceLinkModel,
    EcdI155BalanceModel,
    ExerciseModel,
    add_declared_account_snapshot,
)


class DeclaredRunNotFound(LookupError):
    pass


class DeclaredRunFailed(RuntimeError):
    pass


class DeclaredOfficialReferenceConfigurationError(RuntimeError):
    pass


@dataclass(frozen=True)
class DeclaredRunResult:
    analysis_id: str
    year: int
    status: str
    snapshots_created: int
    status_counts: dict[str, int]


def run_declared_layer(
    session: Session,
    *,
    analysis_id: str,
    year: int,
    official_references: list[OfficialReferenceAccount],
    methodology_rules: list[MethodologyRule],
    purpose: str = "FCO",
) -> DeclaredRunResult:
    _ensure_official_references_available(official_references)

    try:
        analysis = session.get(AnalysisModel, analysis_id)
        if analysis is None:
            raise DeclaredRunNotFound("Analysis not found.")

        exercise = session.scalar(
            select(ExerciseModel)
            .where(ExerciseModel.analysis_id == analysis_id)
            .where(ExerciseModel.year == year)
        )
        if exercise is None:
            raise DeclaredRunNotFound("Exercise not found.")

        ecd_file = session.get(EcdFileModel, analysis.ecd_file_id)
        if ecd_file is None:
            raise DeclaredRunNotFound("ECD file not found.")

        analysis.status = ProcessingStatus.PROCESSING.value
        exercise.status = ProcessingStatus.PROCESSING.value
        session.flush()

        session.execute(
            delete(DeclaredAccountSnapshot)
            .where(DeclaredAccountSnapshot.analysis_id == analysis_id)
            .where(DeclaredAccountSnapshot.exercise_year == year)
        )

        accounts = list(
            session.scalars(
                select(EcdI050AccountModel)
                .where(EcdI050AccountModel.exercise_id == exercise.id)
                .order_by(EcdI050AccountModel.account_code)
            )
        )
        reference_by_account = {
            link.account_code: link.reference_code
            for link in session.scalars(
                select(EcdI051ReferenceLinkModel).where(
                    EcdI051ReferenceLinkModel.exercise_id == exercise.id
                )
            )
        }
        balance_by_account = {
            balance.account_code: balance
            for balance in session.scalars(
                select(EcdI155BalanceModel).where(EcdI155BalanceModel.exercise_id == exercise.id)
            )
        }

        status_counts: dict[str, int] = {}
        for account in accounts:
            balance = balance_by_account.get(account.account_code)
            base_value = balance.final_balance if balance is not None else Decimal("0.00")
            reference_code = reference_by_account.get(account.account_code)
            match_result = match_declared_methodology(
                request=MatchRequest(
                    reference_code=reference_code,
                    year=year,
                    layout=ecd_file.layout,
                    entity_type="PJ_GERAL",
                    purpose=purpose,
                ),
                official_references=official_references,
                methodology_rules=methodology_rules,
            )
            considered_value = _considered_value(base_value, match_result.final_status)
            declared_result = DeclaredAccountResult.from_match(
                account_code=account.account_code,
                account_name=account.account_name,
                declared_reference_code=reference_code,
                purpose=purpose,
                base_value=base_value,
                considered_value=considered_value,
                methodology_version_id=analysis.methodology_version_id,
                match_result=match_result,
            )
            add_declared_account_snapshot(
                session,
                analysis_id=analysis_id,
                exercise_year=year,
                result=declared_result,
            )
            status_counts[declared_result.final_status] = (
                status_counts.get(declared_result.final_status, 0) + 1
            )

        final_status = (
            ProcessingStatus.COMPLETED.value
            if set(status_counts) == {MatchFinalStatus.MAPPED.value}
            else ProcessingStatus.COMPLETED_WITH_ISSUES.value
        )
        analysis.status = final_status
        exercise.status = final_status
        session.commit()

        return DeclaredRunResult(
            analysis_id=analysis_id,
            year=year,
            status=final_status,
            snapshots_created=len(accounts),
            status_counts=status_counts,
        )
    except DeclaredRunNotFound:
        session.rollback()
        raise
    except SQLAlchemyError as exc:
        session.rollback()
        raise DeclaredRunFailed("Declared layer run failed.") from exc


def _ensure_official_references_available(
    official_references: list[OfficialReferenceAccount],
) -> None:
    if len(official_references) == 0:
        raise DeclaredOfficialReferenceConfigurationError(
            "Official reference table is required to run declared layer."
        )


def _considered_value(base_value: Decimal, final_status: MatchFinalStatus) -> Decimal:
    if final_status == MatchFinalStatus.MAPPED:
        return base_value
    return Decimal("0.00")
