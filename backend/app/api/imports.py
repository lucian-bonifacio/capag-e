from __future__ import annotations

from hashlib import sha256
from typing import Iterator

from fastapi import APIRouter, Depends, File, Form, HTTPException, Response, UploadFile, status
from sqlalchemy.orm import Session

from app.application import (
    EcdImportIdentifiers,
    EcdImportNotFound,
    EcdImportRemovalError,
    EcdPersistenceError,
    ExistingEcdImport,
    get_existing_ecd_import_by_hash,
    list_existing_ecd_imports,
    persist_parsed_ecd,
    reprocess_existing_ecd,
    remove_ecd_import,
)
from app.db.session import SessionLocal
from app.domain import EcdPreparationStatus, ProcessingStatus
from app.io import ECD_PARSER_VERSION, EcdParseError, parse_ecd_bytes
from app.schemas.imports import (
    EcdImportConflictResponse,
    EcdImportDeleteResponse,
    EcdImportListResponse,
    EcdImportResponse,
    ExistingEcdImportResponse,
    ImportApiErrorResponse,
)

router = APIRouter(prefix="/api/v1/ecd", tags=["ecd-import"])

MAX_ECD_UPLOAD_BYTES = 5 * 1024 * 1024
ALLOWED_EXTENSIONS = (".ecd", ".txt")


def get_import_session() -> Iterator[Session]:
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


@router.post(
    "/import",
    response_model=EcdImportResponse,
    status_code=status.HTTP_201_CREATED,
    responses={
        400: {"model": ImportApiErrorResponse},
        409: {"model": EcdImportConflictResponse},
        413: {"model": ImportApiErrorResponse},
    },
)
async def import_ecd(
    response: Response,
    file: UploadFile = File(...),
    methodology_version_id: str = Form("metodologia-2024.1"),
    session: Session = Depends(get_import_session),
) -> EcdImportResponse:
    filename = file.filename or "ecd.txt"
    _validate_filename(filename)
    content = await file.read()
    _validate_size(content)
    digest = sha256(content).hexdigest()
    content_hash = f"sha256:{digest}"

    existing_import = get_existing_ecd_import_by_hash(session, content_hash=content_hash)
    is_reprocessing = (
        existing_import is not None
        and existing_import.preparation_status
        == EcdPreparationStatus.REIMPORT_REQUIRED.value
    )
    if existing_import is not None and not is_reprocessing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail={
                "error_code": "ECD_ALREADY_IMPORTED",
                "message": "Este arquivo ECD ja foi importado.",
                "existing_import": _existing_import_response(existing_import).model_dump(
                    mode="json"
                ),
            },
        )
    session.rollback()

    try:
        parsed = parse_ecd_bytes(content)
    except EcdParseError as exc:
        raise _http_error(
            status.HTTP_400_BAD_REQUEST,
            "ECD_PARSE_ERROR",
            str(exc),
        ) from exc

    try:
        if existing_import is not None:
            result = reprocess_existing_ecd(
                session,
                parsed_ecd=parsed,
                existing_import=existing_import,
                original_content=content,
                parser_version=ECD_PARSER_VERSION,
            )
            response.status_code = status.HTTP_200_OK
        else:
            identifiers = EcdImportIdentifiers(
                company_id=f"company-{parsed.header.tax_id}",
                ecd_file_id=f"ecd-{digest[:16]}",
                analysis_id=f"analysis-{digest[:16]}",
                methodology_version_id=methodology_version_id,
                original_filename=filename,
                content_hash=content_hash,
            )
            result = persist_parsed_ecd(
                session,
                parsed_ecd=parsed,
                identifiers=identifiers,
                original_content=content,
                parser_version=ECD_PARSER_VERSION,
            )
    except EcdPersistenceError as exc:
        raise _http_error(
            status.HTTP_400_BAD_REQUEST,
            "ECD_IMPORT_PERSISTENCE_ERROR",
            "Nao foi possivel persistir a importacao ECD.",
        ) from exc

    return EcdImportResponse(
        analysis_id=result.analysis_id,
        company_id=result.company_id,
        ecd_file_id=result.ecd_file_id,
        year=result.year,
        methodology_version_id=methodology_version_id,
        status=ProcessingStatus.NOT_RUN.value,
        parser_version=ECD_PARSER_VERSION,
        balance_preparation_status=EcdPreparationStatus.READY_FOR_RECONCILIATION.value,
        reprocessed=existing_import is not None,
    )


@router.get("/imports", response_model=EcdImportListResponse)
def list_ecd_imports(session: Session = Depends(get_import_session)) -> EcdImportListResponse:
    return EcdImportListResponse(
        imports=[
            _existing_import_response(existing_import)
            for existing_import in list_existing_ecd_imports(session)
        ]
    )


@router.delete(
    "/imports/{ecd_file_id}",
    response_model=EcdImportDeleteResponse,
    responses={
        404: {"model": ImportApiErrorResponse},
        503: {"model": ImportApiErrorResponse},
    },
)
def delete_ecd_import(
    ecd_file_id: str,
    session: Session = Depends(get_import_session),
) -> EcdImportDeleteResponse:
    try:
        removed = remove_ecd_import(session, ecd_file_id=ecd_file_id)
    except EcdImportNotFound as exc:
        raise _http_error(
            status.HTTP_404_NOT_FOUND,
            "ECD_IMPORT_NOT_FOUND",
            str(exc),
        ) from exc
    except EcdImportRemovalError as exc:
        raise _http_error(
            status.HTTP_503_SERVICE_UNAVAILABLE,
            "ECD_IMPORT_REMOVAL_ERROR",
            "Nao foi possivel remover a importacao ECD.",
        ) from exc

    return EcdImportDeleteResponse(
        ecd_file_id=removed.ecd_file_id,
        analysis_id=removed.analysis_id,
        deleted=True,
    )


def _validate_filename(filename: str) -> None:
    if not filename.lower().endswith(ALLOWED_EXTENSIONS):
        raise _http_error(
            status.HTTP_400_BAD_REQUEST,
            "ECD_INVALID_FILENAME",
            "Arquivo ECD deve usar extensao .ecd ou .txt.",
        )


def _validate_size(content: bytes) -> None:
    if len(content) == 0:
        raise _http_error(
            status.HTTP_400_BAD_REQUEST,
            "ECD_EMPTY_FILE",
            "Arquivo ECD vazio.",
        )
    if len(content) > MAX_ECD_UPLOAD_BYTES:
        raise _http_error(
            status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            "ECD_FILE_TOO_LARGE",
            "Arquivo ECD excede o tamanho maximo permitido.",
        )


def _http_error(status_code: int, error_code: str, message: str) -> HTTPException:
    return HTTPException(
        status_code=status_code,
        detail={
            "error_code": error_code,
            "message": message,
        },
    )


def _existing_import_response(existing_import: ExistingEcdImport) -> ExistingEcdImportResponse:
    return ExistingEcdImportResponse(
        analysis_id=existing_import.analysis_id,
        company_id=existing_import.company_id,
        ecd_file_id=existing_import.ecd_file_id,
        original_filename=existing_import.original_filename,
        content_hash=existing_import.content_hash,
        layout=existing_import.layout,
        period_start=existing_import.period_start,
        period_end=existing_import.period_end,
        imported_at=existing_import.imported_at,
        year=existing_import.year,
        methodology_version_id=existing_import.methodology_version_id,
        status=existing_import.status,
        parser_version=existing_import.parser_version,
        balance_preparation_status=existing_import.preparation_status,
        reprocessed_at=existing_import.reprocessed_at,
    )
