import { ArrowLeft } from "lucide-react";
import { useEffect, useState } from "react";
import { Link, useParams } from "react-router-dom";
import { DemoChatPanel } from "@/components/chat/DemoChatPanel";
import { FlashcardsPanel } from "@/components/flashcards/FlashcardsPanel";
import { PublicShell } from "@/components/layout/PublicShell";
import { ProgressPanel } from "@/components/progress/ProgressPanel";
import { TopicMapPanel } from "@/components/topic-map/TopicMapPanel";
import { Badge } from "@/components/ui/Badge";
import { loadDemoDocumentSnapshot, type DemoDocumentSnapshot } from "@/demo/demoData";
import { cn } from "@/lib/cn";

type Tab = "chat" | "topics" | "flashcards" | "progress";

export function DemoDocumentPage() {
  const { documentId } = useParams<{ documentId: string }>();
  const [snap, setSnap] = useState<DemoDocumentSnapshot | null>(null);
  const [tab, setTab] = useState<Tab>("chat");
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!documentId) return;
    void loadDemoDocumentSnapshot(documentId)
      .then(setSnap)
      .catch(() => setError("Demo document not found"));
  }, [documentId]);

  if (!documentId || error) {
    return (
      <PublicShell>
        <p className="text-red-600">{error ?? "Missing document"}</p>
        <Link to="/demo" className="mt-4 inline-block text-accent">
          Back to demo library
        </Link>
      </PublicShell>
    );
  }

  const doc = snap?.document;
  const tabs: { id: Tab; label: string }[] = [
    { id: "chat", label: "Chat" },
    { id: "topics", label: "Topics" },
    { id: "flashcards", label: "Flashcards" },
    { id: "progress", label: "Progress" },
  ];

  return (
    <PublicShell>
      <Link to="/demo" className="mb-4 inline-flex items-center gap-2 text-sm font-medium text-ink-500 hover:text-ink-800">
        <ArrowLeft className="h-4 w-4" />
        Demo library
      </Link>
      <div className="mb-6">
        <h1 className="font-display text-2xl font-bold text-ink-950 sm:text-3xl">{doc?.title ?? "…"}</h1>
        {doc && (
          <div className="mt-2 flex flex-wrap gap-2">
            <Badge label={doc.status} />
            {doc.indexed && <Badge label="indexed" />}
            {doc.topic_map_ready && <Badge label="topics" />}
            {doc.flashcards_ready && <Badge label="flashcards" />}
          </div>
        )}
      </div>
      <div className="mb-6 flex gap-2 overflow-x-auto rounded-2xl bg-white/80 p-1 shadow-card">
        {tabs.map((t) => (
          <button
            key={t.id}
            type="button"
            onClick={() => setTab(t.id)}
            className={cn(
              "rounded-xl px-4 py-2 text-sm font-semibold transition whitespace-nowrap",
              tab === t.id ? "bg-ink-950 text-white" : "text-ink-600 hover:bg-ink-100",
            )}
          >
            {t.label}
          </button>
        ))}
      </div>
      {!snap && <p className="text-sm text-ink-500">Loading…</p>}
      {snap && tab === "chat" && <DemoChatPanel samples={snap.chat_samples} />}
      {snap && tab === "topics" && (
        <TopicMapPanel topicMap={snap.document.topic_map ?? null} preparing={false} indexed={snap.document.indexed} />
      )}
      {snap && tab === "flashcards" && (
        <FlashcardsPanel cards={snap.flashcards} preparing={false} indexed={snap.document.indexed} />
      )}
      {snap && tab === "progress" && (
        <ProgressPanel progress={snap.progress} weak={snap.weak_points} loading={false} />
      )}
    </PublicShell>
  );
}
