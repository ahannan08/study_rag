import threading

import numpy as np
from sentence_transformers import SentenceTransformer

from app.config import get_settings

_lock = threading.Lock()
_model: SentenceTransformer | None = None


def get_embedder() -> SentenceTransformer:
    global _model
    if _model is None:
        with _lock:
            if _model is None:
                settings = get_settings()
                _model = SentenceTransformer(settings.embedding_model)
    return _model


def encode_texts(texts: list[str], batch_size: int = 32) -> np.ndarray:
    model = get_embedder()
    vectors = model.encode(texts, batch_size=batch_size, show_progress_bar=False, normalize_embeddings=True)
    return np.asarray(vectors, dtype=np.float32)


def encode_query(text: str) -> np.ndarray:
    return encode_texts([text])[0]
