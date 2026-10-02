import type { ReactNode } from "react";
import { ListTree } from "lucide-react";
import { Button } from "@/components/ui/Button";
import { Card } from "@/components/ui/Card";
import type { Job } from "@/types/api";

interface TopicMapPanelProps {
  topicMap: unknown | null;
  job: Job | null;
  onGenerate: () => void;
  loading: boolean;
  indexed: boolean;
}

function renderTopics(data: unknown): ReactNode {
  if (!data) return null;
  const obj = data as Record<string, unknown>;
  const topics = (obj.topics ?? data) as unknown[];
  if (!Array.isArray(topics)) {
    return <pre className="overflow-auto text-xs text-ink-700">{JSON.stringify(data, null, 2)}</pre>;
  }
  return (
    <ul className="space-y-3">
      {topics.map((t, i) => {
        const item = t as Record<string, string>;
        return (
          <li key={i} className="rounded-xl border border-ink-100 bg-ink-50/80 px-4 py-3">
            <p className="font-semibold text-ink-900">{item.title ?? `Topic ${i + 1}`}</p>
            {item.summary && <p className="mt-1 text-sm text-ink-600">{item.summary}</p>}
            {item.section_ref && <p className="mt-1 text-xs text-ink-400">{item.section_ref}</p>}
          </li>
        );
      })}
    </ul>
  );
}

export function TopicMapPanel({ topicMap, job, onGenerate, loading, indexed }: TopicMapPanelProps) {
  return (
    <Card>
      <div className="mb-4 flex flex-wrap items-center justify-between gap-3">
        <div className="flex items-center gap-2">
          <ListTree className="h-5 w-5 text-accent" />
          <h2 className="font-display text-xl font-bold text-ink-950">Topic map</h2>
        </div>
        <Button variant="secondary" onClick={onGenerate} loading={loading} disabled={!indexed}>
          Generate
        </Button>
      </div>
      {job && job.status !== "completed" && (
        <p className="mb-3 text-sm text-ink-500">
          Job: {job.status} {job.stage ? `· ${job.stage}` : ""}
        </p>
      )}
      {topicMap ? renderTopics(topicMap) : (
        <p className="text-sm text-ink-500">No topic map yet. Generate one from your indexed document.</p>
      )}
    </Card>
  );
}
