from __future__ import annotations

from collections import defaultdict
from decimal import Decimal

from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.assets.methodology import PlraPolicy, load_plra_policy
from app.assets.reference import load_official_reference_accounts
from app.domain import MethodComponent, PlraAccountInput, PlraCalculation
from app.engine import calculate_plra
from app.engine.methodology_matcher import OfficialReferenceAccount
from app.repositories import (
    AnalysisModel,
    EcdFileModel,
    EcdI050AccountModel,
    EcdI051ReferenceLinkModel,
    EcdI155BalanceModel,
    EcdJ100BalanceRowModel,
    ExerciseModel,
    PlraCalculationNotFound,
    add_plra_calculation,
    get_latest_plra_calculation,
    invalidate_capag_assessments,
    list_adjustment_evidences,
    list_asset_valuations,
)


class PlraContextNotFound(LookupError):
    pass


class PlraRunUnavailable(RuntimeError):
    pass


def run_plra_calculation(
    session: Session,
    *,
    analysis_id: str,
    year: int,
    policy: PlraPolicy | None = None,
    official_references: list[OfficialReferenceAccount] | None = None,
    validated_valuations: dict[str, Decimal] | None = None,
    conditional_decisions: dict[str, bool] | None = None,
    evidence_statuses: dict[str, str] | None = None,
) -> PlraCalculation:
    try:
        analysis, exercise, ecd_file = _get_context(
            session, analysis_id=analysis_id, year=year
        )
        if ecd_file.period_end.month != 12 or ecd_file.period_end.day != 31:
            raise ValueError("PLRA requires an annual exercise ending on 31/12.")
        methodology_version_id = (
            exercise.methodology_version_id or analysis.methodology_version_id
        )
        resolved_policy = policy or load_plra_policy()
        references = official_references or load_official_reference_accounts()
        inputs = _load_account_inputs(
            session,
            exercise_id=exercise.id,
            year=year,
            layout=ecd_file.layout,
            official_references=references,
        )
        j100_available = (
            session.scalar(
                select(EcdJ100BalanceRowModel.id)
                .where(EcdJ100BalanceRowModel.exercise_id == exercise.id)
                .limit(1)
            )
            is not None
        )
        calculation = calculate_plra(
            analysis_id=analysis_id,
            exercise_year=year,
            accounts=inputs,
            policy=resolved_policy,
            methodology_version_id=methodology_version_id,
            validated_valuations=validated_valuations,
            conditional_decisions=conditional_decisions,
            evidence_statuses=evidence_statuses,
            evidences=list_adjustment_evidences(
                session,
                exercise_id=exercise.id,
                method_component=MethodComponent.PLRA,
            ),
            asset_valuations=list_asset_valuations(
                session,
                exercise_id=exercise.id,
            ),
            j100_available=j100_available,
        )
        invalidate_capag_assessments(session, exercise_id=exercise.id)
        add_plra_calculation(
            session,
            exercise_id=exercise.id,
            calculation=calculation,
        )
        session.commit()
        return calculation
    except (PlraContextNotFound, TypeError, ValueError):
        session.rollback()
        raise
    except SQLAlchemyError as exc:
        session.rollback()
        raise PlraRunUnavailable("PLRA calculation run failed.") from exc


def get_plra_calculation(
    session: Session,
    *,
    analysis_id: str,
    year: int,
) -> PlraCalculation:
    try:
        _, exercise, _ = _get_context(session, analysis_id=analysis_id, year=year)
        return get_latest_plra_calculation(session, exercise_id=exercise.id)
    except PlraCalculationNotFound as exc:
        raise PlraContextNotFound(str(exc)) from exc
    except SQLAlchemyError as exc:
        raise PlraRunUnavailable("PLRA calculation query failed.") from exc


def _get_context(
    session: Session,
    *,
    analysis_id: str,
    year: int,
) -> tuple[AnalysisModel, ExerciseModel, EcdFileModel]:
    analysis = session.get(AnalysisModel, analysis_id)
    if analysis is None:
        raise PlraContextNotFound("Analysis not found.")
    exercise = session.scalar(
        select(ExerciseModel)
        .where(ExerciseModel.analysis_id == analysis_id)
        .where(ExerciseModel.year == year)
    )
    if exercise is None:
        raise PlraContextNotFound("Exercise not found.")
    ecd_file = session.get(EcdFileModel, analysis.ecd_file_id)
    if ecd_file is None:
        raise PlraContextNotFound("ECD file not found.")
    return analysis, exercise, ecd_file


def _load_account_inputs(
    session: Session,
    *,
    exercise_id: int,
    year: int,
    layout: str,
    official_references: list[OfficialReferenceAccount],
) -> list[PlraAccountInput]:
    reference_layout = _reference_layout(layout, year)
    accounts = list(
        session.scalars(
            select(EcdI050AccountModel)
            .where(EcdI050AccountModel.exercise_id == exercise_id)
            .order_by(EcdI050AccountModel.line_number)
        )
    )
    links_by_account: dict[str, set[str]] = defaultdict(set)
    for link in session.scalars(
        select(EcdI051ReferenceLinkModel).where(
            EcdI051ReferenceLinkModel.exercise_id == exercise_id
        )
    ):
        links_by_account[link.account_code].add(link.reference_code)
    for account_code, links in links_by_account.items():
        if len(links) > 1:
            raise ValueError(
                f"Account {account_code} has multiple distinct I051 reference codes."
            )
    balances = {
        balance.account_code: balance
        for balance in session.scalars(
            select(EcdI155BalanceModel)
            .where(EcdI155BalanceModel.exercise_id == exercise_id)
            .order_by(EcdI155BalanceModel.line_number)
        )
    }
    official_by_code = {
        reference.reference_code: reference
        for reference in official_references
        if reference.layout == reference_layout
        and reference.entity_type == "PJ_GERAL"
        and reference.status == "ATIVA"
        and year >= reference.valid_from
        and (reference.valid_to is None or year <= reference.valid_to)
    }

    result: list[PlraAccountInput] = []
    for account in accounts:
        reference_code = next(iter(links_by_account.get(account.account_code, ())), None)
        official = official_by_code.get(reference_code) if reference_code else None
        balance = balances.get(account.account_code)
        result.append(
            PlraAccountInput(
                account_code=account.account_code,
                account_name=account.account_name,
                account_type=account.account_type,
                account_level=account.level,
                parent_account_code=account.parent_account_code,
                declared_reference_code=reference_code,
                official_description=(
                    official.official_description if official is not None else None
                ),
                official_nature=official.nature if official is not None else None,
                final_balance=balance.final_balance if balance else Decimal("0.00"),
                final_balance_indicator=(
                    balance.final_balance_indicator if balance else "D"
                ),
            )
        )
    return result


def _reference_layout(layout: str, year: int) -> str:
    if layout == "LECD" and year >= 2020:
        return "ECD_9"
    return layout
