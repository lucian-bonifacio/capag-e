from __future__ import annotations

from dataclasses import replace
from decimal import Decimal

from app.assets.methodology import RoaComponent, RoaMethodology
from app.domain.capag import ComponentStatus
from app.domain.roa import (
    RoaAccountInput,
    RoaAuditRow,
    RoaBlock,
    RoaCashPressureInput,
    RoaCalculation,
    RoaComponentSummary,
    RoaPendingGroup,
    RoaRowStatus,
)
from app.domain.evidence import (
    AdjustmentEvidence,
    EvidenceScopeType,
    MaterialityLevel,
    MethodComponent,
)
from app.engine.evidence import calculate_default_materiality


ZERO = Decimal("0.00")
EVIDENCE_BLOCKS = {
    RoaBlock.OPERATING_EXPENSES,
    RoaBlock.FINANCIAL_RESULT,
    RoaBlock.NON_OPERATING_RESULT,
    RoaBlock.CASH_PRESSURES,
}


def build_roa_audit_rows(
    accounts: tuple[RoaAccountInput, ...],
    methodology: RoaMethodology,
) -> tuple[RoaAuditRow, ...]:
    if not isinstance(accounts, tuple):
        raise TypeError("accounts must be tuple")
    return tuple(_audit_row(account, methodology) for account in accounts)


def build_roa_pressure_rows(
    pressures: tuple[RoaCashPressureInput, ...],
    methodology: RoaMethodology,
) -> tuple[RoaAuditRow, ...]:
    if not isinstance(pressures, tuple):
        raise TypeError("pressures must be tuple")
    rows: list[RoaAuditRow] = []
    for pressure in pressures:
        component = methodology.component(pressure.pressure_type)
        if component.block != RoaBlock.CASH_PRESSURES.value:
            raise ValueError("pressure_type must identify a cash pressure component")
        rows.append(
            RoaAuditRow(
                account_code=pressure.account_code,
                account_name=pressure.account_name,
                reference_code=pressure.reference_code,
                reference_description=None,
                roa_block=RoaBlock.CASH_PRESSURES,
                component_roa=component.code,
                component_label=component.label,
                base_value=pressure.amount,
                signed_value=-pressure.amount,
                treatment="incluir_automaticamente",
                final_status=RoaRowStatus.INCLUDED,
                pending_reason=None,
                evidence_id=None,
                line_reference=pressure.line_reference,
                macrogroup="PRESSAO_COMPLEMENTAR_CAIXA",
                required_evidence_type=component.required_evidence_type,
                source_detail=pressure.source_reference,
            )
        )
    return tuple(rows)


def calculate_roa(
    *,
    exercise_year: int,
    audit_rows: tuple[RoaAuditRow, ...],
    methodology: RoaMethodology,
    j150_available: bool,
    materiality_base_value: Decimal | None = None,
    evidences: tuple[AdjustmentEvidence, ...] = (),
) -> RoaCalculation:
    if not isinstance(audit_rows, tuple):
        raise TypeError("audit_rows must be tuple")
    if not isinstance(j150_available, bool):
        raise TypeError("j150_available must be bool")
    if materiality_base_value is not None and not isinstance(
        materiality_base_value, Decimal
    ):
        raise TypeError("materiality_base_value must be Decimal or None")
    if not isinstance(evidences, tuple):
        raise TypeError("evidences must be tuple")

    evaluated_rows: list[RoaAuditRow] = []
    evidence_groups: list[RoaPendingGroup] = []
    alerts: list[str] = []
    evidence_block = False
    for row in audit_rows:
        if not _requires_evidence(row):
            evaluated_rows.append(row)
            continue
        materiality = calculate_default_materiality(
            amount_impact=abs(row.signed_value),
            impact_base_value=materiality_base_value,
        )
        if materiality.materiality_level == MaterialityLevel.LOW:
            evaluated_rows.append(row)
            continue
        matches = _matching_evidences(row, evidences)
        blocking = [evidence for evidence in matches if evidence.blocks_final_report]
        high_or_critical = materiality.materiality_level in {
            MaterialityLevel.HIGH,
            MaterialityLevel.CRITICAL,
        }
        if not matches:
            blocks = high_or_critical
            evidence_block = evidence_block or blocks
            evidence_groups.append(
                RoaPendingGroup(
                    code="EVIDENCIA_ROA_MATERIAL_AUSENTE",
                    message="Despesa ou pressao material sem evidencia vinculada.",
                    account_code=row.account_code,
                    reference_code=row.reference_code,
                    blocks_roa=blocks,
                    materiality_level=materiality.materiality_level.value,
                    evidence_id=None,
                )
            )
            if blocks:
                row = replace(
                    row,
                    final_status=RoaRowStatus.PENDING_EVIDENCE,
                    pending_reason="evidencia_roa_material_ausente",
                )
            else:
                alerts.append(
                    f"Conta {row.account_code} possui ressalva de evidencia ROA."
                )
        elif blocking:
            evidence = blocking[0]
            evidence_block = True
            evidence_groups.append(
                RoaPendingGroup(
                    code="EVIDENCIA_ROA_BLOQUEANTE",
                    message="Evidencia vinculada bloqueia o ROA final.",
                    account_code=row.account_code,
                    reference_code=row.reference_code,
                    blocks_roa=True,
                    materiality_level=evidence.materiality_level.value,
                    evidence_id=evidence.evidence_id,
                )
            )
            row = replace(
                row,
                final_status=RoaRowStatus.PENDING_EVIDENCE,
                pending_reason="evidencia_roa_bloqueante",
                evidence_id=evidence.evidence_id,
            )
        else:
            row = replace(row, evidence_id=matches[0].evidence_id)
            if any(evidence.requires_reservation for evidence in matches):
                alerts.append(
                    f"Conta {row.account_code} possui ressalva de evidencia ROA."
                )
        evaluated_rows.append(row)

    included = [
        row
        for row in evaluated_rows
        if row.final_status
        in {
            RoaRowStatus.INCLUDED,
            RoaRowStatus.PENDING_EVIDENCE,
            RoaRowStatus.MANUAL_DECISION_APPLIED,
        }
    ]
    gross_revenue = _positive_block_total(included, RoaBlock.GROSS_REVENUE)
    deductions = _reduction_block_total(included, RoaBlock.DEDUCTIONS)
    revenue_taxes = _reduction_block_total(included, RoaBlock.REVENUE_TAXES)
    operating_costs = _reduction_block_total(
        included, RoaBlock.OPERATING_COSTS
    )
    operating_expenses = _reduction_block_total(
        included, RoaBlock.OPERATING_EXPENSES
    )
    financial_result = _signed_block_total(
        included, RoaBlock.FINANCIAL_RESULT
    )
    non_operating_result = _signed_block_total(
        included, RoaBlock.NON_OPERATING_RESULT
    )
    cash_pressures = _reduction_block_total(included, RoaBlock.CASH_PRESSURES)
    net_operating_revenue = gross_revenue - deductions - revenue_taxes
    roa_preliminary = (
        net_operating_revenue
        - operating_costs
        - operating_expenses
        + financial_result
        + non_operating_result
    )
    roa_final = roa_preliminary - cash_pressures

    pending_groups = tuple(
        _pending_group(row)
        for row in evaluated_rows
        if row.final_status in {RoaRowStatus.PENDING_REVIEW, RoaRowStatus.NO_RULE}
    ) + tuple(evidence_groups)
    limitations: list[str] = []
    if not j150_available:
        limitations.append(
            "Conferencia J150 indisponivel; ROA calculado a partir de I155 e codigo referencial."
        )

    if evidence_block:
        status = ComponentStatus.BLOCKED_BY_EVIDENCE
    elif any(group.blocks_roa for group in pending_groups):
        status = ComponentStatus.BLOCKED_BY_PENDING
    elif not evaluated_rows:
        status = ComponentStatus.NOT_CALCULATED
        limitations.append("Nenhuma conta de resultado elegivel foi identificada.")
    else:
        status = ComponentStatus.CALCULATED

    return RoaCalculation(
        exercise_year=exercise_year,
        gross_revenue=gross_revenue,
        deductions=deductions,
        revenue_taxes=revenue_taxes,
        net_operating_revenue=net_operating_revenue,
        operating_costs=operating_costs,
        operating_expenses=operating_expenses,
        financial_result=financial_result,
        non_operating_result=non_operating_result,
        cash_pressure_adjustments=cash_pressures,
        roa_preliminary=roa_preliminary,
        roa_final=roa_final,
        status=status,
        component_summaries=_component_summaries(included, methodology.components),
        audit_rows=tuple(evaluated_rows),
        pending_groups=pending_groups,
        alerts=tuple(dict.fromkeys(alerts)),
        limitations=tuple(limitations),
        methodology_version_id=methodology.methodology_version_id,
    )


def _audit_row(
    account: RoaAccountInput,
    methodology: RoaMethodology,
) -> RoaAuditRow:
    rule = methodology.rule_for(account.reference_code)
    if rule is None:
        return RoaAuditRow(
            account_code=account.account_code,
            account_name=account.account_name,
            reference_code=account.reference_code,
            reference_description=account.reference_description,
            roa_block=None,
            component_roa=None,
            component_label=None,
            base_value=max(account.debit_amount, account.credit_amount),
            signed_value=ZERO,
            treatment="sem_regra",
            final_status=RoaRowStatus.NO_RULE,
            pending_reason=(
                "conta_sem_codigo_referencial"
                if account.reference_code is None
                else "codigo_referencial_sem_regra_roa"
            ),
            evidence_id=None,
            line_reference=account.line_reference,
            macrogroup=None,
            required_evidence_type=None,
            source_detail=None,
        )

    component = methodology.component(rule.component_code)
    effective_side = _effective_natural_side(account, rule.natural_side)
    base_value = _natural_movement(account, effective_side)
    if rule.treatment == "excluir_automaticamente":
        status = RoaRowStatus.EXCLUDED
        signed_value = ZERO
        pending_reason = None
    elif rule.treatment == "condicional":
        status = RoaRowStatus.PENDING_REVIEW
        signed_value = ZERO
        pending_reason = rule.conditional_reason
    else:
        status = RoaRowStatus.INCLUDED
        signed_value = _signed_value(
            base_value=base_value,
            primary_rule=rule.primary_rule,
            debit_amount=account.debit_amount,
            credit_amount=account.credit_amount,
            rule_natural_side=rule.natural_side,
            effective_natural_side=effective_side,
        )
        pending_reason = None

    return RoaAuditRow(
        account_code=account.account_code,
        account_name=account.account_name,
        reference_code=account.reference_code,
        reference_description=account.reference_description,
        roa_block=RoaBlock(rule.block),
        component_roa=component.code,
        component_label=component.label,
        base_value=base_value,
        signed_value=signed_value,
        treatment=rule.treatment,
        final_status=status,
        pending_reason=pending_reason,
        evidence_id=None,
        line_reference=account.line_reference,
        macrogroup=rule.macrogroup,
        required_evidence_type=component.required_evidence_type,
        source_detail=(
            f"Natureza de saldo I155: {account.balance_nature}."
            if account.balance_nature is not None
            else None
        ),
    )


def _effective_natural_side(
    account: RoaAccountInput,
    rule_natural_side: str,
) -> str:
    if account.balance_nature == "C":
        return "credito"
    if account.balance_nature == "D":
        return "debito"
    return rule_natural_side


def _natural_movement(account: RoaAccountInput, natural_side: str) -> Decimal:
    if natural_side == "credito":
        return account.credit_amount
    if natural_side == "debito":
        return account.debit_amount
    return max(account.debit_amount, account.credit_amount)


def _signed_value(
    *,
    base_value: Decimal,
    primary_rule: str,
    debit_amount: Decimal,
    credit_amount: Decimal,
    rule_natural_side: str,
    effective_natural_side: str,
) -> Decimal:
    if primary_rule == "somar":
        return (
            base_value
            if effective_natural_side == rule_natural_side
            else -base_value
        )
    if primary_rule == "subtrair":
        return (
            -base_value
            if effective_natural_side == rule_natural_side
            else base_value
        )
    if primary_rule == "aplicar_sinal_contabil":
        if effective_natural_side == "credito":
            return base_value
        if effective_natural_side == "debito":
            return -base_value
        return credit_amount - debit_amount
    if primary_rule == "excluir":
        return ZERO
    raise ValueError(f"unsupported ROA primary rule: {primary_rule}")


def _positive_block_total(
    rows: list[RoaAuditRow],
    block: RoaBlock,
) -> Decimal:
    return sum(
        (row.signed_value for row in rows if row.roa_block == block),
        ZERO,
    )


def _reduction_block_total(
    rows: list[RoaAuditRow],
    block: RoaBlock,
) -> Decimal:
    return -sum(
        (row.signed_value for row in rows if row.roa_block == block),
        ZERO,
    )


def _signed_block_total(
    rows: list[RoaAuditRow],
    block: RoaBlock,
) -> Decimal:
    return sum(
        (row.signed_value for row in rows if row.roa_block == block),
        ZERO,
    )


def _pending_group(row: RoaAuditRow) -> RoaPendingGroup:
    if row.final_status == RoaRowStatus.NO_RULE:
        code = "CONTA_RESULTADO_SEM_REGRA_ROA"
        message = "Conta de resultado elegivel sem regra ROA."
    else:
        code = "CONTA_ROA_CONDICIONAL"
        message = "Conta condicional exige revisao antes do ROA final."
    return RoaPendingGroup(
        code=code,
        message=message,
        account_code=row.account_code,
        reference_code=row.reference_code,
        blocks_roa=True,
    )


def _requires_evidence(row: RoaAuditRow) -> bool:
    return (
        row.final_status
        in {RoaRowStatus.INCLUDED, RoaRowStatus.MANUAL_DECISION_APPLIED}
        and row.roa_block in EVIDENCE_BLOCKS
        and row.signed_value < ZERO
    )


def _matching_evidences(
    row: RoaAuditRow,
    evidences: tuple[AdjustmentEvidence, ...],
) -> list[AdjustmentEvidence]:
    matches: list[AdjustmentEvidence] = []
    for evidence in evidences:
        if evidence.method_component != MethodComponent.ROA:
            continue
        if (
            evidence.scope_type == EvidenceScopeType.ACCOUNT
            and evidence.scope_key
            in {row.account_code, row.reference_code}
        ) or (
            evidence.scope_type == EvidenceScopeType.ROA_COMPONENT
            and evidence.scope_key == row.component_roa
        ) or (
            evidence.scope_type == EvidenceScopeType.MACROGROUP
            and evidence.scope_key == row.macrogroup
        ):
            matches.append(evidence)
    return matches


def _component_summaries(
    rows: list[RoaAuditRow],
    components: tuple[RoaComponent, ...],
) -> tuple[RoaComponentSummary, ...]:
    summaries: list[RoaComponentSummary] = []
    for component in components:
        component_rows = [
            row for row in rows if row.component_roa == component.code
        ]
        summaries.append(
            RoaComponentSummary(
                block=RoaBlock(component.block),
                component_code=component.code,
                component_label=component.label,
                value=sum((row.signed_value for row in component_rows), ZERO),
                account_count=len(component_rows),
            )
        )
    return tuple(summaries)
