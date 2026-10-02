import { Layers } from "lucide-react";
import { Button } from "@/components/ui/Button";
import { Card } from "@/components/ui/Card";
import type { Flashcard, Job } from "@/types/api";
import { Badge } from "@/components/ui/Badge";

interface FlashcardsPanelProps {
  cards: Flashcard[];
  job: Job | null;
  onGenerate: () => void;
  loading: boolean;
  indexed: boolean;
}

export function FlashcardsPanel({ cards, job, onGenerate, loading, indexed }: FlashcardsPanelProps) {
  return (
    <Card>
      <div className="mb-4 flex flex-wrap items-center justify-between gap-3">
        <div className="flex items-center gap-2">
          <Layers className="h-5 w-5 text-accent" />
          <h2 className="font-display text-xl font-bold text-ink-950">Flashcards</h2>
        </div>
        <Button variant="secondary" onClick={onGenerate} loading={loading} disabled={!indexed}>
          Generate
        </Button>
      </div>
      {job && job.status !== "completed" && (
        <p className="mb-3 text-sm text-ink-500">
          Job: {job.status} {job.stage ? `· ${job.stage}` : ""}
        </p>
      )}
      {cards.length === 0 ? (
        <p className="text-sm text-ink-500">Generate cards from document content, then review them in the Review tab.</p>
      ) : (
        <ul className="grid gap-3 sm:grid-cols-2">
          {cards.map((c) => (
            <li key={c.id} className="rounded-xl border border-ink-100 p-4">
              <Badge label={c.section_tag || "general"} className="mb-2" />
              <p className="font-medium text-ink-900">{c.question}</p>
              <p className="mt-2 text-sm text-ink-600">{c.answer}</p>
            </li>
          ))}
        </ul>
      )}
    </Card>
  );
}
