import uuid

from sqlalchemy.orm import Session

from app.config import get_settings
from app.infrastructure.embeddings.minilm import encode_query
from app.models import Chunk
from app.services.faiss_store import FaissStore, SearchHit


def retrieve_chunks(db: Session, document_id: uuid.UUID, question: str) -> list[tuple[Chunk, float]]:
    settings = get_settings()
    qvec = encode_query(question)
    hits: list[SearchHit] = FaissStore(document_id).search(qvec, settings.retrieval_top_k)
    if not hits:
        return []
    id_to_score = {h.chunk_id: h.score for h in hits}
    chunks = db.query(Chunk).filter(Chunk.id.in_(list(id_to_score.keys()))).all()
    order = {cid: i for i, cid in enumerate(id_to_score.keys())}
    chunks.sort(key=lambda c: order.get(c.id, 999))
    return [(c, id_to_score[c.id]) for c in chunks if c.id in id_to_score]
