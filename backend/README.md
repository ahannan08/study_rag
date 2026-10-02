# Study RAG Backend

FastAPI + Postgres + FAISS + Redis/RQ worker. Run all commands from this `backend/` directory.

See `.env.example`.

## Run locally

```bash
cd backend   # from repo root
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
docker compose up -d postgres redis
uvicorn app.main:app --reload
python -m app.worker.main
```

Or from this folder: `docker compose up` (builds API + worker + postgres + redis).

API: `http://localhost:8000/docs`

Set `XAI_API_KEY` for Grok-backed topic map, flashcards, and chat.
