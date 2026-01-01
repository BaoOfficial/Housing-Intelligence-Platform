# AI Engine Service

AI/RAG service for the Housing Intelligence Platform. Handles LLM calls, embeddings, and vector search.

## Setup

1. Create virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Configure environment:
```bash
cp .env.example .env
# Edit .env with your actual OpenAI API key and other values
```

4. Run ChromaDB (if not already running):
```bash
chroma run --host localhost --port 8000
```

5. Run the AI Engine:
```bash
uvicorn app.main:app --reload --port 8001
```

## API Documentation

Once running, visit:
- Swagger UI: http://localhost:8001/docs
- ReDoc: http://localhost:8001/redoc

## Project Structure

```
ai-engine/
├── app/
│   ├── __init__.py
│   ├── main.py          # FastAPI app
│   ├── config.py        # Settings
│   ├── services/        # LLM, RAG, embeddings
│   ├── core/            # ChromaDB, prompts
│   ├── api/             # API routes
│   └── utils/           # Helpers
├── scripts/             # Seeding scripts
├── tests/               # Tests
└── requirements.txt     # Dependencies
```

## Features

- **Chat**: Conversational AI with context
- **RAG**: Semantic search over tenant reviews
- **Embeddings**: Text embedding service
- **Intent Analysis**: Query classification
