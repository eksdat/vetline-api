from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.config import settings
from app.database import init_db
from app.routers.animals import router as animals_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


app = FastAPI(title=settings.app_name, version="0.1.0", lifespan=lifespan)


@app.get("/")
def root() -> dict[str, str]:
    # A rota raiz serve como check rapido de que a API subiu
    return {
        "message": "Vetline API está pronta para evoluir com CRUD, validação e documentação.",
        "docs": "/docs",
        "api_prefix": settings.api_prefix,
    }


app.include_router(animals_router, prefix=settings.api_prefix)