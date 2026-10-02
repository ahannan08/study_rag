import { cn } from "@/lib/cn";

const styles: Record<string, string> = {
  indexed: "bg-emerald-100 text-emerald-800",
  indexing: "bg-amber-100 text-amber-800",
  uploading: "bg-slate-100 text-slate-700",
  failed: "bg-red-100 text-red-800",
  queued: "bg-slate-100 text-slate-600",
  running: "bg-indigo-100 text-indigo-800",
  completed: "bg-emerald-100 text-emerald-800",
  fully_covered: "bg-emerald-100 text-emerald-800",
  partially_covered: "bg-amber-100 text-amber-800",
  not_in_document: "bg-slate-100 text-slate-600",
};

export function Badge({ label, className }: { label: string; className?: string }) {
  const key = label.toLowerCase().replace(/\s+/g, "_");
  return (
    <span
      className={cn(
        "inline-flex rounded-full px-2.5 py-0.5 text-xs font-medium capitalize",
        styles[key] ?? "bg-ink-100 text-ink-700",
        className,
      )}
    >
      {label.replace(/_/g, " ")}
    </span>
  );
}
