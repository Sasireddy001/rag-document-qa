"""Tests for configuration."""
import os

from rag_app.config import RAGConfig


def test_default_config():
    config = RAGConfig.from_env()
    assert config.llm_provider in {"ollama", "openai"}
    assert config.chunk_size > 0
    assert config.top_k > 0


def test_env_override():
    os.environ["LLM_PROVIDER"] = "openai"
    os.environ["OPENAI_MODEL"] = "gpt-4"
    os.environ["CHUNK_SIZE"] = "250"
    config = RAGConfig.from_env()
    assert config.llm_provider == "openai"
    assert config.openai_model == "gpt-4"
    assert config.chunk_size == 250

    # cleanup
    del os.environ["LLM_PROVIDER"]
    del os.environ["OPENAI_MODEL"]
    del os.environ["CHUNK_SIZE"]
