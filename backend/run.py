#!/usr/bin/env python3
"""
Script to run the backend server
"""

import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from backend.app import main

if __name__ == "__main__":
    print("🚀 Starting Multi-Agent Research Assistant API...")
    print("📖 API Documentation: http://localhost:8000/docs")
    print("🔍 Health Check: http://localhost:8000/health")
    print("\n")
    main()
