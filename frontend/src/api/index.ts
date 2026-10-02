import { apiFetch } from "./client";
import type {
  ChatResponse,
  Document,
  DocumentUploadResponse,
  Flashcard,
  Job,
  ProgressResponse,
  TokenResponse,
  TopicMapResponse,
  User,
  WeakPointsResponse,
} from "@/types/api";

export const authApi = {
  register: (email: string, password: string) =>
    apiFetch<User>("/api/v1/auth/register", {
      method: "POST",
      body: JSON.stringify({ email, password }),
    }, false),

  login: (email: string, password: string) =>
    apiFetch<TokenResponse>("/api/v1/auth/login", {
      method: "POST",
      body: JSON.stringify({ email, password }),
    }, false),

  me: () => apiFetch<User>("/api/v1/auth/me"),
};

export const documentsApi = {
  list: () => apiFetch<Document[]>("/api/v1/documents"),
  get: (id: string) => apiFetch<Document>(`/api/v1/documents/${id}`),
  upload: (file: File) => {
    const form = new FormData();
    form.append("file", file);
    return apiFetch<DocumentUploadResponse>("/api/v1/documents", { method: "POST", body: form });
  },
  remove: (id: string) =>
    apiFetch<void>(`/api/v1/documents/${id}`, { method: "DELETE" }),
};

export const jobsApi = {
  get: (id: string) => apiFetch<Job>(`/api/v1/jobs/${id}`),
};

export const chatApi = {
  ask: (documentId: string, question: string) =>
    apiFetch<ChatResponse>(`/api/v1/documents/${documentId}/chat`, {
      method: "POST",
      body: JSON.stringify({ question }),
    }),
};

export const topicMapApi = {
  get: (documentId: string) =>
    apiFetch<TopicMapResponse>(`/api/v1/documents/${documentId}/topic-map`),
  generate: (documentId: string) =>
    apiFetch<{ job_id: string }>(`/api/v1/documents/${documentId}/topic-map/generate`, {
      method: "POST",
    }),
};

export const flashcardsApi = {
  list: (documentId: string) =>
    apiFetch<Flashcard[]>(`/api/v1/documents/${documentId}/flashcards`),
  generate: (documentId: string) =>
    apiFetch<{ job_id: string }>(`/api/v1/documents/${documentId}/flashcards/generate`, {
      method: "POST",
    }),
  due: () => apiFetch<Flashcard[]>("/api/v1/flashcards/due"),
  review: (flashcardId: string, correct: boolean) =>
    apiFetch<{ flashcard_id: string; next_review_at: string | null; interval_days: number; ease_factor: number }>(
      `/api/v1/flashcards/${flashcardId}/review`,
      { method: "POST", body: JSON.stringify({ correct }) },
    ),
};

export const progressApi = {
  get: (documentId: string) =>
    apiFetch<ProgressResponse>(`/api/v1/documents/${documentId}/progress`),
  weakPoints: (documentId: string) =>
    apiFetch<WeakPointsResponse>(`/api/v1/documents/${documentId}/weak-points`),
};
