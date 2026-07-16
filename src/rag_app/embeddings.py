"""Embedding model wrapper using sentence-transformers."""
from typing import List

from sentence_transformers import SentenceTransformer


class Embedder:
    """Thin wrapper around a sentence-transformer model."""

    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        self.model = SentenceTransformer(model_name)

    def encode(self, texts: List[str]) -> List[List[float]]:
        """Return dense embeddings for a list of texts."""
        if not texts:
            return []
        embeddings = self.model.encode(texts, show_progress_bar=False)
        return embeddings.tolist()
