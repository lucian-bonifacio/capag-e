from __future__ import annotations

from datetime import datetime
from decimal import Decimal
from typing import Any

from sqlalchemy import DateTime, ForeignKey, Integer, JSON, Numeric, String, Text, func, select
from sqlalchemy.orm import Mapped, Session, mapped_column

from app.domain import CapagEAssessment
from app.repositories.declared_snapshots import Base


class CapagAssessmentModel(Base):
    __tablename__ = "capag_assessments"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    exercise_id: Mapped[int] = mapped_column(
        ForeignKey("analysis_exercises.id"),
        nullable=False,
        index=True,
    )
    exercise_year: Mapped[int] = mapped_column(Integer, nullable=False, index=True)
    method: Mapped[str] = mapped_column(String(40), nullable=False, index=True)
    plra_value: Mapped[Decimal | None] = mapped_column(Numeric(18, 2), nullable=True)
    plra_status: Mapped[str] = mapped_column(String(40), nullable=False)
    fca_value: Mapped[Decimal | None] = mapped_column(Numeric(18, 2), nullable=True)
    fca_status: Mapped[str] = mapped_column(String(40), nullable=False)
    roa_value: Mapped[Decimal | None] = mapped_column(Numeric(18, 2), nullable=True)
    roa_status: Mapped[str] = mapped_column(String(40), nullable=False)
    capag_e_value: Mapped[Decimal | None] = mapped_column(Numeric(18, 2), nullable=True)
    capag_e_status: Mapped[str] = mapped_column(String(40), nullable=False, index=True)
    unavailable_reason: Mapped[str | None] = mapped_column(Text(), nullable=True)
    calculation_basis: Mapped[str] = mapped_column(Text(), nullable=False)
    methodology_formula: Mapped[str] = mapped_column(Text(), nullable=False)
    warnings_json: Mapped[list[str]] = mapped_column(JSON, nullable=False)
    limitations_json: Mapped[list[str]] = mapped_column(JSON, nullable=False)
    blocking_issues_json: Mapped[list[str]] = mapped_column(JSON, nullable=False)
    methodology_version_id: Mapped[str] = mapped_column(
        String(120),
        nullable=False,
        index=True,
    )
    snapshot_json: Mapped[dict[str, Any]] = mapped_column(JSON, nullable=False)
    invalidated_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True, index=True
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )

    def to_domain(self) -> CapagEAssessment:
        return CapagEAssessment(
            exercise_year=self.exercise_year,
            method=self.method,
            plra_value=self.plra_value,
            plra_status=self.plra_status,
            fca_value=self.fca_value,
            fca_status=self.fca_status,
            roa_value=self.roa_value,
            roa_status=self.roa_status,
            capag_e_value=self.capag_e_value,
            capag_e_status=self.capag_e_status,
            unavailable_reason=self.unavailable_reason,
            calculation_basis=self.calculation_basis,
            methodology_formula=self.methodology_formula,
            warnings=tuple(self.warnings_json),
            limitations=tuple(self.limitations_json),
            blocking_issues=tuple(self.blocking_issues_json),
            methodology_version_id=self.methodology_version_id,
        )


class CapagAssessmentNotFound(LookupError):
    pass


def add_capag_assessment(
    session: Session,
    *,
    exercise_id: int,
    assessment: CapagEAssessment,
) -> CapagAssessmentModel:
    model = CapagAssessmentModel(
        exercise_id=exercise_id,
        exercise_year=assessment.exercise_year,
        method=assessment.method.value,
        plra_value=assessment.plra_value,
        plra_status=assessment.plra_status.value,
        fca_value=assessment.fca_value,
        fca_status=assessment.fca_status.value,
        roa_value=assessment.roa_value,
        roa_status=assessment.roa_status.value,
        capag_e_value=assessment.capag_e_value,
        capag_e_status=assessment.capag_e_status.value,
        unavailable_reason=assessment.unavailable_reason,
        calculation_basis=assessment.calculation_basis,
        methodology_formula=assessment.methodology_formula,
        warnings_json=list(assessment.warnings),
        limitations_json=list(assessment.limitations),
        blocking_issues_json=list(assessment.blocking_issues),
        methodology_version_id=assessment.methodology_version_id,
        snapshot_json=assessment.to_snapshot(),
    )
    session.add(model)
    return model


def get_latest_capag_assessment(
    session: Session,
    *,
    exercise_id: int,
) -> CapagEAssessment:
    model = session.scalar(
        select(CapagAssessmentModel)
        .where(CapagAssessmentModel.exercise_id == exercise_id)
        .where(CapagAssessmentModel.invalidated_at.is_(None))
        .order_by(CapagAssessmentModel.id.desc())
        .limit(1)
    )
    if model is None:
        raise CapagAssessmentNotFound("CAPAG-E assessment not found.")
    return model.to_domain()
