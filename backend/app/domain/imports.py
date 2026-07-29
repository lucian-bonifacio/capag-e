from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime
from enum import StrEnum


class ProcessingStatus(StrEnum):
    NOT_RUN = "nao_executado"
    PROCESSING = "processando"
    COMPLETED = "concluido"
    COMPLETED_WITH_ISSUES = "concluido_com_pendencias"
    BLOCKED = "bloqueado"
    ERROR = "erro"


class EcdPreparationStatus(StrEnum):
    REIMPORT_REQUIRED = "REIMPORTACAO_NECESSARIA"
    READY_FOR_RECONCILIATION = "PRONTA_PARA_CONCILIACAO"


TERMINAL_PROCESSING_STATUSES = frozenset(
    {
        ProcessingStatus.COMPLETED,
        ProcessingStatus.COMPLETED_WITH_ISSUES,
        ProcessingStatus.BLOCKED,
        ProcessingStatus.ERROR,
    }
)


@dataclass(frozen=True)
class Company:
    company_id: str
    legal_name: str
    tax_id: str


@dataclass(frozen=True)
class EcdFile:
    ecd_file_id: str
    company_id: str
    original_filename: str
    content_hash: str
    layout: str
    period_start: date
    period_end: date
    original_content: bytes | None = None
    content_size: int | None = None
    parser_version: str | None = None
    imported_at: datetime | None = None
    reprocessed_at: datetime | None = None


@dataclass(frozen=True)
class Analysis:
    analysis_id: str
    company_id: str
    ecd_file_id: str
    methodology_version_id: str
    status: ProcessingStatus = ProcessingStatus.NOT_RUN

    def transition_to(self, next_status: ProcessingStatus) -> "Analysis":
        _validate_transition(self.status, next_status)
        return Analysis(
            analysis_id=self.analysis_id,
            company_id=self.company_id,
            ecd_file_id=self.ecd_file_id,
            methodology_version_id=self.methodology_version_id,
            status=next_status,
        )


@dataclass(frozen=True)
class Exercise:
    analysis_id: str
    year: int
    status: ProcessingStatus = ProcessingStatus.NOT_RUN
    methodology_version_id: str | None = None

    def transition_to(self, next_status: ProcessingStatus) -> "Exercise":
        _validate_transition(self.status, next_status)
        return Exercise(
            analysis_id=self.analysis_id,
            year=self.year,
            status=next_status,
            methodology_version_id=self.methodology_version_id,
        )


def _validate_transition(
    current_status: ProcessingStatus,
    next_status: ProcessingStatus,
) -> None:
    if current_status in TERMINAL_PROCESSING_STATUSES and next_status == ProcessingStatus.PROCESSING:
        raise ValueError("Cannot transition terminal processing status back to processing.")
