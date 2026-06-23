from app.engine.methodology_matcher import (
    MatchFinalStatus,
    MatchRequest,
    MethodologyRule,
    OfficialReferenceAccount,
    RuleStatus,
    match_declared_methodology,
)


def test_exact_active_rule_maps_declared_reference_code() -> None:
    result = match_declared_methodology(
        request=_request("2.01.01.07.01"),
        official_references=[_official("2.01.01.07.01")],
        methodology_rules=[
            _rule(
                reference_code="2.01.01.07.01",
                treatment="tratamento_exato_financiamento",
            ),
        ],
    )

    assert result.final_status == MatchFinalStatus.MAPPED
    assert result.methodology_rule_applied == "2.01.01.07.01"
    assert result.official_reference is not None
    assert result.official_reference.official_description == "Descricao oficial de teste"
    assert result.methodology_rule is not None
    assert result.methodology_rule.operational_treatment == "tratamento_exato_financiamento"


def test_prefix_rule_does_not_classify_declared_reference_code() -> None:
    result = match_declared_methodology(
        request=_request("2.01.01.07.01"),
        official_references=[_official("2.01.01.07.01")],
        methodology_rules=[
            _rule(
                reference_code="2.01.01.*",
                treatment="pagamentos_fornecedores",
            )
        ],
    )

    assert result.final_status == MatchFinalStatus.NOT_MAPPED
    assert result.methodology_rule is None
    assert result.methodology_rule_applied is None


def test_absent_exact_rule_returns_not_mapped() -> None:
    result = match_declared_methodology(
        request=_request("2.01.01.07.01"),
        official_references=[_official("2.01.01.07.01")],
        methodology_rules=[
            _rule(reference_code="2.01.01.07.02"),
        ],
    )

    assert result.final_status == MatchFinalStatus.NOT_MAPPED
    assert result.recommended_action == "revisar_metodologia"


def test_blocked_under_review_and_deprecated_exact_rules_do_not_map_new_calculation() -> None:
    expected_statuses = {
        RuleStatus.BLOCKED: MatchFinalStatus.BLOCKED_RULE,
        RuleStatus.UNDER_REVIEW: MatchFinalStatus.UNDER_REVIEW_RULE,
        RuleStatus.DEPRECATED: MatchFinalStatus.DEPRECATED_RULE,
    }

    for rule_status, final_status in expected_statuses.items():
        result = match_declared_methodology(
            request=_request("2.01.01.07.01"),
            official_references=[_official("2.01.01.07.01")],
            methodology_rules=[
                _rule(
                    reference_code="2.01.01.07.01",
                    rule_status=rule_status,
                )
            ],
        )

        assert result.final_status == final_status
        assert result.methodology_rule_status == rule_status
        assert result.recommended_action == "revisar_regra_metodologica"


def test_missing_official_reference_returns_specific_status() -> None:
    result = match_declared_methodology(
        request=_request("9.99.99"),
        official_references=[],
        methodology_rules=[
            _rule(reference_code="9.99.99"),
        ],
    )

    assert result.final_status == MatchFinalStatus.OFFICIAL_REFERENCE_NOT_FOUND
    assert result.recommended_action == "revisar_base_oficial"
    assert result.methodology_rule is None


def test_empty_reference_code_returns_no_reference_link_status() -> None:
    result = match_declared_methodology(
        request=_request(None),
        official_references=[],
        methodology_rules=[],
    )

    assert result.final_status == MatchFinalStatus.NO_REFERENCE_LINK
    assert result.recommended_action == "revisar_vinculo_referencial"


def test_rule_must_match_purpose_and_validity() -> None:
    result = match_declared_methodology(
        request=_request("2.01.01.07.01", year=2024, purpose="FCO"),
        official_references=[_official("2.01.01.07.01", valid_from=2020, valid_to=2025)],
        methodology_rules=[
            _rule(
                reference_code="2.01.01.07.01",
                purpose="PLRA",
            ),
            _rule(
                reference_code="2.01.01.07.01",
                valid_from=2025,
                purpose="FCO",
            ),
        ],
    )

    assert result.final_status == MatchFinalStatus.NOT_MAPPED


def _request(
    reference_code: str | None,
    year: int = 2024,
    layout: str = "ECD_2024",
    entity_type: str = "PJ_GERAL",
    purpose: str = "FCO",
) -> MatchRequest:
    return MatchRequest(
        reference_code=reference_code,
        year=year,
        layout=layout,
        entity_type=entity_type,
        purpose=purpose,
    )


def _official(
    reference_code: str,
    valid_from: int = 2020,
    valid_to: int | None = None,
) -> OfficialReferenceAccount:
    return OfficialReferenceAccount(
        reference_code=reference_code,
        official_description="Descricao oficial de teste",
        parent_reference_code=None,
        level=5,
        nature="PASSIVO",
        valid_from=valid_from,
        valid_to=valid_to,
        layout="ECD_2024",
        entity_type="PJ_GERAL",
        source="fixture_unitaria",
        status="ATIVA",
        methodology_version_id="test-version",
    )


def _rule(
    reference_code: str,
    purpose: str = "FCO",
    rule_status: RuleStatus = RuleStatus.ACTIVE,
    treatment: str = "tratamento_teste",
    valid_from: int = 2020,
    valid_to: int | None = None,
) -> MethodologyRule:
    return MethodologyRule(
        reference_code=reference_code,
        purpose=purpose,
        methodology_description="Regra de teste sem valor metodologico real.",
        plra_category=None,
        fco_category="categoria_teste",
        capag_category=None,
        flow_nature=None,
        operational_treatment=treatment,
        include_in_calculation=True,
        sign=None,
        rule_status=rule_status,
        valid_from=valid_from,
        valid_to=valid_to,
        methodology_version_id="test-version",
        observation=None,
    )
