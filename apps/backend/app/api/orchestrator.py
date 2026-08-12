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
from ..services.backoffice_agent import BackOfficeAgent
from ..config import get_settings
from pydantic import BaseModel

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/orchestrator", tags=["orchestrator"])

# Global orchestrator instance
_orchestrator_instance: Optional[GroqOrchestrator] = None
# Global BackOffice agent instance
_backoffice_agent_instance: Optional[BackOfficeAgent] = None


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


def get_backoffice_agent() -> BackOfficeAgent:
    """Dependency to get BackOffice agent instance"""
    global _backoffice_agent_instance
    
    if _backoffice_agent_instance is None:
        _backoffice_agent_instance = BackOfficeAgent()
    
    return _backoffice_agent_instance


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


class ExecuteRequest(BaseModel):
    """Request model for unified execution endpoint"""
    user_message: str
    conversation_history: Optional[list] = None


@router.post("/execute")
async def execute_request(
    request: ExecuteRequest,
    orchestrator: GroqOrchestrator = Depends(get_orchestrator),
    backoffice_agent: BackOfficeAgent = Depends(get_backoffice_agent)
) -> dict:
    """
    Unified execution endpoint - routes and executes agent actions
    
    Args:
        request: User message and optional conversation history
        
    Returns:
        Complete execution result with trace
    """
    try:
        logger.info(f"Execute request: {request.user_message}")
        
        # Step 1: Route through orchestrator
        orchestrator_request = OrchestratorRequest(
            user_message=request.user_message,
            conversation_history=request.conversation_history
        )
        routing = orchestrator.analyze_request(orchestrator_request)
        
        logger.info(f"Routed to {routing.agent}: {routing.action}")
        
        # Step 2: Execute based on routing
        if routing.agent == "backoffice_agent":
            # Execute through BackOffice Agent
            result = backoffice_agent.execute(request.user_message)
            return {
                "agent": routing.agent,
                "action": result.action,
                "confidence": routing.confidence,
                "reason": routing.reason,
                "result": result.model_dump()
            }
        else:
            # For other agents, return routing info only
            # (SBT and Expense agents would be implemented here)
            return {
                "agent": routing.agent,
                "action": routing.action,
                "confidence": routing.confidence,
                "reason": routing.reason,
                "result": {
                    "action": routing.action,
                    "message": f"Request routed to {routing.agent}. Agent execution not yet implemented for this agent.",
                    "data": None,
                    "trace": []
                }
            }
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Error executing request: {e}")
        raise HTTPException(status_code=500, detail="Error executing request")


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


# ==================== Hotel Tool Endpoints ====================

class ListHotelsRequest(BaseModel):
    """Request model for listing hotels"""
    city: str


class BookHotelRequest(BaseModel):
    """Request model for booking hotel"""
    city: str
    budget: Optional[int] = None
    room_type: Optional[str] = None
    check_in: Optional[str] = None
    check_out: Optional[str] = None


@router.post("/execute/list_hotels")
async def execute_list_hotels(
    request: ListHotelsRequest,
    agent: BackOfficeAgent = Depends(get_backoffice_agent)
) -> dict:
    """
    Execute list_hotels tool
    
    Args:
        request: City to search hotels
        
    Returns:
        Tool result with hotel list and trace
    """
    try:
        logger.info(f"Executing list_hotels for {request.city}")
        result = agent.list_hotels(request.city)
        return result.model_dump()
    except Exception as e:
        logger.error(f"Error executing list_hotels: {e}")
        raise HTTPException(status_code=500, detail="Error listing hotels")


@router.post("/execute/book_hotel")
async def execute_book_hotel(
    request: BookHotelRequest,
    agent: BackOfficeAgent = Depends(get_backoffice_agent)
) -> dict:
    """
    Execute book_hotel tool
    
    Args:
        request: Booking details
        
    Returns:
        Tool result with booking details and trace
    """
    try:
        logger.info(f"Executing book_hotel for {request.city} with budget {request.budget}")
        result = agent.book_hotel(
            city=request.city,
            budget=request.budget,
            room_type=request.room_type,
            check_in=request.check_in,
            check_out=request.check_out
        )
        return result.model_dump()
    except Exception as e:
        logger.error(f"Error executing book_hotel: {e}")
        raise HTTPException(status_code=500, detail="Error booking hotel")


@router.get("/execute/list_bookings")
async def execute_list_bookings(
    agent: BackOfficeAgent = Depends(get_backoffice_agent)
) -> dict:
    """
    Execute list_bookings tool
    
    Returns:
        Tool result with bookings list and trace
    """
    try:
        logger.info("Executing list_bookings")
        result = agent.list_bookings()
        return result.model_dump()
    except Exception as e:
        logger.error(f"Error executing list_bookings: {e}")
        raise HTTPException(status_code=500, detail="Error listing bookings")
