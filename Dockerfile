FROM python:3.10-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy pyproject.toml first for dependency caching
COPY pyproject.toml .

# Install dependencies
RUN pip install --no-cache-dir -e .

# Copy source code
COPY src/ src/

# Create data directory for ChromaDB persistence
RUN mkdir -p /app/data

# Expose FastAPI port
EXPOSE 8000

# Run FastAPI with uvicorn
CMD ["uvicorn", "rag_app.api:app", "--host", "0.0.0.0", "--port", "8000"]
