"""Main FastAPI application."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from config.settings import get_settings
from src.api import auth_router, query_router
from src.db import engine
from src.models import Base
from src.utils.logger import get_logger
import uvicorn

logger = get_logger(__name__)
settings = get_settings()

# Create all tables (users, query_logs, etc. )
Base.metadata.create_all(bind=engine)

# Initialize FastAPI app
app = FastAPI(
    title="LLM Query Service",
    description="LLM-powered query service with user authentication and rate limiting",
    version="0.1.0",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth_router, prefix=settings.api_v1_prefix)
app.include_router(query_router, prefix=settings.api_v1_prefix)


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "ok", "version": "0.1.0"}


if __name__ == "__main__":

    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.debug,
        log_level=settings.log_level.lower(),
    )
