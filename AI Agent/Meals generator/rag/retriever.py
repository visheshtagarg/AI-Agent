import os
from typing import List, Dict, Any

import numpy as np

try:
    import faiss  # type: ignore
except ImportError:
    faiss = None  # type: ignore

try:
    from sentence_transformers import SentenceTransformer  # type: ignore
except ImportError:
    SentenceTransformer = None  # type: ignore


class FaissRetriever:
    def __init__(self, index_path: str, embedding_model: str = 'sentence-transformers/all-MiniLM-L6-v2'):
        self.index_path = index_path
        self.embedding_model_name = embedding_model
        self.index = None
        self.embedder = None
        self.available = False
        self._init()

    def _init(self):
        if faiss is None or SentenceTransformer is None:
            return
        if not os.path.isfile(self.index_path):
            return
        try:
            self.index = faiss.read_index(self.index_path)
            self.embedder = SentenceTransformer(self.embedding_model_name)
            self.available = True
        except Exception:
            self.index = None
            self.embedder = None
            self.available = False

    def embed(self, texts: List[str]) -> np.ndarray:
        if not self.available or self.embedder is None:
            return np.zeros((len(texts), 384), dtype='float32')
        vecs = self.embedder.encode(texts, convert_to_numpy=True)
        if vecs.dtype != np.float32:
            vecs = vecs.astype('float32')
        return vecs

    def query(self, text: str, k: int = 5) -> Dict[str, Any]:
        if not self.available or self.index is None:
            return {"ids": [], "distances": [], "meta": []}
        q = self.embed([text])
        distances, indices = self.index.search(q, k)
        return {"ids": indices.tolist()[0], "distances": distances.tolist()[0], "meta": []}

