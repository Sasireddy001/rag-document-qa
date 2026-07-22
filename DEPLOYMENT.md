# Deployment Guide — RAG Document QA Chatbot

This document covers local, Docker, and cloud deployment options for the RAG chatbot.

---

## Deployment options

| Environment | Method | Best for |
|---|---|---|
| Local | Python + Ollama | Development, no API cost, privacy-first |
| Docker | Docker Compose | Reproducible demo, team sharing |
| Cloud | AWS/GCP + Pinecone/OpenAI | Production, scalable, managed vector DB |

---

## Local deployment

**Time to first answer:** ~5 minutes  
**Cost:** $0 (uses local Ollama)

```bash
# 1. Clone
git clone https://github.com/Sasireddy001/rag-document-qa.git
cd rag-document-qa

# 2. Install Python dependencies
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# 3. Install and run Ollama
# macOS / Linux
curl -fsSL https://ollama.com/install.sh | sh
ollama pull llama3
ollama serve

# 4. Ingest documents and start API
python scripts/ingest.py --docs-dir data/docs
uvicorn app.main:app --reload

# 5. Open Streamlit UI (optional)
streamlit run app/frontend.py
```

**Test the API**

```bash
curl -X POST http://localhost:8000/query \
  -H "Content-Type: application/json" \
  -d '{"question": "What does this chatbot do?"}'
```

---

## Docker deployment

```bash
cp .env.example .env
# Edit .env: set LLM_PROVIDER=ollama or openai and add keys if needed

docker-compose up -d
```

**Access**

- API: `http://localhost:8000`
- UI: `http://localhost:8501`
- Docs: `http://localhost:8000/docs`

---

## Cloud deployment (AWS example)

**High-level architecture**

```
Route 53 → CloudFront → S3 (static frontend)
                 ↓
            ECS / EKS (FastAPI backend)
                 ↓
         Pinecone / pgvector (vector DB)
                 ↓
         OpenAI / Bedrock / self-hosted LLM
```

**Simplified deployment path**

1. Containerize the FastAPI app with `Dockerfile`.
2. Push image to Amazon ECR.
3. Deploy to AWS ECS Fargate or EKS.
4. Use Amazon Aurora PostgreSQL with `pgvector` extension or Pinecone for the vector store.
5. Use Amazon S3 for document storage.
6. Use AWS Secrets Manager for `OPENAI_API_KEY`.

---

## Production considerations

- Replace ChromaDB with a managed vector store (Pinecone, Weaviate, pgvector) for scale.
- Add authentication to the FastAPI endpoints.
- Implement rate limiting and request logging.
- Add an S3 event trigger or upload API for new documents.
- Monitor LLM latency and token cost.

---

## Verification checklist

- [ ] Documents are ingested and chunked.
- [ ] `/query` returns a relevant answer with source citations.
- [ ] Vector search returns the expected top-K chunks.
- [ ] CI/CD pipeline passes `pytest` and `flake8`.
- [ ] Docker container runs end-to-end.

---

## Destroying resources

```bash
# Docker
docker-compose down -v

# AWS
# Delete ECS service, ECR image, and Aurora/Pinecone resources manually or via Terraform.
```
