# Architecture Diagrams (Mermaid)

## 📑 Table of Contents

- [High-Level System Overview](#high-level-system-overview)
- [Component Interaction Flow](#component-interaction-flow)
- [Class Hierarchy](#class-hierarchy)
- [State Flow](#state-flow)
- [Data Flow](#data-flow)
- [Full Stack Architecture](#full-stack-architecture)
- [Frontend Architecture](#frontend-architecture)
- [Docker Deployment](#docker-deployment)
- [Development Workflow](#development-workflow)
- [Data Flow (Complete System)](#data-flow-complete-system)


## High-Level System Overview

```mermaid
graph TB
    subgraph UI["User Interface"]
        WEB[React Frontend<br/>Vite + TypeScript]
        CLI[main.py<br/>Interactive CLI]
        EX[examples.py<br/>Demos]
        NB[Jupyter Notebooks]
    end

    subgraph API["Backend API"]
        FAST[FastAPI Server<br/>Port 8000]
        SERV[Research Service<br/>Wrapper]
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

    WEB -->|HTTP/REST| FAST
    CLI --> RS
    EX --> RS
    NB --> RS
    
    FAST --> SERV
    SERV --> RS
    
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
    style API fill:#fff9c4
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

## Full Stack Architecture

```mermaid
graph TB
    subgraph Frontend["Frontend (Port 5173)"]
        HOME[Home Page<br/>System Status]
        UPLOAD[Upload Page<br/>Config Research]
        DASH[Dashboard<br/>Agent Visualization]
        REPORT[Report Page<br/>Results & Citations]
        API_CLIENT[API Client<br/>Axios]
    end

    subgraph Backend["Backend API (Port 8000)"]
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

    HOME --> API_CLIENT
    UPLOAD --> API_CLIENT
    DASH --> API_CLIENT
    REPORT --> API_CLIENT
    
    API_CLIENT -->|HTTP/REST| ROUTES
    
    ROUTES --> VALID
    VALID --> SERVICE
    SERVICE --> RSYS
    RSYS --> AGENTS
    AGENTS --> DATA
    DATA --> PDFS
    DATA --> CACHE

    style Frontend fill:#e1f5ff
    style Backend fill:#fff3e0
    style Core fill:#f3e5f5
    style Storage fill:#e8f5e9
```

## Frontend Architecture

```mermaid
graph TB
    subgraph Pages["Pages (React Router)"]
        HOME[Home.tsx<br/>Landing & Status]
        UPLOAD[Upload.tsx<br/>Research Config]
        DASH[Dashboard.tsx<br/>Agent Activity]
        REPORT[Report.tsx<br/>Research Results]
    end

    subgraph Components["Components"]
        NAV[Navigation.tsx<br/>App Header]
        TOAST[Toast/Toaster<br/>Notifications]
    end

    subgraph Lib["Libraries & Utils"]
        API[api.ts<br/>Backend Client]
        UTILS[utils.ts<br/>Helpers]
        HOOKS[use-toast.ts<br/>Custom Hook]
    end

    subgraph Styling["Styling"]
        TAILWIND[Tailwind CSS<br/>Utility Classes]
        CSS[index.css<br/>Global Styles]
    end

    subgraph App["App Entry"]
        MAIN[main.tsx<br/>React Mount]
        APP[App.tsx<br/>Router Setup]
    end

    MAIN --> APP
    APP --> NAV
    APP --> HOME
    APP --> UPLOAD
    APP --> DASH
    APP --> REPORT
    
    HOME --> API
    UPLOAD --> API
    DASH --> API
    REPORT --> API
    
    UPLOAD --> HOOKS
    DASH --> HOOKS
    REPORT --> HOOKS
    
    HOOKS --> TOAST
    
    API --> UTILS
    
    NAV --> TAILWIND
    HOME --> TAILWIND
    UPLOAD --> TAILWIND
    DASH --> TAILWIND
    REPORT --> TAILWIND
    
    APP --> CSS

    style Pages fill:#e1f5ff
    style Components fill:#f3e5f5
    style Lib fill:#fff3e0
    style Styling fill:#e8f5e9
    style App fill:#fff9c4
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
        FRONTEND[Frontend Dev<br/>localhost:5173]
        BROWSER[Browser]
    end

    FILES -.->|Volume Mount| VOL
    BROWSER -->|Visit| FRONTEND
    FRONTEND -->|API Calls| APP
    APP --> RSYS
    RSYS --> VOL

    style Container fill:#e1f5ff
    style Host fill:#f3e5f5
```

## Development Workflow

```mermaid
sequenceDiagram
    participant Dev as Developer
    participant FE as Frontend (Vite)
    participant BE as Backend (FastAPI)
    participant RS as Research System
    participant EXT as External APIs

    Dev->>FE: npm run dev
    Note over FE: Starts on :5173<br/>Hot Module Reload
    
    Dev->>BE: python -m backend.run
    Note over BE: Starts on :8000<br/>Auto-reload enabled
    
    Dev->>FE: Opens http://localhost:5173
    FE->>FE: Loads React App
    
    FE->>BE: GET /health
    BE-->>FE: {"status": "healthy"}
    
    Dev->>FE: Configures research topic
    FE->>BE: POST /research
    BE->>RS: Initialize research
    RS->>EXT: Scrape Wikipedia/ArXiv
    EXT-->>RS: External data
    RS->>RS: Multi-agent processing
    RS-->>BE: Research result
    BE-->>FE: JSON response
    FE->>FE: Render results
    FE-->>Dev: Display report

    style Dev fill:#fff9c4
    style FE fill:#e1f5ff
    style BE fill:#fff3e0
    style RS fill:#f3e5f5
    style EXT fill:#e8f5e9
```

## Data Flow (Complete System)

```mermaid
flowchart TB
    subgraph User["User Interaction"]
        BROWSER[Web Browser]
    end

    subgraph Frontend["Frontend Layer"]
        UI[React Components]
        STATE[State Management]
        HTTP[HTTP Client]
    end

    subgraph Backend["Backend Layer"]
        ENDPOINT[REST Endpoints]
        VALIDATION[Request Validation]
        SERVICE[Research Service]
    end

    subgraph Core["Core System"]
        INIT[System Init]
        WORKFLOW[Research Workflow]
    end

    subgraph Agents["Agent Layer"]
        RESEARCHER[Researcher]
        REVIEWERS[Reviewers A/B]
        SYNTH[Synthesizer]
    end

    subgraph Data["Data Layer"]
        LOCAL[PDF Files]
        WIKI[Wikipedia]
        ARXIV[ArXiv]
    end

    BROWSER -->|User Input| UI
    UI --> STATE
    STATE --> HTTP
    HTTP -->|POST /research| ENDPOINT
    ENDPOINT --> VALIDATION
    VALIDATION --> SERVICE
    SERVICE --> INIT
    INIT --> WORKFLOW
    WORKFLOW --> RESEARCHER
    RESEARCHER --> LOCAL
    RESEARCHER --> WIKI
    RESEARCHER --> ARXIV
    RESEARCHER --> REVIEWERS
    REVIEWERS --> SYNTH
    SYNTH --> SERVICE
    SERVICE -->|JSON Response| ENDPOINT
    ENDPOINT --> HTTP
    HTTP --> STATE
    STATE --> UI
    UI -->|Display Results| BROWSER

    style User fill:#fff9c4
    style Frontend fill:#e1f5ff
    style Backend fill:#fff3e0
    style Core fill:#f3e5f5
    style Agents fill:#f8bbd0
    style Data fill:#e8f5e9
```