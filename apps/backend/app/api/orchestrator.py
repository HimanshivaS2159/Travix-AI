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
from ..services.sbt_agent import SBTAgent
from ..services.itinerary_agent import ItineraryAgent
from ..services.rebooking_agent import RebookingAgent
from ..services.revising_agent import RevisingAgent
from ..services.local_guide_agent import LocalGuideAgent
from ..services.expense_agent import ExpenseAgent
from ..config import get_settings
from pydantic import BaseModel

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/orchestrator", tags=["orchestrator"])

# Global agent instances
_orchestrator_instance: Optional[GroqOrchestrator] = None
_backoffice_agent_instance: Optional[BackOfficeAgent] = None
_sbt_agent_instance: Optional[SBTAgent] = None
_itinerary_agent_instance: Optional[ItineraryAgent] = None
_rebooking_agent_instance: Optional[RebookingAgent] = None
_revising_agent_instance: Optional[RevisingAgent] = None
_local_guide_agent_instance: Optional[LocalGuideAgent] = None
_expense_agent_instance: Optional[ExpenseAgent] = None


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


def get_sbt_agent() -> SBTAgent:
    """Dependency to get SBT agent instance"""
    global _sbt_agent_instance
    
    if _sbt_agent_instance is None:
        _sbt_agent_instance = SBTAgent()
    
    return _sbt_agent_instance


def get_itinerary_agent() -> ItineraryAgent:
    """Dependency to get Itinerary agent instance"""
    global _itinerary_agent_instance
    
    if _itinerary_agent_instance is None:
        _itinerary_agent_instance = ItineraryAgent()
    
    return _itinerary_agent_instance


def get_rebooking_agent() -> RebookingAgent:
    """Dependency to get Rebooking agent instance"""
    global _rebooking_agent_instance
    
    if _rebooking_agent_instance is None:
        _rebooking_agent_instance = RebookingAgent()
    
    return _rebooking_agent_instance


def get_revising_agent() -> RevisingAgent:
    """Dependency to get Revising agent instance"""
    global _revising_agent_instance
    
    if _revising_agent_instance is None:
        _revising_agent_instance = RevisingAgent()
    
    return _revising_agent_instance


def get_local_guide_agent() -> LocalGuideAgent:
    """Dependency to get Local Guide agent instance"""
    global _local_guide_agent_instance
    
    if _local_guide_agent_instance is None:
        _local_guide_agent_instance = LocalGuideAgent()
    
    return _local_guide_agent_instance


def get_expense_agent() -> ExpenseAgent:
    """Dependency to get Expense agent instance"""
    global _expense_agent_instance
    
    if _expense_agent_instance is None:
        _expense_agent_instance = ExpenseAgent()
    
    return _expense_agent_instance


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
    backoffice_agent: BackOfficeAgent = Depends(get_backoffice_agent),
    sbt_agent: SBTAgent = Depends(get_sbt_agent),
    itinerary_agent: ItineraryAgent = Depends(get_itinerary_agent),
    rebooking_agent: RebookingAgent = Depends(get_rebooking_agent),
    revising_agent: RevisingAgent = Depends(get_revising_agent),
    local_guide_agent: LocalGuideAgent = Depends(get_local_guide_agent),
    expense_agent: ExpenseAgent = Depends(get_expense_agent)
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
        result = None
        
        if routing.agent == "backoffice_agent":
            result = backoffice_agent.execute(request.user_message)
        elif routing.agent == "sbt_agent":
            result = sbt_agent.execute(request.user_message)
        elif routing.agent == "itinerary_agent":
            result = itinerary_agent.execute(request.user_message)
        elif routing.agent == "rebooking_agent":
            result = rebooking_agent.execute(request.user_message)
        elif routing.agent == "revising_agent":
            result = revising_agent.execute(request.user_message)
        elif routing.agent == "local_guide_agent":
            result = local_guide_agent.execute(request.user_message)
        elif routing.agent == "expense_agent":
            result = expense_agent.execute(request.user_message)
        else:
            # For other agents not yet implemented
            return {
                "agent": routing.agent,
                "action": routing.action,
                "confidence": routing.confidence,
                "reason": routing.reason,
                "result": {
                    "action": routing.action,
                    "message": f"Request routed to {routing.agent}. Agent execution not yet implemented.",
                    "data": None,
                    "trace": [],
                    "success": False
                }
            }
        
        # Return unified response
        return {
            "agent": routing.agent,
            "action": result.action,
            "confidence": routing.confidence,
            "reason": routing.reason,
            "result": result.model_dump()
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


# ==================== Flight Tool Endpoints ====================

class SearchFlightsRequest(BaseModel):
    """Request model for searching flights"""
    from_city: str
    to_city: str
    date: Optional[str] = None


class BookFlightRequest(BaseModel):
    """Request model for booking flight"""
    from_city: str
    to_city: str
    budget: Optional[int] = None
    passenger_name: Optional[str] = "Test User"
    class_type: Optional[str] = "Economy"


@router.post("/execute/search_flights")
async def execute_search_flights(
    request: SearchFlightsRequest,
    agent: SBTAgent = Depends(get_sbt_agent)
) -> dict:
    """
    Execute search_flights tool
    
    Args:
        request: Search parameters (from_city, to_city, date)
        
    Returns:
        Tool result with flight list and trace
    """
    try:
        logger.info(f"Executing search_flights from {request.from_city} to {request.to_city}")
        result = agent.search_flights(
            from_city=request.from_city,
            to_city=request.to_city,
            date=request.date
        )
        return result.model_dump()
    except Exception as e:
        logger.error(f"Error executing search_flights: {e}")
        raise HTTPException(status_code=500, detail="Error searching flights")


@router.post("/execute/book_flight")
async def execute_book_flight(
    request: BookFlightRequest,
    agent: SBTAgent = Depends(get_sbt_agent)
) -> dict:
    """
    Execute book_flight tool
    
    Args:
        request: Booking details
        
    Returns:
        Tool result with booking details and trace
    """
    try:
        logger.info(f"Executing book_flight from {request.from_city} to {request.to_city}")
        result = agent.book_flight(
            from_city=request.from_city,
            to_city=request.to_city,
            budget=request.budget,
            passenger_name=request.passenger_name,
            class_type=request.class_type
        )
        return result.model_dump()
    except Exception as e:
        logger.error(f"Error executing book_flight: {e}")
        raise HTTPException(status_code=500, detail="Error booking flight")


@router.get("/execute/list_flight_bookings")
async def execute_list_flight_bookings(
    agent: SBTAgent = Depends(get_sbt_agent)
) -> dict:
    """
    Execute list_flight_bookings tool
    
    Returns:
        Tool result with flight bookings list and trace
    """
    try:
        logger.info("Executing list_flight_bookings")
        result = agent.list_flight_bookings()
        return result.model_dump()
    except Exception as e:
        logger.error(f"Error executing list_flight_bookings: {e}")
        raise HTTPException(status_code=500, detail="Error listing flight bookings")


# ==================== Local Guide Tool Endpoints ====================

class LocalGuideRequest(BaseModel):
    """Request model for local guide"""
    city: str
    type: Optional[str] = "complete"  # attractions, restaurants, tips, gems, complete


@router.post("/execute/local_guide")
async def execute_local_guide(
    request: LocalGuideRequest,
    agent: LocalGuideAgent = Depends(get_local_guide_agent)
) -> dict:
    """
    Execute local_guide tool
    
    Args:
        request: City and guide type
        
    Returns:
        Tool result with local recommendations and trace
    """
    try:
        logger.info(f"Executing local_guide for {request.city} - {request.type}")
        
        # Build message based on type
        if request.type == "attractions":
            message = f"Show attractions in {request.city}"
        elif request.type == "restaurants":
            message = f"Show restaurants in {request.city}"
        elif request.type == "tips":
            message = f"Show travel tips for {request.city}"
        elif request.type == "gems":
            message = f"Show hidden gems in {request.city}"
        else:
            message = f"Complete local guide for {request.city}"
        
        result = agent.execute(message)
        return result.model_dump()
    except Exception as e:
        logger.error(f"Error executing local_guide: {e}")
        raise HTTPException(status_code=500, detail="Error getting local guide")


# ==================== Expense Tool Endpoints ====================

class CreateExpenseRequest(BaseModel):
    """Request model for creating expense"""
    date: str
    category: str
    merchant: str
    amount: float
    currency: str
    payment_method: str
    gst_amount: Optional[float] = None
    notes: Optional[str] = None
    receipt_url: Optional[str] = None
    associated_trip: Optional[str] = None


class CreateTripRequest(BaseModel):
    """Request model for creating trip"""
    trip_name: str
    start_date: str
    end_date: str
    destination: str
    purpose: str


class ApproveExpenseRequest(BaseModel):
    """Request model for approving expense"""
    expense_id: str
    status: str  # approved, rejected
    notes: Optional[str] = None


@router.post("/execute/create_expense_form")
async def execute_create_expense_form(
    agent: ExpenseAgent = Depends(get_expense_agent)
) -> dict:
    """
    Execute create_expense form
    
    Returns:
        Tool result with expense creation form
    """
    try:
        logger.info("Executing create_expense_form")
        result = agent.create_expense_form([])
        return result.model_dump()
    except Exception as e:
        logger.error(f"Error executing create_expense_form: {e}")
        raise HTTPException(status_code=500, detail="Error creating expense form")


@router.post("/execute/save_expense")
async def execute_save_expense(
    request: CreateExpenseRequest,
    agent: ExpenseAgent = Depends(get_expense_agent)
) -> dict:
    """
    Execute save_expense
    
    Args:
        request: Expense details
        
    Returns:
        Tool result with saved expense
    """
    try:
        logger.info(f"Executing save_expense")
        result = agent.save_expense(request.model_dump())
        return result.model_dump()
    except Exception as e:
        logger.error(f"Error executing save_expense: {e}")
        raise HTTPException(status_code=500, detail="Error saving expense")


@router.get("/execute/show_expenses")
async def execute_show_expenses(
    agent: ExpenseAgent = Depends(get_expense_agent)
) -> dict:
    """
    Execute show_expenses
    
    Returns:
        Tool result with all expenses
    """
    try:
        logger.info("Executing show_expenses")
        result = agent.show_expenses([])
        return result.model_dump()
    except Exception as e:
        logger.error(f"Error executing show_expenses: {e}")
        raise HTTPException(status_code=500, detail="Error showing expenses")


@router.post("/execute/create_trip_form")
async def execute_create_trip_form(
    agent: ExpenseAgent = Depends(get_expense_agent)
) -> dict:
    """
    Execute create_trip form
    
    Returns:
        Tool result with trip creation form
    """
    try:
        logger.info("Executing create_trip_form")
        result = agent.create_trip_form([])
        return result.model_dump()
    except Exception as e:
        logger.error(f"Error executing create_trip_form: {e}")
        raise HTTPException(status_code=500, detail="Error creating trip form")


@router.post("/execute/save_trip")
async def execute_save_trip(
    request: CreateTripRequest,
    agent: ExpenseAgent = Depends(get_expense_agent)
) -> dict:
    """
    Execute save_trip
    
    Args:
        request: Trip details
        
    Returns:
        Tool result with saved trip
    """
    try:
        logger.info(f"Executing save_trip")
        result = agent.save_trip(request.model_dump())
        return result.model_dump()
    except Exception as e:
        logger.error(f"Error executing save_trip: {e}")
        raise HTTPException(status_code=500, detail="Error saving trip")


@router.get("/execute/show_trips")
async def execute_show_trips(
    agent: ExpenseAgent = Depends(get_expense_agent)
) -> dict:
    """
    Execute show_trips
    
    Returns:
        Tool result with all trips
    """
    try:
        logger.info("Executing show_trips")
        result = agent.show_trips([])
        return result.model_dump()
    except Exception as e:
        logger.error(f"Error executing show_trips: {e}")
        raise HTTPException(status_code=500, detail="Error showing trips")


@router.get("/execute/approve_expenses_form")
async def execute_approve_expenses_form(
    agent: ExpenseAgent = Depends(get_expense_agent)
) -> dict:
    """
    Execute approve_expenses form
    
    Returns:
        Tool result with pending expenses
    """
    try:
        logger.info("Executing approve_expenses_form")
        result = agent.approve_expenses_form([])
        return result.model_dump()
    except Exception as e:
        logger.error(f"Error executing approve_expenses_form: {e}")
        raise HTTPException(status_code=500, detail="Error loading approval form")


@router.post("/execute/approve_expense")
async def execute_approve_expense(
    request: ApproveExpenseRequest,
    agent: ExpenseAgent = Depends(get_expense_agent)
) -> dict:
    """
    Execute approve_expense
    
    Args:
        request: Approval details
        
    Returns:
        Tool result with approved expense
    """
    try:
        logger.info(f"Executing approve_expense for {request.expense_id}")
        result = agent.approve_expense(request.expense_id, request.status, request.notes)
        return result.model_dump()
    except Exception as e:
        logger.error(f"Error executing approve_expense: {e}")
        raise HTTPException(status_code=500, detail="Error approving expense")
