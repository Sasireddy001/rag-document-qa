"""RAG pipeline orchestration."""
from typing import Any, Dict, List

from rag_app.config import RAGConfig
from rag_app.embeddings import Embedder
from rag_app.llm import answer
from rag_app.vector_store import ChromaStore


class RAGPipeline:
    """End-to-end RAG pipeline: embed, store, retrieve, generate."""

    def __init__(self, config: RAGConfig | None = None):
        self.config = config or RAGConfig.from_env()
        self.embedder = Embedder(self.config.embedding_model)
        self.store = ChromaStore(
            self.config.chroma_persist_dir,
            self.config.chroma_collection,
        )

    def ingest(self, documents: List[Dict[str, Any]]) -> int:
        """Chunk, embed, and store a list of documents."""
        if not documents:
            return 0

        texts = [doc["text"] for doc in documents]
        ids = [doc["id"] for doc in documents]
        metadatas = [
            {"source": doc["source"], "chunk_index": doc["chunk_index"]}
            for doc in documents
        ]

        embeddings = self.embedder.encode(texts)
        self.store.add(ids, texts, metadatas, embeddings)
        return len(documents)

    def query(self, question: str) -> Dict[str, Any]:
        """Retrieve relevant chunks and generate an answer."""
        query_embedding = self.embedder.encode([question])[0]
        results = self.store.query(query_embedding, top_k=self.config.top_k)

        documents = self._first_results(results, "documents")
        metadatas = self._first_results(results, "metadatas")

        context = "\n\n".join(documents)
        response = answer(self.config, context, question)

        return {
            "question": question,
            "answer": response,
            "sources": [m.get("source") for m in metadatas],
        }

    @staticmethod
    def _first_results(results: Dict[str, Any], key: str) -> List[Any]:
        """Helper to extract the first query's results from ChromaDB output."""
        value = results.get(key)
        if value and isinstance(value, list) and len(value) > 0:
            return value[0] or []
        return []
