import { buildTocEntries, parseTopicMap, type TocLine } from "@/lib/topicMapUtils";
import { cn } from "@/lib/cn";

function TocRow({ line }: { line: TocLine }) {
  const indent = line.depth === 2 ? "pl-8" : line.depth === 1 ? "pl-4" : "pl-0";
  return (
    <li className={cn("py-2", indent)}>
      <div className="flex items-baseline gap-2">
        <span className="shrink-0 font-mono text-xs font-semibold text-accent">{line.number}.</span>
        <span className="min-w-0 flex-1 font-medium text-ink-950">{line.title}</span>
        {line.pageRef && (
          <span className="hidden shrink-0 text-xs text-ink-400 sm:inline">{line.pageRef}</span>
        )}
      </div>
      {line.summary && (
        <p className="mt-1 pl-6 text-sm leading-relaxed text-ink-600">{line.summary}</p>
      )}
    </li>
  );
}

export function TableOfContents({ data }: { data: unknown }) {
  const topics = parseTopicMap(data);
  if (!topics?.length) {
    return (
      <pre className="overflow-auto rounded-lg bg-ink-50 p-4 text-xs text-ink-700">
        {JSON.stringify(data, null, 2)}
      </pre>
    );
  }

  const lines = buildTocEntries(topics);
  return (
    <div>
      <p className="mb-4 border-b border-ink-200 pb-2 font-display text-lg font-bold text-ink-950">
        Table of Contents
      </p>
      <ol className="divide-y divide-ink-100">
        {lines.map((line, i) => (
          <TocRow key={`${line.number}-${i}`} line={line} />
        ))}
      </ol>
    </div>
  );
}
