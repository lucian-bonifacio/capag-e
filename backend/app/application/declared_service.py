from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal
from typing import Protocol

from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.repositories import (
    AnalysisModel,
    DeclaredAccountSnapshot,
    EcdI050AccountModel,
    ExerciseModel,
)


@dataclass(frozen=True)
class DeclaredAccountSnapshotView:
    account_code: str
    account_name: str
    account_type: str | None
    account_nature: str | None
    account_level: int | None
    parent_account_code: str | None
    account_order: int | None
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

        account_metadata = self._account_metadata_by_code(analysis_id=analysis_id, year=year)
        views = [
            DeclaredAccountSnapshotView(
                account_code=snapshot.account_code,
                account_name=snapshot.account_name,
                account_type=(
                    account_metadata[snapshot.account_code].account_type
                    if snapshot.account_code in account_metadata
                    else None
                ),
                account_nature=(
                    account_metadata[snapshot.account_code].account_nature
                    if snapshot.account_code in account_metadata
                    else None
                ),
                account_level=(
                    account_metadata[snapshot.account_code].level
                    if snapshot.account_code in account_metadata
                    else None
                ),
                parent_account_code=(
                    account_metadata[snapshot.account_code].parent_account_code
                    if snapshot.account_code in account_metadata
                    else None
                ),
                account_order=(
                    account_metadata[snapshot.account_code].line_number
                    if snapshot.account_code in account_metadata
                    else None
                ),
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
        return sorted(
            views,
            key=lambda view: (
                view.account_order is None,
                view.account_order or 0,
                view.account_code,
            ),
        )

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

    def _account_metadata_by_code(
        self,
        *,
        analysis_id: str,
        year: int,
    ) -> dict[str, EcdI050AccountModel]:
        try:
            exercise_id = self._exercise_id(analysis_id=analysis_id, year=year)
            if exercise_id is None:
                return {}

            return self._account_metadata_by_exercise_id(exercise_id)
        except SQLAlchemyError as exc:
            raise DeclaredSnapshotsUnavailable("Declared snapshot reader failed.") from exc

    def _account_metadata_by_exercise_id(
        self,
        exercise_id: int,
    ) -> dict[str, EcdI050AccountModel]:
        try:
            accounts = self._session.scalars(
                select(EcdI050AccountModel).where(EcdI050AccountModel.exercise_id == exercise_id)
            )
            return {account.account_code: account for account in accounts}
        except SQLAlchemyError as exc:
            raise DeclaredSnapshotsUnavailable("Declared snapshot reader failed.") from exc

    def _exercise_id(self, *, analysis_id: str, year: int) -> int | None:
        exercise = self._exercise(analysis_id=analysis_id, year=year)
        return exercise.id if exercise is not None else None

    def _exercise(self, *, analysis_id: str, year: int) -> ExerciseModel | None:
        try:
            return self._session.scalar(
                select(ExerciseModel)
                .join(AnalysisModel, AnalysisModel.id == ExerciseModel.analysis_id)
                .where(AnalysisModel.id == analysis_id)
                .where(ExerciseModel.year == year)
            )
        except SQLAlchemyError as exc:
            raise DeclaredSnapshotsUnavailable("Declared snapshot reader failed.") from exc
