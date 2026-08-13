"""
Rebooking Agent Service
Handles cancellations, delays, and rebooking scenarios
"""

import logging
from typing import List, Dict, Any, Optional
from datetime import datetime
from pydantic import BaseModel

logger = logging.getLogger(__name__)

# In-memory storage for rebookings
REBOOKINGS = []


class RebookingRequest(BaseModel):
    """Rebooking request"""
    booking_id: str
    reason: str
    original_date: str
    new_date: Optional[str] = None


class ToolResult(BaseModel):
    """Tool result wrapper"""
    action: str
    message: str
    data: Any
    success: bool
    trace: List[Dict] = []


class RebookingAgent:
    """Agent for handling cancellations, delays, and rebooking"""

    def __init__(self):
        self.rebookings = REBOOKINGS

    def execute(self, user_message: str) -> ToolResult:
        """
        Execute Rebooking Agent based on user message
        
        Args:
            user_message: User's natural language request
            
        Returns:
            ToolResult with rebooking information
        """
        logger.info(f"Rebooking Agent executing: {user_message}")
        
        message_lower = user_message.lower()
        trace = self._generate_initial_trace()

        # Detect cancellation
        if "cancel" in message_lower and ("flight" in message_lower or "booking" in message_lower):
            return self.handle_cancellation(user_message, trace)
        
        # Detect delay
        elif "delay" in message_lower and "flight" in message_lower:
            return self.handle_flight_delay(user_message, trace)
        
        # Detect hotel cancellation
        elif "cancel" in message_lower and "hotel" in message_lower:
            return self.handle_hotel_cancellation(user_message, trace)
        
        # Detect rebook
        elif "rebook" in message_lower or ("reschedule" in message_lower and "booking" in message_lower):
            return self.handle_rebooking(user_message, trace)
        
        else:
            return ToolResult(
                action="help",
                message="I can help with: 1) Flight cancellations 2) Flight delays 3) Hotel cancellations 4) Rebooking requests",
                data={"suggestions": [
                    "My flight is cancelled",
                    "My flight is delayed",
                    "Cancel my hotel booking",
                    "Rebook my flight"
                ]},
                success=True,
                trace=trace
            )

    def handle_flight_delay(self, user_message: str, trace: List[Dict]) -> ToolResult:
        """Handle flight delay"""
        trace.append(self._generate_trace_event(
            "trace-2",
            "tool",
            "rebooking_tool",
            "processing",
            "Analyzing flight delay"
        ))

        # Extract delay information
        delay_info = self._analyze_delay(user_message)

        trace.append(self._generate_trace_event(
            "trace-3",
            "tool",
            "rebooking_tool",
            "completed",
            f"Delay identified: {delay_info['hours']} hours"
        ))

        rebooking = {
            "id": f"RBK-{len(self.rebookings) + 1:03d}",
            "type": "flight_delay",
            "status": "processed",
            "original_flight": delay_info.get("flight", "N/A"),
            "delay_hours": delay_info["hours"],
            "compensation": "₹3,000 (as per airline policy)",
            "options": [
                "Take the delayed flight with compensation",
                "Rebook on next available flight",
                "Full refund + rebooking voucher"
            ],
            "created_at": datetime.now().isoformat()
        }

        self.rebookings.insert(0, rebooking)

        return ToolResult(
            action="rebooking_tool",
            message=f"✈️ Flight delay detected: {delay_info['hours']} hours delay",
            data={
                "rebooking_id": rebooking["id"],
                "delay_hours": delay_info["hours"],
                "compensation": rebooking["compensation"],
                "options": rebooking["options"],
                "original_flight": rebooking["original_flight"],
                "status": "processed"
            },
            success=True,
            trace=trace
        )

    def handle_flight_cancellation(self, user_message: str, trace: List[Dict]) -> ToolResult:
        """Handle flight cancellation"""
        trace.append(self._generate_trace_event(
            "trace-2",
            "tool",
            "rebooking_tool",
            "processing",
            "Processing flight cancellation"
        ))

        flight_info = self._extract_flight_info(user_message)

        trace.append(self._generate_trace_event(
            "trace-3",
            "tool",
            "rebooking_tool",
            "completed",
            "Flight cancellation processed"
        ))

        rebooking = {
            "id": f"RBK-{len(self.rebookings) + 1:03d}",
            "type": "flight_cancellation",
            "status": "processed",
            "original_flight": flight_info.get("flight", "N/A"),
            "cancellation_reason": "Airline cancellation",
            "refund_amount": "₹45,000 (Full ticket price)",
            "rebooking_options": [
                "Air India - Delhi to Mumbai (12:00 PM)",
                "SpiceJet - Delhi to Mumbai (2:30 PM)",
                "Go Air - Delhi to Mumbai (5:15 PM)"
            ],
            "full_refund": True,
            "created_at": datetime.now().isoformat()
        }

        self.rebookings.insert(0, rebooking)

        return ToolResult(
            action="rebooking_tool",
            message="✈️ Flight cancellation detected - Full refund + rebooking options available",
            data={
                "rebooking_id": rebooking["id"],
                "refund_amount": rebooking["refund_amount"],
                "rebooking_options": rebooking["rebooking_options"],
                "original_flight": rebooking["original_flight"],
                "status": "processed"
            },
            success=True,
            trace=trace
        )

    def handle_hotel_cancellation(self, user_message: str, trace: List[Dict]) -> ToolResult:
        """Handle hotel cancellation"""
        trace.append(self._generate_trace_event(
            "trace-2",
            "tool",
            "rebooking_tool",
            "processing",
            "Processing hotel cancellation"
        ))

        hotel_info = self._extract_hotel_info(user_message)

        trace.append(self._generate_trace_event(
            "trace-3",
            "tool",
            "rebooking_tool",
            "completed",
            "Hotel cancellation processed"
        ))

        rebooking = {
            "id": f"RBK-{len(self.rebookings) + 1:03d}",
            "type": "hotel_cancellation",
            "status": "processed",
            "original_booking": hotel_info.get("hotel", "N/A"),
            "check_in": hotel_info.get("check_in", "N/A"),
            "check_out": hotel_info.get("check_out", "N/A"),
            "refund_policy": "50% refund (Cancel within 48 hours)",
            "refund_amount": "₹1,900 (50% of ₹3,800)",
            "alternative_hotels": [
                {"name": "Park Inn Delhi", "price": 4000, "rating": 4.0},
                {"name": "Budget Stay", "price": 2800, "rating": 3.5},
                {"name": "Hotel Royal", "price": 3500, "rating": 4.2}
            ],
            "created_at": datetime.now().isoformat()
        }

        self.rebookings.insert(0, rebooking)

        return ToolResult(
            action="rebooking_tool",
            message="🏨 Hotel cancellation processed - Refund and alternative options available",
            data={
                "rebooking_id": rebooking["id"],
                "refund_policy": rebooking["refund_policy"],
                "refund_amount": rebooking["refund_amount"],
                "alternative_hotels": rebooking["alternative_hotels"],
                "original_booking": rebooking["original_booking"],
                "status": "processed"
            },
            success=True,
            trace=trace
        )

    def handle_cancellation(self, user_message: str, trace: List[Dict]) -> ToolResult:
        """Route to appropriate cancellation handler"""
        if "flight" in user_message.lower():
            return self.handle_flight_cancellation(user_message, trace)
        elif "hotel" in user_message.lower():
            return self.handle_hotel_cancellation(user_message, trace)
        else:
            return self.handle_flight_cancellation(user_message, trace)

    def handle_rebooking(self, user_message: str, trace: List[Dict]) -> ToolResult:
        """Handle rebooking request"""
        trace.append(self._generate_trace_event(
            "trace-2",
            "tool",
            "rebooking_tool",
            "completed",
            "Rebooking options generated"
        ))

        return ToolResult(
            action="rebooking_tool",
            message="Choose your rebooking option:",
            data={
                "rebooking_options": [
                    {
                        "airline": "Air India",
                        "departure": "2:00 PM",
                        "arrival": "4:15 PM",
                        "price": 0,
                        "notes": "No additional charge"
                    },
                    {
                        "airline": "IndiGo",
                        "departure": "5:30 PM",
                        "arrival": "7:45 PM",
                        "price": 2000,
                        "notes": "₹2,000 upgrade charge"
                    }
                ]
            },
            success=True,
            trace=trace
        )

    def _analyze_delay(self, user_message: str) -> Dict:
        """Extract delay information from message"""
        if "2 hour" in user_message.lower():
            return {"hours": 2, "flight": "N/A"}
        elif "3 hour" in user_message.lower():
            return {"hours": 3, "flight": "N/A"}
        elif "4 hour" in user_message.lower():
            return {"hours": 4, "flight": "N/A"}
        else:
            return {"hours": 2, "flight": "N/A"}

    def _extract_flight_info(self, user_message: str) -> Dict:
        """Extract flight information"""
        return {
            "flight": "AI-600",
            "route": "Delhi to Mumbai",
            "date": "2026-08-14"
        }

    def _extract_hotel_info(self, user_message: str) -> Dict:
        """Extract hotel information"""
        return {
            "hotel": "Royal Palace",
            "check_in": "2026-08-14",
            "check_out": "2026-08-15"
        }

    def _generate_initial_trace(self) -> List[Dict]:
        """Generate initial trace event"""
        return [
            self._generate_trace_event(
                "trace-1",
                "agent",
                "rebooking_agent",
                "completed",
                "Rebooking Agent processing started"
            )
        ]

    def _generate_trace_event(self, event_id: str, event_type: str, name: str, 
                             status: str, output: str) -> Dict:
        """Generate a trace event"""
        return {
            "id": event_id,
            "type": event_type,
            "name": name,
            "agent": "rebooking_agent",
            "status": status,
            "output_summary": output,
            "duration_ms": 50,
            "timestamp": datetime.now().isoformat()
        }
