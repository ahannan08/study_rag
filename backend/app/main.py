from contextlib import asynccontextmanager

from fastapi import FastAPI
from sqlalchemy import text

from app.api.v1.router import api_router
from app.db.init_db import init_db
from app.db.session import engine
from app.infrastructure.embeddings.minilm import get_embedder


@asynccontextmanager
async def lifespan(_app: FastAPI):
    init_db()
    get_embedder()
    yield


app = FastAPI(title="Study RAG API", version="1.0.0", lifespan=lifespan)
app.include_router(api_router)


@app.get("/health")
def health() -> dict:
    with engine.connect() as conn:
        conn.execute(text("SELECT 1"))
    return {"status": "ok"}
