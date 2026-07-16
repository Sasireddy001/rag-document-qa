#!/usr/bin/env python
"""CLI script to ingest a folder of documents into the RAG pipeline."""
import argparse
from pathlib import Path

from rag_app.config import RAGConfig
from rag_app.ingest import ingest_directory
from rag_app.query import RAGPipeline


def main() -> None:
    parser = argparse.ArgumentParser(description="Ingest documents into the RAG pipeline")
    parser.add_argument("folder", type=Path, help="Path to the folder containing documents")
    args = parser.parse_args()

    config = RAGConfig.from_env()
    documents = ingest_directory(
        args.folder.expanduser().resolve(),
        config.chunk_size,
        config.chunk_overlap,
    )

    pipeline = RAGPipeline(config)
    count = pipeline.ingest(documents)
    print(f"Ingested {count} chunks from {args.folder}")


if __name__ == "__main__":
    main()
