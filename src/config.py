"""
Configuration module for the Research Assistant
"""

import os
from pathlib import Path
from typing import Optional


class Config:
    """Configuration settings for the research assistant"""
    
    # Project paths
    PROJECT_ROOT = Path(__file__).parent.parent
    FILES_DIR = PROJECT_ROOT / "files"
    
    # ============================================================================
    # API Configuration - CHANGE THIS BEFORE RUNNING!
    # ============================================================================
    # Set it here or as an environment variable GROQ_API_KEY
    GROQ_API_KEY: Optional[str] = os.getenv(
        "GROQ_API_KEY",
        "put-your-groq-api-key-here"  # ⚠️ REPLACE THIS WITH YOUR ACTUAL KEY
    )
    
    # Set environment variable if not already set
    if not os.getenv("GROQ_API_KEY") and GROQ_API_KEY and GROQ_API_KEY != "put-your-groq-api-key-here":
        os.environ["GROQ_API_KEY"] = GROQ_API_KEY
    
    # LLM Configuration
    LLM_MODEL = "llama-3.1-8b-instant"
    LLM_TEMPERATURE = 0
    
    # Document Processing
    CHUNK_SIZE = 1000
    CHUNK_OVERLAP = 200
    
    # Retrieval Configuration
    BM25_TOP_K = 4
    WIKIPEDIA_MAX_ARTICLES = 3
    
    # Snippet Configuration
    MAX_SNIPPET_LENGTH = 800
    
    @classmethod
    def ensure_files_dir(cls):
        """Ensure the files directory exists"""
        cls.FILES_DIR.mkdir(parents=True, exist_ok=True)
        return cls.FILES_DIR
    
    @classmethod
    def set_groq_api_key(cls, api_key: str):
        """Set the GROQ API key"""
        cls.GROQ_API_KEY = api_key
        os.environ["GROQ_API_KEY"] = api_key
