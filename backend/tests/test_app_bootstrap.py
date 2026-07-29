from app.api.health import healthcheck
from app.main import app


def test_app_imports_and_exposes_technical_healthcheck() -> None:
    assert healthcheck() == {"status": "ok"}


def test_openapi_contains_current_api_contracts() -> None:
    paths = set(app.openapi()["paths"])

    assert paths == {
        "/health",
        "/api/v1/ecd/import",
        "/api/v1/ecd/imports",
        "/api/v1/ecd/imports/{ecd_file_id}",
        "/api/v1/analyses/{analysis_id}/exercises/{year}/capag-assessment",
        "/api/v1/analyses/{analysis_id}/exercises/{year}/capag-assessment/run",
        "/api/v1/analyses/{analysis_id}/exercises/{year}/declared",
        "/api/v1/analyses/{analysis_id}/exercises/{year}/declared/run",
        "/api/v1/analyses/{analysis_id}/exercises/{year}/declared/accounts",
        "/api/v1/analyses/{analysis_id}/exercises/{year}/declared/balance/accounts",
        "/api/v1/analyses/{analysis_id}/exercises/{year}/declared/balance/accounts/{aggregation_code}/components",
        "/api/v1/analyses/{analysis_id}/exercises/{year}/declared/export.xlsx",
        "/api/v1/analyses/{analysis_id}/exercises/{year}/dfc",
        "/api/v1/analyses/{analysis_id}/exercises/{year}/dfc/run",
        "/api/v1/analyses/{analysis_id}/exercises/{year}/dfc/decisions",
        "/api/v1/analyses/{analysis_id}/exercises/{year}/dfc/export.xlsx",
        "/api/v1/analyses/{analysis_id}/exercises/{year}/evidences",
        "/api/v1/analyses/{analysis_id}/exercises/{year}/evidences/export.xlsx",
        "/api/v1/evidences/{evidence_id}",
        "/api/v1/analyses/{analysis_id}/exercises/{year}/assets/valuations",
        "/api/v1/assets/valuations/{assessment_id}",
        "/api/v1/analyses/{analysis_id}/exercises/{year}/plra",
        "/api/v1/analyses/{analysis_id}/exercises/{year}/plra/run",
        "/api/v1/analyses/{analysis_id}/exercises/{year}/plra/audit",
        "/api/v1/analyses/{analysis_id}/exercises/{year}/plra/export.xlsx",
        "/api/v1/analyses/{analysis_id}/exercises/{year}/roa",
        "/api/v1/analyses/{analysis_id}/exercises/{year}/roa/run",
        "/api/v1/analyses/{analysis_id}/exercises/{year}/roa/decisions",
        "/api/v1/analyses/{analysis_id}/exercises/{year}/roa/export.xlsx",
    }
