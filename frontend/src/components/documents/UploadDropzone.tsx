import { Upload } from "lucide-react";
import { useCallback, useState } from "react";
import { cn } from "@/lib/cn";

interface UploadDropzoneProps {
  onFile: (file: File) => void;
  disabled?: boolean;
}

export function UploadDropzone({ onFile, disabled }: UploadDropzoneProps) {
  const [drag, setDrag] = useState(false);

  const handleFiles = useCallback(
    (files: FileList | null) => {
      const file = files?.[0];
      if (file) onFile(file);
    },
    [onFile],
  );

  return (
    <label
      className={cn(
        "flex cursor-pointer flex-col items-center justify-center rounded-2xl border-2 border-dashed px-6 py-10 transition",
        drag ? "border-accent bg-accent-muted/40" : "border-ink-200 bg-white/60 hover:border-accent/50",
        disabled && "pointer-events-none opacity-50",
      )}
      onDragOver={(e) => {
        e.preventDefault();
        setDrag(true);
      }}
      onDragLeave={() => setDrag(false)}
      onDrop={(e) => {
        e.preventDefault();
        setDrag(false);
        handleFiles(e.dataTransfer.files);
      }}
    >
      <Upload className="mb-3 h-10 w-10 text-accent" />
      <p className="font-medium text-ink-800">Drop PDF or DOCX here</p>
      <p className="mt-1 text-sm text-ink-500">or click to browse</p>
      <input
        type="file"
        accept=".pdf,.docx,.doc"
        className="sr-only"
        disabled={disabled}
        onChange={(e) => handleFiles(e.target.files)}
      />
    </label>
  );
}
