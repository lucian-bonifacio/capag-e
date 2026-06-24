from __future__ import annotations

from decimal import Decimal

from sqlalchemy import delete

from app.db.session import SessionLocal
from app.repositories import DeclaredAccountSnapshot


ANALYSIS_ID = "analysis-1"
EXERCISE_YEAR = 2024
METHODOLOGY_VERSION_ID = "demo-declarada-2024.1"


def main() -> None:
    with SessionLocal() as session:
        session.execute(
            delete(DeclaredAccountSnapshot)
            .where(DeclaredAccountSnapshot.analysis_id == ANALYSIS_ID)
            .where(DeclaredAccountSnapshot.exercise_year == EXERCISE_YEAR)
        )

        for snapshot in _demo_snapshots():
            session.add(snapshot)

        session.commit()


def _demo_snapshots() -> list[DeclaredAccountSnapshot]:
    return [
        _snapshot(
            account_code="1725",
            account_name="EMPRESTIMO - SICOOB CREDICITRUS - C",
            declared_reference_code="2.01.01.07.01",
            official_description="Emprestimos e financiamentos",
            methodology_rule_applied="2.01.01.07.01",
            methodology_rule_status="ATIVA",
            purpose="FCO",
            treatment="excluir_operacional",
            base_value=Decimal("100000.00"),
            considered_value=Decimal("0.00"),
            final_status="MAPEADO",
            observation="Snapshot demonstrativo para homologacao manual.",
            recommended_action=None,
        ),
        _snapshot(
            account_code="2101",
            account_name="FORNECEDORES NACIONAIS",
            declared_reference_code="2.01.01.03.01",
            official_description="Fornecedores nacionais",
            methodology_rule_applied="2.01.01.03.01",
            methodology_rule_status="ATIVA",
            purpose="FCO",
            treatment="incluir_operacional",
            base_value=Decimal("42500.25"),
            considered_value=Decimal("42500.25"),
            final_status="MAPEADO",
            observation="Snapshot demonstrativo para homologacao manual.",
            recommended_action=None,
        ),
        _snapshot(
            account_code="3001",
            account_name="CONTA REFERENCIAL SEM REGRA EXATA",
            declared_reference_code="9.99.99",
            official_description="Codigo demonstrativo sem cobertura metodologica",
            methodology_rule_applied=None,
            methodology_rule_status=None,
            purpose="AUDITORIA",
            treatment=None,
            base_value=Decimal("1200.00"),
            considered_value=Decimal("1200.00"),
            final_status="NAO_MAPEADO_METODOLOGICAMENTE",
            observation="Nenhuma regra metodologica exata encontrada para a finalidade.",
            recommended_action="revisar_metodologia",
        ),
    ]


def _snapshot(
    *,
    account_code: str,
    account_name: str,
    declared_reference_code: str | None,
    official_description: str | None,
    methodology_rule_applied: str | None,
    methodology_rule_status: str | None,
    purpose: str,
    treatment: str | None,
    base_value: Decimal,
    considered_value: Decimal,
    final_status: str,
    observation: str | None,
    recommended_action: str | None,
) -> DeclaredAccountSnapshot:
    snapshot_json = {
        "account_code": account_code,
        "account_name": account_name,
        "declared_reference_code": declared_reference_code,
        "official_description": official_description,
        "official_reference_status": "ATIVA" if declared_reference_code else None,
        "methodology_rule_applied": methodology_rule_applied,
        "methodology_rule_status": methodology_rule_status,
        "purpose": purpose,
        "treatment": treatment,
        "base_value": str(base_value),
        "considered_value": str(considered_value),
        "final_status": final_status,
        "observation": observation,
        "recommended_action": recommended_action,
        "methodology_version_id": METHODOLOGY_VERSION_ID,
    }

    return DeclaredAccountSnapshot(
        analysis_id=ANALYSIS_ID,
        exercise_year=EXERCISE_YEAR,
        account_code=account_code,
        account_name=account_name,
        declared_reference_code=declared_reference_code,
        official_description=official_description,
        official_reference_status="ATIVA" if declared_reference_code else None,
        methodology_rule_applied=methodology_rule_applied,
        methodology_rule_status=methodology_rule_status,
        purpose=purpose,
        base_value=base_value,
        considered_value=considered_value,
        final_status=final_status,
        observation=observation,
        recommended_action=recommended_action,
        methodology_version_id=METHODOLOGY_VERSION_ID,
        snapshot_json=snapshot_json,
    )


if __name__ == "__main__":
    main()
