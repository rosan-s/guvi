"""
Vercel serverless function handler for FastAPI
"""
import sys
import os
from pathlib import Path

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.app.main import app as fastapi_app

# Add CORS middleware
fastapi_app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Ensure routes work behind /api on Vercel
fastapi_app.root_path = "/api"

# Vercel expects ASGI app named 'app'
app = fastapi_app
