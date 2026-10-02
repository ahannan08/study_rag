import { ListTree } from "lucide-react";
import { Card } from "@/components/ui/Card";
import { TableOfContents } from "@/components/topic-map/TableOfContents";

interface TopicMapPanelProps {
  topicMap: unknown | null;
  preparing: boolean;
  indexed: boolean;
}

export function TopicMapPanel({ topicMap, preparing, indexed }: TopicMapPanelProps) {
  return (
    <Card>
      <div className="mb-4 flex items-center gap-2">
        <ListTree className="h-5 w-5 text-accent" />
        <h2 className="font-display text-xl font-bold text-ink-950">Topics</h2>
      </div>
      {!indexed && (
        <p className="text-sm text-ink-500">Available after the document is indexed.</p>
      )}
      {indexed && preparing && !topicMap && (
        <p className="text-sm text-ink-500">Building table of contents…</p>
      )}
      {indexed && !preparing && !topicMap && (
        <p className="text-sm text-ink-500">Table of contents will appear here after processing.</p>
      )}
      {topicMap != null && <TableOfContents data={topicMap} />}
    </Card>
  );
}
