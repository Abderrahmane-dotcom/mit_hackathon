# System Architecture Visualization

## High-Level Overview

```
┌────────────────────────────────────────────────────────────────┐
│                         USER INTERFACE                         │
│                                                                │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐         │
│  │ React Web UI │  │   main.py    │  │ examples.py  │         │
│  │ (Port 5173)  │  │ (Interactive)│  │ (Demos)      │         │
│  │ TypeScript   │  │     CLI      │  │   Jupyter    │         │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘         │
└─────────┼──────────────────┼──────────────────┼────────────────┘
          │                  │                  │
          │ HTTP/REST        │ Direct Import    │
          ▼                  ▼                  ▼
┌────────────────────────────────────────────────────────────────┐
│                     BACKEND API LAYER                          │
│                    (FastAPI - Port 8000)                       │
│                                                                │
│  ┌──────────────────────────────────────────────────────────┐ │
│  │  API Endpoints: /health /research /reinitialize /config  │ │
│  └──────────────────────────────────────────────────────────┘ │
│                             ▼                                  │
│  ┌──────────────────────────────────────────────────────────┐ │
│  │            Research Service (Wrapper)                    │ │
│  └──────────────────────────────────────────────────────────┘ │
└────────────────────────────┬───────────────────────────────────┘
                             ▼
┌────────────────────────────────────────────────────────────────┐
│                      RESEARCH SYSTEM                           │
│                   (research_system.py)                         │
│                                                                │
│  ┌──────────────────────────────────────────────────────────┐ │
│  │              INITIALIZATION PHASE                        │ │
│  │  1. Load PDFs → 2. Build BM25 Index → 3. Create Agents  │ │
│  └──────────────────────────────────────────────────────────┘ │
│                             ▼                                  │
│  ┌──────────────────────────────────────────────────────────┐ │
│  │               RESEARCH WORKFLOW                          │ │
│  │  Topic → Researcher → Reviewers → Synthesizer → Result  │ │
│  └──────────────────────────────────────────────────────────┘ │
└────────────────────────────────────────────────────────────────┘
                             │
                             ▼
        ┌────────────────────┴────────────────────┐
        │                                         │
        ▼                                         ▼
┌───────────────────┐                  ┌──────────────────┐
│   AGENTS LAYER    │                  │  DATA SOURCES    │
│  (src/agents/)    │                  │                  │
│                   │                  │                  │
│ ┌───────────────┐ │◄─────────────────┤ ┌──────────────┐ │
│ │ Researcher    │ │   Uses           │ │ BM25         │ │
│ │               │ │                  │ │ Retriever    │ │
│ └───────────────┘ │                  │ └──────────────┘ │
│        │          │                  │        │         │
│        ▼          │                  │        ▼         │
│ ┌───────────────┐ │                  │ ┌──────────────┐ │
│ │ ReviewerA     │ │◄─────────────────┤ │ Wikipedia    │ │
│ │ ReviewerB     │ │   Enriches       │ │ Scraper      │ │
│ └───────────────┘ │                  │ └──────────────┘ │
│        │          │                  │        │         │
│        ▼          │                  │        ▼         │
│ ┌───────────────┐ │                  │ ┌──────────────┐ │
│ │ Synthesizer   │ │◄─────────────────┤ │ ArXiv        │ │
│ │               │ │   Optional       │ │ Scraper      │ │
│ └───────────────┘ │                  │ └──────────────┘ │
└───────────────────┘                  └──────────────────┘
        │                                         │
        └────────────────────┬────────────────────┘
                             ▼
                    ┌─────────────────┐
                    │  LANGGRAPH      │
                    │  Orchestration  │
                    └─────────────────┘
```

## Component Interaction Flow

```
┌─────────────────────────────────────────────────────────────────┐
│                        1. USER QUERY                            │
│                     "climate change AI"                         │
└─────────────────────────┬───────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────────┐
│              2. RESEARCHER AGENT PROCESSING                     │
│                                                                 │
│  ┌────────────────────┐         ┌─────────────────────┐        │
│  │  BM25 Retrieval    │         │ Wikipedia Scraping  │        │
│  ├────────────────────┤         ├─────────────────────┤        │
│  │ Query: "climate    │         │ Clean query:        │        │
│  │         change AI" │         │ "climate change ai" │        │
│  │                    │         │                     │        │
│  │ 1. Tokenize query  │         │ 1. Search API       │        │
│  │ 2. Score docs      │         │ 2. Get top results  │        │
│  │ 3. Rank by BM25    │         │ 3. Scrape articles  │        │
│  │ 4. Return top-k    │         │ 4. Extract content  │        │
│  └────────┬───────────┘         └─────────┬───────────┘        │
│           │                               │                    │
│           └───────────────┬───────────────┘                    │
│                           ▼                                    │
│               ┌────────────────────────┐                       │
│               │  Combine Sources       │                       │
│               │  - PDF Chunks (4)      │                       │
│               │  - Wiki Articles (3)   │                       │
│               └────────────┬───────────┘                       │
│                            ▼                                   │
│               ┌────────────────────────┐                       │
│               │   LLM Summarization    │                       │
│               │   (GROQ API)           │                       │
│               └────────────┬───────────┘                       │
│                            ▼                                   │
│               ┌────────────────────────┐                       │
│               │  Research Summary      │                       │
│               │  + Sources List        │                       │
│               │  + Snippets            │                       │
│               └────────────────────────┘                       │
└─────────────────────────┬───────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────────┐
│                3. PARALLEL REVIEW PHASE                         │
│                                                                 │
│  ┌─────────────────────┐          ┌─────────────────────┐      │
│  │   REVIEWER A        │          │   REVIEWER B        │      │
│  ├─────────────────────┤          ├─────────────────────┤      │
│  │ Focus:              │          │ Focus:              │      │
│  │ - Logical issues    │          │ - Gaps & biases     │      │
│  │ - Missing support   │          │ - Alternatives      │      │
│  │ - Contradictions    │          │ - Completeness      │      │
│  │                     │          │                     │      │
│  │ Input: Summary      │          │ Input: Summary      │      │
│  │ Output: Critique A  │          │ Output: Critique B  │      │
│  └─────────┬───────────┘          └─────────┬───────────┘      │
│            │                                │                  │
│            └────────────────┬───────────────┘                  │
└─────────────────────────────┼──────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                  4. SYNTHESIS PHASE                             │
│                                                                 │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │              SYNTHESIZER AGENT                           │  │
│  ├──────────────────────────────────────────────────────────┤  │
│  │ Inputs:                                                  │  │
│  │   - Research Summary                                     │  │
│  │   - Critique A                                           │  │
│  │   - Critique B                                           │  │
│  │   - Source List                                          │  │
│  │                                                          │  │
│  │ Processing:                                              │  │
│  │   1. Combine perspectives                                │  │
│  │   2. Resolve conflicts                                   │  │
│  │   3. Generate hypotheses                                 │  │
│  │   4. Map to sources                                      │  │
│  │                                                          │  │
│  │ Output:                                                  │  │
│  │   - Actionable insight (2-3 sentences)                   │  │
│  │   - Testable hypotheses (2)                              │  │
│  │   - Source attribution                                   │  │
│  └──────────────────────────────────────────────────────────┘  │
└─────────────────────────────┬───────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                    5. FINAL OUTPUT                              │
│                                                                 │
│  ResearchState {                                                │
│    topic: "climate change AI"                                   │
│    summary: "AI technologies are being deployed..."             │
│    critique_A: "- Missing discussion of data quality..."        │
│    critique_B: "- Could explore energy consumption..."          │
│    insight: "AI shows promise for climate modeling..."          │
│    sources: ["paper1.pdf", "Climate change", "AI"]              │
│  }                                                              │
└─────────────────────────────────────────────────────────────────┘
```

## Data Flow Diagram

```
PDF Files                Wikipedia               ArXiv Papers
   │                        │                         │
   ▼                        ▼                         ▼
┌──────────┐          ┌──────────┐             ┌──────────┐
│Document  │          │Wikipedia │             │ArXiv     │
│Loader    │          │Scraper   │             │Scraper   │
└────┬─────┘          └────┬─────┘             └────┬─────┘
     │                     │                        │
     │ DocChunks          │ Articles                │ Papers
     ▼                     ▼                        ▼
┌──────────┐          ┌──────────┐             ┌──────────┐
│BM25      │          │Text      │             │PDF       │
│Index     │          │Processing│             │Extraction│
└────┬─────┘          └────┬─────┘             └────┬─────┘
     │                     │                        │
     └─────────────────────┼────────────────────────┘
                           │
                           ▼
                    ┌────────────┐
                    │Researcher  │
                    │Agent       │
                    └─────┬──────┘
                          │
                          ▼
                    ┌────────────┐
                    │ Summary +  │
                    │ Sources    │
                    └─────┬──────┘
                          │
            ┌─────────────┴─────────────┐
            ▼                           ▼
      ┌──────────┐               ┌──────────┐
      │Reviewer A│               │Reviewer B│
      └─────┬────┘               └─────┬────┘
            │                          │
            └────────────┬─────────────┘
                         ▼
                   ┌────────────┐
                   │Synthesizer │
                   └─────┬──────┘
                         │
                         ▼
                   ┌────────────┐
                   │ Final      │
                   │ Insight    │
                   └────────────┘
```

## Class Hierarchy

```
┌─────────────────────────────────────────────────────────┐
│                    AGENTS                               │
│                                                         │
│  ┌──────────────────────────────────────────────────┐  │
│  │  BaseAgent (ABC)                                 │  │
│  │  ├── llm: ChatGroq                               │  │
│  │  ├── process(state) -> Dict [abstract]           │  │
│  │  └── invoke_llm(prompt) -> str                   │  │
│  └────────────────┬─────────────────────────────────┘  │
│                   │                                     │
│      ┌────────────┼────────────┬──────────────┐        │
│      ▼            ▼            ▼              ▼        │
│  ┌────────┐  ┌────────┐  ┌─────────┐  ┌──────────┐   │
│  │Research│  │Reviewer│  │Reviewer │  │Synthesi- │   │
│  │er      │  │AgentA  │  │AgentB   │  │zer       │   │
│  └────────┘  └────────┘  └─────────┘  └──────────┘   │
│                                                        │
└────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────┐
│                   RETRIEVERS                            │
│                                                         │
│  ┌──────────────────────────────────────────────────┐  │
│  │  DocumentLoader                                  │  │
│  │  ├── chunk_size: int                             │  │
│  │  ├── chunk_overlap: int                          │  │
│  │  └── load_and_chunk_pdfs() -> List[DocChunk]    │  │
│  └──────────────────────────────────────────────────┘  │
│                                                         │
│  ┌──────────────────────────────────────────────────┐  │
│  │  BM25Retriever                                   │  │
│  │  ├── chunks: List[DocChunk]                      │  │
│  │  ├── bm25: BM25Okapi                             │  │
│  │  └── get_relevant_documents() -> List[DocChunk] │  │
│  └──────────────────────────────────────────────────┘  │
│                                                         │
└─────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────┐
│                    SCRAPERS                             │
│                                                         │
│  ┌──────────────────────────────────────────────────┐  │
│  │  WikipediaScraper                                │  │
│  │  ├── headers: Dict                               │  │
│  │  ├── search() -> List[Tuple]                     │  │
│  │  ├── scrape_article() -> Tuple                   │  │
│  │  └── scrape_by_keywords() -> List[Dict]         │  │
│  └──────────────────────────────────────────────────┘  │
│                                                         │
│  ┌──────────────────────────────────────────────────┐  │
│  │  ArxivScraper                                    │  │
│  │  ├── api_url: str                                │  │
│  │  ├── scrape_articles() -> List[Dict]            │  │
│  │  └── extract_pdf_content() -> str [static]      │  │
│  └──────────────────────────────────────────────────┘  │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

## State Management

```
ResearchState (TypedDict)
│
├── topic: str                  # User query
│
├── summary: Optional[str]      # Researcher output
│
├── critique_A: Optional[str]   # Reviewer A output
│
├── critique_B: Optional[str]   # Reviewer B output
│
├── insight: Optional[str]      # Synthesizer output
│
├── sources: Optional[List]     # Document sources
│
└── snippets: Optional[List]    # Content excerpts


Flow through LangGraph:
┌──────────┐
│  Input   │  topic: "AI"
└────┬─────┘
     │
     ▼
┌──────────┐
│Researcher│  + summary, sources, snippets
└────┬─────┘
     │
     ├─────────────┬─────────────┐
     ▼             ▼             │
┌──────────┐ ┌──────────┐       │
│ReviewerA │ │ReviewerB │       │
└────┬─────┘ └────┬─────┘       │
     │            │              │
     │+ critique_A│+ critique_B  │
     │            │              │
     └─────┬──────┘              │
           ▼                     │
     ┌──────────┐                │
     │Synthesi- │◄───────────────┘
     │zer       │
     └────┬─────┘
          │+ insight
          ▼
     ┌──────────┐
     │  Output  │  Complete ResearchState
     └──────────┘
```

## Technology Integration

```
┌─────────────────────────────────────────────────────────┐
│                  EXTERNAL SERVICES                      │
│                                                         │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐             │
│  │  GROQ    │  │Wikipedia │  │  ArXiv   │             │
│  │  LLM API │  │   API    │  │   API    │             │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘             │
│       │             │             │                     │
└───────┼─────────────┼─────────────┼─────────────────────┘
        │             │             │
        ▼             ▼             ▼
┌─────────────────────────────────────────────────────────┐
│                    LIBRARIES                            │
│                                                         │
│  Backend:                         Frontend:            │
│  ┌──────────┐  ┌──────────┐      ┌──────────┐         │
│  │LangChain │  │Beautiful │      │  React   │         │
│  │LangGraph │  │  Soup    │      │ Router   │         │
│  │ FastAPI  │  │  Rank    │      │ Axios    │         │
│  │ Pydantic │  │  BM25    │      │Tailwind  │         │
│  └────┬─────┘  └────┬─────┘      └────┬─────┘         │
└───────┼─────────────┼──────────────────┼───────────────┘
        │             │                  │
        └─────────────┼──────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────┐
│                    OUR CODE                             │
│                                                         │
│  Backend (Python):                                      │
│  ├── backend/                                           │
│  │   ├── app.py           (FastAPI routes)             │
│  │   ├── research_service.py  (Service wrapper)        │
│  │   └── config.py        (Configuration)              │
│  ├── src/                                               │
│  │   ├── agents/          (LangChain + ChatGroq)       │
│  │   ├── retrievers/      (BM25Okapi + LangChain)      │
│  │   ├── scrapers/        (BeautifulSoup + Requests)   │
│  │   ├── utils/           (Pure Python)                │
│  │   └── research_system.py  (LangGraph + All Above)   │
│  │                                                      │
│  Frontend (TypeScript):                                 │
│  └── frontend/                                          │
│      ├── src/pages/       (React components)           │
│      ├── src/components/  (Reusable UI)                │
│      ├── src/lib/         (API client + utils)         │
│      └── src/hooks/       (Custom React hooks)         │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

## Full Stack Communication Flow

```
┌─────────────────────────────────────────────────────────┐
│                  FRONTEND (React)                       │
│                                                         │
│  User Action (e.g., Submit Research Topic)             │
│         │                                               │
│         ▼                                               │
│  [Upload.tsx] → [api.ts client]                        │
│         │                                               │
│         │ POST /research                                │
│         │ { topic: "AI", sources: [...] }              │
└─────────┼───────────────────────────────────────────────┘
          │
          │ HTTP/REST (Port 8000)
          ▼
┌─────────────────────────────────────────────────────────┐
│                  BACKEND (FastAPI)                      │
│                                                         │
│  [app.py] → Validate Request                           │
│         │                                               │
│         ▼                                               │
│  [research_service.py] → Call research()               │
│         │                                               │
│         ▼                                               │
│  [research_system.py] → Execute Workflow               │
│         │                                               │
│         ├─► Researcher Agent                           │
│         ├─► Reviewer Agents                            │
│         └─► Synthesizer Agent                          │
│         │                                               │
│         ▼                                               │
│  Return ResearchState                                  │
│         │                                               │
│         │ { topic, summary, critiques, insight, ... }  │
└─────────┼───────────────────────────────────────────────┘
          │
          │ JSON Response
          ▼
┌─────────────────────────────────────────────────────────┐
│                  FRONTEND (React)                       │
│                                                         │
│  [api.ts] → Parse response                             │
│         │                                               │
│         ▼                                               │
│  [Dashboard.tsx] → Display agent activity              │
│  [Report.tsx] → Show results & citations               │
│         │                                               │
│         ▼                                               │
│  User sees research results                            │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

This architecture provides a **scalable, maintainable, and extensible full-stack research system** with modern web technologies and AI-powered multi-agent capabilities!
