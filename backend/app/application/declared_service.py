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
    EcdJ100BalanceRowModel,
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
class DeclaredBalanceConsistencyWarning:
    warning_code: str
    account_code: str
    account_name: str
    message: str


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

    def list_balance_accounts(
        self,
        *,
        analysis_id: str,
        year: int,
    ) -> list[DeclaredAccountSnapshotView]:
        ...

    def list_balance_consistency_warnings(
        self,
        *,
        analysis_id: str,
        year: int,
    ) -> list[DeclaredBalanceConsistencyWarning]:
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

    def list_balance_accounts(
        self,
        *,
        analysis_id: str,
        year: int,
    ) -> list[DeclaredAccountSnapshotView]:
        raise DeclaredSnapshotsUnavailable("Declared snapshot reader is not configured.")

    def list_balance_consistency_warnings(
        self,
        *,
        analysis_id: str,
        year: int,
    ) -> list[DeclaredBalanceConsistencyWarning]:
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

    def list_balance_accounts(
        self,
        *,
        analysis_id: str,
        year: int,
    ) -> list[DeclaredAccountSnapshotView]:
        exercise = self._exercise(analysis_id=analysis_id, year=year)
        if exercise is None:
            raise DeclaredSnapshotsNotFound("Declared snapshot not found.")

        try:
            j100_rows = list(
                self._session.scalars(
                    select(EcdJ100BalanceRowModel)
                    .where(EcdJ100BalanceRowModel.exercise_id == exercise.id)
                    .where(EcdJ100BalanceRowModel.account_code.is_not(None))
                    .order_by(EcdJ100BalanceRowModel.line_number)
                )
            )
        except SQLAlchemyError as exc:
            raise DeclaredSnapshotsUnavailable("Declared snapshot reader failed.") from exc

        account_metadata = self._account_metadata_by_exercise_id(exercise.id)
        j100_rows = self._final_j100_balance_rows(j100_rows, account_metadata)

        if not j100_rows:
            return self.list_accounts(analysis_id=analysis_id, year=year)

        snapshots_by_code = self._snapshot_by_code(analysis_id=analysis_id, year=year)

        views: list[DeclaredAccountSnapshotView] = []
        for row in j100_rows:
            if row.account_code is None:
                continue

            metadata = account_metadata.get(row.account_code)
            snapshot = snapshots_by_code.get(row.account_code)
            views.append(
                DeclaredAccountSnapshotView(
                    account_code=row.account_code,
                    account_name=metadata.account_name if metadata else row.description,
                    account_type=metadata.account_type if metadata else None,
                    account_nature=metadata.account_nature if metadata else None,
                    account_level=metadata.level if metadata else None,
                    parent_account_code=metadata.parent_account_code if metadata else None,
                    account_order=metadata.line_number if metadata else row.line_number,
                    declared_reference_code=(
                        snapshot.declared_reference_code if snapshot is not None else None
                    ),
                    official_description=(
                        snapshot.official_description if snapshot is not None else None
                    ),
                    official_reference_status=(
                        snapshot.official_reference_status if snapshot is not None else None
                    ),
                    methodology_rule_applied=(
                        snapshot.methodology_rule_applied if snapshot is not None else None
                    ),
                    methodology_rule_status=(
                        snapshot.methodology_rule_status if snapshot is not None else None
                    ),
                    purpose=snapshot.purpose if snapshot is not None else "BALANCO_PATRIMONIAL",
                    treatment=(
                        snapshot.snapshot_json.get("treatment") if snapshot is not None else None
                    ),
                    base_value=row.amount,
                    considered_value=row.amount,
                    final_status=snapshot.final_status if snapshot is not None else "J100_DECLARADO",
                    observation=(
                        snapshot.observation
                        if snapshot is not None
                        else "Linha do balanco patrimonial declarada no J100."
                    ),
                    recommended_action=(
                        snapshot.recommended_action if snapshot is not None else None
                    ),
                    methodology_version_id=(
                        snapshot.methodology_version_id
                        if snapshot is not None
                        else exercise.methodology_version_id
                    ),
                )
            )

        return sorted(
            views,
            key=lambda view: (
                view.account_order is None,
                view.account_order or 0,
                view.account_code,
            ),
        )

    def list_balance_consistency_warnings(
        self,
        *,
        analysis_id: str,
        year: int,
    ) -> list[DeclaredBalanceConsistencyWarning]:
        exercise = self._exercise(analysis_id=analysis_id, year=year)
        if exercise is None:
            raise DeclaredSnapshotsNotFound("Declared snapshot not found.")

        try:
            j100_rows = list(
                self._session.scalars(
                    select(EcdJ100BalanceRowModel)
                    .where(EcdJ100BalanceRowModel.exercise_id == exercise.id)
                    .where(EcdJ100BalanceRowModel.account_code.is_not(None))
                    .order_by(EcdJ100BalanceRowModel.line_number)
                )
            )
        except SQLAlchemyError as exc:
            raise DeclaredSnapshotsUnavailable("Declared snapshot reader failed.") from exc

        account_metadata = self._account_metadata_by_exercise_id(exercise.id)
        j100_rows = self._final_j100_balance_rows(j100_rows, account_metadata)
        if not j100_rows:
            return []

        j100_codes = {row.account_code for row in j100_rows if row.account_code is not None}
        warnings: list[DeclaredBalanceConsistencyWarning] = []

        for row in j100_rows:
            if row.account_code is None or row.account_code in account_metadata:
                continue

            warnings.append(
                DeclaredBalanceConsistencyWarning(
                    warning_code="J100_SEM_I050",
                    account_code=row.account_code,
                    account_name=row.description,
                    message="Linha do J100 sem conta correspondente no I050.",
                )
            )

        for account in account_metadata.values():
            if account.account_nature not in {"01", "02", "03"}:
                continue

            if account.account_code in j100_codes:
                continue

            warnings.append(
                DeclaredBalanceConsistencyWarning(
                    warning_code="I050_PATRIMONIAL_SEM_J100",
                    account_code=account.account_code,
                    account_name=account.account_name,
                    message="Conta patrimonial do I050 ausente do ultimo bloco J100.",
                )
            )

        return sorted(
            warnings,
            key=lambda warning: (
                warning.warning_code,
                warning.account_code,
            ),
        )

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

    def _snapshot_by_code(
        self,
        *,
        analysis_id: str,
        year: int,
    ) -> dict[str, DeclaredAccountSnapshot]:
        snapshots = self._list_snapshots(analysis_id=analysis_id, year=year)
        return {snapshot.account_code: snapshot for snapshot in snapshots}

    def _final_j100_balance_rows(
        self,
        rows: list[EcdJ100BalanceRowModel],
        account_metadata: dict[str, EcdI050AccountModel],
    ) -> list[EcdJ100BalanceRowModel]:
        final_block_start = 0
        for index, row in enumerate(rows):
            if row.account_code is None:
                continue

            metadata = account_metadata.get(row.account_code)
            is_asset_root = (
                metadata is not None
                and metadata.account_nature == "01"
                and metadata.level == 1
                and metadata.parent_account_code is None
            )

            if is_asset_root or row.account_code == "1":
                final_block_start = index

        return rows[final_block_start:]

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
