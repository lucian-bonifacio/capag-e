from __future__ import annotations

from copy import copy
from decimal import Decimal
from io import BytesIO

from openpyxl import Workbook
from openpyxl.worksheet.worksheet import Worksheet

from app.domain import CapagEAssessment


CONTRACT_HEADERS = [
    "exercicio",
    "metodo",
    "formula",
    "plra",
    "status_plra",
    "fca",
    "status_fca",
    "roa",
    "status_roa",
    "capag_e",
    "status_final",
    "limitacoes_metodologicas",
    "warnings",
    "bloqueios",
    "versao_metodologica",
    "motivo_indisponibilidade",
    "base_calculo",
    "status_balanco_declarado",
    "sem_recalculo",
]


def build_capag_assessment_workbook(
    assessment: CapagEAssessment,
) -> Workbook:
    workbook = Workbook()
    sheet = workbook.active
    sheet.title = "contrato_capag_e"
    sheet.append(CONTRACT_HEADERS)
    sheet.append(
        [
            assessment.exercise_year,
            assessment.method.value,
            assessment.methodology_formula,
            _decimal_string(assessment.plra_value),
            assessment.plra_status.value,
            _decimal_string(assessment.fca_value),
            assessment.fca_status.value,
            _decimal_string(assessment.roa_value),
            assessment.roa_status.value,
            _decimal_string(assessment.capag_e_value),
            assessment.capag_e_status.value,
            _join_messages(assessment.limitations),
            _join_messages(assessment.warnings),
            _join_messages(assessment.blocking_issues),
            assessment.methodology_version_id,
            assessment.unavailable_reason,
            assessment.calculation_basis,
            assessment.balance_status.value,
            "true",
        ]
    )
    _style_sheet(sheet)
    return workbook


def serialize_capag_assessment_workbook(
    assessment: CapagEAssessment,
) -> bytes:
    workbook = build_capag_assessment_workbook(assessment)
    buffer = BytesIO()
    workbook.save(buffer)
    return buffer.getvalue()


def _decimal_string(value: Decimal | None) -> str | None:
    if value is None:
        return None
    return format(value, "f")


def _join_messages(messages: tuple[str, ...]) -> str:
    return "\n".join(messages)


def _style_sheet(sheet: Worksheet) -> None:
    sheet.freeze_panes = "A2"
    sheet.auto_filter.ref = sheet.dimensions
    for column_cells in sheet.columns:
        values = [str(cell.value) for cell in column_cells if cell.value is not None]
        width = min(max([len(value) for value in values] or [8]) + 2, 42)
        sheet.column_dimensions[column_cells[0].column_letter].width = width
    for cell in sheet[2]:
        alignment = copy(cell.alignment)
        alignment.wrap_text = True
        alignment.vertical = "top"
        cell.alignment = alignment
