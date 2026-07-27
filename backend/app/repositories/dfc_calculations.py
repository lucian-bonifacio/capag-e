from __future__ import annotations

from datetime import date, datetime, timezone
from decimal import Decimal
from typing import Any

from sqlalchemy import (
    Date,
    DateTime,
    ForeignKey,
    Integer,
    JSON,
    Numeric,
    String,
    Text,
    func,
    select,
    update,
)
from sqlalchemy.orm import Mapped, Session, mapped_column

from app.domain import (
    CashFlowDirection,
    ComponentStatus,
    DfcActivity,
    DfcAuditRow,
    DfcCalculation,
    DfcComponentSummary,
    DfcDecisionAction,
    DfcManualDecision,
    DfcPendingIssue,
    DfcRowStatus,
)
from app.repositories.declared_snapshots import Base


class DfcCalculationModel(Base):
    __tablename__ = "dfc_calculations"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    exercise_id: Mapped[int] = mapped_column(
        ForeignKey("analysis_exercises.id"), nullable=False, index=True
    )
    analysis_id: Mapped[str] = mapped_column(String(64), nullable=False, index=True)
    exercise_year: Mapped[int] = mapped_column(Integer, nullable=False, index=True)
    automatic_value: Mapped[Decimal] = mapped_column(Numeric(18, 2), nullable=False)
    operational_flow: Mapped[Decimal] = mapped_column(Numeric(18, 2), nullable=False)
    investment_flow: Mapped[Decimal] = mapped_column(Numeric(18, 2), nullable=False)
    financing_flow: Mapped[Decimal] = mapped_column(Numeric(18, 2), nullable=False)
    manual_adjustments_value: Mapped[Decimal] = mapped_column(
        Numeric(18, 2), nullable=False
    )
    fca_value: Mapped[Decimal] = mapped_column(Numeric(18, 2), nullable=False)
    fca_status: Mapped[str] = mapped_column(String(40), nullable=False, index=True)
    alerts_json: Mapped[list[str]] = mapped_column(JSON, nullable=False)
    limitations_json: Mapped[list[str]] = mapped_column(JSON, nullable=False)
    pending_issues_json: Mapped[list[dict[str, Any]]] = mapped_column(
        JSON, nullable=False
    )
    methodology_version_id: Mapped[str] = mapped_column(
        String(120), nullable=False, index=True
    )
    snapshot_json: Mapped[dict[str, Any]] = mapped_column(JSON, nullable=False)
    calculated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )
    invalidated_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True, index=True
    )

    def to_domain(self) -> DfcCalculation:
        snapshot = self.snapshot_json
        return DfcCalculation(
            exercise_year=self.exercise_year,
            automatic_value=self.automatic_value,
            operational_flow=self.operational_flow,
            investment_flow=self.investment_flow,
            financing_flow=self.financing_flow,
            manual_adjustments_value=self.manual_adjustments_value,
            fca_value=self.fca_value,
            status=ComponentStatus(self.fca_status),
            component_summaries=tuple(
                DfcComponentSummary(
                    activity=item["activity"],
                    component_code=item["component_code"],
                    component_label=item["component_label"],
                    value=Decimal(item["value"]),
                    movement_count=item["movement_count"],
                )
                for item in snapshot["component_summaries"]
            ),
            audit_rows=tuple(
                _audit_row_from_snapshot(item) for item in snapshot["audit_rows"]
            ),
            pending_issues=tuple(
                DfcPendingIssue(
                    code=item["code"],
                    message=item["message"],
                    entry_number=item["entry_number"],
                    line_number=item["line_number"],
                    materiality_level=item["materiality_level"],
                    blocks_fca=item["blocks_fca"],
                )
                for item in snapshot["pending_issues"]
            ),
            alerts=tuple(self.alerts_json),
            limitations=tuple(self.limitations_json),
            methodology_version_id=self.methodology_version_id,
        )


class DfcAuditRowModel(Base):
    __tablename__ = "dfc_audit_rows"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    calculation_id: Mapped[int] = mapped_column(
        ForeignKey("dfc_calculations.id"), nullable=False, index=True
    )
    entry_number: Mapped[str] = mapped_column(String(80), nullable=False, index=True)
    entry_date: Mapped[date | None] = mapped_column(Date(), nullable=True)
    cash_account_code: Mapped[str] = mapped_column(String(64), nullable=False)
    cash_flow_direction: Mapped[str] = mapped_column(String(20), nullable=False)
    counterparty_account_code: Mapped[str] = mapped_column(
        String(64), nullable=False, index=True
    )
    counterparty_reference_code: Mapped[str | None] = mapped_column(
        String(64), nullable=True, index=True
    )
    dfc_activity: Mapped[str] = mapped_column(String(30), nullable=False, index=True)
    dfc_component_code: Mapped[str | None] = mapped_column(
        String(80), nullable=True, index=True
    )
    movement_value: Mapped[Decimal] = mapped_column(Numeric(18, 2), nullable=False)
    included_value: Mapped[Decimal] = mapped_column(Numeric(18, 2), nullable=False)
    final_status: Mapped[str] = mapped_column(String(50), nullable=False, index=True)
    pending_reason: Mapped[str | None] = mapped_column(Text(), nullable=True)
    line_number: Mapped[int] = mapped_column(Integer, nullable=False)
    snapshot_json: Mapped[dict[str, Any]] = mapped_column(JSON, nullable=False)


class DfcManualDecisionModel(Base):
    __tablename__ = "dfc_manual_decisions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    decision_id: Mapped[str] = mapped_column(
        String(64), nullable=False, unique=True, index=True
    )
    exercise_id: Mapped[int] = mapped_column(
        ForeignKey("analysis_exercises.id"), nullable=False, index=True
    )
    entry_number: Mapped[str] = mapped_column(String(80), nullable=False, index=True)
    line_number: Mapped[int] = mapped_column(Integer, nullable=False)
    action: Mapped[str] = mapped_column(String(20), nullable=False)
    activity: Mapped[str | None] = mapped_column(String(30), nullable=True)
    component_code: Mapped[str | None] = mapped_column(String(80), nullable=True)
    justification: Mapped[str] = mapped_column(Text(), nullable=False)
    evidence_id: Mapped[str | None] = mapped_column(
        ForeignKey("adjustment_evidences.evidence_id"), nullable=True
    )
    decided_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    methodology_version_id: Mapped[str] = mapped_column(
        String(120), nullable=False, index=True
    )

    def to_domain(self) -> DfcManualDecision:
        return DfcManualDecision(
            decision_id=self.decision_id,
            entry_number=self.entry_number,
            line_number=self.line_number,
            action=DfcDecisionAction(self.action),
            activity=DfcActivity(self.activity) if self.activity else None,
            component_code=self.component_code,
            justification=self.justification,
            evidence_id=self.evidence_id,
            decided_at=_ensure_timezone(self.decided_at),
            methodology_version_id=self.methodology_version_id,
        )


class DfcCalculationNotFound(LookupError):
    pass


def add_dfc_calculation(
    session: Session,
    *,
    exercise_id: int,
    analysis_id: str,
    calculation: DfcCalculation,
) -> DfcCalculationModel:
    model = DfcCalculationModel(
        exercise_id=exercise_id,
        analysis_id=analysis_id,
        exercise_year=calculation.exercise_year,
        automatic_value=calculation.automatic_value,
        operational_flow=calculation.operational_flow,
        investment_flow=calculation.investment_flow,
        financing_flow=calculation.financing_flow,
        manual_adjustments_value=calculation.manual_adjustments_value,
        fca_value=calculation.fca_value,
        fca_status=calculation.status.value,
        alerts_json=list(calculation.alerts),
        limitations_json=list(calculation.limitations),
        pending_issues_json=[
            issue.to_snapshot() for issue in calculation.pending_issues
        ],
        methodology_version_id=calculation.methodology_version_id,
        snapshot_json=calculation.to_snapshot(),
    )
    session.add(model)
    session.flush()
    for row in calculation.audit_rows:
        session.add(
            DfcAuditRowModel(
                calculation_id=model.id,
                entry_number=row.entry_number,
                entry_date=row.entry_date,
                cash_account_code=row.cash_account_code,
                cash_flow_direction=row.cash_flow_direction.value,
                counterparty_account_code=row.counterparty_account_code,
                counterparty_reference_code=row.counterparty_reference_code,
                dfc_activity=row.dfc_activity.value,
                dfc_component_code=row.dfc_component_code,
                movement_value=row.movement_value,
                included_value=row.included_value,
                final_status=row.final_status.value,
                pending_reason=row.pending_reason,
                line_number=row.line_number,
                snapshot_json=row.to_snapshot(),
            )
        )
    return model


def get_latest_dfc_calculation(
    session: Session,
    *,
    exercise_id: int,
) -> DfcCalculation:
    model = session.scalar(
        select(DfcCalculationModel)
        .where(DfcCalculationModel.exercise_id == exercise_id)
        .where(DfcCalculationModel.invalidated_at.is_(None))
        .order_by(DfcCalculationModel.id.desc())
        .limit(1)
    )
    if model is None:
        raise DfcCalculationNotFound("DFC calculation not found.")
    return model.to_domain()


def invalidate_dfc_calculations(session: Session, *, exercise_id: int) -> int:
    result = session.execute(
        update(DfcCalculationModel)
        .where(DfcCalculationModel.exercise_id == exercise_id)
        .where(DfcCalculationModel.invalidated_at.is_(None))
        .values(invalidated_at=datetime.now(timezone.utc))
    )
    return result.rowcount or 0


def save_dfc_manual_decision(
    session: Session,
    *,
    exercise_id: int,
    decision: DfcManualDecision,
) -> DfcManualDecisionModel:
    model = DfcManualDecisionModel(
        decision_id=decision.decision_id,
        exercise_id=exercise_id,
        entry_number=decision.entry_number,
        line_number=decision.line_number,
        action=decision.action.value,
        activity=decision.activity.value if decision.activity else None,
        component_code=decision.component_code,
        justification=decision.justification,
        evidence_id=decision.evidence_id,
        decided_at=decision.decided_at,
        methodology_version_id=decision.methodology_version_id,
    )
    session.add(model)
    session.flush()
    return model


def list_dfc_manual_decisions(
    session: Session,
    *,
    exercise_id: int,
) -> list[DfcManualDecision]:
    statement = (
        select(DfcManualDecisionModel)
        .where(DfcManualDecisionModel.exercise_id == exercise_id)
        .order_by(DfcManualDecisionModel.id)
    )
    return [model.to_domain() for model in session.scalars(statement)]


def _audit_row_from_snapshot(snapshot: dict[str, Any]) -> DfcAuditRow:
    return DfcAuditRow(
        entry_number=snapshot["entry_number"],
        entry_date=(
            date.fromisoformat(snapshot["entry_date"])
            if snapshot["entry_date"] is not None
            else None
        ),
        cash_account_code=snapshot["cash_account_code"],
        cash_flow_direction=CashFlowDirection(snapshot["cash_flow_direction"]),
        counterparty_account_code=snapshot["counterparty_account_code"],
        counterparty_account_name=snapshot["counterparty_account_name"],
        counterparty_reference_code=snapshot["counterparty_reference_code"],
        dfc_activity=DfcActivity(snapshot["dfc_activity"]),
        dfc_component_code=snapshot["dfc_component_code"],
        dfc_component_label=snapshot["dfc_component_label"],
        movement_value=Decimal(snapshot["movement_value"]),
        included_value=Decimal(snapshot["included_value"]),
        final_status=DfcRowStatus(snapshot["final_status"]),
        pending_reason=snapshot["pending_reason"],
        history=snapshot["history"],
        line_number=snapshot["line_number"],
    )


def _ensure_timezone(value: datetime) -> datetime:
    return value if value.tzinfo is not None else value.replace(tzinfo=timezone.utc)
