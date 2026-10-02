# Study RAG

Monorepo layout:

- [`study-rag-spec.pdf`](study-rag-spec.pdf) — product specification
- [`backend/`](backend/) — FastAPI API, worker, Postgres, FAISS, Redis
- [`frontend/`](frontend/) — React + TypeScript UI (Vite)

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

## Frontend

```bash
cd frontend
npm install
npm run dev
```

Open http://localhost:5173 — API requests proxy to http://127.0.0.1:8000.

See [backend/README.md](backend/README.md) and [frontend/README.md](frontend/README.md).
