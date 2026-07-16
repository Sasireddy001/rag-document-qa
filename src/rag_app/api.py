"""FastAPI application for the RAG pipeline."""
import shutil
import tempfile
from pathlib import Path
from typing import List

from fastapi import FastAPI, HTTPException, UploadFile

from rag_app.config import RAGConfig
from rag_app.ingest import ingest_directory
from rag_app.query import RAGPipeline

app = FastAPI(title="RAG Document QA", version="0.1.0")

# Global pipeline instance (loads config from environment)
pipeline = RAGPipeline()


@app.get("/health")
def health() -> dict:
    """Health check endpoint."""
    return {"status": "ok"}


@app.post("/ingest")
def ingest_folder(path: str) -> dict:
    """Ingest all supported files from a local folder."""
    folder = Path(path).expanduser().resolve()
    if not folder.exists() or not folder.is_dir():
        raise HTTPException(status_code=400, detail=f"Folder not found: {path}")

    config = RAGConfig.from_env()
    documents = ingest_directory(folder, config.chunk_size, config.chunk_overlap)
    count = pipeline.ingest(documents)
    return {"ingested": count}


@app.post("/upload")
async def upload_files(files: List[UploadFile]) -> dict:
    """Upload files, save them temporarily, and ingest them."""
    count = 0
    with tempfile.TemporaryDirectory() as tmpdir:
        tmp_path = Path(tmpdir)
        for file in files:
            if not file.filename:
                continue
            dest = tmp_path / Path(file.filename).name
            with dest.open("wb") as buffer:
                shutil.copyfileobj(file.file, buffer)

        config = RAGConfig.from_env()
        documents = ingest_directory(tmp_path, config.chunk_size, config.chunk_overlap)
        count = pipeline.ingest(documents)

    return {"ingested": count}


@app.post("/query")
def query(payload: dict) -> dict:
    """Answer a question using the ingested documents."""
    question = payload.get("question")
    if not question or not isinstance(question, str):
        raise HTTPException(status_code=400, detail="question field is required")

    return pipeline.query(question)
