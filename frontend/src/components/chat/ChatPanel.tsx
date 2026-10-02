import { Send } from "lucide-react";
import { useState } from "react";
import { chatApi } from "@/api";
import { Badge } from "@/components/ui/Badge";
import { Button } from "@/components/ui/Button";
import { Card } from "@/components/ui/Card";
import { Input } from "@/components/ui/Input";
import type { ChatResponse, Citation } from "@/types/api";

interface Message {
  role: "user" | "assistant";
  text: string;
  meta?: ChatResponse;
}

function CitationList({ citations }: { citations: Citation[] }) {
  if (!citations.length) return null;
  return (
    <ul className="mt-3 space-y-2 border-t border-ink-100 pt-3">
      {citations.map((c) => (
        <li key={c.chunk_id} className="rounded-lg bg-ink-50 px-3 py-2 text-xs text-ink-600">
          <p className="font-medium text-ink-800">{c.label}</p>
          <p className="mt-1 line-clamp-2">{c.excerpt}</p>
        </li>
      ))}
    </ul>
  );
}

export function ChatPanel({ documentId, enabled }: { documentId: string; enabled: boolean }) {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const send = async () => {
    const q = input.trim();
    if (!q || !enabled) return;
    setInput("");
    setError(null);
    setMessages((m) => [...m, { role: "user", text: q }]);
    setLoading(true);
    try {
      const res = await chatApi.ask(documentId, q);
      setMessages((m) => [...m, { role: "assistant", text: res.answer, meta: res }]);
    } catch (e) {
      setError(e instanceof Error ? e.message : "Chat failed");
    } finally {
      setLoading(false);
    }
  };

  return (
    <Card className="flex h-[min(70vh,640px)] flex-col">
      <div className="mb-4 flex items-center justify-between">
        <h2 className="font-display text-xl font-bold text-ink-950">Ask your document</h2>
        {!enabled && <Badge label="indexing" />}
      </div>
      <div className="flex-1 space-y-4 overflow-y-auto pr-1">
        {messages.length === 0 && (
          <p className="text-sm text-ink-500">
            Questions are answered only from this file, with section citations and coverage signals.
          </p>
        )}
        {messages.map((msg, i) => (
          <div
            key={i}
            className={msg.role === "user" ? "ml-8 rounded-2xl bg-accent px-4 py-3 text-white" : "mr-4 rounded-2xl bg-ink-50 px-4 py-3 text-ink-800"}
          >
            <p className="whitespace-pre-wrap text-sm">{msg.text}</p>
            {msg.meta && (
              <>
                <div className="mt-2 flex flex-wrap gap-2">
                  <Badge label={msg.meta.coverage_label} />
                  {msg.meta.refusal && <Badge label="refusal" className="bg-amber-100 text-amber-800" />}
                </div>
                <CitationList citations={msg.meta.citations} />
              </>
            )}
          </div>
        ))}
      </div>
      {error && <p className="mt-2 text-sm text-red-600">{error}</p>}
      <form
        className="mt-4 flex gap-2"
        onSubmit={(e) => {
          e.preventDefault();
          void send();
        }}
      >
        <Input
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder={enabled ? "What does this document say about…?" : "Wait until indexing completes"}
          disabled={!enabled || loading}
        />
        <Button type="submit" loading={loading} disabled={!enabled}>
          <Send className="h-4 w-4" />
        </Button>
      </form>
    </Card>
  );
}
