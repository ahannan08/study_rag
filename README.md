# Study RAG

Monorepo for a document-grounded study assistant (chat, topic map, flashcards, spaced review).

**Start here:** [**GETTING_STARTED.md**](GETTING_STARTED.md) — architecture, setup, user flow, and API overview for frontend + backend together.

| Path | Purpose |
|------|---------|
| [`study-rag-spec.pdf`](study-rag-spec.pdf) | Product specification |
| [`backend/`](backend/) | FastAPI, Postgres, FAISS, Grok |
| [`frontend/`](frontend/) | React + TypeScript (Vite) |

Quick start:

```bash
# Terminal 1 — backend (from backend/, with Postgres + .env configured)
cd backend && source .venv/bin/activate && uvicorn app.main:app --reload

# Terminal 2 — frontend
cd frontend && npm run dev
```

Open http://localhost:5173
