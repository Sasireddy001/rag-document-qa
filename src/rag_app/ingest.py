"""Document loading, cleaning, and chunking."""
import re
from pathlib import Path
from typing import List

try:
    from pypdf import PdfReader
except Exception:  # pragma: no cover
    PdfReader = None


def clean_text(text: str) -> str:
    """Collapse whitespace and strip text."""
    return re.sub(r"\s+", " ", text).strip()


def chunk_text(text: str, chunk_size: int = 500, chunk_overlap: int = 100) -> List[str]:
    """Split text into overlapping chunks by character count."""
    chunks = []
    start = 0
    step = max(1, chunk_size - chunk_overlap)
    while start < len(text):
        chunk = text[start : start + chunk_size].strip()
        if chunk:
            chunks.append(chunk)
        start += step
    return chunks


def load_file(path: Path) -> str:
    """Load text from supported file types."""
    suffix = path.suffix.lower()
    text_extensions = {".txt", ".md", ".py", ".json", ".yaml", ".yml", ".csv"}

    if suffix in text_extensions:
        return path.read_text(encoding="utf-8", errors="ignore")

    if suffix == ".pdf" and PdfReader is not None:
        reader = PdfReader(str(path))
        return "\n".join(page.extract_text() or "" for page in reader.pages)

    return ""


def ingest_directory(
    dir_path: Path, chunk_size: int = 500, chunk_overlap: int = 100
) -> List[dict]:
    """Recursively load and chunk all supported files under a directory."""
    documents = []
    for file_path in Path(dir_path).rglob("*"):
        if not file_path.is_file():
            continue

        raw = load_file(file_path)
        if not raw:
            continue

        text = clean_text(raw)
        for i, chunk in enumerate(chunk_text(text, chunk_size, chunk_overlap)):
            documents.append(
                {
                    "id": f"{file_path.name}::chunk-{i}",
                    "text": chunk,
                    "source": str(file_path),
                    "chunk_index": i,
                }
            )
    return documents
