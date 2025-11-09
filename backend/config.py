"""
Configuration module for the Research Assistant Backend
"""

import os
from pathlib import Path
from typing import Optional


class Config:
    """Configuration settings for the research assistant backend"""
    
    # Project paths
    BACKEND_ROOT = Path(__file__).parent
    PROJECT_ROOT = BACKEND_ROOT.parent
    FILES_DIR = PROJECT_ROOT / "files"
    
    # ============================================================================
    # API Configuration
    # ============================================================================
    GROQ_API_KEY: Optional[str] = os.getenv("GROQ_API_KEY")
    
    # Set environment variable if not already set
    if GROQ_API_KEY and GROQ_API_KEY != "put-your-groq-api-key-here":
        os.environ["GROQ_API_KEY"] = GROQ_API_KEY
    
    # LLM Configuration
    LLM_MODEL = os.getenv("LLM_MODEL", "llama-3.1-8b-instant")
    LLM_TEMPERATURE = float(os.getenv("LLM_TEMPERATURE", "0"))
    
    # Document Processing
    CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", "1000"))
    CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP", "200"))
    
    # Retrieval Configuration
    BM25_TOP_K = int(os.getenv("BM25_TOP_K", "4"))
    WIKIPEDIA_MAX_ARTICLES = int(os.getenv("WIKIPEDIA_MAX_ARTICLES", "3"))
    ARXIV_MAX_PAPERS = int(os.getenv("ARXIV_MAX_PAPERS", "3"))
    
    # Snippet Configuration
    MAX_SNIPPET_LENGTH = int(os.getenv("MAX_SNIPPET_LENGTH", "800"))
    
    # API Server Configuration
    HOST = os.getenv("HOST", "0.0.0.0")
    PORT = int(os.getenv("PORT", "8000"))
    DEBUG = os.getenv("DEBUG", "False").lower() == "true"
    
    @classmethod
    def ensure_files_dir(cls):
        """Ensure the files directory exists"""
        cls.FILES_DIR.mkdir(parents=True, exist_ok=True)
        return cls.FILES_DIR
    
    @classmethod
    def set_groq_api_key(cls, api_key: str):
        """Set GROQ API key"""
        cls.GROQ_API_KEY = api_key
        os.environ["GROQ_API_KEY"] = api_key
    
    @classmethod
    def validate_config(cls) -> bool:
        """Validate configuration"""
        if not cls.GROQ_API_KEY:
            raise ValueError(
                "GROQ_API_KEY is not set. Please set it as an environment variable "
                "or in the .env file."
            )
        return True
