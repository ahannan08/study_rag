import { useEffect, useState } from "react";
import { flashcardsApi } from "@/api";
import { AppShell } from "@/components/layout/AppShell";
import { Button } from "@/components/ui/Button";
import { Card } from "@/components/ui/Card";
import type { Flashcard } from "@/types/api";
import { cn } from "@/lib/cn";

export function ReviewPage() {
  const [due, setDue] = useState<Flashcard[]>([]);
  const [index, setIndex] = useState(0);
  const [flipped, setFlipped] = useState(false);
  const [loading, setLoading] = useState(true);

  const load = async () => {
    setLoading(true);
    try {
      const cards = await flashcardsApi.due();
      setDue(cards);
      setIndex(0);
      setFlipped(false);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    void load();
  }, []);

  const current = due[index];

  const answer = async (correct: boolean) => {
    if (!current) return;
    await flashcardsApi.review(current.id, correct);
    if (index + 1 < due.length) {
      setIndex((i) => i + 1);
      setFlipped(false);
    } else {
      await load();
    }
  };

  return (
    <AppShell>
      <h1 className="font-display text-3xl font-bold text-ink-950">Spaced review</h1>
      <p className="mt-1 text-ink-500">Cards due across all your documents.</p>
      {loading ? (
        <Card className="mt-8"><p className="text-sm text-ink-500">Loading…</p></Card>
      ) : !current ? (
        <Card className="mt-8">
          <p className="text-ink-600">You&apos;re all caught up — no cards due right now.</p>
        </Card>
      ) : (
        <div className="mx-auto mt-8 max-w-xl">
          <p className="mb-3 text-center text-sm text-ink-500">
            Card {index + 1} of {due.length}
          </p>
          <button
            type="button"
            onClick={() => setFlipped((f) => !f)}
            className={cn(
              "min-h-[220px] w-full rounded-3xl border border-ink-100 bg-white p-8 text-left shadow-card transition hover:shadow-glow",
            )}
          >
            <p className="text-xs font-medium uppercase tracking-wide text-accent">{current.section_tag || "General"}</p>
            <p className="mt-4 font-display text-xl font-semibold text-ink-950">
              {flipped ? current.answer : current.question}
            </p>
            <p className="mt-6 text-sm text-ink-400">{flipped ? "Tap to see question" : "Tap to reveal answer"}</p>
          </button>
          {flipped && (
            <div className="mt-6 flex gap-3">
              <Button variant="danger" className="flex-1" onClick={() => void answer(false)}>
                Again
              </Button>
              <Button className="flex-1" onClick={() => void answer(true)}>
                Got it
              </Button>
            </div>
          )}
        </div>
      )}
    </AppShell>
  );
}
