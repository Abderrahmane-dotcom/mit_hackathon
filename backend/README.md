# 🚀 Backend API for Multi-Agent Research Assistant

A FastAPI-based backend service that provides REST API endpoints for the Multi-Agent Research Assistant.

## 📋 Table of Contents

- [Features](#features)
- [Quick Start](#quick-start)
- [API Endpoints](#api-endpoints)
- [Configuration](#configuration)
- [Deployment](#deployment)

## ✨ Features

- **REST API** for research queries
- **Multi-source research** (PDFs, Wikipedia, ArXiv)
- **Configurable scrapers** per request
- **CORS support** for web frontend integration
- **Health checks** and status endpoints
- **Auto-reload** in development mode

## 🚀 Quick Start

### 1. Install Dependencies

```bash
# From the backend directory
cd backend
pip install -r requirements.txt
```

### 2. Set Environment Variables

Create a `.env` file in the project root:

```env
GROQ_API_KEY=your-groq-api-key-here

# Optional configuration
LLM_MODEL=llama-3.1-8b-instant
LLM_TEMPERATURE=0
HOST=0.0.0.0
PORT=8000
DEBUG=True
```

### 3. Run the Server

```bash
# Development mode (auto-reload)
python -m backend.app

# Or using uvicorn directly
uvicorn backend.app:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`

## 📡 API Endpoints

### GET `/`
Root endpoint - Returns API status

**Response:**
```json
{
  "status": "running",
  "message": "Multi-Agent Research Assistant API",
  "system_initialized": true
}
```

### GET `/health`
Health check endpoint

**Response:**
```json
{
  "status": "healthy",
  "message": "Service is running",
  "system_initialized": true,
  "pdf_count": 5
}
```

### POST `/research`
Perform research on a topic

**Request Body:**
```json
{
  "topic": "machine learning for climate change",
  "use_wikipedia": true,
  "use_arxiv": true,
  "max_wikipedia_articles": 3,
  "max_arxiv_papers": 3
}
```

**Response:**
```json
{
  "topic": "machine learning for climate change",
  "summary": "Researcher's summary...",
  "critique_a": "Reviewer A's critique...",
  "critique_b": "Reviewer B's critique...",
  "insight": "Synthesizer's collective insight...",
  "sources": [
    "PDF: document1.pdf",
    "Wikipedia: Machine Learning",
    "ArXiv: Paper Title"
  ],
  "status": "success"
}
```

### POST `/reinitialize`
Reinitialize the research system (useful after uploading new PDFs)

**Response:**
```json
{
  "status": "success",
  "message": "Research service reinitialized successfully",
  "system_initialized": true,
  "pdf_count": 6
}
```

### GET `/config`
Get current configuration (excluding sensitive data)

**Response:**
```json
{
  "llm_model": "llama-3.1-8b-instant",
  "llm_temperature": 0,
  "chunk_size": 1000,
  "chunk_overlap": 200,
  "bm25_top_k": 4,
  "wikipedia_max_articles": 3,
  "arxiv_max_papers": 3,
  "max_snippet_length": 800,
  "files_dir": "/path/to/files",
  "api_key_set": true
}
```

## ⚙️ Configuration

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `GROQ_API_KEY` | - | **Required** GROQ API key |
| `LLM_MODEL` | `llama-3.1-8b-instant` | LLM model to use |
| `LLM_TEMPERATURE` | `0` | Temperature for LLM |
| `CHUNK_SIZE` | `1000` | Document chunk size |
| `CHUNK_OVERLAP` | `200` | Chunk overlap size |
| `BM25_TOP_K` | `4` | Top K results from BM25 |
| `WIKIPEDIA_MAX_ARTICLES` | `3` | Default max Wikipedia articles |
| `ARXIV_MAX_PAPERS` | `3` | Default max ArXiv papers |
| `MAX_SNIPPET_LENGTH` | `800` | Max snippet length |
| `HOST` | `0.0.0.0` | API host |
| `PORT` | `8000` | API port |
| `DEBUG` | `False` | Enable debug mode |

### Configuration in Code

You can also configure the service programmatically:

```python
from backend.config import Config
from backend.research_service import ResearchService

# Set API key
Config.set_groq_api_key("your-api-key")

# Initialize service with custom settings
service = ResearchService()
service.initialize(
    use_wikipedia=True,
    use_arxiv=True,
    max_wikipedia_articles=5,
    max_arxiv_papers=5
)
```

## 🚢 Deployment

### Using Docker (Recommended)

Create a `Dockerfile` in the backend directory:

```dockerfile
FROM python:3.10-slim

WORKDIR /app

# Copy requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Expose port
EXPOSE 8000

# Run application
CMD ["uvicorn", "backend.app:app", "--host", "0.0.0.0", "--port", "8000"]
```

Build and run:
```bash
docker build -t research-api .
docker run -p 8000:8000 -e GROQ_API_KEY=your-key research-api
```

### Using Gunicorn (Production)

```bash
pip install gunicorn
gunicorn backend.app:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

### Using systemd (Linux)

Create `/etc/systemd/system/research-api.service`:

```ini
[Unit]
Description=Research Assistant API
After=network.target

[Service]
Type=notify
User=www-data
WorkingDirectory=/path/to/mit_hackathon
Environment="GROQ_API_KEY=your-key"
ExecStart=/path/to/venv/bin/uvicorn backend.app:app --host 0.0.0.0 --port 8000

[Install]
WantedBy=multi-user.target
```

Enable and start:
```bash
sudo systemctl enable research-api
sudo systemctl start research-api
```

## 📚 API Documentation

Once the server is running, visit:
- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

## 🔒 Security Considerations

For production deployment:

1. **CORS**: Update `allow_origins` in `app.py` to whitelist specific domains
2. **API Key**: Never commit API keys to version control
3. **Rate Limiting**: Consider adding rate limiting middleware
4. **HTTPS**: Use reverse proxy (nginx) with SSL/TLS
5. **Authentication**: Add authentication for production use

## 🧪 Testing

```bash
# Test the API
curl http://localhost:8000/health

# Research request
curl -X POST http://localhost:8000/research \
  -H "Content-Type: application/json" \
  -d '{"topic": "quantum computing", "use_wikipedia": true, "use_arxiv": true}'
```

## 📝 Example Client Code

### Python

```python
import requests

response = requests.post(
    "http://localhost:8000/research",
    json={
        "topic": "renewable energy",
        "use_wikipedia": True,
        "use_arxiv": True,
        "max_wikipedia_articles": 3,
        "max_arxiv_papers": 3
    }
)

result = response.json()
print(f"Summary: {result['summary']}")
print(f"Sources: {result['sources']}")
```

### JavaScript

```javascript
fetch('http://localhost:8000/research', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    topic: 'artificial intelligence',
    use_wikipedia: true,
    use_arxiv: true,
    max_wikipedia_articles: 3,
    max_arxiv_papers: 3
  })
})
  .then(res => res.json())
  .then(data => console.log(data));
```

## 🤝 Contributing

See the main [README.md](../README.md) for contribution guidelines.

## 📄 License

This project is part of the Multi-Agent Research Assistant system.
