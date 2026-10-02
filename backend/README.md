# Study RAG Backend

FastAPI + Postgres + FAISS. Background jobs (index, topic map, flashcards) run in-process via FastAPI `BackgroundTasks` — **no Redis or separate worker**.

See `.env.example`.

## Run locally

```bash
cd backend   # from repo root
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# start Postgres, set DATABASE_URL in .env
uvicorn app.main:app --reload
```

Or from this folder: `docker compose up` (API + postgres only).

API: `http://localhost:8000/docs`

Set **`GROQ_API_KEY`** (Groq) or **`XAI_API_KEY`** (xAI) for topic map, flashcards, and chat. See `.env.example`.
