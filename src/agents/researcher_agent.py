"""
Researcher agent that gathers information from multiple sources
"""

from typing import Optional, List
from .base_agent import BaseAgent
from ..retrievers import BM25Retriever
from ..scrapers import WikipediaScraper, ArxivScraper
from ..config import Config


class ResearcherAgent(BaseAgent):
    """Agent responsible for gathering and summarizing research"""
    
    def __init__(
        self,
        llm,
        retriever: Optional[BM25Retriever] = None,
        wikipedia_scraper: Optional[WikipediaScraper] = None,
        arxiv_scraper: Optional[ArxivScraper] = None,
        k: int = 4,
        max_wikipedia_articles: int = 3,
        max_arxiv_papers: int = 3
    ):
        """
        Initialize researcher agent.
        
        Args:
            llm: Language model for text generation
            retriever: BM25 retriever for local PDFs
            wikipedia_scraper: Wikipedia scraper instance
            arxiv_scraper: ArXiv scraper instance
            k: Number of documents to retrieve from BM25
            max_wikipedia_articles: Maximum Wikipedia articles to retrieve
            max_arxiv_papers: Maximum ArXiv papers to retrieve
        """
        super().__init__(llm)
        self.retriever = retriever
        self.wikipedia_scraper = wikipedia_scraper
        self.arxiv_scraper = arxiv_scraper
        self.k = k
        self.max_wikipedia_articles = max_wikipedia_articles
        self.max_arxiv_papers = max_arxiv_papers
    
    def process(self, state: dict) -> dict:
        """
        Gather information from all sources and create summary.
        
        Args:
            state: Current research state
            
        Returns:
            Updated state with summary and sources
        """
        topic = state.get("topic", "").strip()
        
        if not topic:
            return {"summary": "No topic provided.", "sources": []}
        
        context_pieces = []
        sources = []
        
        # 1. Retrieve from local PDFs using BM25
        if self.retriever:
            print(f"📄 Searching local PDFs for: '{topic}'")
            docs = self.retriever.get_relevant_documents(topic, k=self.k)
            
            for d in docs:
                snippet = d.page_content.strip()
                if len(snippet) > Config.MAX_SNIPPET_LENGTH:
                    snippet = snippet[:Config.MAX_SNIPPET_LENGTH].rsplit(" ", 1)[0] + " ..."
                
                source = d.metadata.get("source", "unknown")
                chunk_id = d.metadata.get("chunk_id", "")
                context_pieces.append(
                    f"[PDF SOURCE: {source} | CHUNK: {chunk_id}]\n{snippet}"
                )
                sources.append(f"PDF: {source}")
        
        # 2. Scrape Wikipedia
        if self.wikipedia_scraper:
            print(f"🔍 Searching Wikipedia for: '{topic}'")
            wiki_articles = self.wikipedia_scraper.scrape_by_keywords(
                topic,
                max_articles=self.max_wikipedia_articles
            )
            
            wiki_results = wiki_articles.get("results", [])
            is_fallback = wiki_articles.get("is_fallback", False)
            fallback_message = wiki_articles.get("message", "")
            
            # Add fallback warning if present
            if is_fallback and fallback_message:
                context_pieces.append(
                    f"[WIKIPEDIA SEARCH NOTE: {fallback_message}]"
                )
            
            for article in wiki_results:
                title = article.get("title", "Unknown")
                content = article.get("content", "")
                
                snippet = content.strip()
                if len(snippet) > Config.MAX_SNIPPET_LENGTH:
                    snippet = snippet[:Config.MAX_SNIPPET_LENGTH].rsplit(" ", 1)[0] + " ..."
                
                result_type = "WIKIPEDIA (FALLBACK)" if is_fallback else "WIKIPEDIA"
                context_pieces.append(
                    f"[{result_type}: {title}]\n{snippet}"
                )
                source_prefix = "Wikipedia (Fallback)" if is_fallback else "Wikipedia"
                sources.append(f"{source_prefix}: {title}")
        
        # 3. Scrape ArXiv papers
        if self.arxiv_scraper:
            print(f"📚 Searching ArXiv for: '{topic}'")
            try:
                arxiv_papers = self.arxiv_scraper.scrape_articles(
                    query=topic,
                    max_results=self.max_arxiv_papers,
                    save_pdf=False,  # Don't save PDFs
                    extract_content=True  # Extract text content
                )
                
                for paper in arxiv_papers:
                    title = paper.get("title", "Unknown")
                    content = paper.get("content", "")
                    abstract = paper.get("abstract", "")
                    
                    # Use content if available, otherwise use abstract
                    text = content if content and not content.startswith("[") else abstract
                    
                    if text:
                        snippet = text.strip()
                        if len(snippet) > Config.MAX_SNIPPET_LENGTH:
                            snippet = snippet[:Config.MAX_SNIPPET_LENGTH].rsplit(" ", 1)[0] + " ..."
                        
                        context_pieces.append(
                            f"[ARXIV: {title}]\n{snippet}"
                        )
                        sources.append(f"ArXiv: {title}")
            except Exception as e:
                print(f"⚠️  ArXiv scraping failed: {e}")
        
        # Check if we have any sources
        if not context_pieces:
            return {
                "summary": "No relevant information found from any source.",
                "sources": []
            }
        
        # Combine all context
        context = "\n\n---\n\n".join(context_pieces)
        
        # Create prompt
        source_types = []
        if self.retriever:
            source_types.append("local PDFs")
        if self.wikipedia_scraper:
            source_types.append("Wikipedia")
        if self.arxiv_scraper:
            source_types.append("ArXiv papers")
        
        source_desc = ", ".join(source_types)
        
        prompt = (
            f"You are a research assistant. The user asked about: '{topic}'.\n\n"
            f"Read the following excerpts from {source_desc} and produce a concise summary "
            f"of the main findings or facts relevant to the topic. "
            f"Be explicit about which sources support which points.\n\n"
            f"Note any search fallback messages or less relevant results to maintain transparency.\n\n"
            f"EXCERPTS:\n\n{context}\n\n"
            "Return a comprehensive summary that:\n"
            "1. Synthesizes information from all sources\n"
            "2. Highlights key findings from academic papers (ArXiv)\n"
            "3. Incorporates general knowledge (Wikipedia)\n"
            "4. References specific PDF documents when relevant\n"
            "5. Notes any search fallbacks or relevance warnings\n"
            "6. Notes any conflicts or complementary information between sources"
        )
        
        # Get LLM response
        resp = self.llm.invoke(prompt)
        summary_text = getattr(resp, "content", None) or str(resp)
        
        # Remove duplicate sources while preserving order
        unique_sources = list(dict.fromkeys(sources))
        
        print(f"✅ Gathered information from {len(unique_sources)} sources")
        
        return {
            "summary": summary_text,
            "sources": unique_sources
        }
