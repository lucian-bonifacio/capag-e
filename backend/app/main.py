from fastapi import FastAPI

from app.api.declared import router as declared_router
from app.api.health import router as health_router
from app.api.imports import router as imports_router


def create_app() -> FastAPI:
    app = FastAPI(title="CAPAG API")
    app.include_router(health_router)
    app.include_router(imports_router)
    app.include_router(declared_router)
    return app


app = create_app()
