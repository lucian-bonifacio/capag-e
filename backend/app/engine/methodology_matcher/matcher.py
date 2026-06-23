from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum


class RuleStatus(StrEnum):
    ACTIVE = "ATIVA"
    BLOCKED = "BLOQUEADA"
    UNDER_REVIEW = "EM_REVISAO"
    DEPRECATED = "DEPRECIADA"


class MatchFinalStatus(StrEnum):
    MAPPED = "MAPEADO"
    NOT_MAPPED = "NAO_MAPEADO_METODOLOGICAMENTE"
    OFFICIAL_REFERENCE_NOT_FOUND = "COD_CTA_REF_NAO_ENCONTRADO_NA_TABELA_OFICIAL"
    NO_REFERENCE_LINK = "SEM_VINCULO_REFERENCIAL"
    BLOCKED_RULE = "REGRA_BLOQUEADA"
    UNDER_REVIEW_RULE = "REGRA_EM_REVISAO"
    DEPRECATED_RULE = "REGRA_DEPRECIADA"


@dataclass(frozen=True)
class OfficialReferenceAccount:
    reference_code: str
    official_description: str
    parent_reference_code: str | None
    level: int
    nature: str
    valid_from: int
    valid_to: int | None
    layout: str
    entity_type: str
    source: str
    status: str
    methodology_version_id: str


@dataclass(frozen=True)
class MethodologyRule:
    reference_code: str
    purpose: str
    methodology_description: str
    plra_category: str | None
    fco_category: str | None
    capag_category: str | None
    flow_nature: str | None
    operational_treatment: str | None
    include_in_calculation: bool
    sign: str | None
    rule_status: RuleStatus
    valid_from: int
    valid_to: int | None
    methodology_version_id: str
    observation: str | None = None


@dataclass(frozen=True)
class MatchRequest:
    reference_code: str | None
    year: int
    layout: str
    entity_type: str
    purpose: str


@dataclass(frozen=True)
class MatchResult:
    final_status: MatchFinalStatus
    official_reference: OfficialReferenceAccount | None
    methodology_rule: MethodologyRule | None
    methodology_rule_applied: str | None
    methodology_rule_status: RuleStatus | None
    recommended_action: str | None
    observation: str | None


def match_declared_methodology(
    request: MatchRequest,
    official_references: list[OfficialReferenceAccount],
    methodology_rules: list[MethodologyRule],
) -> MatchResult:
    if request.reference_code is None or request.reference_code.strip() == "":
        return MatchResult(
            final_status=MatchFinalStatus.NO_REFERENCE_LINK,
            official_reference=None,
            methodology_rule=None,
            methodology_rule_applied=None,
            methodology_rule_status=None,
            recommended_action="revisar_vinculo_referencial",
            observation="Conta sem COD_CTA_REF declarado.",
        )

    reference_code = request.reference_code.strip()
    official_reference = _find_official_reference(reference_code, request, official_references)
    if official_reference is None:
        return MatchResult(
            final_status=MatchFinalStatus.OFFICIAL_REFERENCE_NOT_FOUND,
            official_reference=None,
            methodology_rule=None,
            methodology_rule_applied=None,
            methodology_rule_status=None,
            recommended_action="revisar_base_oficial",
            observation="COD_CTA_REF nao encontrado no plano referencial oficial carregado.",
        )

    methodology_rule = _find_methodology_rule(reference_code, request, methodology_rules)
    if methodology_rule is None:
        return MatchResult(
            final_status=MatchFinalStatus.NOT_MAPPED,
            official_reference=official_reference,
            methodology_rule=None,
            methodology_rule_applied=None,
            methodology_rule_status=None,
            recommended_action="revisar_metodologia",
            observation="Nenhuma regra metodologica exata encontrada para a finalidade.",
        )

    if methodology_rule.rule_status == RuleStatus.BLOCKED:
        return _blocked_rule_result(official_reference, methodology_rule)

    if methodology_rule.rule_status == RuleStatus.UNDER_REVIEW:
        return _under_review_rule_result(official_reference, methodology_rule)

    if methodology_rule.rule_status == RuleStatus.DEPRECATED:
        return _deprecated_rule_result(official_reference, methodology_rule)

    return MatchResult(
        final_status=MatchFinalStatus.MAPPED,
        official_reference=official_reference,
        methodology_rule=methodology_rule,
        methodology_rule_applied=methodology_rule.reference_code,
        methodology_rule_status=methodology_rule.rule_status,
        recommended_action=None,
        observation=methodology_rule.observation,
    )


def _find_official_reference(
    reference_code: str,
    request: MatchRequest,
    official_references: list[OfficialReferenceAccount],
) -> OfficialReferenceAccount | None:
    for account in official_references:
        if (
            account.reference_code == reference_code
            and account.layout == request.layout
            and account.entity_type == request.entity_type
            and _is_year_in_range(request.year, account.valid_from, account.valid_to)
        ):
            return account

    return None


def _find_methodology_rule(
    reference_code: str,
    request: MatchRequest,
    methodology_rules: list[MethodologyRule],
) -> MethodologyRule | None:
    for rule in methodology_rules:
        if (
            rule.reference_code == reference_code
            and rule.purpose == request.purpose
            and _is_year_in_range(request.year, rule.valid_from, rule.valid_to)
        ):
            return rule

    return None


def _blocked_rule_result(
    official_reference: OfficialReferenceAccount,
    methodology_rule: MethodologyRule,
) -> MatchResult:
    return MatchResult(
        final_status=MatchFinalStatus.BLOCKED_RULE,
        official_reference=official_reference,
        methodology_rule=methodology_rule,
        methodology_rule_applied=methodology_rule.reference_code,
        methodology_rule_status=methodology_rule.rule_status,
        recommended_action="revisar_regra_metodologica",
        observation=methodology_rule.observation,
    )


def _under_review_rule_result(
    official_reference: OfficialReferenceAccount,
    methodology_rule: MethodologyRule,
) -> MatchResult:
    return MatchResult(
        final_status=MatchFinalStatus.UNDER_REVIEW_RULE,
        official_reference=official_reference,
        methodology_rule=methodology_rule,
        methodology_rule_applied=methodology_rule.reference_code,
        methodology_rule_status=methodology_rule.rule_status,
        recommended_action="revisar_regra_metodologica",
        observation=methodology_rule.observation,
    )


def _deprecated_rule_result(
    official_reference: OfficialReferenceAccount,
    methodology_rule: MethodologyRule,
) -> MatchResult:
    return MatchResult(
        final_status=MatchFinalStatus.DEPRECATED_RULE,
        official_reference=official_reference,
        methodology_rule=methodology_rule,
        methodology_rule_applied=methodology_rule.reference_code,
        methodology_rule_status=methodology_rule.rule_status,
        recommended_action="revisar_regra_metodologica",
        observation=methodology_rule.observation,
    )


def _is_year_in_range(year: int, valid_from: int, valid_to: int | None) -> bool:
    return year >= valid_from and (valid_to is None or year <= valid_to)
