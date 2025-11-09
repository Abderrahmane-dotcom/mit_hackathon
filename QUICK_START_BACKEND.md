# 🚀 Quick Reference - Backend API

## Start Server

```bash
# Windows
start_backend.bat

# Linux/Mac
./start_backend.sh

# Manual
.\myenv\Scripts\activate
$env:GROQ_API_KEY="your-key"
python -m backend.run

# Docker
cd backend && docker-compose up
```

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `http://localhost:8000/` | GET | Status |
| `http://localhost:8000/health` | GET | Health check |
| `http://localhost:8000/research` | POST | Research topic |
| `http://localhost:8000/reinitialize` | POST | Reload system |
| `http://localhost:8000/config` | GET | Get config |
| `http://localhost:8000/docs` | GET | Swagger UI |

## Research Request

```bash
curl -X POST http://localhost:8000/research \
  -H "Content-Type: application/json" \
  -d '{
    "topic": "your topic here",
    "use_wikipedia": true,
    "use_arxiv": true,
    "max_wikipedia_articles": 3,
    "max_arxiv_papers": 3
  }'
```

## Python Client

```python
import requests

r = requests.post("http://localhost:8000/research", json={
    "topic": "machine learning",
    "use_wikipedia": True,
    "use_arxiv": True
})
print(r.json()["summary"])
```

## Configuration (.env)

```env
GROQ_API_KEY=your-key
LLM_MODEL=llama-3.1-8b-instant
PORT=8000
DEBUG=True
```

## Test Backend

```bash
python test_backend.py
```

## Documentation

- Backend: `backend/README.md`
- Setup: `BACKEND_SETUP.md`
- Migration: `BACKEND_MIGRATION.md`
- API Docs: http://localhost:8000/docs
