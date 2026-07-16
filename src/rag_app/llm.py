"""LLM client that supports OpenAI or Ollama via an OpenAI-compatible endpoint."""
import os

from openai import OpenAI

from rag_app.config import RAGConfig


def get_llm_client(config: RAGConfig) -> OpenAI:
    """Return an OpenAI client configured for OpenAI or Ollama."""
    if config.llm_provider == "openai":
        if not config.openai_api_key:
            raise ValueError("OPENAI_API_KEY is required when LLM_PROVIDER=openai")
        return OpenAI(api_key=config.openai_api_key)

    # Ollama exposes an OpenAI-compatible endpoint at /v1
    api_key = os.getenv("OLLAMA_API_KEY") or "ollama"
    return OpenAI(base_url=config.ollama_base_url, api_key=api_key)


def answer(config: RAGConfig, context: str, question: str) -> str:
    """Generate an answer from the LLM using the retrieved context."""
    client = get_llm_client(config)
    model = config.openai_model if config.llm_provider == "openai" else config.ollama_model

    messages = [
        {
            "role": "system",
            "content": (
                "You are a helpful, factual assistant. Answer the question using only "
                "the provided context. If the context does not contain enough information, "
                "say that you don't know."
            ),
        },
        {
            "role": "user",
            "content": f"Context:\n{context}\n\nQuestion: {question}",
        },
    ]

    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=0.2,
    )
    return response.choices[0].message.content
