from __future__ import annotations

from datetime import datetime, timezone
from decimal import Decimal
from typing import Any

from sqlalchemy import DateTime, ForeignKey, Integer, JSON, Numeric, String, Text, func, select, update
from sqlalchemy.orm import Mapped, Session, mapped_column

from app.domain import (
    ComponentStatus,
    PlraAccountAuditRow,
    PlraCalculation,
    PlraDecisionStatus,
    PlraInclusionStatus,
)
from app.repositories.capag_assessments import CapagAssessmentModel
from app.repositories.declared_snapshots import Base


class PlraCalculationModel(Base):
    __tablename__ = "plra_calculations"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    exercise_id: Mapped[int] = mapped_column(
        ForeignKey("analysis_exercises.id"), nullable=False, index=True
    )
    analysis_id: Mapped[str] = mapped_column(String(64), nullable=False, index=True)
    exercise_year: Mapped[int] = mapped_column(Integer, nullable=False, index=True)
    gross_assets_value: Mapped[Decimal] = mapped_column(Numeric(18, 2), nullable=False)
    gross_economic_liabilities_value: Mapped[Decimal] = mapped_column(
        Numeric(18, 2), nullable=False
    )
    adjusted_assets_value: Mapped[Decimal] = mapped_column(
        Numeric(18, 2), nullable=False
    )
    plr_gross_value: Mapped[Decimal] = mapped_column(Numeric(18, 2), nullable=False)
    plra_value: Mapped[Decimal] = mapped_column(Numeric(18, 2), nullable=False)
    plra_status: Mapped[str] = mapped_column(String(40), nullable=False, index=True)
    calculation_formula: Mapped[str] = mapped_column(Text(), nullable=False)
    pending_accounts_json: Mapped[list[str]] = mapped_column(JSON, nullable=False)
    warnings_json: Mapped[list[str]] = mapped_column(JSON, nullable=False)
    limitations_json: Mapped[list[str]] = mapped_column(JSON, nullable=False)
    blocking_issues_json: Mapped[list[str]] = mapped_column(JSON, nullable=False)
    j100_reconciliation_status: Mapped[str] = mapped_column(
        String(80), nullable=False
    )
    methodology_version_id: Mapped[str] = mapped_column(
        String(120), nullable=False, index=True
    )
    snapshot_json: Mapped[dict[str, Any]] = mapped_column(JSON, nullable=False)
    calculated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    invalidated_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True, index=True
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )

    def to_domain(self) -> PlraCalculation:
        snapshot = self.snapshot_json
        return PlraCalculation(
            analysis_id=self.analysis_id,
            exercise_year=self.exercise_year,
            gross_assets_value=self.gross_assets_value,
            gross_economic_liabilities_value=self.gross_economic_liabilities_value,
            adjusted_assets_value=self.adjusted_assets_value,
            plr_gross_value=self.plr_gross_value,
            plra_value=self.plra_value,
            plra_status=ComponentStatus(self.plra_status),
            calculation_formula=self.calculation_formula,
            account_rows=tuple(
                _audit_row_from_snapshot(row) for row in snapshot["account_rows"]
            ),
            pending_accounts=tuple(self.pending_accounts_json),
            warnings=tuple(self.warnings_json),
            limitations=tuple(self.limitations_json),
            blocking_issues=tuple(self.blocking_issues_json),
            j100_reconciliation_status=self.j100_reconciliation_status,
            methodology_version_id=self.methodology_version_id,
            calculated_at=_ensure_timezone(self.calculated_at),
        )


class PlraAuditRowModel(Base):
    __tablename__ = "plra_audit_rows"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    calculation_id: Mapped[int] = mapped_column(
        ForeignKey("plra_calculations.id"), nullable=False, index=True
    )
    account_code: Mapped[str] = mapped_column(String(64), nullable=False, index=True)
    account_name: Mapped[str] = mapped_column(String(255), nullable=False)
    declared_reference_code: Mapped[str | None] = mapped_column(
        String(64), nullable=True, index=True
    )
    methodology_rule_id: Mapped[str | None] = mapped_column(String(120), nullable=True)
    methodology_group: Mapped[str | None] = mapped_column(String(80), nullable=True)
    macrogroup: Mapped[str | None] = mapped_column(String(80), nullable=True)
    base_value: Mapped[Decimal] = mapped_column(Numeric(18, 2), nullable=False)
    inclusion_status: Mapped[str] = mapped_column(String(50), nullable=False, index=True)
    default_discount_percent: Mapped[Decimal | None] = mapped_column(
        Numeric(8, 6), nullable=True
    )
    default_economic_value: Mapped[Decimal] = mapped_column(
        Numeric(18, 2), nullable=False
    )
    validated_valuation_value: Mapped[Decimal | None] = mapped_column(
        Numeric(18, 2), nullable=True
    )
    final_economic_value: Mapped[Decimal] = mapped_column(
        Numeric(18, 2), nullable=False
    )
    decision_status: Mapped[str] = mapped_column(String(40), nullable=False)
    evidence_status: Mapped[str | None] = mapped_column(String(40), nullable=True)
    reason: Mapped[str] = mapped_column(Text(), nullable=False)
    methodology_version_id: Mapped[str] = mapped_column(
        String(120), nullable=False, index=True
    )
    snapshot_json: Mapped[dict[str, Any]] = mapped_column(JSON, nullable=False)


class PlraCalculationNotFound(LookupError):
    pass


def add_plra_calculation(
    session: Session,
    *,
    exercise_id: int,
    calculation: PlraCalculation,
) -> PlraCalculationModel:
    model = PlraCalculationModel(
        exercise_id=exercise_id,
        analysis_id=calculation.analysis_id,
        exercise_year=calculation.exercise_year,
        gross_assets_value=calculation.gross_assets_value,
        gross_economic_liabilities_value=calculation.gross_economic_liabilities_value,
        adjusted_assets_value=calculation.adjusted_assets_value,
        plr_gross_value=calculation.plr_gross_value,
        plra_value=calculation.plra_value,
        plra_status=calculation.plra_status.value,
        calculation_formula=calculation.calculation_formula,
        pending_accounts_json=list(calculation.pending_accounts),
        warnings_json=list(calculation.warnings),
        limitations_json=list(calculation.limitations),
        blocking_issues_json=list(calculation.blocking_issues),
        j100_reconciliation_status=calculation.j100_reconciliation_status,
        methodology_version_id=calculation.methodology_version_id,
        snapshot_json=calculation.to_snapshot(),
        calculated_at=calculation.calculated_at,
    )
    session.add(model)
    session.flush()
    for row in calculation.account_rows:
        snapshot = row.to_snapshot()
        session.add(
            PlraAuditRowModel(
                calculation_id=model.id,
                account_code=row.account_code,
                account_name=row.account_name,
                declared_reference_code=row.declared_reference_code,
                methodology_rule_id=row.methodology_rule_id,
                methodology_group=row.methodology_group,
                macrogroup=row.macrogroup,
                base_value=row.base_value,
                inclusion_status=row.inclusion_status.value,
                default_discount_percent=row.default_discount_percent,
                default_economic_value=row.default_economic_value,
                validated_valuation_value=row.validated_valuation_value,
                final_economic_value=row.final_economic_value,
                decision_status=row.decision_status.value,
                evidence_status=row.evidence_status,
                reason=row.reason,
                methodology_version_id=row.methodology_version_id,
                snapshot_json=snapshot,
            )
        )
    return model


def get_latest_plra_calculation(
    session: Session,
    *,
    exercise_id: int,
) -> PlraCalculation:
    model = session.scalar(
        select(PlraCalculationModel)
        .where(PlraCalculationModel.exercise_id == exercise_id)
        .where(PlraCalculationModel.invalidated_at.is_(None))
        .order_by(PlraCalculationModel.id.desc())
        .limit(1)
    )
    if model is None:
        raise PlraCalculationNotFound("PLRA calculation not found.")
    return model.to_domain()


def invalidate_capag_assessments(session: Session, *, exercise_id: int) -> int:
    result = session.execute(
        update(CapagAssessmentModel)
        .where(CapagAssessmentModel.exercise_id == exercise_id)
        .where(CapagAssessmentModel.invalidated_at.is_(None))
        .values(invalidated_at=datetime.now(timezone.utc))
    )
    return result.rowcount or 0


def invalidate_plra_calculations(session: Session, *, exercise_id: int) -> int:
    result = session.execute(
        update(PlraCalculationModel)
        .where(PlraCalculationModel.exercise_id == exercise_id)
        .where(PlraCalculationModel.invalidated_at.is_(None))
        .values(invalidated_at=datetime.now(timezone.utc))
    )
    return result.rowcount or 0


def _audit_row_from_snapshot(snapshot: dict[str, Any]) -> PlraAccountAuditRow:
    return PlraAccountAuditRow(
        account_code=snapshot["account_code"],
        account_name=snapshot["account_name"],
        account_type=snapshot["account_type"],
        account_level=snapshot["account_level"],
        parent_account_code=snapshot["parent_account_code"],
        declared_reference_code=snapshot["declared_reference_code"],
        official_description=snapshot["official_description"],
        methodology_rule_id=snapshot["methodology_rule_id"],
        methodology_group=snapshot["methodology_group"],
        macrogroup=snapshot["macrogroup"],
        base_value=Decimal(snapshot["base_value"]),
        sign=snapshot["sign"],
        inclusion_status=PlraInclusionStatus(snapshot["inclusion_status"]),
        default_discount_percent=(
            Decimal(snapshot["default_discount_percent"])
            if snapshot["default_discount_percent"] is not None
            else None
        ),
        default_economic_value=Decimal(snapshot["default_economic_value"]),
        valuation_source=snapshot["valuation_source"],
        validated_valuation_value=(
            Decimal(snapshot["validated_valuation_value"])
            if snapshot["validated_valuation_value"] is not None
            else None
        ),
        final_economic_value=Decimal(snapshot["final_economic_value"]),
        decision_status=PlraDecisionStatus(snapshot["decision_status"]),
        evidence_status=snapshot["evidence_status"],
        reason=snapshot["reason"],
        limitations=tuple(snapshot["limitations"]),
        methodology_version_id=snapshot["methodology_version_id"],
    )


def _ensure_timezone(value: datetime) -> datetime:
    return value if value.tzinfo is not None else value.replace(tzinfo=timezone.utc)
