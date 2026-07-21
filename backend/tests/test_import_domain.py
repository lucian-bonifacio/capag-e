from datetime import date

import pytest

from app.domain import Analysis, Company, EcdFile, Exercise, ProcessingStatus


def test_import_domain_contracts_represent_traceable_ecd_analysis() -> None:
    company = Company(
        company_id="company-1",
        legal_name="Empresa Sintetica Ltda",
        tax_id="00000000000100",
    )
    ecd_file = EcdFile(
        ecd_file_id="ecd-file-1",
        company_id=company.company_id,
        original_filename="fixture-valida.txt",
        content_hash="sha256:abc123",
        layout="ECD_2024",
        period_start=date(2024, 1, 1),
        period_end=date(2024, 12, 31),
    )
    analysis = Analysis(
        analysis_id="analysis-1",
        company_id=company.company_id,
        ecd_file_id=ecd_file.ecd_file_id,
        methodology_version_id="metodologia-2024.1",
    )
    exercise = Exercise(
        analysis_id=analysis.analysis_id,
        year=2024,
        methodology_version_id=analysis.methodology_version_id,
    )

    assert analysis.status == ProcessingStatus.NOT_RUN
    assert exercise.status == ProcessingStatus.NOT_RUN
    assert ecd_file.content_hash == "sha256:abc123"
    assert ecd_file.layout == "ECD_2024"


def test_processing_status_transitions_are_serializable_and_represent_partial_result() -> None:
    analysis = Analysis(
        analysis_id="analysis-1",
        company_id="company-1",
        ecd_file_id="ecd-file-1",
        methodology_version_id="metodologia-2024.1",
    )

    processing = analysis.transition_to(ProcessingStatus.PROCESSING)
    partial = processing.transition_to(ProcessingStatus.COMPLETED_WITH_ISSUES)

    assert processing.status.value == "processando"
    assert partial.status.value == "concluido_com_pendencias"


def test_terminal_status_cannot_return_to_processing() -> None:
    exercise = Exercise(
        analysis_id="analysis-1",
        year=2024,
        status=ProcessingStatus.ERROR,
    )

    with pytest.raises(ValueError, match="terminal processing status"):
        exercise.transition_to(ProcessingStatus.PROCESSING)
