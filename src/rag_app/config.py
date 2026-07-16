"""Environment-driven configuration."""
import os
from dataclasses import dataclass


@dataclass
class RAGConfig:
    """Runtime configuration populated from environment variables."""

    embedding_model: str = "all-MiniLM-L6-v2"
    llm_provider: str = "ollama"  # or "openai"
    ollama_base_url: str = "http://localhost:11434/v1"
    openai_model: str = "gpt-3.5-turbo"
    ollama_model: str = "llama3"
    chroma_collection: str = "documents"
    chroma_persist_dir: str = "./data/chroma"
    chunk_size: int = 500
    chunk_overlap: int = 100
    top_k: int = 5
    openai_api_key: str | None = None

    @classmethod
    def from_env(cls) -> "RAGConfig":
        """Build a configuration instance from environment variables."""
        return cls(
            embedding_model=os.getenv("EMBEDDING_MODEL", cls.embedding_model),
            llm_provider=os.getenv("LLM_PROVIDER", cls.llm_provider).lower(),
            ollama_base_url=os.getenv("OLLAMA_BASE_URL", cls.ollama_base_url),
            openai_model=os.getenv("OPENAI_MODEL", cls.openai_model),
            ollama_model=os.getenv("OLLAMA_MODEL", cls.ollama_model),
            chroma_collection=os.getenv("CHROMA_COLLECTION", cls.chroma_collection),
            chroma_persist_dir=os.getenv("CHROMA_PERSIST_DIR", cls.chroma_persist_dir),
            chunk_size=int(os.getenv("CHUNK_SIZE", cls.chunk_size)),
            chunk_overlap=int(os.getenv("CHUNK_OVERLAP", cls.chunk_overlap)),
            top_k=int(os.getenv("TOP_K", cls.top_k)),
            openai_api_key=os.getenv("OPENAI_API_KEY"),
        )
