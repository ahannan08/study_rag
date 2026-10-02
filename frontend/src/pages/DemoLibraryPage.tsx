import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { DemoDocumentCard } from "@/components/documents/DemoDocumentCard";
import { PublicShell } from "@/components/layout/PublicShell";
import { Card } from "@/components/ui/Card";
import { loadDemoManifest } from "@/demo/demoData";
import type { Document } from "@/types/api";

export function DemoLibraryPage() {
  const [docs, setDocs] = useState<Document[]>([]);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    void loadDemoManifest()
      .then((m) => setDocs(m.documents))
      .catch(() => setError("Demo data not found. Run export_demo_snapshot from the backend."));
  }, []);

  return (
    <PublicShell>
      <Link to="/" className="mb-4 inline-block text-sm font-medium text-ink-500 hover:text-ink-800">
        ← Home
      </Link>
      <h1 className="font-display text-3xl font-bold text-ink-950">Demo library</h1>
      <p className="mt-1 text-ink-500">Sample indexed documents bundled for this portfolio site.</p>
      <div className="mt-8 space-y-4">
        {error && (
          <Card>
            <p className="text-sm text-red-600">{error}</p>
          </Card>
        )}
        {!error && docs.length === 0 && (
          <Card>
            <p className="text-sm text-ink-500">Loading…</p>
          </Card>
        )}
        {docs.map((d) => (
          <DemoDocumentCard key={d.id} doc={d} />
        ))}
      </div>
    </PublicShell>
  );
}
