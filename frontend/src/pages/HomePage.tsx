import { ArrowRight, Github, Sparkles } from "lucide-react";
import { Link } from "react-router-dom";
import { PublicShell } from "@/components/layout/PublicShell";
import { Button } from "@/components/ui/Button";
import { isDemoMode } from "@/lib/demoMode";

export function HomePage() {
  return (
    <PublicShell badge="Portfolio">
      <div className="mx-auto max-w-2xl text-center">
        <div className="mb-6 inline-flex items-center gap-2 rounded-full bg-accent-muted px-4 py-1 text-sm font-medium text-accent">
          <Sparkles className="h-4 w-4" />
          Document-grounded study assistant
        </div>
        <h1 className="font-display text-4xl font-bold tracking-tight text-ink-950 sm:text-5xl">
          Study RAG
        </h1>
        <p className="mt-4 text-lg leading-relaxed text-ink-600">
          Upload course PDFs, chat with citations, explore a book-style topic map, and review flashcards
          generated from your material — all grounded in retrieved chunks, not generic LLM guesses.
        </p>
        <div className="mt-6 flex flex-wrap justify-center gap-2">
          {["React", "FastAPI", "FAISS", "MiniLM", "Groq"].map((t) => (
            <span key={t} className="rounded-lg bg-ink-100 px-3 py-1 text-xs font-semibold text-ink-700">
              {t}
            </span>
          ))}
        </div>
        <div className="mt-10 flex flex-col items-center justify-center gap-3 sm:flex-row">
          <Link to="/demo">
            <Button className="gap-2 px-6 py-3 text-base">
              View demo
              <ArrowRight className="h-4 w-4" />
            </Button>
          </Link>
          {!isDemoMode && (
            <Link to="/login">
              <Button variant="secondary" className="px-6 py-3 text-base">
                Sign in (full app)
              </Button>
            </Link>
          )}
          <a
            href="https://github.com"
            className="inline-flex items-center gap-2 text-sm font-medium text-ink-500 hover:text-ink-800"
            target="_blank"
            rel="noreferrer"
          >
            <Github className="h-4 w-4" />
            Source on GitHub
          </a>
        </div>
        <p className="mt-12 text-sm text-ink-500">
          {isDemoMode ? (
            <>
              This live site uses exported sample documents only. Upload and live Q&amp;A require running the backend
              locally — see GETTING_STARTED in the repo.
            </>
          ) : (
            <>
              Browse the demo without signing in. Run the backend locally and use{" "}
              <Link to="/login" className="font-semibold text-accent hover:underline">
                Sign in
              </Link>{" "}
              for upload and live chat.
            </>
          )}
        </p>
      </div>
    </PublicShell>
  );
}
