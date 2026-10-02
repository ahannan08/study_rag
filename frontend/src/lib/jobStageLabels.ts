export function jobStageLabel(stage: string | null | undefined, status: string): string {
  if (status === "completed") return "Done";
  if (status === "failed") return "Failed";
  switch (stage) {
    case "parsing":
    case "embedding":
    case "storing":
      return "Indexing…";
    case "topic_map":
      return "Building topics…";
    case "flashcards":
      return "Creating flashcards…";
    default:
      return stage ? `Processing (${stage})…` : "Processing…";
  }
}
