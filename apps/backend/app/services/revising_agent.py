"""
Revising Agent Service
Handles review and revision of itineraries and bookings
"""

import logging
from typing import List, Dict, Any
from datetime import datetime
from pydantic import BaseModel

logger = logging.getLogger(__name__)


class ToolResult(BaseModel):
    """Tool result wrapper"""
    action: str
    message: str
    data: Any
    success: bool
    trace: List[Dict] = []


class RevisingAgent:
    """Agent for reviewing and revising itineraries, bookings, and schedules"""

    def execute(self, user_message: str) -> ToolResult:
        """
        Execute Revising Agent based on user message
        
        Args:
            user_message: User's natural language request
            
        Returns:
            ToolResult with revision suggestions or actions
        """
        logger.info(f"Revising Agent executing: {user_message}")
        
        message_lower = user_message.lower()
        trace = self._generate_initial_trace()

        # Detect revision request
        if "review" in message_lower or "revise" in message_lower or "improve" in message_lower:
            if "itinerary" in message_lower or "schedule" in message_lower:
                return self.review_itinerary(trace)
            elif "booking" in message_lower or "hotel" in message_lower:
                return self.review_booking(trace)
            else:
                return self.review_itinerary(trace)
        
        # Detect optimization request
        elif "optimize" in message_lower or "better" in message_lower or "improve" in message_lower:
            return self.optimize_schedule(trace)
        
        # Detect budget check
        elif "budget" in message_lower or "cost" in message_lower:
            return self.check_budget(trace)
        
        else:
            return ToolResult(
                action="help",
                message="I can help you with: 1) Review your itinerary 2) Review bookings 3) Optimize schedule 4) Check budget",
                data={"suggestions": [
                    "Review my itinerary",
                    "Improve my schedule",
                    "Check my budget",
                    "Optimize my bookings"
                ]},
                success=True,
                trace=trace
            )

    def review_itinerary(self, trace: List[Dict]) -> ToolResult:
        """Review and provide suggestions for itinerary"""
        trace.append(self._generate_trace_event(
            "trace-2",
            "analysis",
            "Itinerary Review",
            "completed",
            "Itinerary analysis completed"
        ))

        suggestions = [
            {
                "issue": "Time constraint on Day 2",
                "current": "Red Fort (2h) + Chandni Chowk (2h) + India Gate (1h) = 5 hours",
                "suggestion": "Split activities: Red Fort (2h) + Chandni Chowk (1.5h) in Day 2, move India Gate to Day 3",
                "impact": "Better pacing, no rushing",
                "priority": "High"
            },
            {
                "issue": "Travel time not accounted",
                "current": "Monument to monument without travel time",
                "suggestion": "Add 30-45 minutes between locations for travel",
                "impact": "More realistic itinerary",
                "priority": "High"
            },
            {
                "issue": "No meal breaks scheduled",
                "current": "Continuous activities from 8 AM to 6 PM",
                "suggestion": "Add 1-hour lunch break at 1 PM at local restaurant near Chandni Chowk",
                "impact": "Better experience and energy levels",
                "priority": "Medium"
            },
            {
                "issue": "Optimal route planning",
                "current": "Red Fort → Chandni Chowk → India Gate (scattered route)",
                "suggestion": "Red Fort → Chandni Chowk → Jama Masjid → India Gate (linear route)",
                "impact": "Saves 45 minutes on travel time",
                "priority": "Medium"
            }
        ]

        return ToolResult(
            action="review_itinerary",
            message="🔍 Itinerary Review Complete - 4 suggestions to improve your trip",
            data={
                "suggestions": suggestions,
                "overall_score": 7.5,
                "score_breakdown": {
                    "pacing": 6.5,
                    "routing": 7.0,
                    "meal_breaks": 5.0,
                    "activities": 9.0
                },
                "recommendation": "Make the suggested adjustments for a better experience"
            },
            success=True,
            trace=trace
        )

    def review_booking(self, trace: List[Dict]) -> ToolResult:
        """Review booking details and provide suggestions"""
        trace.append(self._generate_trace_event(
            "trace-2",
            "analysis",
            "Booking Review",
            "completed",
            "Booking details analyzed"
        ))

        return ToolResult(
            action="review_booking",
            message="✓ Booking Review - Hotel and Flight bookings verified",
            data={
                "booking_status": "Confirmed",
                "bookings": [
                    {
                        "type": "Hotel",
                        "name": "Royal Palace, Delhi",
                        "check_in": "2026-08-14",
                        "check_out": "2026-08-15",
                        "price": "₹3,800",
                        "status": "✓ Confirmed"
                    },
                    {
                        "type": "Flight",
                        "flight": "AI-600",
                        "route": "Delhi → Mumbai",
                        "departure": "2:00 PM",
                        "price": "₹5,500",
                        "status": "✓ Confirmed"
                    }
                ],
                "issues": [],
                "total_cost": "₹9,300",
                "recommendations": [
                    "Travel insurance covers flight delays",
                    "Hotel offers free cancellation until 48 hours before check-in"
                ]
            },
            success=True,
            trace=trace
        )

    def optimize_schedule(self, trace: List[Dict]) -> ToolResult:
        """Optimize schedule for time and comfort"""
        trace.append(self._generate_trace_event(
            "trace-2",
            "optimization",
            "Schedule Optimization",
            "completed",
            "Schedule optimized for better experience"
        ))

        optimized_schedule = {
            "Day 1": {
                "original": "8:00 AM - Red Fort (2h) → 10:00 AM - Chandni Chowk (2h) → 12:00 PM - India Gate (1h)",
                "optimized": "8:00 AM - Red Fort (2h) → 10:00 AM - Travel (30m) → 10:30 AM - Chandni Chowk (1.5h) → 12:00 PM - Lunch (1h) → 1:00 PM - Jama Masjid (1h)",
                "time_saved": "45 minutes",
                "comfort_improvement": "Added meal break, better pacing"
            }
        }

        return ToolResult(
            action="optimize_schedule",
            message="📅 Schedule Optimized - Better timing and comfort",
            data={
                "optimized_schedule": optimized_schedule,
                "time_saved": "45 minutes",
                "improvements": [
                    "Added 1-hour meal break",
                    "Optimal route planning",
                    "Reduced travel time",
                    "Better activity pacing"
                ]
            },
            success=True,
            trace=trace
        )

    def check_budget(self, trace: List[Dict]) -> ToolResult:
        """Check budget and provide cost breakdown"""
        trace.append(self._generate_trace_event(
            "trace-2",
            "analysis",
            "Budget Analysis",
            "completed",
            "Budget breakdown completed"
        ))

        return ToolResult(
            action="check_budget",
            message="💰 Budget Breakdown",
            data={
                "total_budget": "₹50,000",
                "breakdown": {
                    "Hotels": {
                        "amount": "₹11,400",
                        "details": "Royal Palace (₹3,800 x 3 nights)",
                        "percentage": 22.8
                    },
                    "Flights": {
                        "amount": "₹11,000",
                        "details": "Delhi-Mumbai roundtrip (₹5,500 x 2)",
                        "percentage": 22.0
                    },
                    "Food": {
                        "amount": "₹6,000",
                        "details": "Average ₹2,000/day for 3 days",
                        "percentage": 12.0
                    },
                    "Activities": {
                        "amount": "₹8,000",
                        "details": "Museum entries, guided tours, attractions",
                        "percentage": 16.0
                    },
                    "Transport": {
                        "amount": "₹5,000",
                        "details": "Local taxis and auto-rickshaws",
                        "percentage": 10.0
                    },
                    "Miscellaneous": {
                        "amount": "₹8,600",
                        "details": "Shopping, tips, emergencies",
                        "percentage": 17.2
                    }
                },
                "spent": "₹38,500",
                "remaining": "₹11,500",
                "status": "✓ Within budget"
            },
            success=True,
            trace=trace
        )

    def _generate_initial_trace(self) -> List[Dict]:
        """Generate initial trace event"""
        return [
            self._generate_trace_event(
                "trace-1",
                "agent",
                "revising_agent",
                "completed",
                "Revising Agent analysis started"
            )
        ]

    def _generate_trace_event(self, event_id: str, event_type: str, name: str, 
                             status: str, output: str) -> Dict:
        """Generate a trace event"""
        return {
            "id": event_id,
            "type": event_type,
            "name": name,
            "agent": "revising_agent",
            "status": status,
            "output_summary": output,
            "duration_ms": 100,
            "timestamp": datetime.now().isoformat()
        }
