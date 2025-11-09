"""
FastAPI application for Multi-Agent Research Assistant
"""

from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Optional, List, Dict
import uvicorn
import sys
import logging
import traceback
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from backend.config import Config
from backend.research_service import ResearchService

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Multi-Agent Research Assistant API",
    description="AI-powered research system with multi-agent debate pattern",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize research service
research_service: Optional[ResearchService] = None


# Request/Response Models
class ResearchRequest(BaseModel):
    """Research request model"""
    topic: str = Field(..., description="Research topic or query", min_length=1)
    use_wikipedia: bool = Field(True, description="Enable Wikipedia scraping")
    use_arxiv: bool = Field(True, description="Enable ArXiv paper scraping")
    max_wikipedia_articles: int = Field(3, description="Max Wikipedia articles", ge=1, le=10)
    max_arxiv_papers: int = Field(3, description="Max ArXiv papers", ge=1, le=10)


class ResearchResponse(BaseModel):
    """Research response model"""
    topic: str
    summary: str
    critique_a: str
    critique_b: str
    insight: str
    sources: List[str]
    status: str = "success"


class StatusResponse(BaseModel):
    """Status response model"""
    status: str
    message: str
    system_initialized: bool
    pdf_count: Optional[int] = None


class ErrorResponse(BaseModel):
    """Error response model"""
    status: str = "error"
    message: str
    detail: Optional[str] = None


@app.on_event("startup")
async def startup_event():
    """Initialize the research service on startup"""
    global research_service
    try:
        print("🚀 Initializing Research Service...")
        Config.validate_config()
        research_service = ResearchService()
        research_service.initialize()
        print("✅ Research Service Ready!")
    except Exception as e:
        print(f"❌ Failed to initialize research service: {e}")
        raise


@app.get("/", response_model=StatusResponse)
async def root():
    """Root endpoint"""
    return {
        "status": "running",
        "message": "Multi-Agent Research Assistant API",
        "system_initialized": research_service is not None and research_service.is_initialized()
    }


@app.get("/health", response_model=StatusResponse)
async def health_check():
    """Health check endpoint"""
    if not research_service:
        raise HTTPException(status_code=503, detail="Research service not initialized")
    
    return {
        "status": "healthy",
        "message": "Service is running",
        "system_initialized": research_service.is_initialized(),
        "pdf_count": research_service.get_pdf_count()
    }


@app.post("/research", response_model=ResearchResponse)
async def research_topic(request: ResearchRequest, background_tasks: BackgroundTasks):
    """
    Research a topic using the multi-agent system
    
    Args:
        request: Research request with topic and configuration
        background_tasks: FastAPI background tasks manager
        
    Returns:
        Research results with summary, critiques, and insights
    """
    if not research_service:
        logger.error("Research endpoint called before service initialization")
        raise HTTPException(status_code=503, detail="Research service not initialized")
    
    try:
        logger.info(f"Research request received - Topic: {request.topic}")
        logger.info(f"Config - Wikipedia: {request.use_wikipedia}, ArXiv: {request.use_arxiv}, "
                   f"Max Wiki: {request.max_wikipedia_articles}, Max ArXiv: {request.max_arxiv_papers}")
        
        # Check environment
        if not Config.GROQ_API_KEY:
            logger.error("GROQ API key not configured")
            raise HTTPException(
                status_code=500,
                detail="GROQ_API_KEY not set in environment. Configure the API key and restart the server."
            )
        
        # Validate state
        if not research_service.is_initialized():
            logger.error("Research service reports not initialized")
            raise HTTPException(status_code=503, detail="Research service lost initialization state")
        
        from asyncio import wait_for, TimeoutError
        import asyncio
        from concurrent.futures import ThreadPoolExecutor
        
        # Run research in thread pool with timeout
        logger.info("Starting research with timeout...")
        loop = asyncio.get_event_loop()
        with ThreadPoolExecutor() as pool:
            try:
                research_task = loop.run_in_executor(
                    pool,
                    lambda: research_service.research(
                        topic=request.topic,
                        use_wikipedia=request.use_wikipedia,
                        use_arxiv=request.use_arxiv,
                        max_wikipedia_articles=request.max_wikipedia_articles,
                        max_arxiv_papers=request.max_arxiv_papers
                    )
                )
                result = await wait_for(research_task, timeout=Config.RESEARCH_TIMEOUT)
                
            except TimeoutError:
                logger.error(f"Research timed out after {Config.RESEARCH_TIMEOUT}s")
                raise HTTPException(
                    status_code=504,  # Gateway Timeout
                    detail=f"Research timed out after {Config.RESEARCH_TIMEOUT} seconds. "
                           "Try reducing the number of sources or splitting into smaller queries."
                )
        
        # Validate result structure
        if not isinstance(result, dict):
            logger.error(f"Invalid result type: {type(result)}")
            raise HTTPException(
                status_code=500,
                detail="Research returned invalid result type"
            )
        
        # Construct response, with detailed logging for missing fields
        try:
            response = ResearchResponse(
                topic=result.get("topic", request.topic),
                summary=result.get("summary", ""),
                critique_a=result.get("critique_A", ""),
                critique_b=result.get("critique_B", ""),
                insight=result.get("insight", ""),
                sources=result.get("sources", []),
                status="success"
            )
            logger.info("Research completed successfully")
            return response
            
        except Exception as e:
            logger.error(f"Failed to construct response: {str(e)}")
            logger.error(f"Result keys: {list(result.keys())}")
            raise HTTPException(
                status_code=500,
                detail="Failed to construct research response"
            )
    
    except Exception as e:
        logger.error(f"Research failed: {str(e)}")
        logger.error(f"Traceback: {traceback.format_exc()}")
        raise HTTPException(
            status_code=500,
            detail=f"Research failed: {str(e)}\nCheck server logs for details."
        )


@app.post("/reinitialize")
async def reinitialize_service():
    """Reinitialize the research service (useful after uploading new PDFs)"""
    global research_service
    try:
        print("🔄 Reinitializing Research Service...")
        research_service.initialize()
        print("✅ Research Service Reinitialized!")
        
        return {
            "status": "success",
            "message": "Research service reinitialized successfully",
            "system_initialized": True,
            "pdf_count": research_service.get_pdf_count()
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Reinitialization failed: {str(e)}"
        )


@app.get("/config")
async def get_config():
    """Get current configuration (excluding sensitive data)"""
    return {
        "llm_model": Config.LLM_MODEL,
        "llm_temperature": Config.LLM_TEMPERATURE,
        "chunk_size": Config.CHUNK_SIZE,
        "chunk_overlap": Config.CHUNK_OVERLAP,
        "bm25_top_k": Config.BM25_TOP_K,
        "wikipedia_max_articles": Config.WIKIPEDIA_MAX_ARTICLES,
        "arxiv_max_papers": Config.ARXIV_MAX_PAPERS,
        "max_snippet_length": Config.MAX_SNIPPET_LENGTH,
        "files_dir": str(Config.FILES_DIR),
        "api_key_set": bool(Config.GROQ_API_KEY)
    }


def main():
    """Run the FastAPI server"""
    uvicorn.run(
        "backend.app:app",
        host=Config.HOST,
        port=Config.PORT,
        reload=Config.DEBUG
    )


if __name__ == "__main__":
    main()
