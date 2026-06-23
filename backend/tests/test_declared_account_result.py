from decimal import Decimal

import pytest

from app.domain import DeclaredAccountResult
from app.engine.methodology_matcher import (
    MatchFinalStatus,
    MatchRequest,
    MethodologyRule,
    OfficialReferenceAccount,
    RuleStatus,
    match_declared_methodology,
)


def test_declared_account_result_preserves_declared_reading_and_decimal_values() -> None:
    match_result = match_declared_methodology(
        request=_request("2.01.01.07.01"),
        official_references=[_official("2.01.01.07.01")],
        methodology_rules=[_rule("2.01.01.07.01")],
    )

    result = DeclaredAccountResult.from_match(
        account_code="1725",
        account_name="EMPRESTIMO - SICOOB CREDICITRUS - C",
        declared_reference_code="2.01.01.07.01",
        purpose="FCO",
        base_value=Decimal("100000.00"),
        considered_value=Decimal("0.00"),
        methodology_version_id="test-version",
        match_result=match_result,
    )

    assert result.account_code == "1725"
    assert result.declared_reference_code == "2.01.01.07.01"
    assert result.official_description == "Descricao oficial de teste"
    assert result.methodology_rule_applied == "2.01.01.07.01"
    assert result.methodology_rule_status == "ATIVA"
    assert result.final_status == "MAPEADO"
    assert result.base_value == Decimal("100000.00")
    assert result.considered_value == Decimal("0.00")


def test_declared_account_result_snapshot_serializes_decimal_without_api_contract() -> None:
    match_result = match_declared_methodology(
        request=_request("2.01.01.07.01"),
        official_references=[_official("2.01.01.07.01")],
        methodology_rules=[_rule("2.01.01.07.01")],
    )
    result = DeclaredAccountResult.from_match(
        account_code="1725",
        account_name="Conta de teste",
        declared_reference_code="2.01.01.07.01",
        purpose="FCO",
        base_value=Decimal("100000.00"),
        considered_value=Decimal("0.00"),
        methodology_version_id="test-version",
        match_result=match_result,
    )

    snapshot = result.to_snapshot()

    assert snapshot["base_value"] == "100000.00"
    assert snapshot["considered_value"] == "0.00"
    assert snapshot["declared_reference_code"] == "2.01.01.07.01"
    assert snapshot["methodology_version_id"] == "test-version"


def test_declared_account_result_keeps_not_mapped_status_explicit() -> None:
    match_result = match_declared_methodology(
        request=_request("2.01.01.07.01"),
        official_references=[_official("2.01.01.07.01")],
        methodology_rules=[],
    )

    result = DeclaredAccountResult.from_match(
        account_code="1725",
        account_name="Conta de teste",
        declared_reference_code="2.01.01.07.01",
        purpose="FCO",
        base_value=Decimal("100000.00"),
        considered_value=Decimal("100000.00"),
        methodology_version_id="test-version",
        match_result=match_result,
    )

    assert result.final_status == MatchFinalStatus.NOT_MAPPED.value
    assert result.methodology_rule_applied is None
    assert result.methodology_rule_status is None
    assert result.recommended_action == "revisar_metodologia"


def test_declared_account_result_rejects_non_decimal_values() -> None:
    match_result = match_declared_methodology(
        request=_request("2.01.01.07.01"),
        official_references=[_official("2.01.01.07.01")],
        methodology_rules=[_rule("2.01.01.07.01")],
    )

    with pytest.raises(TypeError, match="base_value must be Decimal"):
        DeclaredAccountResult.from_match(
            account_code="1725",
            account_name="Conta de teste",
            declared_reference_code="2.01.01.07.01",
            purpose="FCO",
            base_value=100000,
            considered_value=Decimal("0.00"),
            methodology_version_id="test-version",
            match_result=match_result,
        )


def _request(reference_code: str | None, purpose: str = "FCO") -> MatchRequest:
    return MatchRequest(
        reference_code=reference_code,
        year=2024,
        layout="ECD_2024",
        entity_type="PJ_GERAL",
        purpose=purpose,
    )


def _official(reference_code: str) -> OfficialReferenceAccount:
    return OfficialReferenceAccount(
        reference_code=reference_code,
        official_description="Descricao oficial de teste",
        parent_reference_code=None,
        level=5,
        nature="PASSIVO",
        valid_from=2020,
        valid_to=None,
        layout="ECD_2024",
        entity_type="PJ_GERAL",
        source="fixture_unitaria",
        status="ATIVA",
        methodology_version_id="test-version",
    )


def _rule(reference_code: str, purpose: str = "FCO") -> MethodologyRule:
    return MethodologyRule(
        reference_code=reference_code,
        purpose=purpose,
        methodology_description="Regra de teste sem valor metodologico real.",
        plra_category=None,
        fco_category="categoria_teste",
        capag_category=None,
        flow_nature=None,
        operational_treatment="tratamento_teste",
        include_in_calculation=True,
        sign=None,
        rule_status=RuleStatus.ACTIVE,
        valid_from=2020,
        valid_to=None,
        methodology_version_id="test-version",
        observation=None,
    )
