import { BookOpen, Sparkles } from "lucide-react";
import { Link } from "react-router-dom";
import { cn } from "@/lib/cn";

export function PublicShell({
  children,
  badge = "Demo · read-only",
}: {
  children: React.ReactNode;
  badge?: string;
}) {
  return (
    <div className="min-h-screen bg-gradient-to-br from-ink-50 via-white to-accent-muted/30">
      <header className="sticky top-0 z-40 border-b border-ink-100/80 bg-white/70 backdrop-blur-md">
        <div className="mx-auto flex max-w-6xl items-center justify-between gap-4 px-4 py-3 sm:px-6">
          <Link to="/" className="flex items-center gap-3">
            <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-accent text-white shadow-glow">
              <Sparkles className="h-5 w-5" />
            </div>
            <div>
              <p className="font-display text-lg font-bold leading-tight text-ink-950">Study RAG</p>
              <p className="text-xs text-ink-500">Grounded in your documents</p>
            </div>
          </Link>
          <div className="flex items-center gap-3">
            <span className={cn("rounded-full bg-amber-100 px-3 py-1 text-xs font-semibold text-amber-900")}>
              {badge}
            </span>
            <Link
              to="/demo"
              className="hidden rounded-xl px-3 py-2 text-sm font-medium text-ink-600 hover:bg-ink-100 sm:inline-flex sm:items-center sm:gap-2"
            >
              <BookOpen className="h-4 w-4" />
              Demo library
            </Link>
          </div>
        </div>
      </header>
      <main className="mx-auto max-w-6xl px-4 py-8 sm:px-6">{children}</main>
    </div>
  );
}
