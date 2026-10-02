import { useCallback, useEffect, useState } from "react";
import { documentsApi } from "@/api";
import { DocumentCard } from "@/components/documents/DocumentCard";
import { UploadDropzone } from "@/components/documents/UploadDropzone";
import { AppShell } from "@/components/layout/AppShell";
import { Card } from "@/components/ui/Card";
import { useJobPoll } from "@/hooks/useJobPoll";
import type { Document } from "@/types/api";

export function LibraryPage() {
  const [docs, setDocs] = useState<Document[]>([]);
  const [uploadJobId, setUploadJobId] = useState<string | null>(null);
  const [uploading, setUploading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const refresh = useCallback(async () => {
    const list = await documentsApi.list();
    setDocs(list);
  }, []);

  useEffect(() => {
    void refresh().catch(() => setError("Failed to load documents"));
  }, [refresh]);

  const { job: uploadJob } = useJobPoll(uploadJobId, () => {
    setUploadJobId(null);
    void refresh();
  });

  const onUpload = async (file: File) => {
    setUploading(true);
    setError(null);
    try {
      const res = await documentsApi.upload(file);
      setUploadJobId(res.job_id);
      await refresh();
    } catch (e) {
      setError(e instanceof Error ? e.message : "Upload failed");
    } finally {
      setUploading(false);
    }
  };

  const onDelete = async (id: string) => {
    if (!confirm("Delete this document and all study data?")) return;
    await documentsApi.remove(id);
    await refresh();
  };

  return (
    <AppShell>
      <div className="mb-8">
        <h1 className="font-display text-3xl font-bold text-ink-950">Your library</h1>
        <p className="mt-1 text-ink-500">Upload course materials and study with grounded chat & flashcards.</p>
      </div>
      <div className="grid gap-8 lg:grid-cols-5">
        <div className="lg:col-span-2">
          <UploadDropzone onFile={(f) => void onUpload(f)} disabled={uploading} />
          {uploadJob && (
            <p className="mt-3 text-sm text-ink-500">
              Indexing: {uploadJob.status} {uploadJob.stage ? `· ${uploadJob.stage}` : ""}
            </p>
          )}
          {error && <p className="mt-2 text-sm text-red-600">{error}</p>}
        </div>
        <div className="space-y-4 lg:col-span-3">
          {docs.length === 0 ? (
            <Card>
              <p className="text-sm text-ink-500">No documents yet. Upload your first PDF or DOCX.</p>
            </Card>
          ) : (
            docs.map((d) => <DocumentCard key={d.id} doc={d} onDelete={(id) => void onDelete(id)} />)
          )}
        </div>
      </div>
    </AppShell>
  );
}
