from fastapi import APIRouter

from app.api.v1.endpoints import auth, chat, documents, flashcards, jobs, progress, topic_map

api_router = APIRouter(prefix="/api/v1")
api_router.include_router(auth.router)
api_router.include_router(documents.router)
api_router.include_router(jobs.router)
api_router.include_router(topic_map.router)
api_router.include_router(flashcards.router)
api_router.include_router(chat.router)
api_router.include_router(progress.router)
