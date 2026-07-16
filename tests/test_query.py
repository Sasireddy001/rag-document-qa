"""Tests for the RAG pipeline."""
from unittest.mock import MagicMock, patch

from rag_app.config import RAGConfig
from rag_app.query import RAGPipeline


def test_ingest_and_query_pipeline():
    config = RAGConfig(
        chroma_persist_dir="/tmp/test_chroma_pipeline",
        chroma_collection="test_pipeline",
        llm_provider="ollama",
        ollama_model="dummy-model",
    )

    with patch("rag_app.query.Embedder") as mock_embedder_cls, \
         patch("rag_app.query.ChromaStore") as mock_store_cls, \
         patch("rag_app.query.answer") as mock_answer:

        mock_embedder = MagicMock()
        mock_embedder.encode.return_value = [[0.1] * 384]
        mock_embedder_cls.return_value = mock_embedder

        mock_store = MagicMock()
        mock_store.query.return_value = {
            "documents": [["relevant context"]],
            "metadatas": [[{"source": "doc.md"}]],
        }
        mock_store_cls.return_value = mock_store

        mock_answer.return_value = "This is the answer."

        pipeline = RAGPipeline(config)

        # Test ingestion
        count = pipeline.ingest([
            {"id": "doc-0", "text": "some text", "source": "doc.md", "chunk_index": 0},
        ])
        assert count == 1
        mock_store.add.assert_called_once()

        # Test query
        result = pipeline.query("What is the answer?")
        assert result["answer"] == "This is the answer."
        assert result["question"] == "What is the answer?"
        assert "doc.md" in result["sources"]
