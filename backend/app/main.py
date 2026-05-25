from fastapi import FastAPI

from app.api.auditoria import router as auditoria_router
from app.api.facultades import router as facultades_router
from app.api.reservas import router as reservas_router
from app.api.salas import router as salas_router
from app.api.usuarios import router as usuarios_router
from app.core.config import settings

app = FastAPI(title=settings.app_name, version="1.0.0")


@app.get("/health", tags=["health"])
def health():
    return {"status": "ok"}


app.include_router(facultades_router)
app.include_router(usuarios_router)
app.include_router(salas_router)
app.include_router(reservas_router)
app.include_router(auditoria_router)
