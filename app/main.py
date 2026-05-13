from fastapi import FastAPI

from app.api.v1.routes import meta, readings
from app.core.config import settings
from app.core.response import success_response


app = FastAPI(title=settings.app_name)

app.include_router(readings.router, prefix="/api/v1", tags=["readings"])
app.include_router(meta.router, prefix="/api/v1/meta", tags=["meta"])


@app.get("/")
def root() -> dict:
    return success_response("Application is running", {"app": settings.app_name})


@app.get("/health")
def health() -> dict:
    return success_response("Health check passed")
