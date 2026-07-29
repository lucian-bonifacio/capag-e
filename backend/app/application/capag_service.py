from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal

from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.domain import (
    CapagEAssessment,
    CapagEMethod,
    ComponentStatus,
    DfcCalculation,
    PlraCalculation,
    RoaCalculation,
)
from app.engine import calculate_capag_e_assessment
from app.repositories import (
    AnalysisModel,
    CapagAssessmentNotFound,
    ExerciseModel,
    PlraCalculationNotFound,
    add_capag_assessment,
    get_latest_capag_assessment,
    get_latest_plra_calculation,
)


class CapagAssessmentContextNotFound(LookupError):
    pass


class CapagAssessmentUnavailable(RuntimeError):
    pass


@dataclass(frozen=True)
class CapagAssessmentRunInput:
    method: CapagEMethod
    fca_value: Decimal | None
    fca_status: ComponentStatus
    roa_value: Decimal | None
    roa_status: ComponentStatus
    fco_value: Decimal | None
    warnings: tuple[str, ...]
    limitations: tuple[str, ...]
    blocking_issues: tuple[str, ...]


def calculate_roa_plra_assessment(
    *,
    plra: PlraCalculation,
    roa: RoaCalculation,
    fca: DfcCalculation | None = None,
) -> CapagEAssessment:
    _validate_component_context(plra=plra, roa=roa, fca=fca)
    method = (
        CapagEMethod.COMPARATIVO_FCA_ROA
        if fca is not None
        else CapagEMethod.ROA_PLRA
    )
    fca_alerts = () if fca is None else fca.alerts
    fca_limitations = () if fca is None else fca.limitations
    fca_blocking_issues = (
        ()
        if fca is None
        else tuple(
            f"FCA:{issue.code}:{issue.entry_number or 'sem_lancamento'}"
            for issue in fca.pending_issues
            if issue.blocks_fca
        )
    )
    roa_blocking_issues = tuple(
        f"ROA:{group.code}:{group.account_code or 'sem_conta'}"
        for group in roa.pending_groups
        if group.blocks_roa
    )

    return calculate_capag_e_assessment(
        exercise_year=roa.exercise_year,
        method=method,
        plra_value=plra.plra_value,
        plra_status=plra.plra_status,
        fca_value=None if fca is None else fca.fca_value,
        fca_status=(
            ComponentStatus.NOT_CALCULATED if fca is None else fca.status
        ),
        roa_value=roa.roa_final,
        roa_status=roa.status,
        warnings=_merge_messages(plra.warnings, roa.alerts, fca_alerts),
        limitations=_merge_messages(
            plra.limitations,
            roa.limitations,
            fca_limitations,
        ),
        blocking_issues=_merge_messages(
            plra.blocking_issues,
            roa_blocking_issues,
            fca_blocking_issues,
        ),
        methodology_version_id=roa.methodology_version_id,
        balance_status=plra.balance_status,
    )


def run_capag_assessment(
    session: Session,
    *,
    analysis_id: str,
    year: int,
    run_input: CapagAssessmentRunInput,
) -> CapagEAssessment:
    try:
        analysis, exercise = _get_context(
            session,
            analysis_id=analysis_id,
            year=year,
        )
        methodology_version_id = (
            exercise.methodology_version_id or analysis.methodology_version_id
        )
        try:
            plra = get_latest_plra_calculation(session, exercise_id=exercise.id)
        except PlraCalculationNotFound as exc:
            raise ValueError(
                "A persisted PLRA snapshot is required before CAPAG-E assessment."
            ) from exc
        if plra.methodology_version_id != methodology_version_id:
            raise ValueError(
                "The latest PLRA snapshot uses a different methodology version."
            )
        assessment = calculate_capag_e_assessment(
            exercise_year=year,
            method=run_input.method,
            plra_value=plra.plra_value,
            plra_status=plra.plra_status,
            fca_value=run_input.fca_value,
            fca_status=run_input.fca_status,
            roa_value=run_input.roa_value,
            roa_status=run_input.roa_status,
            fco_value=run_input.fco_value,
            warnings=_merge_messages(plra.warnings, run_input.warnings),
            limitations=_merge_messages(plra.limitations, run_input.limitations),
            blocking_issues=_merge_messages(
                plra.blocking_issues, run_input.blocking_issues
            ),
            methodology_version_id=methodology_version_id,
            balance_status=plra.balance_status,
        )
        add_capag_assessment(
            session,
            exercise_id=exercise.id,
            assessment=assessment,
        )
        session.commit()
        return assessment
    except CapagAssessmentContextNotFound:
        session.rollback()
        raise
    except (TypeError, ValueError):
        session.rollback()
        raise
    except SQLAlchemyError as exc:
        session.rollback()
        raise CapagAssessmentUnavailable("CAPAG-E assessment run failed.") from exc


def get_capag_assessment(
    session: Session,
    *,
    analysis_id: str,
    year: int,
) -> CapagEAssessment:
    try:
        _, exercise = _get_context(
            session,
            analysis_id=analysis_id,
            year=year,
        )
        return get_latest_capag_assessment(session, exercise_id=exercise.id)
    except CapagAssessmentNotFound as exc:
        raise CapagAssessmentContextNotFound(str(exc)) from exc
    except SQLAlchemyError as exc:
        raise CapagAssessmentUnavailable("CAPAG-E assessment query failed.") from exc


def _get_context(
    session: Session,
    *,
    analysis_id: str,
    year: int,
) -> tuple[AnalysisModel, ExerciseModel]:
    analysis = session.get(AnalysisModel, analysis_id)
    if analysis is None:
        raise CapagAssessmentContextNotFound("Analysis not found.")

    exercise = session.scalar(
        select(ExerciseModel)
        .where(ExerciseModel.analysis_id == analysis_id)
        .where(ExerciseModel.year == year)
    )
    if exercise is None:
        raise CapagAssessmentContextNotFound("Exercise not found.")
    return analysis, exercise


def _merge_messages(*groups: tuple[str, ...]) -> tuple[str, ...]:
    return tuple(dict.fromkeys(message for group in groups for message in group))


def _validate_component_context(
    *,
    plra: PlraCalculation,
    roa: RoaCalculation,
    fca: DfcCalculation | None,
) -> None:
    if plra.exercise_year != roa.exercise_year:
        raise ValueError("PLRA and ROA must use the same exercise.")
    if plra.methodology_version_id != roa.methodology_version_id:
        raise ValueError("PLRA and ROA must use the same methodology version.")
    if fca is None:
        return
    if fca.exercise_year != roa.exercise_year:
        raise ValueError("FCA and ROA must use the same exercise.")
    if fca.methodology_version_id != roa.methodology_version_id:
        raise ValueError("FCA and ROA must use the same methodology version.")
