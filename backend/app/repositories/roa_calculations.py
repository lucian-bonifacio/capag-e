from __future__ import annotations

from datetime import datetime, timezone
from decimal import Decimal
from typing import Any

from sqlalchemy import (
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
    ComponentStatus,
    RoaAuditRow,
    RoaBlock,
    RoaCalculation,
    RoaComponentSummary,
    RoaDecisionAction,
    RoaManualDecision,
    RoaPendingGroup,
    RoaRowStatus,
)
from app.repositories.declared_snapshots import Base


class RoaCalculationModel(Base):
    __tablename__ = "roa_calculations"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    exercise_id: Mapped[int] = mapped_column(
        ForeignKey("analysis_exercises.id"), nullable=False, index=True
    )
    analysis_id: Mapped[str] = mapped_column(String(64), nullable=False, index=True)
    exercise_year: Mapped[int] = mapped_column(Integer, nullable=False, index=True)
    gross_revenue: Mapped[Decimal] = mapped_column(Numeric(18, 2), nullable=False)
    deductions: Mapped[Decimal] = mapped_column(Numeric(18, 2), nullable=False)
    revenue_taxes: Mapped[Decimal] = mapped_column(Numeric(18, 2), nullable=False)
    net_operating_revenue: Mapped[Decimal] = mapped_column(
        Numeric(18, 2), nullable=False
    )
    operating_costs: Mapped[Decimal] = mapped_column(Numeric(18, 2), nullable=False)
    operating_expenses: Mapped[Decimal] = mapped_column(
        Numeric(18, 2), nullable=False
    )
    financial_result: Mapped[Decimal] = mapped_column(Numeric(18, 2), nullable=False)
    non_operating_result: Mapped[Decimal] = mapped_column(
        Numeric(18, 2), nullable=False
    )
    cash_pressure_adjustments: Mapped[Decimal] = mapped_column(
        Numeric(18, 2), nullable=False
    )
    roa_preliminary: Mapped[Decimal] = mapped_column(Numeric(18, 2), nullable=False)
    roa_final: Mapped[Decimal] = mapped_column(Numeric(18, 2), nullable=False)
    roa_status: Mapped[str] = mapped_column(String(40), nullable=False, index=True)
    alerts_json: Mapped[list[str]] = mapped_column(JSON, nullable=False)
    limitations_json: Mapped[list[str]] = mapped_column(JSON, nullable=False)
    pending_groups_json: Mapped[list[dict[str, Any]]] = mapped_column(
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

    def to_domain(self) -> RoaCalculation:
        snapshot = self.snapshot_json
        return RoaCalculation(
            exercise_year=self.exercise_year,
            gross_revenue=self.gross_revenue,
            deductions=self.deductions,
            revenue_taxes=self.revenue_taxes,
            net_operating_revenue=self.net_operating_revenue,
            operating_costs=self.operating_costs,
            operating_expenses=self.operating_expenses,
            financial_result=self.financial_result,
            non_operating_result=self.non_operating_result,
            cash_pressure_adjustments=self.cash_pressure_adjustments,
            roa_preliminary=self.roa_preliminary,
            roa_final=self.roa_final,
            status=ComponentStatus(self.roa_status),
            component_summaries=tuple(
                RoaComponentSummary(
                    block=item["block"],
                    component_code=item["component_code"],
                    component_label=item["component_label"],
                    value=Decimal(item["value"]),
                    account_count=item["account_count"],
                )
                for item in snapshot["component_summaries"]
            ),
            audit_rows=tuple(
                _audit_row_from_snapshot(item) for item in snapshot["audit_rows"]
            ),
            pending_groups=tuple(
                RoaPendingGroup(
                    code=item["code"],
                    message=item["message"],
                    account_code=item["account_code"],
                    reference_code=item["reference_code"],
                    blocks_roa=item["blocks_roa"],
                    materiality_level=item.get("materiality_level"),
                    evidence_id=item.get("evidence_id"),
                )
                for item in snapshot["pending_groups"]
            ),
            alerts=tuple(self.alerts_json),
            limitations=tuple(self.limitations_json),
            methodology_version_id=self.methodology_version_id,
        )


class RoaAuditRowModel(Base):
    __tablename__ = "roa_audit_rows"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    calculation_id: Mapped[int] = mapped_column(
        ForeignKey("roa_calculations.id"), nullable=False, index=True
    )
    account_code: Mapped[str] = mapped_column(String(64), nullable=False, index=True)
    reference_code: Mapped[str | None] = mapped_column(
        String(64), nullable=True, index=True
    )
    roa_block: Mapped[str | None] = mapped_column(
        String(50), nullable=True, index=True
    )
    component_roa: Mapped[str | None] = mapped_column(
        String(80), nullable=True, index=True
    )
    base_value: Mapped[Decimal] = mapped_column(Numeric(18, 2), nullable=False)
    signed_value: Mapped[Decimal] = mapped_column(Numeric(18, 2), nullable=False)
    final_status: Mapped[str] = mapped_column(String(50), nullable=False, index=True)
    pending_reason: Mapped[str | None] = mapped_column(Text(), nullable=True)
    evidence_id: Mapped[str | None] = mapped_column(String(64), nullable=True)
    line_reference: Mapped[int] = mapped_column(Integer, nullable=False)
    snapshot_json: Mapped[dict[str, Any]] = mapped_column(JSON, nullable=False)


class RoaManualDecisionModel(Base):
    __tablename__ = "roa_manual_decisions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    decision_id: Mapped[str] = mapped_column(
        String(64), nullable=False, unique=True, index=True
    )
    exercise_id: Mapped[int] = mapped_column(
        ForeignKey("analysis_exercises.id"), nullable=False, index=True
    )
    account_code: Mapped[str] = mapped_column(String(64), nullable=False, index=True)
    action: Mapped[str] = mapped_column(String(20), nullable=False)
    justification: Mapped[str] = mapped_column(Text(), nullable=False)
    evidence_id: Mapped[str | None] = mapped_column(
        ForeignKey("adjustment_evidences.evidence_id"), nullable=True
    )
    decided_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    methodology_version_id: Mapped[str] = mapped_column(
        String(120), nullable=False, index=True
    )

    def to_domain(self) -> RoaManualDecision:
        return RoaManualDecision(
            decision_id=self.decision_id,
            account_code=self.account_code,
            action=RoaDecisionAction(self.action),
            justification=self.justification,
            evidence_id=self.evidence_id,
            decided_at=_ensure_timezone(self.decided_at),
            methodology_version_id=self.methodology_version_id,
        )


class RoaCalculationNotFound(LookupError):
    pass


def add_roa_calculation(
    session: Session,
    *,
    exercise_id: int,
    analysis_id: str,
    calculation: RoaCalculation,
) -> RoaCalculationModel:
    model = RoaCalculationModel(
        exercise_id=exercise_id,
        analysis_id=analysis_id,
        exercise_year=calculation.exercise_year,
        gross_revenue=calculation.gross_revenue,
        deductions=calculation.deductions,
        revenue_taxes=calculation.revenue_taxes,
        net_operating_revenue=calculation.net_operating_revenue,
        operating_costs=calculation.operating_costs,
        operating_expenses=calculation.operating_expenses,
        financial_result=calculation.financial_result,
        non_operating_result=calculation.non_operating_result,
        cash_pressure_adjustments=calculation.cash_pressure_adjustments,
        roa_preliminary=calculation.roa_preliminary,
        roa_final=calculation.roa_final,
        roa_status=calculation.status.value,
        alerts_json=list(calculation.alerts),
        limitations_json=list(calculation.limitations),
        pending_groups_json=[
            group.to_snapshot() for group in calculation.pending_groups
        ],
        methodology_version_id=calculation.methodology_version_id,
        snapshot_json=calculation.to_snapshot(),
    )
    session.add(model)
    session.flush()
    for row in calculation.audit_rows:
        session.add(
            RoaAuditRowModel(
                calculation_id=model.id,
                account_code=row.account_code,
                reference_code=row.reference_code,
                roa_block=row.roa_block.value if row.roa_block else None,
                component_roa=row.component_roa,
                base_value=row.base_value,
                signed_value=row.signed_value,
                final_status=row.final_status.value,
                pending_reason=row.pending_reason,
                evidence_id=row.evidence_id,
                line_reference=row.line_reference,
                snapshot_json=row.to_snapshot(),
            )
        )
    return model


def get_latest_roa_calculation(
    session: Session,
    *,
    exercise_id: int,
) -> RoaCalculation:
    model = session.scalar(
        select(RoaCalculationModel)
        .where(RoaCalculationModel.exercise_id == exercise_id)
        .where(RoaCalculationModel.invalidated_at.is_(None))
        .order_by(RoaCalculationModel.id.desc())
        .limit(1)
    )
    if model is None:
        raise RoaCalculationNotFound("ROA calculation not found.")
    return model.to_domain()


def invalidate_roa_calculations(session: Session, *, exercise_id: int) -> int:
    result = session.execute(
        update(RoaCalculationModel)
        .where(RoaCalculationModel.exercise_id == exercise_id)
        .where(RoaCalculationModel.invalidated_at.is_(None))
        .values(invalidated_at=datetime.now(timezone.utc))
    )
    return result.rowcount or 0


def save_roa_manual_decision(
    session: Session,
    *,
    exercise_id: int,
    decision: RoaManualDecision,
) -> RoaManualDecisionModel:
    model = RoaManualDecisionModel(
        decision_id=decision.decision_id,
        exercise_id=exercise_id,
        account_code=decision.account_code,
        action=decision.action.value,
        justification=decision.justification,
        evidence_id=decision.evidence_id,
        decided_at=decision.decided_at,
        methodology_version_id=decision.methodology_version_id,
    )
    session.add(model)
    session.flush()
    return model


def list_roa_manual_decisions(
    session: Session,
    *,
    exercise_id: int,
) -> list[RoaManualDecision]:
    statement = (
        select(RoaManualDecisionModel)
        .where(RoaManualDecisionModel.exercise_id == exercise_id)
        .order_by(RoaManualDecisionModel.id)
    )
    return [model.to_domain() for model in session.scalars(statement)]


def _audit_row_from_snapshot(snapshot: dict[str, Any]) -> RoaAuditRow:
    return RoaAuditRow(
        account_code=snapshot["account_code"],
        account_name=snapshot["account_name"],
        reference_code=snapshot["reference_code"],
        reference_description=snapshot["reference_description"],
        roa_block=(
            RoaBlock(snapshot["roa_block"]) if snapshot["roa_block"] else None
        ),
        component_roa=snapshot["component_roa"],
        component_label=snapshot["component_label"],
        base_value=Decimal(snapshot["base_value"]),
        signed_value=Decimal(snapshot["signed_value"]),
        treatment=snapshot["treatment"],
        final_status=RoaRowStatus(snapshot["final_status"]),
        pending_reason=snapshot["pending_reason"],
        evidence_id=snapshot["evidence_id"],
        line_reference=snapshot["line_reference"],
        macrogroup=snapshot["macrogroup"],
        required_evidence_type=snapshot["required_evidence_type"],
        source_detail=snapshot["source_detail"],
    )


def _ensure_timezone(value: datetime) -> datetime:
    return value if value.tzinfo is not None else value.replace(tzinfo=timezone.utc)
