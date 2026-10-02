export interface User {
  id: string;
  email: string;
  created_at: string;
}

export interface TokenResponse {
  access_token: string;
  token_type: string;
}

export interface Document {
  id: string;
  title: string;
  status: string;
  uploaded_at: string;
  indexed: boolean;
  topic_map_ready: boolean;
  flashcards_ready: boolean;
  chunk_count: number;
  topic_map?: unknown;
  topic_map_at?: string | null;
}

export interface DocumentUploadResponse {
  document_id: string;
  job_id: string;
}

export interface Job {
  id: string;
  document_id: string;
  type: string;
  status: string;
  stage: string | null;
  error: string | null;
  progress: number | null;
  started_at: string | null;
  finished_at: string | null;
  created_at: string;
}

export interface Citation {
  chunk_id: string;
  logical_page: number;
  section_path: string;
  excerpt: string;
  label: string;
}

export interface ChatResponse {
  answer: string;
  citations: Citation[];
  coverage_label: string;
  chunk_ids_used: string[];
  refusal: boolean;
}

export interface Flashcard {
  id: string;
  document_id: string;
  question: string;
  answer: string;
  section_tag: string;
  next_review_at: string | null;
}

export interface TopicMapResponse {
  document_id: string;
  topic_map: unknown;
  generated_at: string;
}

export interface SectionStat {
  section_tag: string;
  question_count: number;
  review_count: number;
  error_rate: number | null;
}

export interface ProgressResponse {
  document_id: string;
  sections: SectionStat[];
  total_questions: number;
  total_reviews: number;
}

export interface WeakPoint {
  section_tag: string;
  error_rate: number;
  suggestion_text: string | null;
}

export interface WeakPointsResponse {
  weak_points: WeakPoint[];
}

export type CoverageLabel = "fully_covered" | "partially_covered" | "not_in_document";
