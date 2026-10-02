# Study RAG Frontend

React 18 + TypeScript + Vite + Tailwind CSS.

## Scripts

```bash
npm install
npm run dev      # http://localhost:5173
npm run build
npm run lint
```

## Environment

| Variable | Purpose |
|----------|---------|
| `VITE_API_URL` | Backend base URL in production. Leave unset in local dev (Vite proxies `/api`). |
| `VITE_DEMO_MODE=true` | Portfolio deploy on Vercel: public home + static demo from `public/demo/` (no backend). |

Local dev with backend (default):

```bash
npm run dev   # app at /app after login
```

Portfolio preview (no backend):

```bash
VITE_DEMO_MODE=true npm run build && VITE_DEMO_MODE=true npm run preview
```

### Vercel (frontend-only demo)

1. Root directory: `frontend`
2. Environment: `VITE_DEMO_MODE=true` (do **not** set `VITE_API_URL`)
3. Build: `npm run build` · Output: `dist`

### Refresh demo data

From `backend/` with Postgres running and your documents indexed:

```bash
source .venv/bin/activate
PYTHONPATH=. python scripts/export_demo_snapshot.py --all-indexed
```

Commits `backend/demo/demo_bundle.json` and `frontend/public/demo/`. Optional seed on empty DB:

```bash
PYTHONPATH=. python scripts/seed_demo.py
```

## Structure

- `src/api/` — typed REST client
- `src/components/` — UI by feature (chat, documents, flashcards, …)
- `src/pages/` — routes
- `src/context/` — auth state
