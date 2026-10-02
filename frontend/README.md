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

Optional `VITE_API_URL` — leave unset in dev (Vite proxies `/api` to the backend).

Production example:

```
VITE_API_URL=https://api.example.com
```

## Structure

- `src/api/` — typed REST client
- `src/components/` — UI by feature (chat, documents, flashcards, …)
- `src/pages/` — routes
- `src/context/` — auth state
