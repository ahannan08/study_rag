import { FileText, Trash2 } from "lucide-react";
import { Link } from "react-router-dom";
import type { Document } from "@/types/api";
import { Badge } from "@/components/ui/Badge";
import { Button } from "@/components/ui/Button";
import { Card } from "@/components/ui/Card";

interface DocumentCardProps {
  doc: Document;
  onDelete: (id: string) => void;
}

export function DocumentCard({ doc, onDelete }: DocumentCardProps) {
  return (
    <Card className="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
      <div className="flex min-w-0 items-start gap-3">
        <div className="rounded-xl bg-ink-100 p-3 text-ink-600">
          <FileText className="h-6 w-6" />
        </div>
        <div className="min-w-0">
          <Link to={`/documents/${doc.id}`} className="truncate font-semibold text-ink-900 hover:text-accent">
            {doc.title}
          </Link>
          <p className="mt-1 text-sm text-ink-500">
            {doc.chunk_count} chunks · {new Date(doc.uploaded_at).toLocaleDateString()}
          </p>
          <div className="mt-2 flex flex-wrap gap-2">
            <Badge label={doc.status} />
            {doc.topic_map_ready && <Badge label="topic map" className="bg-violet-100 text-violet-800" />}
            {doc.flashcards_ready && <Badge label="flashcards" className="bg-sky-100 text-sky-800" />}
          </div>
        </div>
      </div>
      <div className="flex shrink-0 gap-2">
        <Link
          to={`/documents/${doc.id}`}
          className="rounded-xl bg-ink-950 px-4 py-2 text-sm font-semibold text-white hover:bg-ink-800"
        >
          Open
        </Link>
        <Button variant="ghost" onClick={() => onDelete(doc.id)} aria-label="Delete">
          <Trash2 className="h-4 w-4 text-red-500" />
        </Button>
      </div>
    </Card>
  );
}
