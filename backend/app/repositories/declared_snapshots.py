from __future__ import annotations

from datetime import datetime
from decimal import Decimal
from typing import Any

from sqlalchemy import DateTime, Integer, JSON, Numeric, String, func
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column

from app.domain import DeclaredAccountResult


class Base(DeclarativeBase):
    pass


class DeclaredAccountSnapshot(Base):
    __tablename__ = "declared_account_snapshots"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    analysis_id: Mapped[str] = mapped_column(String(64), nullable=False, index=True)
    exercise_year: Mapped[int] = mapped_column(Integer, nullable=False, index=True)
    account_code: Mapped[str] = mapped_column(String(64), nullable=False, index=True)
    account_name: Mapped[str] = mapped_column(String(255), nullable=False)
    declared_reference_code: Mapped[str | None] = mapped_column(String(64), nullable=True)
    official_description: Mapped[str | None] = mapped_column(String(255), nullable=True)
    official_reference_status: Mapped[str | None] = mapped_column(String(80), nullable=True)
    methodology_rule_applied: Mapped[str | None] = mapped_column(String(64), nullable=True)
    methodology_rule_status: Mapped[str | None] = mapped_column(String(80), nullable=True)
    purpose: Mapped[str] = mapped_column(String(80), nullable=False)
    base_value: Mapped[Decimal] = mapped_column(Numeric(18, 2), nullable=False)
    considered_value: Mapped[Decimal] = mapped_column(Numeric(18, 2), nullable=False)
    final_status: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    observation: Mapped[str | None] = mapped_column(String(500), nullable=True)
    recommended_action: Mapped[str | None] = mapped_column(String(120), nullable=True)
    methodology_version_id: Mapped[str] = mapped_column(String(120), nullable=False, index=True)
    snapshot_json: Mapped[dict[str, Any]] = mapped_column(JSON, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )


def add_declared_account_snapshot(
    session: Session,
    *,
    analysis_id: str,
    exercise_year: int,
    result: DeclaredAccountResult,
) -> DeclaredAccountSnapshot:
    snapshot = DeclaredAccountSnapshot(
        analysis_id=analysis_id,
        exercise_year=exercise_year,
        account_code=result.account_code,
        account_name=result.account_name,
        declared_reference_code=result.declared_reference_code,
        official_description=result.official_description,
        official_reference_status=result.official_reference_status,
        methodology_rule_applied=result.methodology_rule_applied,
        methodology_rule_status=result.methodology_rule_status,
        purpose=result.purpose,
        base_value=result.base_value,
        considered_value=result.considered_value,
        final_status=result.final_status,
        observation=result.observation,
        recommended_action=result.recommended_action,
        methodology_version_id=result.methodology_version_id,
        snapshot_json=result.to_snapshot(),
    )
    session.add(snapshot)
    return snapshot
