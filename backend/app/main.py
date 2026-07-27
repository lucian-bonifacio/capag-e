from fastapi import FastAPI

from app.api.capag import router as capag_router
from app.api.declared import router as declared_router
from app.api.dfc import router as dfc_router
from app.api.evidence import router as evidence_router
from app.api.health import router as health_router
from app.api.imports import router as imports_router
from app.api.plra import router as plra_router
from app.api.roa import router as roa_router


def create_app() -> FastAPI:
    app = FastAPI(title="CAPAG API")
    app.include_router(health_router)
    app.include_router(imports_router)
    app.include_router(declared_router)
    app.include_router(dfc_router)
    app.include_router(roa_router)
    app.include_router(plra_router)
    app.include_router(capag_router)
    app.include_router(evidence_router)
    return app


app = create_app()
