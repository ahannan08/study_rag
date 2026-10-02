import { ArrowLeft } from "lucide-react";
import { useCallback, useEffect, useState } from "react";
import { Link, useParams } from "react-router-dom";
import { documentsApi, flashcardsApi, progressApi } from "@/api";
import { ChatPanel } from "@/components/chat/ChatPanel";
import { FlashcardsPanel } from "@/components/flashcards/FlashcardsPanel";
import { AppShell } from "@/components/layout/AppShell";
import { ProgressPanel } from "@/components/progress/ProgressPanel";
import { TopicMapPanel } from "@/components/topic-map/TopicMapPanel";
import { Badge } from "@/components/ui/Badge";
import type { Document, Flashcard, ProgressResponse, WeakPointsResponse } from "@/types/api";
import { cn } from "@/lib/cn";

type Tab = "chat" | "topics" | "flashcards" | "progress";

export function DocumentPage() {
  const { documentId } = useParams<{ documentId: string }>();
  const [doc, setDoc] = useState<Document | null>(null);
  const [tab, setTab] = useState<Tab>("chat");
  const [topicMap, setTopicMap] = useState<unknown | null>(null);
  const [cards, setCards] = useState<Flashcard[]>([]);
  const [progress, setProgress] = useState<ProgressResponse | null>(null);
  const [weak, setWeak] = useState<WeakPointsResponse | null>(null);
  const [error, setError] = useState<string | null>(null);

  const refreshDoc = useCallback(async () => {
    if (!documentId) return;
    const d = await documentsApi.get(documentId);
    setDoc(d);
    setTopicMap(d.topic_map ?? null);
    return d;
  }, [documentId]);

  const refreshFlash = useCallback(async () => {
    if (!documentId) return;
    setCards(await flashcardsApi.list(documentId));
  }, [documentId]);

  const refreshProgress = useCallback(async () => {
    if (!documentId) return;
    setProgress(await progressApi.get(documentId));
    setWeak(await progressApi.weakPoints(documentId));
  }, [documentId]);

  useEffect(() => {
    void refreshDoc().catch(() => setError("Document not found"));
    void refreshFlash();
  }, [refreshDoc, refreshFlash]);

  useEffect(() => {
    if (tab === "progress") void refreshProgress();
  }, [tab, refreshProgress]);

  const pipelinePending =
    !!doc?.indexed && (!doc.topic_map_ready || !doc.flashcards_ready);

  useEffect(() => {
    if (!documentId || !pipelinePending) return;
    const id = window.setInterval(() => {
      void refreshDoc().then((d) => {
        if (d?.flashcards_ready) void refreshFlash();
      });
    }, 3000);
    return () => window.clearInterval(id);
  }, [documentId, pipelinePending, refreshDoc, refreshFlash]);

  if (!documentId || error) {
    return (
      <AppShell>
        <p className="text-red-600">{error ?? "Missing document"}</p>
        <Link to="/" className="mt-4 inline-block text-accent">
          Back to library
        </Link>
      </AppShell>
    );
  }

  const tabs: { id: Tab; label: string }[] = [
    { id: "chat", label: "Chat" },
    { id: "topics", label: "Topics" },
    { id: "flashcards", label: "Flashcards" },
    { id: "progress", label: "Progress" },
  ];

  const topicsPreparing = !!doc?.indexed && !doc.topic_map_ready;
  const flashPreparing = !!doc?.indexed && !doc.flashcards_ready;

  return (
    <AppShell>
      <Link to="/" className="mb-4 inline-flex items-center gap-2 text-sm font-medium text-ink-500 hover:text-ink-800">
        <ArrowLeft className="h-4 w-4" />
        Library
      </Link>
      <div className="mb-6 flex flex-wrap items-end justify-between gap-4">
        <div>
          <h1 className="font-display text-2xl font-bold text-ink-950 sm:text-3xl">{doc?.title ?? "…"}</h1>
          <div className="mt-2 flex flex-wrap gap-2">
            {doc && <Badge label={doc.status} />}
            {doc?.indexed && <Badge label="indexed" />}
            {doc?.topic_map_ready && <Badge label="topics" />}
            {doc?.flashcards_ready && <Badge label="flashcards" />}
          </div>
        </div>
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
      {tab === "chat" && documentId && <ChatPanel documentId={documentId} enabled={!!doc?.indexed} />}
      {tab === "topics" && (
        <TopicMapPanel
          topicMap={topicMap}
          preparing={topicsPreparing}
          indexed={!!doc?.indexed}
        />
      )}
      {tab === "flashcards" && (
        <FlashcardsPanel
          cards={cards}
          preparing={flashPreparing}
          indexed={!!doc?.indexed}
        />
      )}
      {tab === "progress" && <ProgressPanel progress={progress} weak={weak} loading={false} />}
    </AppShell>
  );
}
