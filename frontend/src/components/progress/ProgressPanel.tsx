import { TrendingUp } from "lucide-react";
import { Card } from "@/components/ui/Card";
import type { ProgressResponse, WeakPointsResponse } from "@/types/api";

interface ProgressPanelProps {
  progress: ProgressResponse | null;
  weak: WeakPointsResponse | null;
  loading: boolean;
}

export function ProgressPanel({ progress, weak, loading }: ProgressPanelProps) {
  if (loading) return <Card><p className="text-sm text-ink-500">Loading progress…</p></Card>;
  if (!progress) return null;

  return (
    <div className="grid gap-6 lg:grid-cols-2">
      <Card>
        <div className="mb-4 flex items-center gap-2">
          <TrendingUp className="h-5 w-5 text-accent" />
          <h2 className="font-display text-xl font-bold text-ink-950">Study progress</h2>
        </div>
        <p className="mb-4 text-sm text-ink-500">
          {progress.total_questions} chat questions · {progress.total_reviews} card reviews
        </p>
        <div className="space-y-3">
          {progress.sections.map((s) => (
            <div key={s.section_tag} className="rounded-xl bg-ink-50 px-4 py-3">
              <div className="flex justify-between gap-2">
                <p className="font-medium text-ink-900">{s.section_tag || "General"}</p>
                {s.error_rate != null && (
                  <span className="text-xs text-ink-500">{Math.round(s.error_rate * 100)}% errors</span>
                )}
              </div>
              <p className="mt-1 text-xs text-ink-500">
                {s.question_count} questions · {s.review_count} reviews
              </p>
            </div>
          ))}
          {progress.sections.length === 0 && (
            <p className="text-sm text-ink-500">No activity yet for this document.</p>
          )}
        </div>
      </Card>
      <Card>
        <h2 className="font-display text-xl font-bold text-ink-950">Weak points</h2>
        <ul className="mt-4 space-y-3">
          {(weak?.weak_points ?? []).map((w) => (
            <li key={w.section_tag} className="rounded-xl border border-amber-200 bg-amber-50/80 px-4 py-3">
              <p className="font-medium text-amber-950">{w.section_tag}</p>
              <p className="text-xs text-amber-800/80">{Math.round(w.error_rate * 100)}% error rate</p>
              {w.suggestion_text && <p className="mt-2 text-sm text-amber-900">{w.suggestion_text}</p>}
            </li>
          ))}
          {(weak?.weak_points.length ?? 0) === 0 && (
            <p className="text-sm text-ink-500">No weak sections detected yet — keep studying!</p>
          )}
        </ul>
      </Card>
    </div>
  );
}
