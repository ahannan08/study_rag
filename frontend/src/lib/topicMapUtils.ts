export interface TopicEntry {
  title: string;
  summary?: string;
  section_ref?: string;
}

export interface TocLine {
  number: string;
  title: string;
  summary?: string;
  pageRef?: string;
  depth: number;
}

export function parseTopicMap(data: unknown): TopicEntry[] | null {
  if (!data) return null;
  if (Array.isArray(data)) {
    return data.map(normalizeEntry).filter(Boolean) as TopicEntry[];
  }
  const obj = data as Record<string, unknown>;
  const topics = obj.topics;
  if (Array.isArray(topics)) {
    return topics.map(normalizeEntry).filter(Boolean) as TopicEntry[];
  }
  return null;
}

function normalizeEntry(raw: unknown): TopicEntry | null {
  if (!raw || typeof raw !== "object") return null;
  const item = raw as Record<string, unknown>;
  const title = String(item.title ?? "").trim();
  if (!title) return null;
  return {
    title,
    summary: item.summary ? String(item.summary).trim() : undefined,
    section_ref: item.section_ref ? String(item.section_ref).trim() : undefined,
  };
}

function inferDepth(title: string, sectionRef?: string): number {
  const src = sectionRef || title;
  const chapter = /^(chapter|part|section)\s+\d+/i.test(src);
  const numbered = /^(\d+\.)+\d*\s/.test(src) || /^\d+\.\d+/.test(src);
  if (numbered && src.split(".").length > 2) return 2;
  if (chapter || numbered) return 1;
  return 0;
}

export function buildTocEntries(topics: TopicEntry[]): TocLine[] {
  let top = 0;
  let sub = 0;
  return topics.map((t) => {
    const depth = inferDepth(t.title, t.section_ref);
    let number: string;
    if (depth >= 2) {
      sub += 1;
      number = `${top}.${sub}`;
    } else {
      top += 1;
      sub = 0;
      number = String(top);
    }
    return {
      number,
      title: t.title,
      summary: t.summary,
      pageRef: t.section_ref,
      depth: depth >= 2 ? 2 : depth,
    };
  });
}
