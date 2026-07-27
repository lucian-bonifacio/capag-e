from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, Response

from app.application.plra_service import (
    PlraContextNotFound,
    PlraRunUnavailable,
    get_plra_calculation,
    run_plra_calculation,
)
from app.db.session import SessionLocal
from app.export import serialize_plra_workbook
from app.schemas.plra import (
    PlraApiErrorResponse,
    PlraAuditResponse,
    PlraCalculationResponse,
)


router = APIRouter(
    prefix="/api/v1/analyses/{analysis_id}/exercises/{year}/plra",
    tags=["plra"],
)


def get_plra_session():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


@router.post(
    "/run",
    response_model=PlraCalculationResponse,
    responses={
        404: {"model": PlraApiErrorResponse},
        422: {"model": PlraApiErrorResponse},
        503: {"model": PlraApiErrorResponse},
    },
)
def run_plra_endpoint(
    analysis_id: str,
    year: int,
    session=Depends(get_plra_session),
) -> PlraCalculationResponse:
    try:
        calculation = run_plra_calculation(
            session,
            analysis_id=analysis_id,
            year=year,
        )
    except PlraContextNotFound as exc:
        raise _http_error(404, "PLRA_CONTEXT_NOT_FOUND", str(exc)) from exc
    except (TypeError, ValueError) as exc:
        raise _http_error(422, "PLRA_CONTRACT_ERROR", str(exc)) from exc
    except PlraRunUnavailable as exc:
        raise _http_error(503, "PLRA_UNAVAILABLE", str(exc)) from exc
    return PlraCalculationResponse.from_domain(calculation)


@router.get(
    "",
    response_model=PlraCalculationResponse,
    responses={
        404: {"model": PlraApiErrorResponse},
        503: {"model": PlraApiErrorResponse},
    },
)
def get_plra_endpoint(
    analysis_id: str,
    year: int,
    session=Depends(get_plra_session),
) -> PlraCalculationResponse:
    return PlraCalculationResponse.from_domain(
        _get_calculation(session, analysis_id=analysis_id, year=year)
    )


@router.get(
    "/audit",
    response_model=PlraAuditResponse,
    responses={
        404: {"model": PlraApiErrorResponse},
        503: {"model": PlraApiErrorResponse},
    },
)
def get_plra_audit_endpoint(
    analysis_id: str,
    year: int,
    session=Depends(get_plra_session),
) -> PlraAuditResponse:
    return PlraAuditResponse.from_domain(
        _get_calculation(session, analysis_id=analysis_id, year=year)
    )


@router.get(
    "/export.xlsx",
    responses={
        200: {
            "content": {
                "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet": {}
            },
            "description": "PLRA snapshot Excel workbook.",
        },
        404: {"model": PlraApiErrorResponse},
        503: {"model": PlraApiErrorResponse},
    },
)
def download_plra_workbook(
    analysis_id: str,
    year: int,
    session=Depends(get_plra_session),
) -> Response:
    calculation = _get_calculation(session, analysis_id=analysis_id, year=year)
    filename = f"capag-plra-{analysis_id}-{year}.xlsx"
    return Response(
        content=serialize_plra_workbook(calculation),
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": f'attachment; filename="{filename}"'},
    )


def _get_calculation(session, *, analysis_id: str, year: int):
    try:
        return get_plra_calculation(
            session,
            analysis_id=analysis_id,
            year=year,
        )
    except PlraContextNotFound as exc:
        raise _http_error(404, "PLRA_NOT_FOUND", str(exc)) from exc
    except PlraRunUnavailable as exc:
        raise _http_error(503, "PLRA_UNAVAILABLE", str(exc)) from exc


def _http_error(status_code: int, error_code: str, message: str) -> HTTPException:
    return HTTPException(
        status_code=status_code,
        detail={"error_code": error_code, "message": message},
    )
