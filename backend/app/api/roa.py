from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, Response

from app.application.roa_service import (
    RoaContextNotFound,
    RoaRunUnavailable,
    create_roa_decision,
    get_roa_result,
    run_roa_calculation,
)
from app.db.session import SessionLocal
from app.export import serialize_roa_workbook
from app.schemas.roa import (
    RoaApiErrorResponse,
    RoaCalculationResponse,
    RoaDecisionRequest,
)


router = APIRouter(
    prefix="/api/v1/analyses/{analysis_id}/exercises/{year}/roa",
    tags=["roa"],
)


def get_roa_session():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


@router.post(
    "/run",
    response_model=RoaCalculationResponse,
    responses={
        404: {"model": RoaApiErrorResponse},
        422: {"model": RoaApiErrorResponse},
        503: {"model": RoaApiErrorResponse},
    },
)
def run_roa_endpoint(
    analysis_id: str,
    year: int,
    session=Depends(get_roa_session),
) -> RoaCalculationResponse:
    try:
        result = run_roa_calculation(
            session,
            analysis_id=analysis_id,
            year=year,
        )
    except RoaContextNotFound as exc:
        raise _http_error(404, "ROA_CONTEXT_NOT_FOUND", str(exc)) from exc
    except (TypeError, ValueError) as exc:
        raise _http_error(422, "ROA_CONTRACT_ERROR", str(exc)) from exc
    except RoaRunUnavailable as exc:
        raise _http_error(503, "ROA_UNAVAILABLE", str(exc)) from exc
    return RoaCalculationResponse.from_result(result)


@router.get(
    "",
    response_model=RoaCalculationResponse,
    responses={
        404: {"model": RoaApiErrorResponse},
        503: {"model": RoaApiErrorResponse},
    },
)
def get_roa_endpoint(
    analysis_id: str,
    year: int,
    session=Depends(get_roa_session),
) -> RoaCalculationResponse:
    try:
        result = get_roa_result(
            session,
            analysis_id=analysis_id,
            year=year,
        )
    except RoaContextNotFound as exc:
        raise _http_error(404, "ROA_NOT_FOUND", str(exc)) from exc
    except RoaRunUnavailable as exc:
        raise _http_error(503, "ROA_UNAVAILABLE", str(exc)) from exc
    return RoaCalculationResponse.from_result(result)


@router.get(
    "/export.xlsx",
    responses={
        200: {
            "content": {
                "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet": {}
            },
            "description": "ROA + PLRA persisted snapshot workbook.",
        },
        404: {"model": RoaApiErrorResponse},
        503: {"model": RoaApiErrorResponse},
    },
)
def download_roa_workbook(
    analysis_id: str,
    year: int,
    session=Depends(get_roa_session),
) -> Response:
    try:
        result = get_roa_result(
            session,
            analysis_id=analysis_id,
            year=year,
        )
    except RoaContextNotFound as exc:
        raise _http_error(404, "ROA_NOT_FOUND", str(exc)) from exc
    except RoaRunUnavailable as exc:
        raise _http_error(503, "ROA_UNAVAILABLE", str(exc)) from exc
    filename = f"capag-roa-{analysis_id}-{year}.xlsx"
    return Response(
        content=serialize_roa_workbook(
            result.calculation,
            analysis_id=analysis_id,
            capag_assessment=result.capag_assessment,
        ),
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": f'attachment; filename="{filename}"'},
    )


@router.post(
    "/decisions",
    response_model=RoaCalculationResponse,
    responses={
        404: {"model": RoaApiErrorResponse},
        422: {"model": RoaApiErrorResponse},
        503: {"model": RoaApiErrorResponse},
    },
)
def create_roa_decision_endpoint(
    analysis_id: str,
    year: int,
    payload: RoaDecisionRequest,
    session=Depends(get_roa_session),
) -> RoaCalculationResponse:
    try:
        result = create_roa_decision(
            session,
            analysis_id=analysis_id,
            year=year,
            action=payload.action,
            account_code=payload.account_code,
            justification=payload.justification,
            evidence_id=payload.evidence_id,
        )
    except RoaContextNotFound as exc:
        raise _http_error(404, "ROA_NOT_FOUND", str(exc)) from exc
    except (TypeError, ValueError) as exc:
        raise _http_error(422, "ROA_DECISION_ERROR", str(exc)) from exc
    except RoaRunUnavailable as exc:
        raise _http_error(503, "ROA_UNAVAILABLE", str(exc)) from exc
    return RoaCalculationResponse.from_result(result)


def _http_error(status_code: int, error_code: str, message: str) -> HTTPException:
    return HTTPException(
        status_code=status_code,
        detail={"error_code": error_code, "message": message},
    )
