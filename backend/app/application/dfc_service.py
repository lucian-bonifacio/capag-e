from __future__ import annotations

from collections import defaultdict
from dataclasses import replace
from decimal import Decimal
from uuid import uuid4

from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.assets.methodology import DfcMethodology, load_dfc_methodology
from app.domain import (
    CashFlowDirection,
    DfcActivity,
    DfcCalculation,
    DfcDecisionAction,
    DfcEntry,
    DfcEntryItem,
    DfcManualDecision,
    DfcRowStatus,
    MethodComponent,
)
from app.engine import build_dfc_audit_rows, calculate_dfc
from app.repositories import (
    AdjustmentEvidenceModel,
    AnalysisModel,
    DfcCalculationNotFound,
    EcdI050AccountModel,
    EcdI051ReferenceLinkModel,
    EcdI200EntryModel,
    EcdI250EntryItemModel,
    ExerciseModel,
    add_dfc_calculation,
    get_latest_dfc_calculation,
    invalidate_capag_assessments,
    invalidate_dfc_calculations,
    list_adjustment_evidences,
    list_dfc_manual_decisions,
    save_dfc_manual_decision,
)


class DfcContextNotFound(LookupError):
    pass


class DfcRunUnavailable(RuntimeError):
    pass


def run_dfc_calculation(
    session: Session,
    *,
    analysis_id: str,
    year: int,
    methodology: DfcMethodology | None = None,
) -> DfcCalculation:
    try:
        analysis, exercise = _get_context(
            session,
            analysis_id=analysis_id,
            year=year,
        )
        calculation = _calculate(
            session,
            analysis=analysis,
            exercise=exercise,
            year=year,
            methodology=methodology or load_dfc_methodology(),
        )
        invalidate_dfc_calculations(session, exercise_id=exercise.id)
        invalidate_capag_assessments(session, exercise_id=exercise.id)
        add_dfc_calculation(
            session,
            exercise_id=exercise.id,
            analysis_id=analysis_id,
            calculation=calculation,
        )
        session.commit()
        return calculation
    except (DfcContextNotFound, TypeError, ValueError):
        session.rollback()
        raise
    except SQLAlchemyError as exc:
        session.rollback()
        raise DfcRunUnavailable("DFC calculation run failed.") from exc


def get_dfc_calculation(
    session: Session,
    *,
    analysis_id: str,
    year: int,
) -> DfcCalculation:
    try:
        _, exercise = _get_context(session, analysis_id=analysis_id, year=year)
        return get_latest_dfc_calculation(session, exercise_id=exercise.id)
    except DfcCalculationNotFound as exc:
        raise DfcContextNotFound(str(exc)) from exc
    except SQLAlchemyError as exc:
        raise DfcRunUnavailable("DFC calculation query failed.") from exc


def create_dfc_decision(
    session: Session,
    *,
    analysis_id: str,
    year: int,
    action: DfcDecisionAction,
    entry_number: str,
    line_number: int,
    activity: DfcActivity | None,
    component_code: str | None,
    justification: str,
    evidence_id: str | None,
) -> DfcCalculation:
    try:
        analysis, exercise = _get_context(
            session,
            analysis_id=analysis_id,
            year=year,
        )
        methodology = load_dfc_methodology()
        current = get_latest_dfc_calculation(session, exercise_id=exercise.id)
        if not any(
            row.entry_number == entry_number and row.line_number == line_number
            for row in current.audit_rows
        ):
            raise ValueError("DFC audit row not found for manual decision.")
        resolved_action = DfcDecisionAction(action)
        resolved_activity = DfcActivity(activity) if activity is not None else None
        if resolved_action == DfcDecisionAction.INCLUDE:
            if resolved_activity in {None, DfcActivity.UNCLASSIFIED} or not component_code:
                raise ValueError("Included decision requires activity and component.")
            component = methodology.component(component_code)
            if component.activity != resolved_activity.value:
                raise ValueError("DFC component is incompatible with selected activity.")
        if evidence_id is not None:
            evidence = session.scalar(
                select(AdjustmentEvidenceModel).where(
                    AdjustmentEvidenceModel.evidence_id == evidence_id
                )
            )
            if evidence is None or evidence.exercise_id != exercise.id:
                raise ValueError("Evidence does not belong to the DFC exercise.")
            if evidence.method_component != MethodComponent.FCA.value:
                raise ValueError("Evidence must belong to FCA.")

        methodology_version_id = (
            exercise.methodology_version_id or analysis.methodology_version_id
        )
        decision = DfcManualDecision(
            decision_id=f"dfc-decision-{uuid4().hex}",
            entry_number=entry_number,
            line_number=line_number,
            action=resolved_action,
            activity=resolved_activity,
            component_code=component_code,
            justification=justification,
            evidence_id=evidence_id,
            decided_at=_utc_now(),
            methodology_version_id=methodology_version_id,
        )
        save_dfc_manual_decision(
            session,
            exercise_id=exercise.id,
            decision=decision,
        )
        calculation = _calculate(
            session,
            analysis=analysis,
            exercise=exercise,
            year=year,
            methodology=methodology,
        )
        invalidate_dfc_calculations(session, exercise_id=exercise.id)
        invalidate_capag_assessments(session, exercise_id=exercise.id)
        add_dfc_calculation(
            session,
            exercise_id=exercise.id,
            analysis_id=analysis_id,
            calculation=calculation,
        )
        session.commit()
        return calculation
    except DfcCalculationNotFound as exc:
        session.rollback()
        raise DfcContextNotFound(str(exc)) from exc
    except (DfcContextNotFound, KeyError, TypeError, ValueError) as exc:
        session.rollback()
        if isinstance(exc, KeyError):
            raise ValueError("DFC component not found.") from exc
        raise
    except SQLAlchemyError as exc:
        session.rollback()
        raise DfcRunUnavailable("DFC manual decision failed.") from exc


def _calculate(
    session: Session,
    *,
    analysis: AnalysisModel,
    exercise: ExerciseModel,
    year: int,
    methodology: DfcMethodology,
) -> DfcCalculation:
    methodology_version_id = (
        exercise.methodology_version_id or analysis.methodology_version_id
    )
    if methodology.methodology_version_id != methodology_version_id:
        raise ValueError("DFC methodology version differs from analysis.")
    entries = _load_entries(session, exercise_id=exercise.id)
    rows = build_dfc_audit_rows(tuple(entries), methodology, year=year)
    rows = _apply_manual_decisions(
        rows,
        decisions=list_dfc_manual_decisions(session, exercise_id=exercise.id),
        methodology=methodology,
    )
    materiality_base = sum(
        (
            row.movement_value
            for row in rows
            if row.final_status != DfcRowStatus.EXCLUDED
        ),
        Decimal("0.00"),
    )
    return calculate_dfc(
        exercise_year=year,
        audit_rows=rows,
        methodology_version_id=methodology_version_id,
        materiality_base_value=(
            materiality_base if materiality_base > Decimal("0") else None
        ),
        evidences=tuple(
            list_adjustment_evidences(
                session,
                exercise_id=exercise.id,
                method_component=MethodComponent.FCA,
            )
        ),
        methodology_components=methodology.components,
    )


def _load_entries(session: Session, *, exercise_id: int) -> list[DfcEntry]:
    accounts = {
        account.account_code: account
        for account in session.scalars(
            select(EcdI050AccountModel).where(
                EcdI050AccountModel.exercise_id == exercise_id
            )
        )
    }
    links: dict[str, set[str]] = defaultdict(set)
    for link in session.scalars(
        select(EcdI051ReferenceLinkModel).where(
            EcdI051ReferenceLinkModel.exercise_id == exercise_id
        )
    ):
        links[link.account_code].add(link.reference_code)
    for account_code, reference_codes in links.items():
        if len(reference_codes) > 1:
            raise ValueError(
                f"Account {account_code} has multiple distinct I051 reference codes."
            )
    reference_by_account = {
        account_code: next(iter(reference_codes))
        for account_code, reference_codes in links.items()
    }
    entry_models = list(
        session.scalars(
            select(EcdI200EntryModel)
            .where(EcdI200EntryModel.exercise_id == exercise_id)
            .order_by(EcdI200EntryModel.line_number)
        )
    )
    items_by_entry: dict[int, list[EcdI250EntryItemModel]] = defaultdict(list)
    for item in session.scalars(
        select(EcdI250EntryItemModel)
        .join(EcdI200EntryModel)
        .where(EcdI200EntryModel.exercise_id == exercise_id)
        .order_by(EcdI250EntryItemModel.line_number)
    ):
        items_by_entry[item.entry_id].append(item)

    entries: list[DfcEntry] = []
    for entry in entry_models:
        items: list[DfcEntryItem] = []
        for item in items_by_entry.get(entry.id, []):
            if item.debit_credit_indicator not in {"D", "C"}:
                raise ValueError(
                    f"I250 line {item.line_number} has invalid debit/credit indicator."
                )
            account = accounts.get(item.account_code)
            items.append(
                DfcEntryItem(
                    account_code=item.account_code,
                    account_name=(
                        account.account_name if account is not None else item.account_code
                    ),
                    reference_code=reference_by_account.get(item.account_code),
                    amount=item.amount,
                    debit_credit_indicator=item.debit_credit_indicator,
                    history=item.history,
                    line_number=item.line_number,
                )
            )
        entries.append(
            DfcEntry(
                entry_number=entry.entry_number,
                entry_date=entry.entry_date,
                items=tuple(items),
            )
        )
    return entries


def _apply_manual_decisions(
    rows: tuple,
    *,
    decisions: list[DfcManualDecision],
    methodology: DfcMethodology,
) -> tuple:
    latest_by_row = {
        (decision.entry_number, decision.line_number): decision
        for decision in decisions
    }
    result = []
    for row in rows:
        decision = latest_by_row.get((row.entry_number, row.line_number))
        if decision is None:
            result.append(row)
            continue
        if decision.action == DfcDecisionAction.EXCLUDE:
            result.append(
                replace(
                    row,
                    included_value=Decimal("0.00"),
                    final_status=DfcRowStatus.MANUAL_DECISION_APPLIED,
                    pending_reason=None,
                )
            )
            continue
        component = methodology.component(decision.component_code or "")
        included_value = (
            row.movement_value
            if row.cash_flow_direction == CashFlowDirection.INFLOW
            else -row.movement_value
        )
        result.append(
            replace(
                row,
                dfc_activity=decision.activity,
                dfc_component_code=component.code,
                dfc_component_label=component.label,
                included_value=included_value,
                final_status=DfcRowStatus.MANUAL_DECISION_APPLIED,
                pending_reason=None,
            )
        )
    return tuple(result)


def _get_context(
    session: Session,
    *,
    analysis_id: str,
    year: int,
) -> tuple[AnalysisModel, ExerciseModel]:
    analysis = session.get(AnalysisModel, analysis_id)
    if analysis is None:
        raise DfcContextNotFound("Analysis not found.")
    exercise = session.scalar(
        select(ExerciseModel)
        .where(ExerciseModel.analysis_id == analysis_id)
        .where(ExerciseModel.year == year)
    )
    if exercise is None:
        raise DfcContextNotFound("Exercise not found.")
    return analysis, exercise


def _utc_now():
    from datetime import datetime, timezone

    return datetime.now(timezone.utc)
