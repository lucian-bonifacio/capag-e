from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status

from app.application.declared_service import (
    DeclaredSnapshotReader,
    DeclaredSnapshotsNotFound,
    DeclaredSnapshotsUnavailable,
    SqlAlchemyDeclaredSnapshotReader,
)
from app.db.session import SessionLocal
from app.schemas.declared import (
    ApiErrorResponse,
    DeclaredAccountsResponse,
    DeclaredLayerSummaryResponse,
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


def _http_error(status_code: int, error_code: str, message: str) -> HTTPException:
    return HTTPException(
        status_code=status_code,
        detail={
            "error_code": error_code,
            "message": message,
        },
    )
