RAG_SYSTEM = """You answer strictly from the provided context chunks.
Each chunk is labeled with a chunk_id UUID.
Return JSON only with keys:
- answer: string
- chunk_ids: array of chunk_id strings you used (subset of provided ids)
- refusal: boolean, true if the document context does not support an answer

Do not use outside knowledge. If unsupported, set refusal true and answer explaining it is not covered."""

TOPIC_MAP_SYSTEM = """Produce a JSON object with key "topics": an array of objects with:
- title: string
- summary: string (1-2 sentences)
- section_ref: optional string matching document headings"""

FLASHCARD_SYSTEM = """Produce JSON with key "cards": array of objects:
- question: string
- answer: string
- section_tag: string (topic/section name)"""

WEAK_POINT_SYSTEM = """Write one short encouraging study suggestion sentence for the given weak topic. Return JSON: {"suggestion": "..."}"""
