import type { ChatResponse, Document, Flashcard, ProgressResponse, WeakPointsResponse } from "@/types/api";

export interface DemoChatSample {
  question: string;
  answer: string;
  coverage_label: string;
  citations: ChatResponse["citations"];
}

export interface DemoDocumentSnapshot {
  document: Document;
  flashcards: Flashcard[];
  progress: ProgressResponse;
  weak_points: WeakPointsResponse;
  chat_samples: DemoChatSample[];
}

export interface DemoManifest {
  documents: Document[];
}

export async function loadDemoManifest(): Promise<DemoManifest> {
  const res = await fetch("/demo/manifest.json");
  if (!res.ok) throw new Error("Demo manifest not found");
  return res.json() as Promise<DemoManifest>;
}

export async function loadDemoDocumentSnapshot(documentId: string): Promise<DemoDocumentSnapshot> {
  const res = await fetch(`/demo/documents/${documentId}.json`);
  if (!res.ok) throw new Error("Demo document not found");
  return res.json() as Promise<DemoDocumentSnapshot>;
}
