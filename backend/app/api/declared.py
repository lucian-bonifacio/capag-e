from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, Response, status

from app.assets.reference import OfficialReferenceAssetError, load_official_reference_accounts
from app.application.declared_service import (
    DeclaredSnapshotReader,
    DeclaredSnapshotsNotFound,
    DeclaredSnapshotsUnavailable,
    SqlAlchemyDeclaredSnapshotReader,
)
from app.application.declared_run_service import (
    DeclaredOfficialReferenceConfigurationError,
    DeclaredRunFailed,
    DeclaredRunNotFound,
    run_declared_layer,
)
from app.db.session import SessionLocal
from app.engine.methodology_matcher import MethodologyRule, OfficialReferenceAccount
from app.export import serialize_declared_layer_workbook
from app.schemas.declared import (
    ApiErrorResponse,
    DeclaredAccountsResponse,
    DeclaredLayerSummaryResponse,
    DeclaredRunResponse,
)

router = APIRouter(
    prefix="/api/v1/analyses/{analysis_id}/exercises/{year}/declared",
    tags=["declared"],
)


def get_declared_snapshot_reader() -> DeclaredSnapshotReader:
    session = SessionLocal()
    try:
        yield SqlAlchemyDeclaredSnapshotReader(session)
    finally:
        session.close()


def get_declared_run_session():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


def get_official_references() -> list[OfficialReferenceAccount]:
    try:
        return load_official_reference_accounts()
    except OfficialReferenceAssetError as exc:
        raise _http_error(
            status.HTTP_503_SERVICE_UNAVAILABLE,
            "OFFICIAL_REFERENCE_CONFIGURATION_UNAVAILABLE",
            str(exc),
        ) from exc


def get_methodology_rules() -> list[MethodologyRule]:
    return []


@router.post(
    "/run",
    response_model=DeclaredRunResponse,
    responses={
        404: {"model": ApiErrorResponse},
        503: {"model": ApiErrorResponse},
    },
)
def run_declared_layer_endpoint(
    analysis_id: str,
    year: int,
    session=Depends(get_declared_run_session),
    official_references: list[OfficialReferenceAccount] = Depends(get_official_references),
    methodology_rules: list[MethodologyRule] = Depends(get_methodology_rules),
) -> DeclaredRunResponse:
    try:
        result = run_declared_layer(
            session,
            analysis_id=analysis_id,
            year=year,
            official_references=official_references,
            methodology_rules=methodology_rules,
        )
    except DeclaredRunNotFound as exc:
        raise _http_error(
            status.HTTP_404_NOT_FOUND,
            "DECLARED_RUN_NOT_FOUND",
            str(exc),
        ) from exc
    except DeclaredOfficialReferenceConfigurationError as exc:
        raise _http_error(
            status.HTTP_503_SERVICE_UNAVAILABLE,
            "OFFICIAL_REFERENCE_CONFIGURATION_UNAVAILABLE",
            str(exc),
        ) from exc
    except DeclaredRunFailed as exc:
        raise _http_error(
            status.HTTP_503_SERVICE_UNAVAILABLE,
            "DECLARED_RUN_FAILED",
            str(exc),
        ) from exc

    return DeclaredRunResponse(
        analysis_id=result.analysis_id,
        year=result.year,
        status=result.status,
        snapshots_created=result.snapshots_created,
        status_counts=result.status_counts,
    )


@router.get(
    "",
    response_model=DeclaredLayerSummaryResponse,
    responses={
        404: {"model": ApiErrorResponse},
        503: {"model": ApiErrorResponse},
    },
)
def get_declared_layer_summary(
    analysis_id: str,
    year: int,
    reader: DeclaredSnapshotReader = Depends(get_declared_snapshot_reader),
) -> DeclaredLayerSummaryResponse:
    try:
        summary = reader.get_summary(analysis_id=analysis_id, year=year)
    except DeclaredSnapshotsNotFound as exc:
        raise _http_error(
            status.HTTP_404_NOT_FOUND,
            "DECLARED_SNAPSHOT_NOT_FOUND",
            str(exc),
        ) from exc
    except DeclaredSnapshotsUnavailable as exc:
        raise _http_error(
            status.HTTP_503_SERVICE_UNAVAILABLE,
            "DECLARED_SNAPSHOT_READER_UNAVAILABLE",
            str(exc),
        ) from exc

    return DeclaredLayerSummaryResponse.model_validate(summary, from_attributes=True)


@router.get(
    "/accounts",
    response_model=DeclaredAccountsResponse,
    responses={
        404: {"model": ApiErrorResponse},
        503: {"model": ApiErrorResponse},
    },
)
def list_declared_layer_accounts(
    analysis_id: str,
    year: int,
    reader: DeclaredSnapshotReader = Depends(get_declared_snapshot_reader),
) -> DeclaredAccountsResponse:
    try:
        accounts = reader.list_accounts(analysis_id=analysis_id, year=year)
    except DeclaredSnapshotsNotFound as exc:
        raise _http_error(
            status.HTTP_404_NOT_FOUND,
            "DECLARED_SNAPSHOT_NOT_FOUND",
            str(exc),
        ) from exc
    except DeclaredSnapshotsUnavailable as exc:
        raise _http_error(
            status.HTTP_503_SERVICE_UNAVAILABLE,
            "DECLARED_SNAPSHOT_READER_UNAVAILABLE",
            str(exc),
        ) from exc

    return DeclaredAccountsResponse(
        analysis_id=analysis_id,
        year=year,
        accounts=accounts,
    )


@router.get(
    "/balance/accounts",
    response_model=DeclaredAccountsResponse,
    responses={
        404: {"model": ApiErrorResponse},
        503: {"model": ApiErrorResponse},
    },
)
def list_declared_balance_accounts(
    analysis_id: str,
    year: int,
    reader: DeclaredSnapshotReader = Depends(get_declared_snapshot_reader),
) -> DeclaredAccountsResponse:
    try:
        accounts = reader.list_balance_accounts(analysis_id=analysis_id, year=year)
        consistency_warnings = reader.list_balance_consistency_warnings(
            analysis_id=analysis_id,
            year=year,
        )
    except DeclaredSnapshotsNotFound as exc:
        raise _http_error(
            status.HTTP_404_NOT_FOUND,
            "DECLARED_SNAPSHOT_NOT_FOUND",
            str(exc),
        ) from exc
    except DeclaredSnapshotsUnavailable as exc:
        raise _http_error(
            status.HTTP_503_SERVICE_UNAVAILABLE,
            "DECLARED_SNAPSHOT_READER_UNAVAILABLE",
            str(exc),
        ) from exc

    return DeclaredAccountsResponse(
        analysis_id=analysis_id,
        year=year,
        accounts=accounts,
        consistency_warnings=consistency_warnings,
    )


@router.get(
    "/export.xlsx",
    responses={
        200: {
            "content": {
                "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet": {}
            },
            "description": "Declared layer Excel workbook.",
        },
        404: {"model": ApiErrorResponse},
        503: {"model": ApiErrorResponse},
    },
)
def download_declared_layer_workbook(
    analysis_id: str,
    year: int,
    reader: DeclaredSnapshotReader = Depends(get_declared_snapshot_reader),
) -> Response:
    try:
        summary = reader.get_summary(analysis_id=analysis_id, year=year)
        accounts = reader.list_accounts(analysis_id=analysis_id, year=year)
    except DeclaredSnapshotsNotFound as exc:
        raise _http_error(
            status.HTTP_404_NOT_FOUND,
            "DECLARED_SNAPSHOT_NOT_FOUND",
            str(exc),
        ) from exc
    except DeclaredSnapshotsUnavailable as exc:
        raise _http_error(
            status.HTTP_503_SERVICE_UNAVAILABLE,
            "DECLARED_SNAPSHOT_READER_UNAVAILABLE",
            str(exc),
        ) from exc

    payload = serialize_declared_layer_workbook(summary=summary, accounts=accounts)
    filename = f"capag-declarada-{analysis_id}-{year}.xlsx"
    return Response(
        content=payload,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": f'attachment; filename="{filename}"'},
    )


def _http_error(status_code: int, error_code: str, message: str) -> HTTPException:
    return HTTPException(
        status_code=status_code,
        detail={
            "error_code": error_code,
            "message": message,
        },
    )
