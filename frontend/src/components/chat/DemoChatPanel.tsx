import { useState } from "react";
import { Badge } from "@/components/ui/Badge";
import { Button } from "@/components/ui/Button";
import { Card } from "@/components/ui/Card";
import type { DemoChatSample } from "@/demo/demoData";
import type { ChatResponse, Citation } from "@/types/api";

interface Message {
  role: "user" | "assistant";
  text: string;
  meta?: Pick<ChatResponse, "citations" | "coverage_label">;
}

function CitationList({ citations }: { citations: Citation[] }) {
  if (!citations.length) return null;
  return (
    <ul className="mt-3 space-y-2 border-t border-ink-100 pt-3">
      {citations.map((c, i) => (
        <li key={`${c.chunk_id}-${i}`} className="rounded-lg bg-ink-50 px-3 py-2 text-xs text-ink-600">
          <p className="font-medium text-ink-800">{c.label}</p>
          <p className="mt-1 line-clamp-2">{c.excerpt}</p>
        </li>
      ))}
    </ul>
  );
}

export function DemoChatPanel({ samples }: { samples: DemoChatSample[] }) {
  const [messages, setMessages] = useState<Message[]>([]);

  const showSample = (sample: DemoChatSample) => {
    setMessages([
      { role: "user", text: sample.question },
      {
        role: "assistant",
        text: sample.answer,
        meta: { coverage_label: sample.coverage_label, citations: sample.citations },
      },
    ]);
  };

  return (
    <Card className="flex h-[min(70vh,640px)] flex-col">
      <div className="mb-4 flex flex-wrap items-center justify-between gap-2">
        <h2 className="font-display text-xl font-bold text-ink-950">Ask your document</h2>
        <Badge label="sample answers" className="bg-amber-100 text-amber-900" />
      </div>
      <p className="mb-3 text-sm text-ink-500">
        Live chat needs a running backend. Try a sample question recorded from local testing:
      </p>
      <div className="mb-4 flex flex-wrap gap-2">
        {samples.map((s, i) => (
          <Button key={i} variant="secondary" type="button" className="text-left text-xs" onClick={() => showSample(s)}>
            {s.question.length > 48 ? `${s.question.slice(0, 48)}…` : s.question}
          </Button>
        ))}
      </div>
      <div className="flex-1 space-y-4 overflow-y-auto pr-1">
        {messages.length === 0 && (
          <p className="text-sm text-ink-500">Pick a sample question above to see a grounded-style answer.</p>
        )}
        {messages.map((msg, i) => (
          <div
            key={i}
            className={
              msg.role === "user"
                ? "ml-8 rounded-2xl bg-accent px-4 py-3 text-white"
                : "mr-4 rounded-2xl bg-ink-50 px-4 py-3 text-ink-800"
            }
          >
            <p className="whitespace-pre-wrap text-sm">{msg.text}</p>
            {msg.meta && (
              <>
                <div className="mt-2 flex flex-wrap gap-2">
                  <Badge label={msg.meta.coverage_label} />
                </div>
                <CitationList citations={msg.meta.citations} />
              </>
            )}
          </div>
        ))}
      </div>
    </Card>
  );
}
