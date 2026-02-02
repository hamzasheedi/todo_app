#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Application startup script for the Todo API.

This script properly configures the Python path and starts the FastAPI application.
"""

import sys
import os
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent
backend_dir = project_root / "backend"
src_dir = project_root / "src"
app_dir = src_dir / "app"

if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

if str(backend_dir) not in sys.path:
    sys.path.insert(0, str(backend_dir))

if str(src_dir) not in sys.path:
    sys.path.insert(0, str(src_dir))

if str(app_dir) not in sys.path:
    sys.path.insert(0, str(app_dir))

# Now we can import from backend
from backend.main import app

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)