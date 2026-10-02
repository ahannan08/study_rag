# Study RAG — Full stack guide

How the **frontend**, **backend**, **Postgres**, and **FAISS** fit together, how to run everything locally, and what happens when you use the app.

For the product spec, see [`study-rag-spec.pdf`](study-rag-spec.pdf).

---

## Architecture

```mermaid
flowchart TB
  subgraph browser [Browser]
    UI[React UI :5173]
  end
  subgraph backend [Backend :8000]
    API[FastAPI]
    BG[BackgroundTasks]
    Emb[MiniLM embeddings]
    API --> BG
    BG --> Emb
  end
  PG[(Postgres)]
  FAISS[(FAISS files per doc)]
  Grok[xAI Grok API]

  UI -->|JWT /api/v1| API
  API --> PG
  BG --> PG
  BG --> FAISS
  API --> Emb
  API --> Grok
  BG --> Grok
```

| Piece | Role |
|--------|------|
| **Frontend** (`frontend/`) | Login, upload, chat, topic map, flashcards, review, progress |
| **Backend** (`backend/`) | REST API, auth, ingestion, RAG, Grok calls |
| **Postgres** | Users, documents, chunks (text + metadata), jobs, flashcards, logs |
| **FAISS** | Vector index per document on disk (`backend/data/faiss/`) |
| **MiniLM** | Local embeddings (no API key) |
| **Grok (xAI)** | Topic map, flashcards, chat answers (needs `XAI_API_KEY`) |

There is **no Redis** and **no separate worker**. Upload and generate jobs run in the API process after the HTTP response (`BackgroundTasks`).

---

## Prerequisites

- **Python 3.12+** (backend)
- **Node 18+** (frontend)
- **PostgreSQL** running locally (or Docker via `backend/docker-compose.yml`)
- **xAI API key** (optional until you use chat / topic map / flashcard generation)

---

## First-time setup

### 1. Postgres

Create a database and user, or use Docker from `backend/`:

```bash
cd backend
docker compose up -d postgres
```

Example local URL (adjust user, password, db name):

```env
DATABASE_URL=postgresql+psycopg2://USER:PASSWORD@localhost:5432/YOUR_DB
```

Tables are created automatically when the API starts (`create_all()`).

### 2. Backend

```bash
cd backend
cp .env.example .env
# Edit .env: DATABASE_URL, JWT_SECRET, XAI_API_KEY, XAI_MODEL
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

- API: http://localhost:8000  
- OpenAPI: http://localhost:8000/docs  
- Health: http://localhost:8000/health → `{"status":"ok"}` if Postgres is reachable  

Run **`uvicorn` from the `backend/` directory** so `.env` is loaded.

**Grok env** (in `backend/.env` only):

```env
XAI_API_KEY=your-key-from-console.x.ai
XAI_MODEL=grok-2-1212
```

Use the model id shown in your [xAI console](https://console.x.ai/) if the default fails.

### 3. Frontend

In a **second terminal**:

```bash
cd frontend
npm install
npm run dev
```

- UI: http://localhost:5173  
- Dev server **proxies** `/api` and `/health` to `http://127.0.0.1:8000` (see `frontend/vite.config.ts`).

No API key in the frontend — the browser only talks to your backend.

---

## Daily start (two terminals)

| Terminal | Command | URL |
|----------|---------|-----|
| 1 | `cd backend && source .venv/bin/activate && uvicorn app.main:app --reload` | :8000 |
| 2 | `cd frontend && npm run dev` | :5173 |

Ensure Postgres is running before starting the backend.

---

## User flow (UI → backend)

```mermaid
sequenceDiagram
  participant U as User
  participant FE as Frontend
  participant API as Backend
  participant DB as Postgres
  participant F as FAISS
  participant G as Grok

  U->>FE: Register / Login
  FE->>API: POST /api/v1/auth/login
  API-->>FE: JWT

  U->>FE: Upload PDF/DOCX
  FE->>API: POST /api/v1/documents
  API->>DB: document + job
  API-->>FE: 202 job_id
  Note over API: BackgroundTasks index doc
  API->>F: embed chunks + FAISS
  FE->>API: GET /api/v1/jobs/id poll
  API-->>FE: completed indexed

  U->>FE: Generate topic map
  FE->>API: POST .../topic-map/generate
  API->>G: topic JSON
  API->>DB: topic_map

  U->>FE: Chat question
  FE->>API: POST .../chat
  API->>F: retrieve chunks
  API->>G: grounded answer
  API-->>FE: answer + citations + coverage

  U->>FE: Review flashcards
  FE->>API: POST .../flashcards/id/review
  API->>DB: SM-2 schedule
```

### Step-by-step in the app

1. **Register / sign in** — JWT stored in the browser; all `/api/v1/*` routes (except auth) require `Authorization: Bearer …`.

2. **Library** — Upload a PDF or DOCX. Backend returns `document_id` and `job_id`. Poll job status until **indexed** (or check document status on refresh).

3. **Open document**
   - **Chat** — Ask questions; answers use retrieved chunks only, with citations and coverage labels (`fully_covered`, `partially_covered`, `not_in_document`).
   - **Topics** — Click **Generate**; poll job; view topic map.
   - **Flashcards** — Click **Generate**; poll job; browse cards.
   - **Progress** — Section stats and weak points (optional Grok wording).

4. **Review** (nav) — Due flashcards across all documents; **Again** / **Got it** updates spaced repetition.

---

## Backend API map (base `/api/v1`)

| Area | Methods | Notes |
|------|---------|--------|
| Auth | `POST /auth/register`, `/login`, `GET /me` | JWT |
| Documents | `POST/GET/DELETE /documents` | Upload starts index job |
| Jobs | `GET /jobs/{id}` | Poll after upload / generate |
| Chat | `POST /documents/{id}/chat` | Requires `indexed` |
| Topic map | `GET/POST .../topic-map`, `.../generate` | Grok |
| Flashcards | `GET/POST .../flashcards/generate`, `GET /flashcards/due`, `POST .../review` | Generate uses Grok; review is local SM-2 |
| Progress | `GET .../progress`, `.../weak-points` | |

Public: `GET /health`.

---

## Data on disk

Under `backend/data/` (gitignored):

- `uploads/` — original files  
- `faiss/{document_id}.index` + `.mapping.json` — vectors per document  

Deleting a document via API removes DB rows, upload file, and FAISS files.

---

## Troubleshooting

| Symptom | Check |
|---------|--------|
| Health fails | Postgres up? `DATABASE_URL` correct? Use `postgresql+psycopg2://...` if driver errors. |
| Upload stuck / job failed | API logs; file type PDF/DOCX; empty PDF text. |
| Chat / generate errors | `XAI_API_KEY` and `XAI_MODEL` in `backend/.env`; restart uvicorn. Wrong var name (`GROK_API_KEY` is ignored — use `XAI_API_KEY`). |
| Frontend can’t reach API | Backend on :8000; frontend dev server running (proxy). |
| CORS errors | Backend allows `localhost:5173` in [`backend/app/main.py`](backend/app/main.py). |

---

## Repo layout

```
study_rag/
├── GETTING_STARTED.md    ← this file
├── study-rag-spec.pdf
├── backend/              # FastAPI, app/, requirements.txt, .env
├── frontend/             # Vite + React + TypeScript
└── README.md             # Short index
```

More detail: [`backend/README.md`](backend/README.md), [`frontend/README.md`](frontend/README.md).
