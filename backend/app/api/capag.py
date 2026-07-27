from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status

from app.application.capag_service import (
    CapagAssessmentContextNotFound,
    CapagAssessmentUnavailable,
    get_capag_assessment,
    run_capag_assessment,
)
from app.db.session import SessionLocal
from app.schemas.capag import (
    CapagApiErrorResponse,
    CapagAssessmentResponse,
    CapagAssessmentRunRequest,
)


router = APIRouter(
    prefix="/api/v1/analyses/{analysis_id}/exercises/{year}/capag-assessment",
    tags=["capag-assessment"],
)


def get_capag_session():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


@router.post(
    "/run",
    response_model=CapagAssessmentResponse,
    responses={
        404: {"model": CapagApiErrorResponse},
        422: {"model": CapagApiErrorResponse},
        503: {"model": CapagApiErrorResponse},
    },
)
def run_capag_assessment_endpoint(
    analysis_id: str,
    year: int,
    payload: CapagAssessmentRunRequest,
    session=Depends(get_capag_session),
) -> CapagAssessmentResponse:
    try:
        assessment = run_capag_assessment(
            session,
            analysis_id=analysis_id,
            year=year,
            run_input=payload.to_run_input(),
        )
    except CapagAssessmentContextNotFound as exc:
        raise _http_error(404, "CAPAG_ASSESSMENT_CONTEXT_NOT_FOUND", str(exc)) from exc
    except (TypeError, ValueError) as exc:
        raise _http_error(422, "CAPAG_ASSESSMENT_CONTRACT_ERROR", str(exc)) from exc
    except CapagAssessmentUnavailable as exc:
        raise _http_error(503, "CAPAG_ASSESSMENT_UNAVAILABLE", str(exc)) from exc
    return CapagAssessmentResponse.from_domain(assessment)


@router.get(
    "",
    response_model=CapagAssessmentResponse,
    responses={
        404: {"model": CapagApiErrorResponse},
        503: {"model": CapagApiErrorResponse},
    },
)
def get_capag_assessment_endpoint(
    analysis_id: str,
    year: int,
    session=Depends(get_capag_session),
) -> CapagAssessmentResponse:
    try:
        assessment = get_capag_assessment(
            session,
            analysis_id=analysis_id,
            year=year,
        )
    except CapagAssessmentContextNotFound as exc:
        raise _http_error(404, "CAPAG_ASSESSMENT_NOT_FOUND", str(exc)) from exc
    except CapagAssessmentUnavailable as exc:
        raise _http_error(503, "CAPAG_ASSESSMENT_UNAVAILABLE", str(exc)) from exc
    return CapagAssessmentResponse.from_domain(assessment)


def _http_error(status_code: int, error_code: str, message: str) -> HTTPException:
    return HTTPException(
        status_code=status_code,
        detail={"error_code": error_code, "message": message},
    )
