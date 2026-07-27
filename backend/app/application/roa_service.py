from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass, replace
from decimal import Decimal
from uuid import uuid4

from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.application.capag_service import calculate_roa_plra_assessment
from app.assets.methodology import RoaMethodology, load_roa_methodology
from app.assets.reference import load_official_reference_accounts
from app.domain import (
    CapagEAssessment,
    MethodComponent,
    RoaAccountInput,
    RoaAuditRow,
    RoaCalculation,
    RoaDecisionAction,
    RoaManualDecision,
    RoaRowStatus,
)
from app.engine import build_roa_audit_rows, calculate_roa
from app.repositories import (
    AdjustmentEvidenceModel,
    AnalysisModel,
    DfcCalculationNotFound,
    EcdI050AccountModel,
    EcdI051ReferenceLinkModel,
    EcdI155BalanceModel,
    ExerciseModel,
    PlraCalculationNotFound,
    RoaCalculationNotFound,
    add_capag_assessment,
    add_roa_calculation,
    get_latest_dfc_calculation,
    get_latest_plra_calculation,
    get_latest_roa_calculation,
    invalidate_capag_assessments,
    invalidate_roa_calculations,
    list_adjustment_evidences,
    list_roa_manual_decisions,
    save_roa_manual_decision,
)


class RoaContextNotFound(LookupError):
    pass


class RoaRunUnavailable(RuntimeError):
    pass


@dataclass(frozen=True)
class RoaResult:
    calculation: RoaCalculation
    capag_assessment: CapagEAssessment | None


def run_roa_calculation(
    session: Session,
    *,
    analysis_id: str,
    year: int,
    methodology: RoaMethodology | None = None,
) -> RoaResult:
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
            methodology=methodology or load_roa_methodology(),
        )
        result = _persist_result(
            session,
            analysis=analysis,
            exercise=exercise,
            calculation=calculation,
        )
        session.commit()
        return result
    except (RoaContextNotFound, TypeError, ValueError):
        session.rollback()
        raise
    except SQLAlchemyError as exc:
        session.rollback()
        raise RoaRunUnavailable("ROA calculation run failed.") from exc


def get_roa_result(
    session: Session,
    *,
    analysis_id: str,
    year: int,
) -> RoaResult:
    try:
        _, exercise = _get_context(session, analysis_id=analysis_id, year=year)
        calculation = get_latest_roa_calculation(
            session,
            exercise_id=exercise.id,
        )
        return RoaResult(
            calculation=calculation,
            capag_assessment=_build_assessment(
                session,
                exercise=exercise,
                calculation=calculation,
            ),
        )
    except RoaCalculationNotFound as exc:
        raise RoaContextNotFound(str(exc)) from exc
    except SQLAlchemyError as exc:
        raise RoaRunUnavailable("ROA calculation query failed.") from exc


def create_roa_decision(
    session: Session,
    *,
    analysis_id: str,
    year: int,
    action: RoaDecisionAction,
    account_code: str,
    justification: str,
    evidence_id: str | None,
) -> RoaResult:
    try:
        analysis, exercise = _get_context(
            session,
            analysis_id=analysis_id,
            year=year,
        )
        current = get_latest_roa_calculation(session, exercise_id=exercise.id)
        row = next(
            (item for item in current.audit_rows if item.account_code == account_code),
            None,
        )
        if row is None:
            raise ValueError("ROA audit row not found for manual decision.")
        resolved_action = RoaDecisionAction(action)
        if (
            resolved_action == RoaDecisionAction.INCLUDE
            and row.final_status == RoaRowStatus.NO_RULE
        ):
            raise ValueError(
                "ROA account without methodology rule cannot be included manually."
            )
        if resolved_action == RoaDecisionAction.INCLUDE and (
            row.final_status != RoaRowStatus.PENDING_REVIEW
        ):
            raise ValueError("Only conditional ROA accounts can be included manually.")
        if evidence_id is not None:
            evidence = session.scalar(
                select(AdjustmentEvidenceModel).where(
                    AdjustmentEvidenceModel.evidence_id == evidence_id
                )
            )
            if evidence is None or evidence.exercise_id != exercise.id:
                raise ValueError("Evidence does not belong to the ROA exercise.")
            if evidence.method_component != MethodComponent.ROA.value:
                raise ValueError("Evidence must belong to ROA.")

        methodology_version_id = (
            exercise.methodology_version_id or analysis.methodology_version_id
        )
        save_roa_manual_decision(
            session,
            exercise_id=exercise.id,
            decision=RoaManualDecision(
                decision_id=f"roa-decision-{uuid4().hex}",
                account_code=account_code,
                action=resolved_action,
                justification=justification,
                evidence_id=evidence_id,
                decided_at=_utc_now(),
                methodology_version_id=methodology_version_id,
            ),
        )
        calculation = _calculate(
            session,
            analysis=analysis,
            exercise=exercise,
            year=year,
            methodology=load_roa_methodology(),
        )
        result = _persist_result(
            session,
            analysis=analysis,
            exercise=exercise,
            calculation=calculation,
        )
        session.commit()
        return result
    except RoaCalculationNotFound as exc:
        session.rollback()
        raise RoaContextNotFound(str(exc)) from exc
    except (RoaContextNotFound, TypeError, ValueError):
        session.rollback()
        raise
    except SQLAlchemyError as exc:
        session.rollback()
        raise RoaRunUnavailable("ROA manual decision failed.") from exc


def _calculate(
    session: Session,
    *,
    analysis: AnalysisModel,
    exercise: ExerciseModel,
    year: int,
    methodology: RoaMethodology,
) -> RoaCalculation:
    methodology_version_id = (
        exercise.methodology_version_id or analysis.methodology_version_id
    )
    if methodology.methodology_version_id != methodology_version_id:
        raise ValueError("ROA methodology version differs from analysis.")
    accounts = _load_accounts(session, exercise_id=exercise.id)
    rows = build_roa_audit_rows(tuple(accounts), methodology)
    rows = _apply_manual_decisions(
        rows,
        accounts={account.account_code: account for account in accounts},
        decisions=list_roa_manual_decisions(session, exercise_id=exercise.id),
        methodology=methodology,
    )
    materiality_base = sum(
        (row.base_value for row in rows if row.final_status != RoaRowStatus.EXCLUDED),
        Decimal("0.00"),
    )
    return calculate_roa(
        exercise_year=year,
        audit_rows=rows,
        methodology=methodology,
        j150_available=False,
        materiality_base_value=(
            materiality_base if materiality_base > Decimal("0") else None
        ),
        evidences=tuple(
            list_adjustment_evidences(
                session,
                exercise_id=exercise.id,
                method_component=MethodComponent.ROA,
            )
        ),
    )


def _load_accounts(
    session: Session,
    *,
    exercise_id: int,
) -> list[RoaAccountInput]:
    accounts = list(
        session.scalars(
            select(EcdI050AccountModel)
            .where(EcdI050AccountModel.exercise_id == exercise_id)
            .where(EcdI050AccountModel.account_nature == "04")
            .where(EcdI050AccountModel.account_type == "A")
            .order_by(EcdI050AccountModel.line_number)
        )
    )
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
    references = {
        account.reference_code: account.official_description
        for account in load_official_reference_accounts()
    }
    balances: dict[str, list[EcdI155BalanceModel]] = defaultdict(list)
    for balance in session.scalars(
        select(EcdI155BalanceModel)
        .where(EcdI155BalanceModel.exercise_id == exercise_id)
        .order_by(EcdI155BalanceModel.line_number)
    ):
        balances[balance.account_code].append(balance)

    result: list[RoaAccountInput] = []
    for account in accounts:
        account_balances = balances.get(account.account_code, [])
        if not account_balances:
            continue
        reference_codes = links.get(account.account_code, set())
        reference_code = next(iter(reference_codes)) if reference_codes else None
        result.append(
            RoaAccountInput(
                account_code=account.account_code,
                account_name=account.account_name,
                reference_code=reference_code,
                reference_description=references.get(reference_code),
                debit_amount=sum(
                    (balance.debit_amount for balance in account_balances),
                    Decimal("0.00"),
                ),
                credit_amount=sum(
                    (balance.credit_amount for balance in account_balances),
                    Decimal("0.00"),
                ),
                line_reference=min(
                    balance.line_number for balance in account_balances
                ),
                balance_nature=_balance_nature(
                    account.account_code,
                    account_balances,
                ),
            )
        )
    return result


def _apply_manual_decisions(
    rows: tuple[RoaAuditRow, ...],
    *,
    accounts: dict[str, RoaAccountInput],
    decisions: list[RoaManualDecision],
    methodology: RoaMethodology,
) -> tuple[RoaAuditRow, ...]:
    latest_by_account = {decision.account_code: decision for decision in decisions}
    result: list[RoaAuditRow] = []
    for row in rows:
        decision = latest_by_account.get(row.account_code)
        if decision is None:
            result.append(row)
            continue
        if decision.action == RoaDecisionAction.EXCLUDE:
            result.append(
                replace(
                    row,
                    signed_value=Decimal("0.00"),
                    final_status=RoaRowStatus.MANUAL_DECISION_APPLIED,
                    pending_reason=None,
                    evidence_id=decision.evidence_id,
                    source_detail=f"Decisao manual: {decision.justification}",
                )
            )
            continue
        rule = methodology.rule_for(row.reference_code)
        account = accounts[row.account_code]
        if rule is None or row.final_status != RoaRowStatus.PENDING_REVIEW:
            raise ValueError(
                f"Account {row.account_code} cannot be manually included in ROA."
            )
        if rule.primary_rule == "somar":
            signed_value = (
                row.base_value
                if _side_for(account, rule.natural_side) == rule.natural_side
                else -row.base_value
            )
        elif rule.primary_rule == "subtrair":
            signed_value = (
                -row.base_value
                if _side_for(account, rule.natural_side) == rule.natural_side
                else row.base_value
            )
        elif rule.primary_rule == "aplicar_sinal_contabil":
            effective_side = _side_for(account, rule.natural_side)
            signed_value = (
                row.base_value
                if effective_side == "credito"
                else -row.base_value
                if effective_side == "debito"
                else account.credit_amount - account.debit_amount
            )
        else:
            raise ValueError(
                f"Account {row.account_code} has no includable ROA rule."
            )
        result.append(
            replace(
                row,
                signed_value=signed_value,
                final_status=RoaRowStatus.MANUAL_DECISION_APPLIED,
                pending_reason=None,
                evidence_id=decision.evidence_id,
                source_detail=f"Decisao manual: {decision.justification}",
            )
        )
    return tuple(result)


def _balance_nature(
    account_code: str,
    balances: list[EcdI155BalanceModel],
) -> str | None:
    weighted = {"D": Decimal("0.00"), "C": Decimal("0.00")}
    counts = {"D": 0, "C": 0}
    for balance in balances:
        for amount, indicator in (
            (balance.initial_balance, balance.initial_balance_indicator),
            (balance.final_balance, balance.final_balance_indicator),
        ):
            if indicator not in weighted:
                continue
            counts[indicator] += 1
            if amount > Decimal("0"):
                weighted[indicator] += amount
    if weighted["D"] != weighted["C"]:
        return max(weighted, key=weighted.get)
    if counts["D"] != counts["C"]:
        return max(counts, key=counts.get)
    if counts["D"] == 0:
        return None
    if counts["D"] == counts["C"]:
        raise ValueError(
            f"Account {account_code} has conflicting I155 balance natures."
        )
    return None


def _side_for(account: RoaAccountInput, fallback: str) -> str:
    if account.balance_nature == "C":
        return "credito"
    if account.balance_nature == "D":
        return "debito"
    return fallback


def _persist_result(
    session: Session,
    *,
    analysis: AnalysisModel,
    exercise: ExerciseModel,
    calculation: RoaCalculation,
) -> RoaResult:
    invalidate_roa_calculations(session, exercise_id=exercise.id)
    invalidate_capag_assessments(session, exercise_id=exercise.id)
    add_roa_calculation(
        session,
        exercise_id=exercise.id,
        analysis_id=analysis.id,
        calculation=calculation,
    )
    assessment = _build_assessment(
        session,
        exercise=exercise,
        calculation=calculation,
    )
    if assessment is not None:
        add_capag_assessment(
            session,
            exercise_id=exercise.id,
            assessment=assessment,
        )
    return RoaResult(calculation=calculation, capag_assessment=assessment)


def _build_assessment(
    session: Session,
    *,
    exercise: ExerciseModel,
    calculation: RoaCalculation,
) -> CapagEAssessment | None:
    try:
        plra = get_latest_plra_calculation(session, exercise_id=exercise.id)
    except PlraCalculationNotFound:
        return None
    try:
        fca = get_latest_dfc_calculation(session, exercise_id=exercise.id)
    except DfcCalculationNotFound:
        fca = None
    return calculate_roa_plra_assessment(
        plra=plra,
        roa=calculation,
        fca=fca,
    )


def _get_context(
    session: Session,
    *,
    analysis_id: str,
    year: int,
) -> tuple[AnalysisModel, ExerciseModel]:
    analysis = session.get(AnalysisModel, analysis_id)
    if analysis is None:
        raise RoaContextNotFound("Analysis not found.")
    exercise = session.scalar(
        select(ExerciseModel)
        .where(ExerciseModel.analysis_id == analysis_id)
        .where(ExerciseModel.year == year)
    )
    if exercise is None:
        raise RoaContextNotFound("Exercise not found.")
    return analysis, exercise


def _utc_now():
    from datetime import datetime, timezone

    return datetime.now(timezone.utc)
