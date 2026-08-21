from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .api.orchestrator import router as orchestrator_router
from .api.expense_tracker import router as expense_tracker_router
from .api.flights import router as flights_router
from .config import get_settings
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Travix AI Backend",
    version="0.1.0",
    description="AI-powered travel assistant with Groq API orchestrator and Excel-based expense tracker"
)

# Get settings
settings = get_settings()

# Configure CORS
cors_origins = settings.cors_origins.split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(orchestrator_router)
app.include_router(expense_tracker_router)
app.include_router(flights_router)


@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "travix-backend",
        "version": "0.1.0",
        "groq_configured": bool(settings.groq_api_key)
    }


@app.get("/")
def root():
    """Root endpoint"""
    return {
        "service": "Travix AI Backend",
        "version": "0.1.0",
        "environment": settings.environment,
        "endpoints": {
            "health": "/health",
            "orchestrator_analyze": "/api/orchestrator/analyze",
            "agents_list": "/api/orchestrator/agents",
            "agent_tools": "/api/orchestrator/agents/{agent_name}/tools",
            "expense_tracker": "/api/expense-tracker",
            "flights_search": "/api/flights/search",
            "flights_statistics": "/api/flights/statistics",
            "flights_initialize": "/api/flights/initialize",
            "api_docs": "/docs"
        }
    }
