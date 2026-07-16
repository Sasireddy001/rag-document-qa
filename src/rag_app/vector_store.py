"""ChromaDB vector store wrapper."""
from typing import Any, Dict, List

import chromadb
from chromadb.config import Settings


class ChromaStore:
    """Wrapper around a persistent ChromaDB collection."""

    def __init__(self, persist_dir: str, collection_name: str):
        self.client = chromadb.PersistentClient(
            path=persist_dir,
            settings=Settings(anonymized_telemetry=False),
        )
        self.collection = self.client.get_or_create_collection(name=collection_name)

    def add(
        self,
        ids: List[str],
        documents: List[str],
        metadatas: List[Dict[str, Any]],
        embeddings: List[List[float]],
    ) -> None:
        """Add documents and their embeddings to the store."""
        if not ids:
            return
        self.collection.add(
            ids=ids,
            documents=documents,
            metadatas=metadatas,
            embeddings=embeddings,
        )

    def query(self, query_embedding: List[float], top_k: int = 5) -> Dict[str, Any]:
        """Retrieve the top-k most similar documents."""
        return self.collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k,
        )
