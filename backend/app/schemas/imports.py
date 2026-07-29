from __future__ import annotations

from datetime import date, datetime

from pydantic import BaseModel


class EcdImportResponse(BaseModel):
    analysis_id: str
    company_id: str
    ecd_file_id: str
    year: int
    methodology_version_id: str
    status: str
    parser_version: str
    balance_preparation_status: str
    reprocessed: bool


class ExistingEcdImportResponse(BaseModel):
    analysis_id: str
    company_id: str
    ecd_file_id: str
    original_filename: str
    content_hash: str
    layout: str
    period_start: date
    period_end: date
    imported_at: datetime
    year: int
    methodology_version_id: str
    status: str
    parser_version: str | None
    balance_preparation_status: str
    reprocessed_at: datetime | None


class EcdImportConflictResponse(BaseModel):
    error_code: str
    message: str
    existing_import: ExistingEcdImportResponse


class EcdImportListResponse(BaseModel):
    imports: list[ExistingEcdImportResponse]


class EcdImportDeleteResponse(BaseModel):
    ecd_file_id: str
    analysis_id: str
    deleted: bool


class ImportApiErrorResponse(BaseModel):
    error_code: str
    message: str
