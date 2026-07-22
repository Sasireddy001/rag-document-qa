# Contributing to RAG Document QA Chatbot

Thanks for your interest in improving this project.

## How to Contribute

1. Fork the repository.
2. Create a feature branch: `git checkout -b feature/your-feature-name`.
3. Make your changes and add or update tests.
4. Run `pytest` and `flake8` locally.
5. Open a pull request with a clear description and any relevant design or API changes.

## Reporting Issues

Use [GitHub Issues](https://github.com/Sasireddy001/rag-document-qa/issues) to report bugs, request features, or ask questions.

## Code Style

- Follow PEP 8 and keep functions small and testable.
- Keep LLM and vector store providers behind the abstraction layer in `llm.py` and `vector_store.py`.
- Update `ARCHITECTURE.md` and `SYSTEM_DESIGN.md` if the architecture changes.
