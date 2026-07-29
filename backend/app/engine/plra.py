from __future__ import annotations

from datetime import datetime, timezone
from decimal import Decimal

from app.assets.methodology import PlraPolicy, PlraRule
from app.domain import ComponentStatus
from app.domain.declared_balance import DeclaredBalanceStatus
from app.domain.evidence import (
    AdjustmentEvidence,
    AssetValuationAssessment,
    EvidenceScopeType,
    ValuationValueSource,
)
from app.domain.plra import (
    PlraAccountAuditRow,
    PlraAccountInput,
    PlraCalculation,
    PlraDecisionStatus,
    PlraInclusionStatus,
)


ZERO = Decimal("0.00")
ONE = Decimal("1")
PLRA_FORMULA = (
    "PLR bruto = ativos incluidos - passivos economicos exigiveis; "
    "PLRA = ativos ajustados - passivos economicos exigiveis"
)
BLOCKING_EVIDENCE_STATUSES = {"pendente_critica", "rejeitada"}


def calculate_plra(
    *,
    analysis_id: str,
    exercise_year: int,
    accounts: list[PlraAccountInput],
    policy: PlraPolicy,
    methodology_version_id: str,
    validated_valuations: dict[str, Decimal] | None = None,
    conditional_decisions: dict[str, bool] | None = None,
    evidence_statuses: dict[str, str] | None = None,
    evidences: list[AdjustmentEvidence] | None = None,
    asset_valuations: list[AssetValuationAssessment] | None = None,
    balance_status: DeclaredBalanceStatus | str = DeclaredBalanceStatus.VALIDO,
    calculated_at: datetime | None = None,
) -> PlraCalculation:
    if methodology_version_id != policy.methodology_version_id:
        raise ValueError("PLRA policy and analysis methodology versions differ.")
    valuations = validated_valuations or {}
    decisions = conditional_decisions or {}
    legacy_evidence_statuses = evidence_statuses or {}
    evidence_records = list(evidences or [])
    valuation_records = list(asset_valuations or [])
    _validate_decimal_mapping("validated_valuations", valuations)

    evidence_by_account = {
        evidence.scope_key: evidence
        for evidence in evidence_records
        if evidence.scope_type == EvidenceScopeType.ACCOUNT
    }
    valuation_by_account = {
        assessment.account_code: assessment
        for assessment in valuation_records
    }

    rows: list[PlraAccountAuditRow] = []
    pending_accounts: list[str] = []
    warnings: list[str] = []
    limitations: list[str] = []
    blocking_issues: list[str] = []
    gross_assets = ZERO
    adjusted_assets = ZERO
    liabilities = ZERO
    no_reference_count = 0
    uncovered_nonzero_count = 0
    synthetic_nonzero_count = 0

    for evidence in evidence_records:
        if evidence.methodology_version_id != methodology_version_id:
            blocking_issues.append(
                f"EVIDENCIA_BLOQUEANTE:VERSAO_DIVERGENTE:{evidence.evidence_id}"
            )
        elif evidence.blocks_final_report:
            blocking_issues.append(
                f"EVIDENCIA_BLOQUEANTE:{evidence.scope_key}:{evidence.evidence_status.value}"
            )
        elif evidence.requires_reservation:
            limitations.append(
                "Ressalva documental "
                f"{evidence.evidence_id}: {evidence.materiality_level.value}/"
                f"{evidence.evidence_status.value}."
            )

    children_by_parent = _children_by_parent(accounts)
    for account in accounts:
        if _must_ignore_synthetic(account, children_by_parent):
            row = _audit_row(
                account,
                methodology_version_id=methodology_version_id,
                inclusion_status=PlraInclusionStatus.IGNORED_HIERARCHY,
                decision_status=PlraDecisionStatus.NOT_APPLICABLE,
                reason="Conta sintetica ignorada para evitar dupla contagem.",
            )
            rows.append(row)
            if account.final_balance != ZERO and not children_by_parent.get(
                account.account_code
            ):
                synthetic_nonzero_count += 1
                pending_accounts.append(account.account_code)
            continue

        if account.declared_reference_code is None:
            no_reference_count += 1
            rows.append(
                _audit_row(
                    account,
                    methodology_version_id=methodology_version_id,
                    inclusion_status=PlraInclusionStatus.NO_REFERENCE,
                    decision_status=PlraDecisionStatus.NOT_APPLICABLE,
                    reason="Conta sem COD_CTA_REF declarado; nenhuma inferencia aplicada.",
                )
            )
            continue

        if account.official_nature in {"RESULTADO", "PATRIMONIO_LIQUIDO"}:
            rule = policy.rule_for(account.declared_reference_code, exercise_year)
            rows.append(
                _audit_row(
                    account,
                    methodology_version_id=methodology_version_id,
                    rule=rule,
                    inclusion_status=PlraInclusionStatus.NON_PATRIMONIAL,
                    decision_status=PlraDecisionStatus.NOT_APPLICABLE,
                    reason=(
                        rule.reason
                        if rule is not None
                        else "Conta nao patrimonial realizavel/exigivel fora do PLRA."
                    ),
                )
            )
            continue

        rule = policy.rule_for(account.declared_reference_code, exercise_year)
        if rule is None or rule.rule_status != "ATIVA":
            rows.append(
                _audit_row(
                    account,
                    methodology_version_id=methodology_version_id,
                    rule=rule,
                    inclusion_status=PlraInclusionStatus.PENDING,
                    decision_status=PlraDecisionStatus.PENDING,
                    reason="Codigo patrimonial sem regra PLRA exata e ativa.",
                    limitations=("Cobertura metodologica incompleta.",),
                )
            )
            if account.final_balance != ZERO:
                uncovered_nonzero_count += 1
                pending_accounts.append(account.account_code)
            continue

        evidence_record = evidence_by_account.get(account.account_code)
        evidence_status = (
            evidence_record.evidence_status.value
            if evidence_record is not None
            else legacy_evidence_statuses.get(account.account_code)
        )
        if rule.treatment == "INCLUIR_ATIVO":
            asset_assessment = valuation_by_account.get(account.account_code)
            if asset_assessment is not None and (
                asset_assessment.methodology_version_id != methodology_version_id
                or asset_assessment.reference_code
                != account.declared_reference_code
            ):
                blocking_issues.append(
                    f"EVIDENCIA_BLOQUEANTE:AVALIACAO_DIVERGENTE:{account.account_code}"
                )
                asset_assessment = None
            row = _included_asset_row(
                account,
                rule=rule,
                policy=policy,
                methodology_version_id=methodology_version_id,
                validated_value=valuations.get(account.account_code),
                asset_assessment=asset_assessment,
                evidence_status=evidence_status,
            )
            gross_assets += row.base_value
            adjusted_assets += row.final_economic_value
            if (
                asset_assessment is not None
                and asset_assessment.blocks_plra
            ):
                for issue in asset_assessment.blocking_reasons:
                    blocking_issues.append(
                        f"EVIDENCIA_BLOQUEANTE:{account.account_code}:{issue}"
                    )
        elif rule.treatment == "INCLUIR_PASSIVO":
            row = _included_liability_row(
                account,
                rule=rule,
                methodology_version_id=methodology_version_id,
                evidence_status=evidence_status,
            )
            liabilities += row.final_economic_value
        elif rule.treatment == "PASSIVO_CONDICIONAL":
            decision = decisions.get(account.account_code)
            if decision is None and account.final_balance != ZERO:
                pending_accounts.append(account.account_code)
                blocking_issues.append(
                    f"PASSIVO_CONDICIONAL_SEM_DECISAO:{account.account_code}"
                )
                row = _audit_row(
                    account,
                    methodology_version_id=methodology_version_id,
                    rule=rule,
                    inclusion_status=PlraInclusionStatus.PENDING,
                    decision_status=PlraDecisionStatus.PENDING,
                    reason="Passivo condicional exige decisao valida.",
                    evidence_status=evidence_status,
                )
            elif decision:
                row = _included_liability_row(
                    account,
                    rule=rule,
                    methodology_version_id=methodology_version_id,
                    evidence_status=evidence_status,
                    decision_status=PlraDecisionStatus.VALIDATED,
                )
                liabilities += row.final_economic_value
            else:
                row = _excluded_row(
                    account,
                    rule=rule,
                    methodology_version_id=methodology_version_id,
                    evidence_status=evidence_status,
                    decision_status=PlraDecisionStatus.VALIDATED,
                )
        else:
            row = _excluded_row(
                account,
                rule=rule,
                methodology_version_id=methodology_version_id,
                evidence_status=evidence_status,
            )
        rows.append(row)

        if evidence_status in BLOCKING_EVIDENCE_STATUSES and account.final_balance != ZERO:
            blocking_issues.append(
                f"EVIDENCIA_BLOQUEANTE:{account.account_code}:{evidence_status}"
            )

    if no_reference_count:
        warnings.append(
            f"{no_reference_count} conta(s) sem vinculo I051 foram auditadas e excluidas."
        )
    if uncovered_nonzero_count:
        limitations.append(
            f"{uncovered_nonzero_count} conta(s) patrimonial(is) com saldo nao possuem regra exata."
        )
    if synthetic_nonzero_count:
        limitations.append(
            f"{synthetic_nonzero_count} conta(s) sintetica(s) com saldo nao possuem composicao analitica."
        )

    plr_gross = gross_assets - liabilities
    plra_value = adjusted_assets - liabilities
    status = _calculation_status(
        blocking_issues=blocking_issues,
        uncovered_nonzero_count=uncovered_nonzero_count,
        synthetic_nonzero_count=synthetic_nonzero_count,
    )
    resolved_balance_status = DeclaredBalanceStatus(balance_status)
    if resolved_balance_status != DeclaredBalanceStatus.VALIDO:
        limitations.append(
            "Resultado PLRA mantido apenas para diagnostico: "
            f"balanco declarado com status {resolved_balance_status.value}."
        )
        blocking_issues.append(
            f"BALANCO_DECLARADO_NAO_VALIDO:{resolved_balance_status.value}"
        )
        if status == ComponentStatus.CALCULATED:
            status = ComponentStatus.PARTIAL

    return PlraCalculation(
        analysis_id=analysis_id,
        exercise_year=exercise_year,
        gross_assets_value=gross_assets,
        gross_economic_liabilities_value=liabilities,
        adjusted_assets_value=adjusted_assets,
        plr_gross_value=plr_gross,
        plra_value=plra_value,
        plra_status=status,
        calculation_formula=PLRA_FORMULA,
        account_rows=tuple(rows),
        pending_accounts=tuple(dict.fromkeys(pending_accounts)),
        warnings=tuple(warnings),
        limitations=tuple(limitations),
        blocking_issues=tuple(blocking_issues),
        balance_status=resolved_balance_status,
        methodology_version_id=methodology_version_id,
        calculated_at=calculated_at or datetime.now(timezone.utc),
    )


def _included_asset_row(
    account: PlraAccountInput,
    *,
    rule: PlraRule,
    policy: PlraPolicy,
    methodology_version_id: str,
    validated_value: Decimal | None,
    asset_assessment: AssetValuationAssessment | None,
    evidence_status: str | None,
) -> PlraAccountAuditRow:
    base_value = _signed_value(account, debit_positive=True)
    discount = policy.default_discounts[rule.default_discount_group or ""]
    default_value = base_value * (ONE - discount)
    final_value = (
        asset_assessment.final_economic_value
        if asset_assessment is not None
        else validated_value
        if validated_value is not None
        else default_value
    )
    valuation_source = (
        asset_assessment.final_value_source.value
        if asset_assessment is not None
        else "avaliacao_validada"
        if validated_value is not None
        else "default_interno"
    )
    audited_validated_value = (
        asset_assessment.final_economic_value
        if asset_assessment is not None
        and asset_assessment.final_value_source
        in {
            ValuationValueSource.FORCED_LIQUIDATION,
            ValuationValueSource.ANALYST_ADJUSTMENT,
        }
        else validated_value
    )
    return _audit_row(
        account,
        methodology_version_id=methodology_version_id,
        rule=rule,
        base_value=base_value,
        inclusion_status=PlraInclusionStatus.INCLUDED_ASSET,
        default_discount_percent=discount,
        default_economic_value=default_value,
        valuation_source=valuation_source,
        validated_valuation_value=audited_validated_value,
        final_economic_value=final_value,
        decision_status=(
            PlraDecisionStatus.VALIDATED
            if validated_value is not None
            or (
                asset_assessment is not None
                and asset_assessment.final_value_source
                != ValuationValueSource.DEFAULT_POLICY
            )
            else PlraDecisionStatus.AUTOMATIC
        ),
        evidence_status=evidence_status,
        reason=rule.reason,
    )


def _included_liability_row(
    account: PlraAccountInput,
    *,
    rule: PlraRule,
    methodology_version_id: str,
    evidence_status: str | None,
    decision_status: PlraDecisionStatus = PlraDecisionStatus.AUTOMATIC,
) -> PlraAccountAuditRow:
    value = _signed_value(account, debit_positive=False)
    return _audit_row(
        account,
        methodology_version_id=methodology_version_id,
        rule=rule,
        base_value=value,
        inclusion_status=PlraInclusionStatus.INCLUDED_LIABILITY,
        default_economic_value=value,
        final_economic_value=value,
        decision_status=decision_status,
        evidence_status=evidence_status,
        reason=rule.reason,
    )


def _excluded_row(
    account: PlraAccountInput,
    *,
    rule: PlraRule,
    methodology_version_id: str,
    evidence_status: str | None,
    decision_status: PlraDecisionStatus = PlraDecisionStatus.AUTOMATIC,
) -> PlraAccountAuditRow:
    return _audit_row(
        account,
        methodology_version_id=methodology_version_id,
        rule=rule,
        base_value=_signed_value(account, debit_positive=True),
        inclusion_status=PlraInclusionStatus.EXCLUDED,
        decision_status=decision_status,
        evidence_status=evidence_status,
        reason=rule.reason,
    )


def _audit_row(
    account: PlraAccountInput,
    *,
    methodology_version_id: str,
    inclusion_status: PlraInclusionStatus,
    decision_status: PlraDecisionStatus,
    reason: str,
    rule: PlraRule | None = None,
    base_value: Decimal | None = None,
    default_discount_percent: Decimal | None = None,
    default_economic_value: Decimal = ZERO,
    valuation_source: str | None = None,
    validated_valuation_value: Decimal | None = None,
    final_economic_value: Decimal = ZERO,
    evidence_status: str | None = None,
    limitations: tuple[str, ...] = (),
) -> PlraAccountAuditRow:
    return PlraAccountAuditRow(
        account_code=account.account_code,
        account_name=account.account_name,
        account_type=account.account_type,
        account_level=account.account_level,
        parent_account_code=account.parent_account_code,
        declared_reference_code=account.declared_reference_code,
        official_description=account.official_description,
        methodology_rule_id=rule.methodology_rule_id if rule else None,
        methodology_group=rule.methodology_group if rule else None,
        macrogroup=rule.macrogroup if rule else None,
        base_value=(
            base_value
            if base_value is not None
            else _signed_value(account, debit_positive=True)
        ),
        sign=account.final_balance_indicator,
        inclusion_status=inclusion_status,
        default_discount_percent=default_discount_percent,
        default_economic_value=default_economic_value,
        valuation_source=valuation_source,
        validated_valuation_value=validated_valuation_value,
        final_economic_value=final_economic_value,
        decision_status=decision_status,
        evidence_status=evidence_status,
        reason=reason,
        limitations=limitations,
        methodology_version_id=methodology_version_id,
    )


def _children_by_parent(
    accounts: list[PlraAccountInput],
) -> dict[str, list[PlraAccountInput]]:
    result: dict[str, list[PlraAccountInput]] = {}
    for account in accounts:
        if account.parent_account_code:
            result.setdefault(account.parent_account_code, []).append(account)
    return result


def _must_ignore_synthetic(
    account: PlraAccountInput,
    children_by_parent: dict[str, list[PlraAccountInput]],
) -> bool:
    return account.account_type != "A" or bool(children_by_parent.get(account.account_code))


def _signed_value(account: PlraAccountInput, *, debit_positive: bool) -> Decimal:
    positive_indicator = "D" if debit_positive else "C"
    multiplier = Decimal("1") if account.final_balance_indicator == positive_indicator else Decimal("-1")
    return account.final_balance * multiplier


def _calculation_status(
    *,
    blocking_issues: list[str],
    uncovered_nonzero_count: int,
    synthetic_nonzero_count: int,
) -> ComponentStatus:
    if any(issue.startswith("EVIDENCIA_BLOQUEANTE") for issue in blocking_issues):
        return ComponentStatus.BLOCKED_BY_EVIDENCE
    if blocking_issues:
        return ComponentStatus.BLOCKED_BY_PENDING
    if uncovered_nonzero_count or synthetic_nonzero_count:
        return ComponentStatus.PARTIAL
    return ComponentStatus.CALCULATED


def _validate_decimal_mapping(name: str, values: dict[str, Decimal]) -> None:
    for value in values.values():
        if not isinstance(value, Decimal):
            raise TypeError(f"{name} values must be Decimal.")
        if not value.is_finite():
            raise ValueError(f"{name} values must be finite.")
