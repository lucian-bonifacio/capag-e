from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, Response

from app.application.dfc_service import (
    DfcContextNotFound,
    DfcRunUnavailable,
    create_dfc_decision,
    get_dfc_calculation,
    run_dfc_calculation,
)
from app.db.session import SessionLocal
from app.export import serialize_dfc_workbook
from app.schemas.dfc import (
    DfcApiErrorResponse,
    DfcCalculationResponse,
    DfcDecisionRequest,
)


router = APIRouter(
    prefix="/api/v1/analyses/{analysis_id}/exercises/{year}/dfc",
    tags=["dfc"],
)


def get_dfc_session():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


@router.post(
    "/run",
    response_model=DfcCalculationResponse,
    responses={
        404: {"model": DfcApiErrorResponse},
        422: {"model": DfcApiErrorResponse},
        503: {"model": DfcApiErrorResponse},
    },
)
def run_dfc_endpoint(
    analysis_id: str,
    year: int,
    session=Depends(get_dfc_session),
) -> DfcCalculationResponse:
    try:
        calculation = run_dfc_calculation(
            session,
            analysis_id=analysis_id,
            year=year,
        )
    except DfcContextNotFound as exc:
        raise _http_error(404, "DFC_CONTEXT_NOT_FOUND", str(exc)) from exc
    except (TypeError, ValueError) as exc:
        raise _http_error(422, "DFC_CONTRACT_ERROR", str(exc)) from exc
    except DfcRunUnavailable as exc:
        raise _http_error(503, "DFC_UNAVAILABLE", str(exc)) from exc
    return DfcCalculationResponse.from_domain(calculation)


@router.get(
    "",
    response_model=DfcCalculationResponse,
    responses={
        404: {"model": DfcApiErrorResponse},
        503: {"model": DfcApiErrorResponse},
    },
)
def get_dfc_endpoint(
    analysis_id: str,
    year: int,
    session=Depends(get_dfc_session),
) -> DfcCalculationResponse:
    try:
        calculation = get_dfc_calculation(
            session,
            analysis_id=analysis_id,
            year=year,
        )
    except DfcContextNotFound as exc:
        raise _http_error(404, "DFC_NOT_FOUND", str(exc)) from exc
    except DfcRunUnavailable as exc:
        raise _http_error(503, "DFC_UNAVAILABLE", str(exc)) from exc
    return DfcCalculationResponse.from_domain(calculation)


@router.get(
    "/export.xlsx",
    responses={
        200: {
            "content": {
                "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet": {}
            },
            "description": "DFC/FCA persisted snapshot workbook.",
        },
        404: {"model": DfcApiErrorResponse},
        503: {"model": DfcApiErrorResponse},
    },
)
def download_dfc_workbook(
    analysis_id: str,
    year: int,
    session=Depends(get_dfc_session),
) -> Response:
    try:
        calculation = get_dfc_calculation(
            session,
            analysis_id=analysis_id,
            year=year,
        )
    except DfcContextNotFound as exc:
        raise _http_error(404, "DFC_NOT_FOUND", str(exc)) from exc
    except DfcRunUnavailable as exc:
        raise _http_error(503, "DFC_UNAVAILABLE", str(exc)) from exc
    filename = f"capag-dfc-{analysis_id}-{year}.xlsx"
    return Response(
        content=serialize_dfc_workbook(calculation, analysis_id=analysis_id),
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": f'attachment; filename="{filename}"'},
    )


@router.post(
    "/decisions",
    response_model=DfcCalculationResponse,
    responses={
        404: {"model": DfcApiErrorResponse},
        422: {"model": DfcApiErrorResponse},
        503: {"model": DfcApiErrorResponse},
    },
)
def create_dfc_decision_endpoint(
    analysis_id: str,
    year: int,
    payload: DfcDecisionRequest,
    session=Depends(get_dfc_session),
) -> DfcCalculationResponse:
    try:
        calculation = create_dfc_decision(
            session,
            analysis_id=analysis_id,
            year=year,
            action=payload.action,
            entry_number=payload.entry_number,
            line_number=payload.line_number,
            activity=payload.activity,
            component_code=payload.component_code,
            justification=payload.justification,
            evidence_id=payload.evidence_id,
        )
    except DfcContextNotFound as exc:
        raise _http_error(404, "DFC_NOT_FOUND", str(exc)) from exc
    except (TypeError, ValueError) as exc:
        raise _http_error(422, "DFC_DECISION_ERROR", str(exc)) from exc
    except DfcRunUnavailable as exc:
        raise _http_error(503, "DFC_UNAVAILABLE", str(exc)) from exc
    return DfcCalculationResponse.from_domain(calculation)


def _http_error(status_code: int, error_code: str, message: str) -> HTTPException:
    return HTTPException(
        status_code=status_code,
        detail={"error_code": error_code, "message": message},
    )
