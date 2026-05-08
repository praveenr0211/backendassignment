"""
FastAPI application factory and configuration.
"""
from fastapi import FastAPI, APIRouter
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
import logging
import logging.config
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

from app.core.config import settings
from app.database import create_tables
from app.middleware import setup_middleware
from app.routes import auth, tasks, admin

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan context manager.
    
    Handles startup and shutdown events.
    """
    # Startup
    logger.info("Starting Task Management API...")
    try:
        create_tables()
        logger.info("Database tables created successfully")
    except Exception as e:
        logger.error(f"Error creating database tables: {str(e)}")
    
    yield
    
    # Shutdown
    logger.info("Shutting down Task Management API...")


def create_app() -> FastAPI:
    """
    Create and configure FastAPI application.
    
    Returns:
        FastAPI application instance.
    """
    # Create FastAPI app
    app = FastAPI(
        title=settings.APP_NAME,
        description="A scalable task management REST API with authentication and role-based access control",
        version=settings.APP_VERSION,
        docs_url="/api/docs",
        redoc_url="/api/redoc",
        openapi_url="/api/openapi.json",
        lifespan=lifespan
    )
    
    # Setup middleware
    setup_middleware(app)
    
    # Include routes
    app.include_router(auth.router)
    app.include_router(tasks.router)
    app.include_router(admin.router)
    
    # Health check endpoint
    @app.get(
        "/health",
        status_code=200,
        summary="Health check",
        tags=["Health"]
    )
    async def health_check():
        """
        Health check endpoint.
        
        Returns:
            Status and version information.
        """
        return {
            "status": "healthy",
            "app": settings.APP_NAME,
            "version": settings.APP_VERSION
        }
    
    # Root endpoint
    @app.get(
        "/",
        status_code=200,
        tags=["Root"]
    )
    async def root():
        """
        Root endpoint.
        
        Returns:
            API information.
        """
        return {
            "message": "Welcome to Task Management API",
            "version": settings.APP_VERSION,
            "docs": "/api/docs",
            "health": "/health"
        }
    
    logger.info("FastAPI application created successfully")
    
    return app


# Create app instance
app = create_app()


if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG
    )
