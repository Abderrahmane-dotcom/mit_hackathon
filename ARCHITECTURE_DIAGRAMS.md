# Architecture Diagrams (Mermaid)

## High-Level System Overview

```mermaid
graph TB
    subgraph UI["User Interface"]
        CLI[main.py<br/>Interactive CLI]
        EX[examples.py<br/>Demos]
        NB[Jupyter Notebooks]
    end

    subgraph RS["Research System"]
        INIT[Initialization<br/>Load PDFs → Build Index]
        WORK[Research Workflow<br/>Topic → Result]
    end

    subgraph AGENTS["Agents Layer"]
        R[Researcher<br/>Agent]
        RA[Reviewer A<br/>Critical]
        RB[Reviewer B<br/>Balanced]
        S[Synthesizer<br/>Agent]
    end

    subgraph DATA["Data Sources"]
        BM25[BM25<br/>Retriever]
        WIKI[Wikipedia<br/>Scraper]
        ARXIV[ArXiv<br/>Scraper]
    end

    CLI --> RS
    EX --> RS
    NB --> RS
    
    RS --> INIT
    INIT --> WORK
    
    WORK --> R
    R --> RA
    R --> RB
    RA --> S
    RB --> S
    
    R --> BM25
    R --> WIKI
    R --> ARXIV

    style UI fill:#e1f5ff
    style RS fill:#fff3e0
    style AGENTS fill:#f3e5f5
    style DATA fill:#e8f5e9
```

## Component Interaction Flow

```mermaid
sequenceDiagram
    participant User
    participant Researcher
    participant BM25
    participant Wikipedia
    participant ArXiv
    participant ReviewerA
    participant ReviewerB
    participant Synthesizer

    User->>Researcher: Query: "climate change AI"
    
    par Parallel Retrieval
        Researcher->>BM25: Search local PDFs
        BM25-->>Researcher: Top 4 chunks
    and
        Researcher->>Wikipedia: Scrape articles
        Wikipedia-->>Researcher: 3 articles
    and
        Researcher->>ArXiv: Search papers
        ArXiv-->>Researcher: 3 papers
    end
    
    Researcher->>Researcher: Combine & Summarize
    
    par Parallel Review
        Researcher->>ReviewerA: Summary
        ReviewerA-->>Synthesizer: Critique A
    and
        Researcher->>ReviewerB: Summary
        ReviewerB-->>Synthesizer: Critique B
    end
    
    Synthesizer->>Synthesizer: Generate Insight
    Synthesizer-->>User: Final Result
```

## Class Hierarchy

```mermaid
classDiagram
    class BaseAgent {
        <<abstract>>
        +llm: ChatGroq
        +process(state)* Dict
        +invoke_llm(prompt) str
    }

    class ResearcherAgent {
        +retriever: BM25Retriever
        +wikipedia_scraper: WikipediaScraper
        +arxiv_scraper: ArxivScraper
        +k: int
        +process(state) Dict
    }

    class ReviewerAgentA {
        +process(state) Dict
    }

    class ReviewerAgentB {
        +process(state) Dict
    }

    class SynthesizerAgent {
        +process(state) Dict
    }

    BaseAgent <|-- ResearcherAgent
    BaseAgent <|-- ReviewerAgentA
    BaseAgent <|-- ReviewerAgentB
    BaseAgent <|-- SynthesizerAgent

    class BM25Retriever {
        +chunks: List~DocChunk~
        +bm25: BM25Okapi
        +get_relevant_documents(query, k) List
    }

    class WikipediaScraper {
        +headers: Dict
        +search(query) List
        +scrape_article(url) Tuple
        +scrape_by_keywords(keywords, max) List
    }

    class ArxivScraper {
        +api_url: str
        +scrape_articles(query, max) List
        +extract_pdf_content(pdf_data)$ str
    }

    ResearcherAgent --> BM25Retriever
    ResearcherAgent --> WikipediaScraper
    ResearcherAgent --> ArxivScraper
```

## State Flow

```mermaid
stateDiagram-v2
    [*] --> Input: topic="AI for climate"
    
    Input --> Researcher: Process Query
    note right of Researcher
        Adds:
        + summary
        + sources
        + snippets
    end note
    
    Researcher --> ReviewerA: Send Summary
    Researcher --> ReviewerB: Send Summary
    
    note right of ReviewerA
        Adds:
        + critique_A
    end note
    
    note right of ReviewerB
        Adds:
        + critique_B
    end note
    
    ReviewerA --> Synthesizer: Critique A
    ReviewerB --> Synthesizer: Critique B
    
    note right of Synthesizer
        Adds:
        + insight
    end note
    
    Synthesizer --> Output: Final Result
    
    note right of Output
        Complete ResearchState
        with all fields
    end note
    
    Output --> [*]
```

## Data Flow

```mermaid
flowchart LR
    subgraph Input["Data Sources"]
        PDF[PDF Files]
        WIKI[Wikipedia]
        ARXIV[ArXiv Papers]
    end

    subgraph Processing["Processing Layer"]
        LOADER[Document Loader]
        WSCRAPER[Wikipedia Scraper]
        ASCRAPER[ArXiv Scraper]
        BM25[BM25 Index]
        TPROC[Text Processing]
        PDFEXT[PDF Extraction]
    end

    subgraph Agents["Agent Layer"]
        RESEARCHER[Researcher Agent]
        REVIEW_A[Reviewer A]
        REVIEW_B[Reviewer B]
        SYNTH[Synthesizer]
    end

    subgraph Output["Output"]
        SUMMARY[Summary + Sources]
        FINAL[Final Insight]
    end

    PDF --> LOADER
    WIKI --> WSCRAPER
    ARXIV --> ASCRAPER
    
    LOADER --> BM25
    WSCRAPER --> TPROC
    ASCRAPER --> PDFEXT
    
    BM25 --> RESEARCHER
    TPROC --> RESEARCHER
    PDFEXT --> RESEARCHER
    
    RESEARCHER --> SUMMARY
    SUMMARY --> REVIEW_A
    SUMMARY --> REVIEW_B
    
    REVIEW_A --> SYNTH
    REVIEW_B --> SYNTH
    
    SYNTH --> FINAL

    style Input fill:#e8f5e9
    style Processing fill:#fff3e0
    style Agents fill:#f3e5f5
    style Output fill:#e1f5ff
```

## Backend Architecture

```mermaid
graph TB
    subgraph Client["Client Applications"]
        WEB[Web Browser]
        CURL[cURL/Postman]
        PY[Python Client]
    end

    subgraph API["FastAPI Backend"]
        ROUTES[API Routes<br/>/health /research /config]
        SERVICE[Research Service]
        VALID[Pydantic Validation]
    end

    subgraph Core["Research System Core"]
        RSYS[Research System]
        AGENTS[Multi-Agent System]
        DATA[Data Sources]
    end

    subgraph Storage["Data Storage"]
        PDFS[PDF Files]
        CACHE[Cache/Memory]
    end

    WEB -->|HTTP/REST| ROUTES
    CURL -->|HTTP/REST| ROUTES
    PY -->|HTTP/REST| ROUTES
    
    ROUTES --> VALID
    VALID --> SERVICE
    SERVICE --> RSYS
    RSYS --> AGENTS
    AGENTS --> DATA
    DATA --> PDFS
    DATA --> CACHE

    style Client fill:#e3f2fd
    style API fill:#fff3e0
    style Core fill:#f3e5f5
    style Storage fill:#e8f5e9
```

## Docker Deployment

```mermaid
graph LR
    subgraph Docker["Docker Environment"]
        subgraph Container["FastAPI Container"]
            APP[FastAPI App<br/>Port 8000]
            RSYS[Research System]
            VOL[Volume Mount<br/>/app/files]
        end
    end

    subgraph Host["Host Machine"]
        FILES[PDF Files<br/>./files/]
        BROWSER[Browser<br/>localhost:8000]
    end

    FILES -.->|Volume Mount| VOL
    BROWSER -->|HTTP| APP
    APP --> RSYS
    RSYS --> VOL

    style Container fill:#e1f5ff
    style Host fill:#f3e5f5
```