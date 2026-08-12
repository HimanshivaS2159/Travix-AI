"""
Orchestrator API Endpoints
Handles routing user requests through Groq API to appropriate agents
"""

from fastapi import APIRouter, HTTPException, Depends
from typing import Optional
import logging
from ..services.groq_orchestrator import (
    GroqOrchestrator,
    OrchestratorRequest,
    OrchestratorResponse
)
from ..config import get_settings

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/orchestrator", tags=["orchestrator"])

# Global orchestrator instance
_orchestrator_instance: Optional[GroqOrchestrator] = None


def get_orchestrator() -> GroqOrchestrator:
    """Dependency to get orchestrator instance"""
    global _orchestrator_instance
    
    if _orchestrator_instance is None:
        settings = get_settings()
        if not settings.groq_api_key:
            raise HTTPException(
                status_code=500,
                detail="GROQ_API_KEY environment variable not set"
            )
        _orchestrator_instance = GroqOrchestrator(
            api_key=settings.groq_api_key,
            model=settings.groq_model
        )
    
    return _orchestrator_instance


@router.post("/analyze", response_model=OrchestratorResponse)
async def analyze_request(
    request: OrchestratorRequest,
    orchestrator: GroqOrchestrator = Depends(get_orchestrator)
) -> OrchestratorResponse:
    """
    Analyze user request and route to appropriate agent
    
    Args:
        request: User message and optional conversation history
        
    Returns:
        Orchestrator response with routing decision
    """
    try:
        logger.info(f"Received request: {request.user_message}")
        
        # Analyze request using Groq
        response = orchestrator.analyze_request(request)
        
        logger.info(f"Routing to {response.agent}: {response.action}")
        
        return response
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Error analyzing request: {e}")
        raise HTTPException(status_code=500, detail="Error processing request")


@router.get("/agents")
async def get_agents(
    orchestrator: GroqOrchestrator = Depends(get_orchestrator)
) -> dict:
    """Get list of available agents"""
    try:
        agents = orchestrator.get_available_agents()
        return {
            "agents": agents,
            "total": len(agents)
        }
    except Exception as e:
        logger.error(f"Error fetching agents: {e}")
        raise HTTPException(status_code=500, detail="Error fetching agents")


@router.get("/agents/{agent_name}/tools")
async def get_agent_tools(
    agent_name: str,
    orchestrator: GroqOrchestrator = Depends(get_orchestrator)
) -> dict:
    """Get tools available for a specific agent"""
    try:
        tools = orchestrator.get_tools_for_agent(agent_name)
        return {
            "agent": agent_name,
            "tools": tools,
            "tool_count": len(tools)
        }
    except Exception as e:
        logger.error(f"Error fetching tools for {agent_name}: {e}")
        raise HTTPException(status_code=500, detail="Error fetching tools")
