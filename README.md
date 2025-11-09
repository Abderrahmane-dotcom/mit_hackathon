<div align="center">
  <img src="image/logo.jpg" alt="Research Agent Logo" width="300"/>
</div>

# 🤖 Multi-Agent Research Assistant

A sophisticated AI-powered research system that combines BM25 document retrieval, Wikipedia scraping, and multi-agent debate patterns using LangGraph for comprehensive topic analysis.

## 📚 Documentation

- 🔧 **[API Documentation](API.md)** - Complete API reference
- 📁 **[Project Structure](PROJECT_STRUCTURE.md)** - Detailed folder structure overview
- 🏗️ **[Architecture](ARCHIECTURE.md)** - Detailed architecture agents and design pater
- 🤝 **[Summary](SUMMARY.md)** - Summary of the project

## 🌟 Features

- **Multi-Source Research**: Combines PDF document analysis with real-time Wikipedia scraping
- **BM25 Retrieval**: Fast and efficient lexical search over document corpus
- **Multi-Agent Debate**: Three-agent system (Researcher → 2 Reviewers → Synthesizer) for balanced insights
- **ArXiv Integration**: Scrape academic papers with PDF content extraction
- **REST API Backend**: FastAPI-based API for easy integration
- **Modular Architecture**: Clean, class-based design with separated concerns

## 🏗️ Architecture

```
┌─────────────┐
│   User      │
│   Query     │
└──────┬──────┘
       │
       ▼
┌─────────────────────────────────┐
│   Researcher Agent              │
│   - BM25 PDF Retrieval          │
│   - Wikipedia Scraping          │
│   - Summary Generation          │
└──────┬──────────────────────────┘
       │
       ├──────────┬─────────────┐
       ▼          ▼             ▼
┌───────────┐ ┌───────────┐ ┌──────────────┐
│ Reviewer  │ │ Reviewer  │ │              │
│    A      │ │    B      │ │              │
│(Critical) │ │(Balanced) │ │              │
└─────┬─────┘ └─────┬─────┘ │              │
      │             │        │              │
      └──────┬──────┘        │              │
             ▼               ▼              ▼
      ┌─────────────────────────────────────┐
      │     Synthesizer Agent               │
      │     - Collective Insights           │
      │     - Testable Hypotheses           │
      │     - Source Attribution            │
      └─────────────────────────────────────┘
```

## 📁 Project Structure

```
mit_hackathon/
├── main.py                          # Main entry point (CLI)
├── examples.py                      # Usage examples
├── README.md                        # This file
├── requirements.txt                 # Python dependencies
├── .gitignore                       # Git ignore rules
├── .env.example                     # Environment variables template
├── API_KEY_SETUP.md                 # API key setup guide
├── files/                           # PDF documents directory
├── backend/                         # 🆕 FastAPI Backend
│   ├── __init__.py
│   ├── app.py                      # FastAPI application
│   ├── config.py                   # Backend configuration
│   ├── research_service.py         # Research service wrapper
│   ├── run.py                      # Server runner script
│   ├── requirements.txt            # Backend dependencies
│   ├── README.md                   # Backend documentation
│   ├── Dockerfile                  # Docker configuration
│   └── docker-compose.yml          # Docker Compose setup
├── src/
│   ├── __init__.py
│   ├── config.py                    # Configuration settings
│   ├── research_system.py           # Main orchestrator
│   ├── agents/
│   │   ├── __init__.py
│   │   ├── base_agent.py           # Abstract base agent
│   │   ├── researcher_agent.py     # Research & gathering
│   │   ├── reviewer_agent.py       # Critical analysis (A & B)
│   │   ├── synthesizer_agent.py    # Insight synthesis
│   │   └── state.py                # Shared state schema
│   ├── retrievers/
│   │   ├── __init__.py
│   │   ├── bm25_retriever.py       # BM25 search
│   │   └── document_loader.py      # PDF loading & chunking
│   ├── scrapers/
│   │   ├── __init__.py
│   │   ├── wikipedia_scraper.py    # Wikipedia API
│   │   └── arxiv_scraper.py        # ArXiv papers
│   └── utils/
│       ├── __init__.py
│       ├── tokenizer.py            # Text tokenization
│       └── text_utils.py           # Text processing
├── notebook/
│   ├── groq_agent.ipynb            # Agent design patterns
│   └── scraping_test.ipynb         # Scraper examples
├── scrape_arxiv.py                 # Standalone ArXiv scraper
└── scrape_wiki.py                  # Standalone Wikipedia scraper
```

## 🚀 Quick Start

### Prerequisites

- Python 3.10+
- GROQ API key (for LLM access) - **[Get your free API key here](https://console.groq.com/)**

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/Abderrahmane-dotcom/mit_hackathon.git
cd mit_hackathon
```

2. **Create and activate virtual environment**
```bash
# Windows
python -m venv myenv
myenv\Scripts\activate

# Linux/Mac
python3 -m venv myenv
source myenv/bin/activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Set up API key** (Required)

   **📖 See detailed instructions:** [API_KEY_SETUP.md](API_KEY_SETUP.md)

   **Quick Options:**

   **Option 1 - Environment Variable (Recommended):**
   ```bash
   # Windows PowerShell
   $env:GROQ_API_KEY="your-api-key-here"

   # Linux/Mac
   export GROQ_API_KEY="your-api-key-here"
   ```

   **Option 2 - .env file:**
   ```bash
   # Copy the example file
   cp .env.example .env
   
   # Edit .env and add your key
   # GROQ_API_KEY=your-actual-key-here
   ```

   **Option 3 - Edit config.py (Not recommended for Git):**
   - Edit `src/config.py` line 23
   - Replace `"put-your-groq-api-key-here"` with your actual key
   - ⚠️ **Don't commit this change to Git!**

5. **Add PDF documents** (Optional)

Place PDF files in the `files/` directory for document retrieval:
```bash
# The directory is created automatically
cp your_documents/*.pdf files/
```

### Running the System

**Interactive Mode (Main Application):**
```bash
python main.py
```

**Run Examples (Demonstrations):**
```bash
python examples.py
```

**Example Session:**
```
🔍 Enter a research topic (or 'exit' to quit): climate change mitigation

🔬 Running debate pipeline for: climate change mitigation
   Researcher → Reviewers → Synthesizer

🔍 Searching Wikipedia for: 'climate change mitigation'
...

================================================================================
📝 Topic: climate change mitigation

📘 Researcher Summary:
[Summary from PDF documents and Wikipedia...]

🔍 Reviewer A Critique:
- [Critical analysis points...]

🧐 Reviewer B Critique:
- [Alternative perspectives...]

💡 Collective Insight:
[Synthesized insights and hypotheses...]

📚 Sources used: document1.pdf, Climate change, Carbon sequestration
================================================================================
```

## 📚 Usage Examples

### Using the Main System

```python
from src.research_system import ResearchSystem

# Initialize system
system = ResearchSystem()
system.initialize()

# Research a topic
result = system.research("artificial intelligence ethics")

# Display results
system.display_results(result)
```

### Using Individual Components

**BM25 Retriever:**
```python
from src.retrievers import DocumentLoader, BM25Retriever

# Load documents
loader = DocumentLoader()
chunks = loader.load_and_chunk_pdfs("files")

# Create retriever
retriever = BM25Retriever(chunks)

# Search
docs = retriever.get_relevant_documents("machine learning", k=5)
```

**Wikipedia Scraper:**
```python
from src.scrapers import WikipediaScraper

scraper = WikipediaScraper()
articles = scraper.scrape_by_keywords("quantum computing", max_articles=3)

for article in articles:
    print(f"{article['title']}: {article['content'][:200]}...")
```

**ArXiv Scraper:**
```python
from src.scrapers import ArxivScraper

scraper = ArxivScraper()
papers = scraper.scrape_articles(
    query="deep learning",
    max_results=5,
    extract_content=True,  # Extract PDF text
    save_pdf=False         # Don't save files
)

for paper in papers:
    print(f"{paper['title']}")
    print(f"Content length: {len(paper['content'])} chars")
```

**Standalone Scrapers:**
```bash
# Test Wikipedia scraper
python scrape_wiki.py

# Test ArXiv scraper
python scrape_arxiv.py
```

## 🌐 Backend API

The project includes a FastAPI-based REST API for easy integration with web applications and other services.

### Quick Start

```bash
# Install backend dependencies
cd backend
pip install -r requirements.txt

# Set environment variables
export GROQ_API_KEY="your-api-key-here"

# Run the server
python run.py
```

The API will be available at `http://localhost:8000`

### API Endpoints

- `GET /` - API status
- `GET /health` - Health check
- `POST /research` - Perform research
- `POST /reinitialize` - Reinitialize system
- `GET /config` - Get configuration

### Example Request

```bash
curl -X POST http://localhost:8000/research \
  -H "Content-Type: application/json" \
  -d '{
    "topic": "machine learning",
    "use_wikipedia": true,
    "use_arxiv": true,
    "max_wikipedia_articles": 3,
    "max_arxiv_papers": 3
  }'
```

### Docker Deployment

```bash
# Build and run with Docker Compose
cd backend
docker-compose up --build
```

**📖 See full documentation:** [backend/README.md](backend/README.md)

## 🔧 Configuration

Edit `src/config.py` to customize:

```python
class Config:
    # API Configuration
    GROQ_API_KEY = os.getenv("GROQ_API_KEY", "put-your-groq-api-key-here")
    
    # LLM Configuration
    LLM_MODEL = "llama-3.3-70b-versatile"
    LLM_TEMPERATURE = 0
    
    # Document Processing
    CHUNK_SIZE = 1000
    CHUNK_OVERLAP = 200
    
    # Retrieval Configuration
    BM25_TOP_K = 4
    WIKIPEDIA_MAX_ARTICLES = 3
    MAX_SNIPPET_LENGTH = 800
```

## 🧪 Testing

Run the Jupyter notebooks for interactive exploration:

```bash
jupyter notebook notebook/groq_agent.ipynb
jupyter notebook notebook/scraping_test.ipynb
```

## 📦 Dependencies

Core packages:
- `langchain` - LangChain framework
- `langchain-community` - Community integrations
- `langchain-groq` - GROQ LLM provider
- `langgraph` - Multi-agent orchestration
- `rank-bm25` - BM25 ranking algorithm
- `beautifulsoup4` - Web scraping
- `requests` - HTTP requests
- `pypdf` - PDF text extraction
- `python-dotenv` - Environment variable management (optional)

See `requirements.txt` for complete list.

## 🎯 Use Cases

1. **Academic Research**: Combine paper PDFs with Wikipedia for comprehensive topic analysis
2. **Literature Review**: Multi-perspective critique of research summaries
3. **Knowledge Synthesis**: Generate actionable insights from multiple sources
4. **Fact Checking**: Cross-reference information from PDFs and Wikipedia
5. **Hypothesis Generation**: Create testable hypotheses from research findings

## 🤝 Contributing

Contributions are welcome! Areas for improvement:

- [ ] Add vector database support (ChromaDB, Pinecone)
- [ ] Implement semantic search (embeddings)
- [ ] Add more data sources (PubMed, Google Scholar)
- [ ] Web interface (Streamlit/Gradio)
- [ ] Export results to PDF/Markdown
- [ ] Unit tests and CI/CD

## 📝 License

This project is part of the MIT Hackathon. Licensed under the MIT License.

## 🐛 Troubleshooting

### Common Issues

**API Key Not Set:**
```bash
# Error: "GROQ_API_KEY not set!"
# Solution: Set environment variable or edit config.py
# See API_KEY_SETUP.md for detailed instructions
```

**Rate Limit Exceeded:**
```bash
# Error: "Rate limit reached for model llama-3.3-70b-versatile"
# Solution 1: Wait for quota to reset (daily limit)
# Solution 2: Switch to smaller model in src/config.py:
#   LLM_MODEL = "llama-3.1-8b-instant"
# Solution 3: Upgrade Groq account tier
```

**No documents found:**
```bash
# Warning: "No PDFs indexed"
# Solution: Add PDFs to files directory
mkdir files
cp your_pdfs/*.pdf files/
```

**Import errors:**
```bash
# Make sure virtual environment is activated
# Windows: myenv\Scripts\activate
# Linux/Mac: source myenv/bin/activate

# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

**Wikipedia 403 errors:**
- The scraper includes proper User-Agent headers
- If issues persist, increase `time.sleep()` in `src/scrapers/wikipedia_scraper.py`

**Module not found errors:**
```bash
# Make sure you're running from project root
cd mit_hackathon
python main.py
```

## 📞 Support

For issues and questions:
- Open an issue on GitHub
- Check [API_KEY_SETUP.md](API_KEY_SETUP.md) for API configuration
- Review example notebooks in `notebook/`
- Try standalone scrapers: `python scrape_wiki.py` or `python scrape_arxiv.py`

## 🎓 Learn More

- **Jupyter Notebooks**: Explore `notebook/` for interactive examples
  - `groq_agent.ipynb` - Agent design patterns and LangGraph usage
  - `scraping_test.ipynb` - Web scraping demonstrations
- **Standalone Scripts**: Test individual components
  - `scrape_wiki.py` - Wikipedia article scraping
  - `scrape_arxiv.py` - ArXiv paper scraping with PDF extraction
- **Examples**: Run `python examples.py` for demonstrations

## 👥 Authors

MIT Hackathon Team - [@Abderrahmane-dotcom](https://github.com/Abderrahmane-dotcom)

## 🙏 Acknowledgments

- LangChain for the agent framework
- GROQ for LLM API access
- Wikipedia for open knowledge
- ArXiv for academic papers
- MIT Hackathon organizers

---

**Happy Researching! 🚀**
