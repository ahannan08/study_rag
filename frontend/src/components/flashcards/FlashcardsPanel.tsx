import { Layers } from "lucide-react";
import { Card } from "@/components/ui/Card";
import type { Flashcard } from "@/types/api";
import { FlashcardGroup } from "@/components/flashcards/FlashcardGroup";

interface FlashcardsPanelProps {
  cards: Flashcard[];
  preparing: boolean;
  indexed: boolean;
}

function groupCards(cards: Flashcard[]): Map<string, Flashcard[]> {
  const map = new Map<string, Flashcard[]>();
  for (const c of cards) {
    const tag = c.section_tag?.trim() || "General";
    const list = map.get(tag) ?? [];
    list.push(c);
    map.set(tag, list);
  }
  return new Map([...map.entries()].sort(([a], [b]) => a.localeCompare(b)));
}

export function FlashcardsPanel({ cards, preparing, indexed }: FlashcardsPanelProps) {
  const groups = groupCards(cards);

  return (
    <Card>
      <div className="mb-4 flex items-center gap-2">
        <Layers className="h-5 w-5 text-accent" />
        <h2 className="font-display text-xl font-bold text-ink-950">Flashcards</h2>
      </div>
      {!indexed && (
        <p className="text-sm text-ink-500">Available after the document is indexed.</p>
      )}
      {indexed && preparing && cards.length === 0 && (
        <p className="text-sm text-ink-500">Generating flashcards by topic…</p>
      )}
      {indexed && !preparing && cards.length === 0 && (
        <p className="text-sm text-ink-500">Flashcards will appear here after processing.</p>
      )}
      {cards.length > 0 && (
        <div className="space-y-4">
          {[...groups.entries()].map(([tag, sectionCards]) => (
            <FlashcardGroup key={tag} sectionTag={tag} cards={sectionCards} previewCount={4} />
          ))}
        </div>
      )}
    </Card>
  );
}
