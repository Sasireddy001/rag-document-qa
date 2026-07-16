"""Tests for document ingestion utilities."""
from pathlib import Path

from rag_app.ingest import chunk_text, clean_text, ingest_directory, load_file


def test_clean_text():
    assert clean_text("hello\n\n   world") == "hello world"
    assert clean_text("  leading and trailing  ") == "leading and trailing"


def test_chunk_text():
    text = "word " * 100
    chunks = chunk_text(text, chunk_size=50, chunk_overlap=10)
    assert len(chunks) > 0
    for chunk in chunks:
        assert len(chunk) <= 250  # "word " * 50 ~= 245 chars


def test_load_file(tmp_path: Path):
    text_file = tmp_path / "sample.txt"
    text_file.write_text("hello world", encoding="utf-8")
    assert load_file(text_file) == "hello world"


def test_ingest_directory(tmp_path: Path):
    (tmp_path / "doc1.txt").write_text("This is the first document. " * 5, encoding="utf-8")
    (tmp_path / "doc2.md").write_text("This is the second document. " * 5, encoding="utf-8")

    docs = ingest_directory(tmp_path, chunk_size=30, chunk_overlap=5)
    assert len(docs) > 0
    assert all("source" in doc for doc in docs)
    assert all("id" in doc for doc in docs)
    assert all("chunk_index" in doc for doc in docs)
