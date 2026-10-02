import { useState } from "react";
import { ChevronDown, ChevronRight } from "lucide-react";
import type { Flashcard } from "@/types/api";
import { cn } from "@/lib/cn";

interface FlashcardGroupProps {
  sectionTag: string;
  cards: Flashcard[];
  previewCount?: number;
}

export function FlashcardGroup({ sectionTag, cards, previewCount = 4 }: FlashcardGroupProps) {
  const [open, setOpen] = useState(true);
  const [expanded, setExpanded] = useState(false);
  const visible = expanded ? cards : cards.slice(0, previewCount);
  const hidden = cards.length - previewCount;

  return (
    <section className="rounded-xl border border-ink-100 bg-white/80">
      <button
        type="button"
        className="flex w-full items-center justify-between gap-2 px-4 py-3 text-left"
        onClick={() => setOpen((o) => !o)}
      >
        <span className="flex items-center gap-2 font-semibold text-ink-900">
          {open ? <ChevronDown className="h-4 w-4" /> : <ChevronRight className="h-4 w-4" />}
          {sectionTag}
        </span>
        <span className="text-xs font-medium text-ink-500">{cards.length} cards</span>
      </button>
      {open && (
        <ul className="space-y-2 border-t border-ink-100 px-4 py-3">
          {visible.map((c) => (
            <li key={c.id} className="rounded-lg bg-ink-50/90 px-3 py-2.5">
              <p className="text-sm font-medium text-ink-900">{c.question}</p>
              <p className="mt-1 text-xs text-ink-600">{c.answer}</p>
            </li>
          ))}
          {!expanded && hidden > 0 && (
            <li>
              <button
                type="button"
                className="text-sm font-semibold text-accent hover:underline"
                onClick={() => setExpanded(true)}
              >
                Show all {cards.length} cards
              </button>
            </li>
          )}
          {expanded && cards.length > previewCount && (
            <li>
              <button
                type="button"
                className={cn("text-sm font-medium text-ink-500 hover:text-ink-800")}
                onClick={() => setExpanded(false)}
              >
                Show fewer
              </button>
            </li>
          )}
        </ul>
      )}
    </section>
  );
}
