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
        "/api/v1/analyses/{analysis_id}/exercises/{year}/declared",
        "/api/v1/analyses/{analysis_id}/exercises/{year}/declared/run",
        "/api/v1/analyses/{analysis_id}/exercises/{year}/declared/accounts",
        "/api/v1/analyses/{analysis_id}/exercises/{year}/declared/export.xlsx",
    }
