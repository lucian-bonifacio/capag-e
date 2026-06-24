from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal
from typing import Protocol

from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.repositories import DeclaredAccountSnapshot


@dataclass(frozen=True)
class DeclaredAccountSnapshotView:
    account_code: str
    account_name: str
    declared_reference_code: str | None
    official_description: str | None
    official_reference_status: str | None
    methodology_rule_applied: str | None
    methodology_rule_status: str | None
    purpose: str
    treatment: str | None
    base_value: Decimal
    considered_value: Decimal
    final_status: str
    observation: str | None
    recommended_action: str | None
    methodology_version_id: str


@dataclass(frozen=True)
class DeclaredLayerSummary:
    analysis_id: str
    year: int
    total_accounts: int
    status_counts: dict[str, int]
    methodology_version_id: str | None


class DeclaredSnapshotReader(Protocol):
    def get_summary(self, *, analysis_id: str, year: int) -> DeclaredLayerSummary:
        ...

    def list_accounts(
        self,
        *,
        analysis_id: str,
        year: int,
    ) -> list[DeclaredAccountSnapshotView]:
        ...


class DeclaredSnapshotsUnavailable(RuntimeError):
    pass


class DeclaredSnapshotsNotFound(LookupError):
    pass


class UnconfiguredDeclaredSnapshotReader:
    def get_summary(self, *, analysis_id: str, year: int) -> DeclaredLayerSummary:
        raise DeclaredSnapshotsUnavailable("Declared snapshot reader is not configured.")

    def list_accounts(
        self,
        *,
        analysis_id: str,
        year: int,
    ) -> list[DeclaredAccountSnapshotView]:
        raise DeclaredSnapshotsUnavailable("Declared snapshot reader is not configured.")


class SqlAlchemyDeclaredSnapshotReader:
    def __init__(self, session: Session) -> None:
        self._session = session

    def get_summary(self, *, analysis_id: str, year: int) -> DeclaredLayerSummary:
        snapshots = self._list_snapshots(analysis_id=analysis_id, year=year)
        if not snapshots:
            raise DeclaredSnapshotsNotFound("Declared snapshot not found.")

        status_counts: dict[str, int] = {}
        methodology_versions: set[str] = set()
        for snapshot in snapshots:
            status_counts[snapshot.final_status] = status_counts.get(snapshot.final_status, 0) + 1
            methodology_versions.add(snapshot.methodology_version_id)

        return DeclaredLayerSummary(
            analysis_id=analysis_id,
            year=year,
            total_accounts=len(snapshots),
            status_counts=status_counts,
            methodology_version_id=(
                next(iter(methodology_versions)) if len(methodology_versions) == 1 else None
            ),
        )

    def list_accounts(
        self,
        *,
        analysis_id: str,
        year: int,
    ) -> list[DeclaredAccountSnapshotView]:
        snapshots = self._list_snapshots(analysis_id=analysis_id, year=year)
        if not snapshots:
            raise DeclaredSnapshotsNotFound("Declared snapshot not found.")

        return [
            DeclaredAccountSnapshotView(
                account_code=snapshot.account_code,
                account_name=snapshot.account_name,
                declared_reference_code=snapshot.declared_reference_code,
                official_description=snapshot.official_description,
                official_reference_status=snapshot.official_reference_status,
                methodology_rule_applied=snapshot.methodology_rule_applied,
                methodology_rule_status=snapshot.methodology_rule_status,
                purpose=snapshot.purpose,
                treatment=snapshot.snapshot_json.get("treatment"),
                base_value=snapshot.base_value,
                considered_value=snapshot.considered_value,
                final_status=snapshot.final_status,
                observation=snapshot.observation,
                recommended_action=snapshot.recommended_action,
                methodology_version_id=snapshot.methodology_version_id,
            )
            for snapshot in snapshots
        ]

    def _list_snapshots(
        self,
        *,
        analysis_id: str,
        year: int,
    ) -> list[DeclaredAccountSnapshot]:
        try:
            return list(
                self._session.scalars(
                    select(DeclaredAccountSnapshot)
                    .where(DeclaredAccountSnapshot.analysis_id == analysis_id)
                    .where(DeclaredAccountSnapshot.exercise_year == year)
                    .order_by(DeclaredAccountSnapshot.account_code, DeclaredAccountSnapshot.id)
                )
            )
        except SQLAlchemyError as exc:
            raise DeclaredSnapshotsUnavailable("Declared snapshot reader failed.") from exc
