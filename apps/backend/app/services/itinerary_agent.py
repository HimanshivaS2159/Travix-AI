"""
Itinerary Agent Service
Handles day-wise schedule creation and management
"""

import logging
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
from pydantic import BaseModel
import json

logger = logging.getLogger(__name__)

# In-memory storage for schedules
SCHEDULES = []


class ScheduleItem(BaseModel):
    """Single schedule item in a day"""
    time: str
    activity: str
    location: str
    duration: str
    notes: str


class DailySchedule(BaseModel):
    """Daily schedule"""
    day: int
    date: str
    title: str
    items: List[ScheduleItem]


class ItineraryRequest(BaseModel):
    """Itinerary creation request"""
    trip_name: str
    start_date: str
    end_date: str
    city: str
    activities: List[str]


class ToolResult(BaseModel):
    """Tool result wrapper"""
    action: str
    message: str
    data: Any
    success: bool
    trace: List[Dict] = []


class ItineraryAgent:
    """Agent for creating and managing travel itineraries"""

    def __init__(self):
        self.schedules = SCHEDULES

    def execute(self, user_message: str) -> ToolResult:
        """
        Execute Itinerary Agent based on user message
        
        Args:
            user_message: User's natural language request
            
        Returns:
            ToolResult with schedule or action result
        """
        logger.info(f"Itinerary Agent executing: {user_message}")
        
        message_lower = user_message.lower()
        trace = self._generate_initial_trace()

        # Determine intent
        if "create" in message_lower and "schedule" in message_lower:
            return self.create_schedule_form(trace)
        
        elif "show" in message_lower and "schedule" in message_lower:
            return self.show_schedules(trace)
        
        elif "day" in message_lower and ("schedule" in message_lower or "itinerary" in message_lower):
            return self.create_schedule_form(trace)
        
        else:
            return ToolResult(
                action="help",
                message="I can help you with: 1) Create a day-wise schedule 2) Show saved schedules",
                data={"suggestions": [
                    "Create a day-wise schedule",
                    "Show me all schedules",
                    "View my itinerary"
                ]},
                success=True,
                trace=trace
            )

    def create_schedule_form(self, trace: List[Dict]) -> ToolResult:
        """Return form for creating schedule"""
        trace.append(self._generate_trace_event(
            "trace-2",
            "tool",
            "schedule_making_tool",
            "completed",
            "Schedule form prepared"
        ))

        return ToolResult(
            action="schedule_making_tool",
            message="Let's create your day-wise schedule. Please fill in the details:",
            data={
                "form_type": "schedule_creator",
                "fields": [
                    {
                        "name": "trip_name",
                        "label": "Trip Name",
                        "type": "text",
                        "placeholder": "e.g., Delhi Adventure 2026",
                        "required": True
                    },
                    {
                        "name": "start_date",
                        "label": "Start Date",
                        "type": "date",
                        "required": True
                    },
                    {
                        "name": "end_date",
                        "label": "End Date",
                        "type": "date",
                        "required": True
                    },
                    {
                        "name": "city",
                        "label": "City",
                        "type": "select",
                        "options": ["Delhi", "Mumbai", "Bangalore", "Goa"],
                        "required": True
                    },
                    {
                        "name": "daily_schedules",
                        "label": "Daily Schedules",
                        "type": "array",
                        "item_fields": [
                            {
                                "name": "day",
                                "label": "Day Number",
                                "type": "number",
                                "required": True
                            },
                            {
                                "name": "title",
                                "label": "Day Title",
                                "type": "text",
                                "placeholder": "e.g., Day 1 - City Exploration",
                                "required": True
                            },
                            {
                                "name": "items",
                                "label": "Schedule Items",
                                "type": "array",
                                "item_fields": [
                                    {
                                        "name": "time",
                                        "label": "Time",
                                        "type": "time",
                                        "required": True
                                    },
                                    {
                                        "name": "activity",
                                        "label": "Activity",
                                        "type": "text",
                                        "placeholder": "e.g., Breakfast",
                                        "required": True
                                    },
                                    {
                                        "name": "location",
                                        "label": "Location",
                                        "type": "text",
                                        "placeholder": "e.g., Hotel Restaurant",
                                        "required": True
                                    },
                                    {
                                        "name": "duration",
                                        "label": "Duration",
                                        "type": "text",
                                        "placeholder": "e.g., 1 hour",
                                        "required": True
                                    },
                                    {
                                        "name": "notes",
                                        "label": "Notes",
                                        "type": "textarea",
                                        "placeholder": "Any additional notes",
                                        "required": False
                                    }
                                ]
                            }
                        ]
                    }
                ]
            },
            success=True,
            trace=trace
        )

    def save_schedule(self, schedule_data: Dict) -> ToolResult:
        """Save schedule to in-memory storage"""
        trace = self._generate_initial_trace()
        trace.append(self._generate_trace_event(
            "trace-2",
            "tool",
            "schedule_making_tool",
            "processing",
            "Validating schedule data"
        ))

        try:
            # Validate data
            if not all(k in schedule_data for k in ["trip_name", "start_date", "end_date", "city"]):
                return ToolResult(
                    action="error",
                    message="Missing required fields",
                    data={"missing_fields": ["trip_name", "start_date", "end_date", "city"]},
                    success=False,
                    trace=trace
                )

            # Create schedule object
            schedule = {
                "id": f"SCH-{len(self.schedules) + 1:03d}",
                "trip_name": schedule_data["trip_name"],
                "city": schedule_data["city"],
                "start_date": schedule_data["start_date"],
                "end_date": schedule_data["end_date"],
                "daily_schedules": schedule_data.get("daily_schedules", []),
                "created_at": datetime.now().isoformat(),
                "status": "active"
            }

            trace.append(self._generate_trace_event(
                "trace-3",
                "booking",
                "schedule_making_tool",
                "completed",
                f"Schedule {schedule['id']} saved"
            ))

            # Save to in-memory storage
            self.schedules.insert(0, schedule)

            return ToolResult(
                action="schedule_saved",
                message=f"✓ Schedule '{schedule_data['trip_name']}' saved successfully!",
                data={
                    "schedule_id": schedule["id"],
                    "trip_name": schedule["trip_name"],
                    "city": schedule["city"],
                    "duration": f"{schedule['start_date']} to {schedule['end_date']}",
                    "schedule": schedule
                },
                success=True,
                trace=trace
            )

        except Exception as e:
            logger.error(f"Error saving schedule: {e}")
            trace.append(self._generate_trace_event(
                "trace-3",
                "error",
                "schedule_making_tool",
                "failed",
                str(e)
            ))
            return ToolResult(
                action="error",
                message=f"Error saving schedule: {str(e)}",
                data={},
                success=False,
                trace=trace
            )

    def show_schedules(self, trace: List[Dict]) -> ToolResult:
        """Show all saved schedules"""
        trace.append(self._generate_trace_event(
            "trace-2",
            "tool",
            "show_schedule",
            "completed",
            f"Retrieved {len(self.schedules)} schedules"
        ))

        if not self.schedules:
            return ToolResult(
                action="show_schedule",
                message="No schedules found. Create your first schedule!",
                data={"schedules": []},
                success=True,
                trace=trace
            )

        return ToolResult(
            action="show_schedule",
            message=f"Found {len(self.schedules)} saved schedule(s):",
            data={
                "schedules": self.schedules,
                "total": len(self.schedules)
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
                "itinerary_agent",
                "completed",
                "Itinerary Agent processing started"
            )
        ]

    def _generate_trace_event(self, event_id: str, event_type: str, name: str, 
                             status: str, output: str) -> Dict:
        """Generate a trace event"""
        return {
            "id": event_id,
            "type": event_type,
            "name": name,
            "agent": "itinerary_agent",
            "status": status,
            "output_summary": output,
            "duration_ms": 50,
            "timestamp": datetime.now().isoformat()
        }
