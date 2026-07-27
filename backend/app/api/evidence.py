from __future__ import annotations

from decimal import Decimal

from fastapi import APIRouter, Depends, HTTPException, Query, Response

from app.application.evidence_service import (
    EvidenceContextNotFound,
    EvidenceOperationUnavailable,
    create_evidence,
    get_asset_valuations,
    get_evidences,
    revise_evidence,
    update_asset_valuation,
)
from app.db.session import SessionLocal
from app.domain import EvidenceStatus, MethodComponent
from app.export import serialize_evidence_workbook
from app.schemas.evidence import (
    AssetValuationListResponse,
    AssetValuationResponse,
    AssetValuationUpdateRequest,
    EvidenceApiErrorResponse,
    EvidenceCreateRequest,
    EvidenceListResponse,
    EvidenceResponse,
    EvidenceUpdateRequest,
)


router = APIRouter(prefix="/api/v1", tags=["evidences"])


def get_evidence_session():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


@router.get(
    "/analyses/{analysis_id}/exercises/{year}/evidences",
    response_model=EvidenceListResponse,
    responses={
        404: {"model": EvidenceApiErrorResponse},
        503: {"model": EvidenceApiErrorResponse},
    },
)
def list_evidences_endpoint(
    analysis_id: str,
    year: int,
    method_component: MethodComponent | None = Query(default=None),
    evidence_status: EvidenceStatus | None = Query(default=None),
    session=Depends(get_evidence_session),
) -> EvidenceListResponse:
    try:
        evidences = get_evidences(
            session,
            analysis_id=analysis_id,
            year=year,
            method_component=method_component,
            evidence_status=evidence_status,
        )
    except EvidenceContextNotFound as exc:
        raise _http_error(404, "EVIDENCE_CONTEXT_NOT_FOUND", str(exc)) from exc
    except EvidenceOperationUnavailable as exc:
        raise _http_error(503, "EVIDENCE_UNAVAILABLE", str(exc)) from exc
    return EvidenceListResponse.from_domain(evidences)


@router.post(
    "/analyses/{analysis_id}/exercises/{year}/evidences",
    response_model=EvidenceResponse,
    status_code=201,
    responses={
        404: {"model": EvidenceApiErrorResponse},
        422: {"model": EvidenceApiErrorResponse},
        503: {"model": EvidenceApiErrorResponse},
    },
)
def create_evidence_endpoint(
    analysis_id: str,
    year: int,
    payload: EvidenceCreateRequest,
    session=Depends(get_evidence_session),
) -> EvidenceResponse:
    try:
        evidence = create_evidence(
            session,
            analysis_id=analysis_id,
            year=year,
            scope_type=payload.scope_type,
            scope_key=payload.scope_key,
            adjustment_type=payload.adjustment_type,
            method_component=payload.method_component,
            amount_impact=Decimal(payload.amount_impact),
            impact_base_value=(
                Decimal(payload.impact_base_value)
                if payload.impact_base_value is not None
                else None
            ),
            required_evidence_type=payload.required_evidence_type,
            evidence_status=payload.evidence_status,
            analyst_justification=payload.analyst_justification,
            review_notes=payload.review_notes,
            can_change_capag_status=payload.can_change_capag_status,
            can_reverse_prudential_sign=(
                payload.can_reverse_prudential_sign
            ),
        )
    except EvidenceContextNotFound as exc:
        raise _http_error(404, "EVIDENCE_CONTEXT_NOT_FOUND", str(exc)) from exc
    except (TypeError, ValueError) as exc:
        raise _http_error(422, "EVIDENCE_CONTRACT_ERROR", str(exc)) from exc
    except EvidenceOperationUnavailable as exc:
        raise _http_error(503, "EVIDENCE_UNAVAILABLE", str(exc)) from exc
    return EvidenceResponse.from_domain(evidence)


@router.put(
    "/evidences/{evidence_id}",
    response_model=EvidenceResponse,
    responses={
        404: {"model": EvidenceApiErrorResponse},
        422: {"model": EvidenceApiErrorResponse},
        503: {"model": EvidenceApiErrorResponse},
    },
)
def revise_evidence_endpoint(
    evidence_id: str,
    payload: EvidenceUpdateRequest,
    session=Depends(get_evidence_session),
) -> EvidenceResponse:
    override = payload.materiality_override
    try:
        evidence = revise_evidence(
            session,
            evidence_id=evidence_id,
            required_evidence_type=payload.required_evidence_type,
            evidence_status=payload.evidence_status,
            analyst_justification=payload.analyst_justification,
            review_notes=payload.review_notes,
            override_level=(
                override.materiality_level if override is not None else None
            ),
            override_justification=(
                override.justification if override is not None else None
            ),
        )
    except EvidenceContextNotFound as exc:
        raise _http_error(404, "EVIDENCE_NOT_FOUND", str(exc)) from exc
    except (TypeError, ValueError) as exc:
        raise _http_error(422, "EVIDENCE_CONTRACT_ERROR", str(exc)) from exc
    except EvidenceOperationUnavailable as exc:
        raise _http_error(503, "EVIDENCE_UNAVAILABLE", str(exc)) from exc
    return EvidenceResponse.from_domain(evidence)


@router.get(
    "/analyses/{analysis_id}/exercises/{year}/assets/valuations",
    response_model=AssetValuationListResponse,
    responses={
        404: {"model": EvidenceApiErrorResponse},
        503: {"model": EvidenceApiErrorResponse},
    },
)
def list_asset_valuations_endpoint(
    analysis_id: str,
    year: int,
    session=Depends(get_evidence_session),
) -> AssetValuationListResponse:
    try:
        assessments = get_asset_valuations(
            session, analysis_id=analysis_id, year=year
        )
    except EvidenceContextNotFound as exc:
        raise _http_error(404, "EVIDENCE_CONTEXT_NOT_FOUND", str(exc)) from exc
    except EvidenceOperationUnavailable as exc:
        raise _http_error(503, "EVIDENCE_UNAVAILABLE", str(exc)) from exc
    return AssetValuationListResponse.from_domain(assessments)


@router.get(
    "/analyses/{analysis_id}/exercises/{year}/evidences/export.xlsx",
    responses={
        200: {
            "content": {
                "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet": {}
            },
            "description": "Evidence and asset valuation workbook.",
        },
        404: {"model": EvidenceApiErrorResponse},
        503: {"model": EvidenceApiErrorResponse},
    },
)
def download_evidence_workbook(
    analysis_id: str,
    year: int,
    session=Depends(get_evidence_session),
) -> Response:
    try:
        evidences = get_evidences(
            session, analysis_id=analysis_id, year=year
        )
        assessments = get_asset_valuations(
            session, analysis_id=analysis_id, year=year
        )
    except EvidenceContextNotFound as exc:
        raise _http_error(404, "EVIDENCE_CONTEXT_NOT_FOUND", str(exc)) from exc
    except EvidenceOperationUnavailable as exc:
        raise _http_error(503, "EVIDENCE_UNAVAILABLE", str(exc)) from exc
    filename = f"capag-evidencias-{analysis_id}-{year}.xlsx"
    return Response(
        content=serialize_evidence_workbook(evidences, assessments),
        media_type=(
            "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        ),
        headers={"Content-Disposition": f'attachment; filename="{filename}"'},
    )


@router.put(
    "/assets/valuations/{assessment_id}",
    response_model=AssetValuationResponse,
    responses={
        404: {"model": EvidenceApiErrorResponse},
        422: {"model": EvidenceApiErrorResponse},
        503: {"model": EvidenceApiErrorResponse},
    },
)
def update_asset_valuation_endpoint(
    assessment_id: str,
    payload: AssetValuationUpdateRequest,
    session=Depends(get_evidence_session),
) -> AssetValuationResponse:
    try:
        assessment = update_asset_valuation(
            session,
            assessment_id=assessment_id,
            analysis_id=payload.analysis_id,
            year=payload.exercise_year,
            account_code=payload.account_code,
            realizability_classification=(
                payload.realizability_classification
            ),
            valuation_required=payload.valuation_required,
            valuation_basis=payload.valuation_basis,
            forced_liquidation_value=(
                Decimal(payload.forced_liquidation_value)
                if payload.forced_liquidation_value is not None
                else None
            ),
            analyst_adjusted_value=(
                Decimal(payload.analyst_adjusted_value)
                if payload.analyst_adjusted_value is not None
                else None
            ),
            essentiality_status=payload.essentiality_status,
            valuation_status=payload.valuation_status,
            evidence_id=payload.evidence_id,
        )
    except EvidenceContextNotFound as exc:
        raise _http_error(404, "ASSET_VALUATION_CONTEXT_NOT_FOUND", str(exc)) from exc
    except (TypeError, ValueError) as exc:
        raise _http_error(422, "ASSET_VALUATION_CONTRACT_ERROR", str(exc)) from exc
    except EvidenceOperationUnavailable as exc:
        raise _http_error(503, "EVIDENCE_UNAVAILABLE", str(exc)) from exc
    return AssetValuationResponse.from_domain(assessment)


def _http_error(status_code: int, error_code: str, message: str) -> HTTPException:
    return HTTPException(
        status_code=status_code,
        detail={"error_code": error_code, "message": message},
    )
