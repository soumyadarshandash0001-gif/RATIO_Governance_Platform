"""RATIO Backend Initialization."""
from fastapi import FastAPI

def create_app():
    """Application factory."""
    from app.main import app
    return app
