import json
import uuid
from dataclasses import dataclass
from pathlib import Path

import faiss
import numpy as np

from app.config import get_settings


@dataclass
class SearchHit:
    chunk_id: uuid.UUID
    score: float
    faiss_row: int


class FaissStore:
    def __init__(self, document_id: uuid.UUID) -> None:
        self.document_id = document_id
        settings = get_settings()
        self.index_path = settings.faiss_dir / f"{document_id}.index"
        self.mapping_path = settings.faiss_dir / f"{document_id}.mapping.json"
        self._index: faiss.Index | None = None
        self._row_to_chunk: list[str] = []

    def build(self, chunk_ids: list[uuid.UUID], vectors: np.ndarray) -> str:
        if len(chunk_ids) == 0:
            raise ValueError("Cannot build FAISS index with zero chunks")
        dim = vectors.shape[1]
        index = faiss.IndexFlatIP(dim)
        index.add(vectors)
        self.index_path.parent.mkdir(parents=True, exist_ok=True)
        faiss.write_index(index, str(self.index_path))
        self._row_to_chunk = [str(cid) for cid in chunk_ids]
        self.mapping_path.write_text(json.dumps(self._row_to_chunk), encoding="utf-8")
        self._index = index
        return str(self.index_path)

    def load(self) -> None:
        if not self.index_path.exists() or not self.mapping_path.exists():
            raise FileNotFoundError(f"FAISS index missing for document {self.document_id}")
        self._index = faiss.read_index(str(self.index_path))
        self._row_to_chunk = json.loads(self.mapping_path.read_text(encoding="utf-8"))

    def search(self, query_vector: np.ndarray, top_k: int) -> list[SearchHit]:
        if self._index is None:
            self.load()
        assert self._index is not None
        q = query_vector.reshape(1, -1).astype(np.float32)
        scores, indices = self._index.search(q, top_k)
        hits: list[SearchHit] = []
        for score, row in zip(scores[0], indices[0], strict=True):
            if row < 0:
                continue
            chunk_id = uuid.UUID(self._row_to_chunk[int(row)])
            hits.append(SearchHit(chunk_id=chunk_id, score=float(score), faiss_row=int(row)))
        return hits

    def delete_files(self) -> None:
        if self.index_path.exists():
            self.index_path.unlink()
        if self.mapping_path.exists():
            self.mapping_path.unlink()
