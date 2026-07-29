from pathlib import Path


FIXTURES_DIR = Path(__file__).parent / "fixtures" / "ecd"


EXPECTED_FIXTURES = {
    "valid_declared.ecd",
    "missing_i051.ecd",
    "official_reference_missing.ecd",
    "methodology_missing.ecd",
    "blocked_rule.ecd",
    "dangerous_prefix.ecd",
}

BALANCE_STATE_FIXTURES = {
    "balance_declared_valid.ecd",
    "balance_declared_divergent.ecd",
    "balance_declared_required_absent.ecd",
    "balance_declared_invalid_structure.ecd",
    "balance_declared_not_required.ecd",
}


def test_ecd_fixtures_are_present_and_documented_as_synthetic() -> None:
    readme = (FIXTURES_DIR / "README.md").read_text(encoding="utf-8")

    assert "sinteticas" in readme
    assert "nao versionar ECD real" in readme
    assert EXPECTED_FIXTURES.issubset({path.name for path in FIXTURES_DIR.glob("*.ecd")})
    assert BALANCE_STATE_FIXTURES.issubset(
        {path.name for path in FIXTURES_DIR.glob("*.ecd")}
    )


def test_ecd_fixtures_contain_required_minimum_records() -> None:
    for fixture_name in EXPECTED_FIXTURES:
        content = (FIXTURES_DIR / fixture_name).read_text(encoding="utf-8")

        assert "|0000|" in content
        assert "|I050|" in content
        assert "|I155|" in content
        assert "|I200|" in content
        assert "|I250|" in content
        assert "|J100|" in content


def test_ecd_fixtures_cover_required_declared_layer_cases() -> None:
    assert "|I051|2.01.01.07.01|" in (FIXTURES_DIR / "dangerous_prefix.ecd").read_text(
        encoding="utf-8"
    )
    assert "|I051|" not in (FIXTURES_DIR / "missing_i051.ecd").read_text(encoding="utf-8")
    assert "|I051|9.99.99.99.99|" in (
        FIXTURES_DIR / "official_reference_missing.ecd"
    ).read_text(encoding="utf-8")
    assert "|I051|1.01.02.03.04|" in (FIXTURES_DIR / "methodology_missing.ecd").read_text(
        encoding="utf-8"
    )
    assert "|I051|2.99.99.99.99|" in (FIXTURES_DIR / "blocked_rule.ecd").read_text(
        encoding="utf-8"
    )
