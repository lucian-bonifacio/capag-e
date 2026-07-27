from __future__ import annotations

from dataclasses import replace
from decimal import Decimal

from app.assets.methodology import DfcComponent, DfcMethodology
from app.domain.capag import ComponentStatus
from app.domain.dfc import (
    CashFlowDirection,
    DfcActivity,
    DfcAuditRow,
    DfcCalculation,
    DfcComponentSummary,
    DfcEntry,
    DfcEntryItem,
    DfcManualAdjustment,
    DfcPendingIssue,
    DfcRowStatus,
)
from app.domain.evidence import (
    AdjustmentEvidence,
    EvidenceScopeType,
    EvidenceStatus,
    MaterialityLevel,
    MethodComponent,
)
from app.engine.evidence import calculate_default_materiality


def build_dfc_audit_rows(
    entries: tuple[DfcEntry, ...],
    methodology: DfcMethodology,
    *,
    year: int,
) -> tuple[DfcAuditRow, ...]:
    if not isinstance(entries, tuple):
        raise TypeError("entries must be tuple")
    if isinstance(year, bool) or not isinstance(year, int):
        raise TypeError("year must be int")

    rows: list[DfcAuditRow] = []
    for entry in entries:
        cash_items = [
            item
            for item in entry.items
            if methodology.is_cash_reference(item.reference_code)
        ]
        if not cash_items:
            continue
        counterparties = [
            item
            for item in entry.items
            if not methodology.is_cash_reference(item.reference_code)
        ]
        if not counterparties:
            rows.append(_internal_cash_transfer_row(entry, cash_items))
            continue
        for counterparty in counterparties:
            rows.append(
                _counterparty_row(
                    entry=entry,
                    cash_items=cash_items,
                    counterparty=counterparty,
                    methodology=methodology,
                    year=year,
                )
            )
    return tuple(rows)


def calculate_dfc(
    *,
    exercise_year: int,
    audit_rows: tuple[DfcAuditRow, ...],
    methodology_version_id: str,
    materiality_base_value: Decimal | None,
    evidences: tuple[AdjustmentEvidence, ...] = (),
    manual_adjustments: tuple[DfcManualAdjustment, ...] = (),
    complete_activity_scan: bool = True,
    methodology_components: tuple[DfcComponent, ...] = (),
) -> DfcCalculation:
    if not isinstance(audit_rows, tuple):
        raise TypeError("audit_rows must be tuple")
    if not isinstance(evidences, tuple):
        raise TypeError("evidences must be tuple")
    if not isinstance(manual_adjustments, tuple):
        raise TypeError("manual_adjustments must be tuple")
    if materiality_base_value is not None and not isinstance(
        materiality_base_value, Decimal
    ):
        raise TypeError("materiality_base_value must be Decimal or None")

    rows: list[DfcAuditRow] = []
    issues: list[DfcPendingIssue] = []
    alerts: list[str] = []
    limitations: list[str] = []
    evidence_block = False
    pending_block = False

    for row in audit_rows:
        decision = calculate_default_materiality(
            amount_impact=row.movement_value,
            impact_base_value=materiality_base_value,
        )
        material = decision.materiality_level != MaterialityLevel.LOW
        high_or_critical = decision.materiality_level in {
            MaterialityLevel.HIGH,
            MaterialityLevel.CRITICAL,
        }
        matching_evidences = _matching_evidences(row, evidences)

        if row.final_status in {
            DfcRowStatus.UNCLASSIFIED,
            DfcRowStatus.INCOMPATIBLE_FLOW,
        }:
            blocks = material
            pending_block = pending_block or blocks
            issues.append(
                DfcPendingIssue(
                    code=row.pending_reason or "MOVIMENTO_DFC_PENDENTE",
                    message="Movimento nao classificado exige decisao antes do FCA final.",
                    entry_number=row.entry_number,
                    line_number=row.line_number,
                    materiality_level=decision.materiality_level.value,
                    blocks_fca=blocks,
                )
            )

        if row.final_status == DfcRowStatus.INCLUDED and material:
            if not matching_evidences:
                blocks = high_or_critical
                evidence_block = evidence_block or blocks
                issues.append(
                    DfcPendingIssue(
                        code="EVIDENCIA_MATERIAL_AUSENTE",
                        message="Movimento material incluido sem evidencia vinculada.",
                        entry_number=row.entry_number,
                        line_number=row.line_number,
                        materiality_level=decision.materiality_level.value,
                        blocks_fca=blocks,
                    )
                )
                if blocks:
                    row = replace(
                        row,
                        final_status=DfcRowStatus.PENDING_EVIDENCE,
                        pending_reason="evidencia_material_ausente",
                    )
            else:
                blocking = [evidence for evidence in matching_evidences if evidence.blocks_final_report]
                if blocking:
                    evidence_block = True
                    issues.append(
                        DfcPendingIssue(
                            code="EVIDENCIA_MATERIAL_BLOQUEANTE",
                            message="Evidencia vinculada bloqueia o resultado final.",
                            entry_number=row.entry_number,
                            line_number=row.line_number,
                            materiality_level=decision.materiality_level.value,
                            blocks_fca=True,
                        )
                    )
                    row = replace(
                        row,
                        final_status=DfcRowStatus.PENDING_EVIDENCE,
                        pending_reason="evidencia_material_bloqueante",
                    )
        rows.append(row)

    validated_adjustments = [
        adjustment for adjustment in manual_adjustments if adjustment.validated
    ]
    for adjustment in manual_adjustments:
        if not adjustment.validated:
            pending_block = True
            issues.append(
                DfcPendingIssue(
                    code="AJUSTE_MANUAL_NAO_VALIDADO",
                    message="Ajuste manual nao validado foi excluido do FCA.",
                    entry_number=None,
                    line_number=None,
                    materiality_level=None,
                    blocks_fca=True,
                )
            )

    included_rows = [
        row
        for row in rows
        if row.final_status in {
            DfcRowStatus.INCLUDED,
            DfcRowStatus.PENDING_EVIDENCE,
            DfcRowStatus.MANUAL_DECISION_APPLIED,
        }
    ]
    operational = _activity_sum(included_rows, DfcActivity.OPERATIONAL)
    investment = _activity_sum(included_rows, DfcActivity.INVESTMENT)
    financing = _activity_sum(included_rows, DfcActivity.FINANCING)
    automatic = operational + investment + financing
    manual_value = sum(
        (adjustment.value for adjustment in validated_adjustments),
        Decimal("0.00"),
    )
    fca_value = automatic + manual_value

    if evidence_block:
        status = ComponentStatus.BLOCKED_BY_EVIDENCE
    elif pending_block:
        status = ComponentStatus.BLOCKED_BY_PENDING
    elif not audit_rows:
        status = ComponentStatus.NOT_CALCULATED
        limitations.append("Nenhum movimento com disponibilidades foi identificado.")
    elif not complete_activity_scan:
        status = ComponentStatus.PARTIAL
        limitations.append(
            "FCA parcial: somente o fluxo de caixa operacional (FCO) foi fornecido."
        )
    elif any(
        row.final_status
        in {DfcRowStatus.UNCLASSIFIED, DfcRowStatus.INCOMPATIBLE_FLOW}
        for row in rows
    ):
        status = ComponentStatus.PARTIAL
        limitations.append("Existem movimentos nao classificados de baixa materialidade.")
    else:
        status = ComponentStatus.CALCULATED

    if any(issue.code == "EVIDENCIA_MATERIAL_AUSENTE" and not issue.blocks_fca for issue in issues):
        alerts.append("Existem movimentos materiais com ressalva de evidencia.")

    return DfcCalculation(
        exercise_year=exercise_year,
        automatic_value=automatic,
        operational_flow=operational,
        investment_flow=investment,
        financing_flow=financing,
        manual_adjustments_value=manual_value,
        fca_value=fca_value,
        status=status,
        component_summaries=_component_summaries(
            included_rows,
            methodology_components,
        ),
        audit_rows=tuple(rows),
        pending_issues=tuple(issues),
        alerts=tuple(alerts),
        limitations=tuple(limitations),
        methodology_version_id=methodology_version_id,
    )


def _matching_evidences(
    row: DfcAuditRow,
    evidences: tuple[AdjustmentEvidence, ...],
) -> list[AdjustmentEvidence]:
    movement_keys = {
        row.entry_number,
        f"{row.entry_number}:{row.line_number}",
    }
    matches: list[AdjustmentEvidence] = []
    for evidence in evidences:
        if evidence.method_component != MethodComponent.FCA:
            continue
        if (
            evidence.scope_type == EvidenceScopeType.FCO_MOVEMENT
            and evidence.scope_key in movement_keys
        ) or (
            evidence.scope_type == EvidenceScopeType.DFC_COMPONENT
            and evidence.scope_key == row.dfc_component_code
        ):
            matches.append(evidence)
    return matches


def _activity_sum(rows: list[DfcAuditRow], activity: DfcActivity) -> Decimal:
    return sum(
        (row.included_value for row in rows if row.dfc_activity == activity),
        Decimal("0.00"),
    )


def _component_summaries(
    rows: list[DfcAuditRow],
    methodology_components: tuple[DfcComponent, ...],
) -> tuple[DfcComponentSummary, ...]:
    grouped: dict[tuple[DfcActivity, str, str], list[DfcAuditRow]] = {}
    for row in rows:
        if row.dfc_component_code is None or row.dfc_component_label is None:
            continue
        key = (row.dfc_activity, row.dfc_component_code, row.dfc_component_label)
        grouped.setdefault(key, []).append(row)
    summaries = [
        DfcComponentSummary(
            activity=activity,
            component_code=code,
            component_label=label,
            value=sum((row.included_value for row in component_rows), Decimal("0.00")),
            movement_count=len(component_rows),
        )
        for (activity, code, label), component_rows in sorted(
            grouped.items(), key=lambda item: (item[0][0].value, item[0][1])
        )
    ]
    existing_codes = {summary.component_code for summary in summaries}
    summaries.extend(
        DfcComponentSummary(
            activity=DfcActivity(component.activity),
            component_code=component.code,
            component_label=component.label,
            value=Decimal("0.00"),
            movement_count=0,
        )
        for component in methodology_components
        if component.code not in existing_codes
    )
    return tuple(
        sorted(summaries, key=lambda summary: (summary.activity.value, summary.component_code))
    )


def _counterparty_row(
    *,
    entry: DfcEntry,
    cash_items: list[DfcEntryItem],
    counterparty: DfcEntryItem,
    methodology: DfcMethodology,
    year: int,
) -> DfcAuditRow:
    direction = (
        CashFlowDirection.INFLOW
        if counterparty.debit_credit_indicator == "C"
        else CashFlowDirection.OUTFLOW
    )
    expected_cash_indicator = "D" if direction == CashFlowDirection.INFLOW else "C"
    matching_cash = [
        item
        for item in cash_items
        if item.debit_credit_indicator == expected_cash_indicator
    ]
    cash_item = matching_cash[0] if matching_cash else cash_items[0]
    base = {
        "entry_number": entry.entry_number,
        "entry_date": entry.entry_date,
        "cash_account_code": cash_item.account_code,
        "cash_flow_direction": direction,
        "counterparty_account_code": counterparty.account_code,
        "counterparty_account_name": counterparty.account_name,
        "counterparty_reference_code": counterparty.reference_code,
        "movement_value": counterparty.amount,
        "history": counterparty.history,
        "line_number": counterparty.line_number,
    }
    if not matching_cash:
        return DfcAuditRow(
            **base,
            dfc_activity=DfcActivity.UNCLASSIFIED,
            dfc_component_code=None,
            dfc_component_label=None,
            included_value=Decimal("0.00"),
            final_status=DfcRowStatus.INCOMPATIBLE_FLOW,
            pending_reason="direcao_sem_partida_compativel_em_disponibilidades",
        )
    if counterparty.reference_code is None:
        return _unclassified_row(
            base,
            "contrapartida_sem_codigo_referencial",
        )
    rule = methodology.rule_for(counterparty.reference_code, year)
    if rule is None:
        return _unclassified_row(base, "codigo_referencial_sem_regra_dfc")
    component_code = rule.component_for(direction.value)
    if component_code is None:
        return DfcAuditRow(
            **base,
            dfc_activity=DfcActivity(rule.activity),
            dfc_component_code=None,
            dfc_component_label=None,
            included_value=Decimal("0.00"),
            final_status=DfcRowStatus.INCOMPATIBLE_FLOW,
            pending_reason="direcao_incompativel_com_regra_dfc",
        )
    component = methodology.component(component_code)
    if rule.requires_review:
        return DfcAuditRow(
            **base,
            dfc_activity=DfcActivity(rule.activity),
            dfc_component_code=component.code,
            dfc_component_label=component.label,
            included_value=Decimal("0.00"),
            final_status=DfcRowStatus.UNCLASSIFIED,
            pending_reason="componente_exige_revisao",
        )
    signed_value = (
        counterparty.amount
        if direction == CashFlowDirection.INFLOW
        else -counterparty.amount
    )
    return DfcAuditRow(
        **base,
        dfc_activity=DfcActivity(rule.activity),
        dfc_component_code=component.code,
        dfc_component_label=component.label,
        included_value=signed_value,
        final_status=DfcRowStatus.INCLUDED,
        pending_reason=None,
    )


def _unclassified_row(base: dict, reason: str) -> DfcAuditRow:
    return DfcAuditRow(
        **base,
        dfc_activity=DfcActivity.UNCLASSIFIED,
        dfc_component_code=None,
        dfc_component_label=None,
        included_value=Decimal("0.00"),
        final_status=DfcRowStatus.UNCLASSIFIED,
        pending_reason=reason,
    )


def _internal_cash_transfer_row(
    entry: DfcEntry,
    cash_items: list[DfcEntryItem],
) -> DfcAuditRow:
    cash_item = next(
        (item for item in cash_items if item.debit_credit_indicator == "D"),
        cash_items[0],
    )
    counterparty = next(
        (item for item in cash_items if item is not cash_item),
        cash_item,
    )
    direction = (
        CashFlowDirection.INFLOW
        if cash_item.debit_credit_indicator == "D"
        else CashFlowDirection.OUTFLOW
    )
    return DfcAuditRow(
        entry_number=entry.entry_number,
        entry_date=entry.entry_date,
        cash_account_code=cash_item.account_code,
        cash_flow_direction=direction,
        counterparty_account_code=counterparty.account_code,
        counterparty_account_name=counterparty.account_name,
        counterparty_reference_code=counterparty.reference_code,
        dfc_activity=DfcActivity.UNCLASSIFIED,
        dfc_component_code=None,
        dfc_component_label=None,
        movement_value=cash_item.amount,
        included_value=Decimal("0.00"),
        final_status=DfcRowStatus.EXCLUDED,
        pending_reason="transferencia_entre_disponibilidades",
        history=cash_item.history,
        line_number=cash_item.line_number,
    )
