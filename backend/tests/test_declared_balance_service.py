from hashlib import sha256
from pathlib import Path

import pytest
from sqlalchemy import create_engine, func, select
from sqlalchemy.orm import Session

from app.application import (
    EcdImportIdentifiers,
    get_declared_balance,
    persist_parsed_ecd,
)
from app.domain import BalanceLineStatus, DeclaredBalanceStatus
from app.io import parse_ecd_file
from app.repositories import Base, DeclaredAccountSnapshot


FIXTURES_DIR = Path(__file__).parent / "fixtures" / "ecd"


@pytest.mark.parametrize(
    ("fixture_name", "expected_status"),
    [
        ("balance_declared_valid.ecd", DeclaredBalanceStatus.VALIDO),
        ("balance_declared_divergent.ecd", DeclaredBalanceStatus.DIVERGENTE),
        (
            "balance_declared_required_absent.ecd",
            DeclaredBalanceStatus.OBRIGATORIO_AUSENTE,
        ),
        (
            "balance_declared_invalid_structure.ecd",
            DeclaredBalanceStatus.ESTRUTURA_INVALIDA,
        ),
        (
            "balance_declared_not_required.ecd",
            DeclaredBalanceStatus.NAO_OBRIGATORIO,
        ),
    ],
)
def test_service_reads_all_balance_states_without_creating_snapshot(
    fixture_name: str,
    expected_status: DeclaredBalanceStatus,
) -> None:
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    fixture = FIXTURES_DIR / fixture_name
    raw = fixture.read_bytes()

    with Session(engine) as session:
        persist_parsed_ecd(
            session,
            parsed_ecd=parse_ecd_file(fixture),
            identifiers=EcdImportIdentifiers(
                company_id="company-balance",
                ecd_file_id="ecd-balance",
                analysis_id="analysis-balance",
                methodology_version_id="metodologia-2024.1",
                original_filename=fixture.name,
                content_hash=f"sha256:{sha256(raw).hexdigest()}",
            ),
            original_content=raw,
            parser_version="2.0.0",
        )

    with Session(engine) as session:
        before = session.scalar(select(func.count()).select_from(DeclaredAccountSnapshot))
        result = get_declared_balance(
            session,
            analysis_id="analysis-balance",
            year=2024,
        )
        after = session.scalar(select(func.count()).select_from(DeclaredAccountSnapshot))

    assert result.status == expected_status
    assert before == after == 0
    if expected_status == DeclaredBalanceStatus.VALIDO:
        assert result.rows[0].children[0].aggregation_code == "AGL-CAIXA"
        assert result.rows[0].children[0].components[0].account_code == "1.01.01.001"
        assert result.rows[0].children[0].initial_amount != (
            result.rows[0].children[0].final_amount
        )
        assert (
            result.rows[0].children[0].reconciliation_status
            == BalanceLineStatus.CONCILIADA
        )
        assert (
            result.rows[1].children[0].reconciliation_status
            == BalanceLineStatus.CONCILIADA
        )
