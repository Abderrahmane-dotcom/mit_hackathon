"""
Research service that wraps the research system for API usage
"""

import sys
import logging
import traceback
from pathlib import Path
from typing import Optional, Dict, Any

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.research_system import ResearchSystem
from backend.config import Config

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class ResearchService:
    """Service layer for research system"""
    
    def __init__(self):
        """Initialize research service"""
        self.system: Optional[ResearchSystem] = None
        self._initialized = False
    
    def initialize(
        self,
        use_wikipedia: bool = True,
        use_arxiv: bool = True,
        max_wikipedia_articles: Optional[int] = None,
        max_arxiv_papers: Optional[int] = None
    ):
        """
        Initialize the research system
        
        Args:
            use_wikipedia: Enable Wikipedia scraper
            use_arxiv: Enable ArXiv scraper
            max_wikipedia_articles: Max Wikipedia articles (uses config default if None)
            max_arxiv_papers: Max ArXiv papers (uses config default if None)
        """
        try:
            # Ensure files directory exists
            Config.ensure_files_dir()
            
            # Initialize research system
            self.system = ResearchSystem(
                api_key=Config.GROQ_API_KEY,
                files_dir=str(Config.FILES_DIR),
                use_wikipedia=use_wikipedia,
                use_arxiv=use_arxiv,
                max_wikipedia_articles=max_wikipedia_articles or Config.WIKIPEDIA_MAX_ARTICLES,
                max_arxiv_papers=max_arxiv_papers or Config.ARXIV_MAX_PAPERS
            )
            
            self.system.initialize()
            self._initialized = True
            
            print("✅ Research service initialized successfully")
            
        except Exception as e:
            print(f"❌ Failed to initialize research service: {e}")
            raise
    
    def is_initialized(self) -> bool:
        """Check if service is initialized"""
        return self._initialized and self.system is not None
    
    def get_pdf_count(self) -> int:
        """Get count of indexed PDFs"""
        if not self.is_initialized():
            return 0
        
        if self.system.retriever:
            return len(set(
                doc.metadata.get("source", "")
                for doc in self.system.retriever.chunks
            ))
        return 0
    
    def research(
        self,
        topic: str,
        use_wikipedia: Optional[bool] = None,
        use_arxiv: Optional[bool] = None,
        max_wikipedia_articles: Optional[int] = None,
        max_arxiv_papers: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Perform research on a topic
        
        Args:
            topic: Research topic
            use_wikipedia: Override Wikipedia usage for this request
            use_arxiv: Override ArXiv usage for this request
            max_wikipedia_articles: Override max Wikipedia articles for this request
            max_arxiv_papers: Override max ArXiv papers for this request
            
        Returns:
            Research results dictionary
        """
        if not self.is_initialized():
            logger.error("Research attempted before initialization")
            raise RuntimeError("Research service not initialized")
        
        try:
            logger.info(f"Starting research on topic: {topic}")
            logger.info(f"Config - Wikipedia: {use_wikipedia}, ArXiv: {use_arxiv}, "
                       f"Max Wiki: {max_wikipedia_articles}, Max ArXiv: {max_arxiv_papers}")
            
            # If scrapers need to be reconfigured, reinitialize
            if (use_wikipedia is not None or use_arxiv is not None or
                max_wikipedia_articles is not None or max_arxiv_papers is not None):
                
                logger.info("Reinitializing with new scraper configuration...")
                self.initialize(
                    use_wikipedia=use_wikipedia if use_wikipedia is not None else True,
                    use_arxiv=use_arxiv if use_arxiv is not None else True,
                    max_wikipedia_articles=max_wikipedia_articles,
                    max_arxiv_papers=max_arxiv_papers
                )
            
            # Check LLM configuration
            if not Config.GROQ_API_KEY:
                logger.error("GROQ API key not configured")
                raise RuntimeError("GROQ_API_KEY not set in environment")
            
            # Check if we have any sources enabled
            if not (self.system.use_wikipedia or self.system.use_arxiv or self.system.retriever):
                logger.warning("No research sources enabled (no PDFs indexed, Wikipedia and ArXiv disabled)")
            
            # Perform research
            logger.info("Starting multi-agent research workflow...")
            result = self.system.research(topic)
            
            # Validate result structure
            required_keys = ['topic', 'summary', 'critique_A', 'critique_B', 'insight']
            missing_keys = [k for k in required_keys if k not in result]
            if missing_keys:
                logger.error(f"Research result missing required keys: {missing_keys}")
                raise ValueError(f"Incomplete research result, missing: {missing_keys}")
            
            logger.info("Research completed successfully")
            return result
            
        except Exception as e:
            logger.error(f"Research failed: {str(e)}")
            logger.error(f"Traceback: {traceback.format_exc()}")
            raise
    
    def get_system_info(self) -> Dict[str, Any]:
        """Get information about the research system"""
        if not self.is_initialized():
            return {
                "initialized": False,
                "message": "System not initialized"
            }
        
        return {
            "initialized": True,
            "pdf_count": self.get_pdf_count(),
            "wikipedia_enabled": self.system.use_wikipedia,
            "arxiv_enabled": self.system.use_arxiv,
            "max_wikipedia_articles": self.system.max_wikipedia_articles,
            "max_arxiv_papers": self.system.max_arxiv_papers,
            "files_dir": str(Config.FILES_DIR)
        }
