from __future__ import annotations

from decimal import Decimal

from app.domain import (
    CapagEAssessment,
    CapagEMethod,
    CapagEStatus,
    ComponentStatus,
)
from app.domain.capag import CENT


FORMULAS = {
    CapagEMethod.FCA_PLRA: "CAPAG-E = PLRA + FCA",
    CapagEMethod.ROA_PLRA: "CAPAG-E = PLRA + ROA",
    CapagEMethod.COMPARATIVO_FCA_ROA: (
        "Comparativo: CAPAG-E = PLRA + FCA; CAPAG-E = PLRA + ROA"
    ),
    CapagEMethod.UNDEFINED: "Metodo CAPAG-E nao definido",
}


def calculate_capag_e_assessment(
    *,
    exercise_year: int,
    method: CapagEMethod | str,
    plra_value: Decimal | None,
    plra_status: ComponentStatus | str,
    fca_value: Decimal | None = None,
    fca_status: ComponentStatus | str = ComponentStatus.NOT_CALCULATED,
    roa_value: Decimal | None = None,
    roa_status: ComponentStatus | str = ComponentStatus.NOT_CALCULATED,
    fco_value: Decimal | None = None,
    warnings: tuple[str, ...] | list[str] = (),
    limitations: tuple[str, ...] | list[str] = (),
    blocking_issues: tuple[str, ...] | list[str] = (),
    methodology_version_id: str,
) -> CapagEAssessment:
    resolved_method = CapagEMethod(method)
    resolved_plra_status = ComponentStatus(plra_status)
    resolved_fca_status = ComponentStatus(fca_status)
    resolved_roa_status = ComponentStatus(roa_status)

    _require_optional_decimal("plra_value", plra_value)
    _require_optional_decimal("fca_value", fca_value)
    _require_optional_decimal("roa_value", roa_value)
    _require_optional_decimal("fco_value", fco_value)

    resolved_limitations = list(limitations)
    resolved_warnings = list(warnings)
    resolved_blocking_issues = list(blocking_issues)

    if fco_value is not None:
        if fca_value is not None or resolved_fca_status != ComponentStatus.NOT_CALCULATED:
            raise ValueError("FCO and FCA cannot be supplied for the same assessment")
        fca_value = fco_value
        resolved_fca_status = ComponentStatus.PARTIAL
        resolved_limitations.append(
            "FCA parcial: somente o fluxo de caixa operacional (FCO) esta disponivel."
        )

    component_values = {
        "PLRA": plra_value,
        "FCA": fca_value,
        "ROA": roa_value,
    }
    calculation_basis = _calculation_basis(component_values)

    if resolved_method == CapagEMethod.UNDEFINED:
        resolved_blocking_issues.append("METODO_CAPAG_E_NAO_DEFINIDO")
        return _assessment(
            exercise_year=exercise_year,
            method=resolved_method,
            plra_value=plra_value,
            plra_status=resolved_plra_status,
            fca_value=fca_value,
            fca_status=resolved_fca_status,
            roa_value=roa_value,
            roa_status=resolved_roa_status,
            capag_e_value=None,
            capag_e_status=CapagEStatus.BLOCKED,
            unavailable_reason="Metodo CAPAG-E nao definido.",
            calculation_basis=calculation_basis,
            warnings=resolved_warnings,
            limitations=resolved_limitations,
            blocking_issues=resolved_blocking_issues,
            methodology_version_id=methodology_version_id,
        )

    plra_block = _plra_block(
        value=plra_value,
        status=resolved_plra_status,
    )
    if plra_block is not None:
        final_status, reason, issue = plra_block
        resolved_blocking_issues.append(issue)
        return _assessment(
            exercise_year=exercise_year,
            method=resolved_method,
            plra_value=plra_value,
            plra_status=resolved_plra_status,
            fca_value=fca_value,
            fca_status=resolved_fca_status,
            roa_value=roa_value,
            roa_status=resolved_roa_status,
            capag_e_value=None,
            capag_e_status=final_status,
            unavailable_reason=reason,
            calculation_basis=calculation_basis,
            warnings=resolved_warnings,
            limitations=resolved_limitations,
            blocking_issues=resolved_blocking_issues,
            methodology_version_id=methodology_version_id,
        )

    if resolved_method == CapagEMethod.COMPARATIVO_FCA_ROA:
        return _calculate_comparison(
            exercise_year=exercise_year,
            plra_value=plra_value,
            plra_status=resolved_plra_status,
            fca_value=fca_value,
            fca_status=resolved_fca_status,
            roa_value=roa_value,
            roa_status=resolved_roa_status,
            warnings=resolved_warnings,
            limitations=resolved_limitations,
            blocking_issues=resolved_blocking_issues,
            methodology_version_id=methodology_version_id,
        )

    selected_name = "FCA" if resolved_method == CapagEMethod.FCA_PLRA else "ROA"
    selected_value = fca_value if selected_name == "FCA" else roa_value
    selected_status = resolved_fca_status if selected_name == "FCA" else resolved_roa_status

    capag_e_value, capag_e_status, unavailable_reason = _calculate_selected_path(
        plra_value=plra_value,
        component_name=selected_name,
        component_value=selected_value,
        component_status=selected_status,
        limitations=resolved_limitations,
        blocking_issues=resolved_blocking_issues,
    )
    if resolved_blocking_issues and capag_e_status == CapagEStatus.CALCULATED:
        capag_e_status = CapagEStatus.BLOCKED
        unavailable_reason = "Existem bloqueios registrados para o assessment."

    return _assessment(
        exercise_year=exercise_year,
        method=resolved_method,
        plra_value=plra_value,
        plra_status=resolved_plra_status,
        fca_value=fca_value,
        fca_status=resolved_fca_status,
        roa_value=roa_value,
        roa_status=resolved_roa_status,
        capag_e_value=capag_e_value,
        capag_e_status=capag_e_status,
        unavailable_reason=unavailable_reason,
        calculation_basis=calculation_basis,
        warnings=resolved_warnings,
        limitations=resolved_limitations,
        blocking_issues=resolved_blocking_issues,
        methodology_version_id=methodology_version_id,
    )


def map_plr_ajustado_to_plra(value: Decimal) -> Decimal:
    _require_optional_decimal("plr_ajustado", value)
    return value.quantize(CENT)


def _calculate_selected_path(
    *,
    plra_value: Decimal,
    component_name: str,
    component_value: Decimal | None,
    component_status: ComponentStatus,
    limitations: list[str],
    blocking_issues: list[str],
) -> tuple[Decimal | None, CapagEStatus, str | None]:
    if component_status == ComponentStatus.METHODOLOGY_ERROR:
        blocking_issues.append(f"{component_name}_ERRO_METODOLOGICO")
        return None, CapagEStatus.METHODOLOGY_ERROR, f"{component_name} com erro metodologico."

    if component_status == ComponentStatus.PARTIAL and component_value is not None:
        limitations.append(
            f"Resultado parcial: {component_name} ainda nao possui status calculado."
        )
        return plra_value + component_value, CapagEStatus.PARTIAL, None

    if component_status != ComponentStatus.CALCULATED or component_value is None:
        blocking_issues.append(f"{component_name}_FINAL_INDISPONIVEL")
        return (
            None,
            CapagEStatus.BLOCKED,
            f"{component_name} final indisponivel para o metodo selecionado.",
        )

    return plra_value + component_value, CapagEStatus.CALCULATED, None


def _calculate_comparison(
    *,
    exercise_year: int,
    plra_value: Decimal,
    plra_status: ComponentStatus,
    fca_value: Decimal | None,
    fca_status: ComponentStatus,
    roa_value: Decimal | None,
    roa_status: ComponentStatus,
    warnings: list[str],
    limitations: list[str],
    blocking_issues: list[str],
    methodology_version_id: str,
) -> CapagEAssessment:
    if (
        fca_status == ComponentStatus.METHODOLOGY_ERROR
        or roa_status == ComponentStatus.METHODOLOGY_ERROR
    ):
        blocking_issues.append("CAMINHO_COMPARATIVO_COM_ERRO_METODOLOGICO")
        final_status = CapagEStatus.METHODOLOGY_ERROR
        unavailable_reason = "Um dos caminhos comparativos possui erro metodologico."
    else:
        fca_path = _path_value(plra_value, fca_value, fca_status)
        roa_path = _path_value(plra_value, roa_value, roa_status)
        if fca_path is None and roa_path is None:
            blocking_issues.append("CAMINHOS_COMPARATIVOS_INDISPONIVEIS")
            final_status = CapagEStatus.BLOCKED
            unavailable_reason = "FCA e ROA indisponiveis para comparacao."
        else:
            final_status = CapagEStatus.PARTIAL
            unavailable_reason = None
            limitations.append(
                "Metodo comparativo nao seleciona um resultado final unico."
            )
            if fca_path is not None and roa_path is not None and fca_path != roa_path:
                warnings.append(
                    "Divergencia entre os caminhos PLRA + FCA e PLRA + ROA."
                )

    basis = _comparison_basis(
        plra_value=plra_value,
        fca_value=fca_value,
        fca_status=fca_status,
        roa_value=roa_value,
        roa_status=roa_status,
    )
    return _assessment(
        exercise_year=exercise_year,
        method=CapagEMethod.COMPARATIVO_FCA_ROA,
        plra_value=plra_value,
        plra_status=plra_status,
        fca_value=fca_value,
        fca_status=fca_status,
        roa_value=roa_value,
        roa_status=roa_status,
        capag_e_value=None,
        capag_e_status=final_status,
        unavailable_reason=unavailable_reason,
        calculation_basis=basis,
        warnings=warnings,
        limitations=limitations,
        blocking_issues=blocking_issues,
        methodology_version_id=methodology_version_id,
    )


def _path_value(
    plra_value: Decimal,
    component_value: Decimal | None,
    component_status: ComponentStatus,
) -> Decimal | None:
    if component_value is None:
        return None
    if component_status not in {ComponentStatus.CALCULATED, ComponentStatus.PARTIAL}:
        return None
    return (plra_value + component_value).quantize(CENT)


def _plra_block(
    *,
    value: Decimal | None,
    status: ComponentStatus,
) -> tuple[CapagEStatus, str, str] | None:
    if status == ComponentStatus.METHODOLOGY_ERROR:
        return (
            CapagEStatus.METHODOLOGY_ERROR,
            "PLRA com erro metodologico.",
            "PLRA_ERRO_METODOLOGICO",
        )
    if status != ComponentStatus.CALCULATED or value is None:
        return (
            CapagEStatus.BLOCKED,
            "PLRA final indisponivel.",
            "PLRA_FINAL_INDISPONIVEL",
        )
    return None


def _assessment(
    *,
    exercise_year: int,
    method: CapagEMethod,
    plra_value: Decimal | None,
    plra_status: ComponentStatus,
    fca_value: Decimal | None,
    fca_status: ComponentStatus,
    roa_value: Decimal | None,
    roa_status: ComponentStatus,
    capag_e_value: Decimal | None,
    capag_e_status: CapagEStatus,
    unavailable_reason: str | None,
    calculation_basis: str,
    warnings: list[str],
    limitations: list[str],
    blocking_issues: list[str],
    methodology_version_id: str,
) -> CapagEAssessment:
    return CapagEAssessment(
        exercise_year=exercise_year,
        method=method,
        plra_value=plra_value,
        plra_status=plra_status,
        fca_value=fca_value,
        fca_status=fca_status,
        roa_value=roa_value,
        roa_status=roa_status,
        capag_e_value=capag_e_value,
        capag_e_status=capag_e_status,
        unavailable_reason=unavailable_reason,
        calculation_basis=calculation_basis,
        methodology_formula=FORMULAS[method],
        warnings=tuple(warnings),
        limitations=tuple(limitations),
        blocking_issues=tuple(blocking_issues),
        methodology_version_id=methodology_version_id,
    )


def _comparison_basis(
    *,
    plra_value: Decimal,
    fca_value: Decimal | None,
    fca_status: ComponentStatus,
    roa_value: Decimal | None,
    roa_status: ComponentStatus,
) -> str:
    fca_path = _path_value(plra_value, fca_value, fca_status)
    roa_path = _path_value(plra_value, roa_value, roa_status)
    return (
        f"PLRA={_format_decimal(plra_value)}; "
        f"PLRA+FCA={_format_decimal(fca_path)}; "
        f"PLRA+ROA={_format_decimal(roa_path)}"
    )


def _calculation_basis(values: dict[str, Decimal | None]) -> str:
    return "; ".join(
        f"{name}={_format_decimal(value)}" for name, value in values.items()
    )


def _format_decimal(value: Decimal | None) -> str:
    if value is None:
        return "indisponivel"
    return format(value.quantize(CENT), "f")


def _require_optional_decimal(field_name: str, value: object) -> None:
    if value is not None and not isinstance(value, Decimal):
        raise TypeError(f"{field_name} must be Decimal or None")
