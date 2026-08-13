"""
Groq API Orchestrator Service
Routes user requests to appropriate agents based on intent analysis
"""

import json
import logging
from typing import Optional
from pydantic import BaseModel
from groq import Groq

logger = logging.getLogger(__name__)


class OrchestratorRequest(BaseModel):
    """Request model for orchestrator"""
    user_message: str
    conversation_history: Optional[list] = None


class OrchestratorResponse(BaseModel):
    """Response model from orchestrator"""
    agent: str
    action: str
    confidence: float
    reason: str
    tools: Optional[list] = None


class AgentDefinition(BaseModel):
    """Definition of an available agent"""
    name: str
    description: str
    capabilities: list
    icon: str


class GroqOrchestrator:
    """
    Orchestrator service that uses Groq API to intelligently route
    user requests to appropriate agents
    """

    # Define available agents
    AGENTS = {
        "orchestrator": AgentDefinition(
            name="Orchestrator",
            description="Routes users across flight and preference workflows",
            capabilities=["flight_search", "preference_management", "route_planning"],
            icon="O"
        ),
        "sbt_agent": AgentDefinition(
            name="SBT Agent",
            description="Collects flight search requirements and provides flight booking services",
            capabilities=["flight_search", "flight_booking", "route_suggestions", "price_analysis"],
            icon="S"
        ),
        "expense_agent": AgentDefinition(
            name="Expense Agent",
            description="Handles trips, approvals, invoices and expense mutation tools",
            capabilities=["expense_tracking", "trip_management", "invoice_generation", "approval_workflow"],
            icon="E"
        ),
        "backoffice_agent": AgentDefinition(
            name="BackOffice Agent",
            description="Handles hotel search, booking, and booking history",
            capabilities=["hotel_search", "hotel_booking", "booking_management"],
            icon="B"
        ),
        "itinerary_agent": AgentDefinition(
            name="Itinerary Agent",
            description="Creates day-wise schedules and itineraries for trips",
            capabilities=["schedule_creation", "day_planning", "activity_scheduling"],
            icon="I"
        ),
        "rebooking_agent": AgentDefinition(
            name="Rebooking Agent",
            description="Handles flight/hotel cancellations, delays, and rebooking",
            capabilities=["flight_cancellation", "hotel_cancellation", "delay_handling", "rebooking"],
            icon="R"
        ),
        "revising_agent": AgentDefinition(
            name="Revising Agent",
            description="Reviews and revises itineraries, optimizes schedules and budgets",
            capabilities=["itinerary_review", "schedule_optimization", "budget_analysis"],
            icon="V"
        ),
    }

    def __init__(self, api_key: str, model: str = "llama-3.3-70b-versatile"):
        """Initialize Groq orchestrator"""
        self.client = Groq(api_key=api_key)
        self.model = model
        self.system_prompt = self._build_system_prompt()

    def _build_system_prompt(self) -> str:
        """Build system prompt with agent definitions"""
        agents_info = "\n".join([
            f"- {agent.name}: {agent.description}"
            for agent in self.AGENTS.values()
        ])

        return f"""You are an AI orchestrator that intelligently routes user requests to appropriate agents.

Available Agents:
{agents_info}

Your task is to:
1. Analyze the user's message to understand their intent
2. Determine which agent is best suited to handle the request
3. Identify the specific action needed
4. Provide a confidence score (0.0 to 1.0) for your routing decision
5. Explain your reasoning

IMPORTANT: You MUST respond with valid JSON only, no other text. Use this format:
{{
    "agent": "agent_name",
    "action": "action_name",
    "confidence": 0.85,
    "reason": "explanation of why this agent was selected",
    "tools": ["tool1", "tool2"]
}}

Agent names must be exactly one of: orchestrator, sbt_agent, expense_agent, backoffice_agent, itinerary_agent, rebooking_agent, revising_agent"""

    def analyze_request(self, request: OrchestratorRequest) -> OrchestratorResponse:
        """
        Analyze user request and route to appropriate agent
        
        Args:
            request: User request with message and optional conversation history
            
        Returns:
            OrchestratorResponse with routing decision
        """
        try:
            # Build conversation for Groq
            messages = []
            
            # Add conversation history if provided
            if request.conversation_history:
                messages.extend(request.conversation_history)
            
            # Add current user message
            messages.append({
                "role": "user",
                "content": request.user_message
            })

            logger.info(f"Analyzing request: {request.user_message}")

            # Call Groq API
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": self.system_prompt
                    },
                    *messages
                ],
                temperature=0.3,
                max_tokens=500,
                top_p=0.9,
            )

            # Extract response content
            response_text = response.choices[0].message.content.strip()
            
            logger.info(f"Groq response: {response_text}")

            # Parse JSON response
            routing_data = json.loads(response_text)

            # Validate routing decision
            if routing_data["agent"] not in self.AGENTS:
                logger.warning(f"Invalid agent: {routing_data['agent']}, defaulting to orchestrator")
                routing_data["agent"] = "orchestrator"

            # Create response
            return OrchestratorResponse(
                agent=routing_data["agent"],
                action=routing_data.get("action", "unknown"),
                confidence=min(max(routing_data.get("confidence", 0.5), 0.0), 1.0),
                reason=routing_data.get("reason", "Orchestrated by Groq API"),
                tools=routing_data.get("tools", [])
            )

        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse JSON response: {e}")
            raise ValueError(f"Invalid orchestrator response format: {e}")
        except Exception as e:
            logger.error(f"Orchestrator error: {e}")
            raise

    def get_available_agents(self) -> dict:
        """Get list of available agents"""
        return {
            name: {
                "name": agent.name,
                "description": agent.description,
                "capabilities": agent.capabilities,
                "icon": agent.icon
            }
            for name, agent in self.AGENTS.items()
        }

    def get_tools_for_agent(self, agent_name: str) -> list:
        """Get list of tools available for a specific agent"""
        agent_tools = {
            "orchestrator": [
                "search_flights",
                "manage_preferences",
                "create_itinerary"
            ],
            "sbt_agent": [
                "search_flights",
                "book_flight",
                "list_flight_bookings",
                "filter_routes",
                "analyze_prices",
                "suggest_alternatives"
            ],
            "expense_agent": [
                "create_expense",
                "approve_expense",
                "generate_invoice",
                "track_trip_costs",
                "create_trip"
            ],
            "backoffice_agent": [
                "list_hotels",
                "book_hotel",
                "list_bookings"
            ],
            "itinerary_agent": [
                "schedule_making_tool",
                "show_schedule"
            ],
            "rebooking_agent": [
                "rebooking_tool",
                "handle_cancellation",
                "handle_delay"
            ],
            "revising_agent": [
                "review_itinerary",
                "optimize_schedule",
                "check_budget"
            ]
        }
        return agent_tools.get(agent_name, [])
