# Study RAG

Monorepo layout:

- [`study-rag-spec.pdf`](study-rag-spec.pdf) — product specification
- [`backend/`](backend/) — FastAPI API, worker, Postgres, FAISS, Redis

## Backend

```bash
cd backend
cp .env.example .env
docker compose up -d postgres redis
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
python -m app.worker.main
```

API docs: http://localhost:8000/docs

See [backend/README.md](backend/README.md) for details.
