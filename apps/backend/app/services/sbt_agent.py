"""
SBT Agent Service
Handles flight-related workflows: search_flights, book_flight, list_flight_bookings
"""

import logging
import random
import uuid
from datetime import datetime, timedelta
from typing import Optional, List, Dict, Any
from pydantic import BaseModel

logger = logging.getLogger(__name__)


# ==================== Models ====================

class Flight(BaseModel):
    """Flight model"""
    id: str
    airline: str
    flight_number: str
    from_city: str
    from_code: str
    to_city: str
    to_code: str
    departure_time: str
    arrival_time: str
    duration: str
    price: int
    currency: str = "INR"
    class_type: str
    stops: int
    available_seats: int
    baggage: str
    amenities: List[str]


class FlightBooking(BaseModel):
    """Flight booking model"""
    booking_id: str
    flight_id: str
    airline: str
    flight_number: str
    from_city: str
    from_code: str
    to_city: str
    to_code: str
    departure_time: str
    arrival_time: str
    duration: str
    price: int
    currency: str
    class_type: str
    passenger_name: str
    booking_date: str
    status: str


class ToolResult(BaseModel):
    """Result from tool execution"""
    action: str
    message: str
    data: Optional[Any] = None
    trace: List[Dict[str, Any]]


# ==================== Mock Flight Data ====================

MOCK_FLIGHTS = {
    ("delhi", "dubai"): [
        Flight(
            id="DEL-DXB-001",
            airline="Emirates",
            flight_number="EK-511",
            from_city="Delhi",
            from_code="DEL",
            to_city="Dubai",
            to_code="DXB",
            departure_time="23:35",
            arrival_time="02:45+1",
            duration="4h 10m",
            price=18500,
            class_type="Economy",
            stops=0,
            available_seats=42,
            baggage="30kg",
            amenities=["Wi-Fi", "Meals", "Entertainment"]
        ),
        Flight(
            id="DEL-DXB-002",
            airline="Air India",
            flight_number="AI-995",
            from_city="Delhi",
            from_code="DEL",
            to_city="Dubai",
            to_code="DXB",
            departure_time="14:20",
            arrival_time="17:15",
            duration="3h 55m",
            price=15200,
            class_type="Economy",
            stops=0,
            available_seats=28,
            baggage="25kg",
            amenities=["Meals", "Entertainment"]
        ),
        Flight(
            id="DEL-DXB-003",
            airline="IndiGo",
            flight_number="6E-1135",
            from_city="Delhi",
            from_code="DEL",
            to_city="Dubai",
            to_code="DXB",
            departure_time="08:45",
            arrival_time="11:30",
            duration="3h 45m",
            price=12800,
            class_type="Economy",
            stops=0,
            available_seats=56,
            baggage="20kg",
            amenities=["Meals"]
        ),
        Flight(
            id="DEL-DXB-004",
            airline="FlyDubai",
            flight_number="FZ-433",
            from_city="Delhi",
            from_code="DEL",
            to_city="Dubai",
            to_code="DXB",
            departure_time="19:00",
            arrival_time="22:05",
            duration="4h 05m",
            price=13500,
            class_type="Economy",
            stops=0,
            available_seats=38,
            baggage="23kg",
            amenities=["Meals", "Wi-Fi"]
        ),
    ],
    ("delhi", "mumbai"): [
        Flight(
            id="DEL-BOM-001",
            airline="Air India",
            flight_number="AI-864",
            from_city="Delhi",
            from_code="DEL",
            to_city="Mumbai",
            to_code="BOM",
            departure_time="06:00",
            arrival_time="08:15",
            duration="2h 15m",
            price=5500,
            class_type="Economy",
            stops=0,
            available_seats=45,
            baggage="25kg",
            amenities=["Meals", "Entertainment"]
        ),
        Flight(
            id="DEL-BOM-002",
            airline="IndiGo",
            flight_number="6E-2134",
            from_city="Delhi",
            from_code="DEL",
            to_city="Mumbai",
            to_code="BOM",
            departure_time="09:30",
            arrival_time="11:40",
            duration="2h 10m",
            price=4800,
            class_type="Economy",
            stops=0,
            available_seats=62,
            baggage="15kg",
            amenities=["Snacks"]
        ),
        Flight(
            id="DEL-BOM-003",
            airline="Vistara",
            flight_number="UK-995",
            from_city="Delhi",
            from_code="DEL",
            to_city="Mumbai",
            to_code="BOM",
            departure_time="13:45",
            arrival_time="16:00",
            duration="2h 15m",
            price=6200,
            class_type="Economy",
            stops=0,
            available_seats=38,
            baggage="20kg",
            amenities=["Meals", "Wi-Fi", "Entertainment"]
        ),
        Flight(
            id="DEL-BOM-004",
            airline="SpiceJet",
            flight_number="SG-8937",
            from_city="Delhi",
            from_code="DEL",
            to_city="Mumbai",
            to_code="BOM",
            departure_time="18:20",
            arrival_time="20:35",
            duration="2h 15m",
            price=4200,
            class_type="Economy",
            stops=0,
            available_seats=51,
            baggage="15kg",
            amenities=["Snacks"]
        ),
    ],
    ("mumbai", "dubai"): [
        Flight(
            id="BOM-DXB-001",
            airline="Emirates",
            flight_number="EK-502",
            from_city="Mumbai",
            from_code="BOM",
            to_city="Dubai",
            to_code="DXB",
            departure_time="04:25",
            arrival_time="06:50",
            duration="3h 25m",
            price=16200,
            class_type="Economy",
            stops=0,
            available_seats=35,
            baggage="30kg",
            amenities=["Wi-Fi", "Meals", "Entertainment"]
        ),
        Flight(
            id="BOM-DXB-002",
            airline="Air India",
            flight_number="AI-979",
            from_city="Mumbai",
            from_code="BOM",
            to_city="Dubai",
            to_code="DXB",
            departure_time="14:50",
            arrival_time="17:05",
            duration="3h 15m",
            price=14500,
            class_type="Economy",
            stops=0,
            available_seats=42,
            baggage="25kg",
            amenities=["Meals", "Entertainment"]
        ),
        Flight(
            id="BOM-DXB-003",
            airline="IndiGo",
            flight_number="6E-1401",
            from_city="Mumbai",
            from_code="BOM",
            to_city="Dubai",
            to_code="DXB",
            departure_time="22:10",
            arrival_time="00:25+1",
            duration="3h 15m",
            price=12900,
            class_type="Economy",
            stops=0,
            available_seats=58,
            baggage="20kg",
            amenities=["Meals"]
        ),
    ],
    ("mumbai", "delhi"): [
        Flight(
            id="BOM-DEL-001",
            airline="Air India",
            flight_number="AI-865",
            from_city="Mumbai",
            from_code="BOM",
            to_city="Delhi",
            to_code="DEL",
            departure_time="07:30",
            arrival_time="09:45",
            duration="2h 15m",
            price=5800,
            class_type="Economy",
            stops=0,
            available_seats=38,
            baggage="25kg",
            amenities=["Meals", "Entertainment"]
        ),
        Flight(
            id="BOM-DEL-002",
            airline="IndiGo",
            flight_number="6E-2135",
            from_city="Mumbai",
            from_code="BOM",
            to_city="Delhi",
            to_code="DEL",
            departure_time="11:15",
            arrival_time="13:25",
            duration="2h 10m",
            price=5100,
            class_type="Economy",
            stops=0,
            available_seats=54,
            baggage="15kg",
            amenities=["Snacks"]
        ),
        Flight(
            id="BOM-DEL-003",
            airline="Vistara",
            flight_number="UK-996",
            from_city="Mumbai",
            from_code="BOM",
            to_city="Delhi",
            to_code="DEL",
            departure_time="15:30",
            arrival_time="17:45",
            duration="2h 15m",
            price=6500,
            class_type="Economy",
            stops=0,
            available_seats=32,
            baggage="20kg",
            amenities=["Meals", "Wi-Fi", "Entertainment"]
        ),
        Flight(
            id="BOM-DEL-004",
            airline="SpiceJet",
            flight_number="SG-8938",
            from_city="Mumbai",
            from_code="BOM",
            to_city="Delhi",
            to_code="DEL",
            departure_time="20:10",
            arrival_time="22:25",
            duration="2h 15m",
            price=4500,
            class_type="Economy",
            stops=0,
            available_seats=48,
            baggage="15kg",
            amenities=["Snacks"]
        ),
    ],
    ("dubai", "delhi"): [
        Flight(
            id="DXB-DEL-001",
            airline="Emirates",
            flight_number="EK-512",
            from_city="Dubai",
            from_code="DXB",
            to_city="Delhi",
            to_code="DEL",
            departure_time="03:35",
            arrival_time="08:45",
            duration="4h 10m",
            price=19500,
            class_type="Economy",
            stops=0,
            available_seats=45,
            baggage="30kg",
            amenities=["Wi-Fi", "Meals", "Entertainment"]
        ),
        Flight(
            id="DXB-DEL-002",
            airline="Air India",
            flight_number="AI-996",
            from_city="Dubai",
            from_code="DXB",
            to_city="Delhi",
            to_code="DEL",
            departure_time="09:15",
            arrival_time="14:20",
            duration="3h 55m",
            price=16200,
            class_type="Economy",
            stops=0,
            available_seats=32,
            baggage="25kg",
            amenities=["Meals", "Entertainment"]
        ),
        Flight(
            id="DXB-DEL-003",
            airline="IndiGo",
            flight_number="6E-1136",
            from_city="Dubai",
            from_code="DXB",
            to_city="Delhi",
            to_code="DEL",
            departure_time="16:30",
            arrival_time="21:15",
            duration="3h 45m",
            price=13800,
            class_type="Economy",
            stops=0,
            available_seats=52,
            baggage="20kg",
            amenities=["Meals"]
        ),
    ],
    ("dubai", "mumbai"): [
        Flight(
            id="DXB-BOM-001",
            airline="Emirates",
            flight_number="EK-503",
            from_city="Dubai",
            from_code="DXB",
            to_city="Mumbai",
            to_code="BOM",
            departure_time="08:50",
            arrival_time="14:15",
            duration="3h 25m",
            price=17200,
            class_type="Economy",
            stops=0,
            available_seats=38,
            baggage="30kg",
            amenities=["Wi-Fi", "Meals", "Entertainment"]
        ),
        Flight(
            id="DXB-BOM-002",
            airline="Air India",
            flight_number="AI-980",
            from_city="Dubai",
            from_code="DXB",
            to_city="Mumbai",
            to_code="BOM",
            departure_time="20:05",
            arrival_time="01:20+1",
            duration="3h 15m",
            price=15500,
            class_type="Economy",
            stops=0,
            available_seats=44,
            baggage="25kg",
            amenities=["Meals", "Entertainment"]
        ),
        Flight(
            id="DXB-BOM-003",
            airline="IndiGo",
            flight_number="6E-1402",
            from_city="Dubai",
            from_code="DXB",
            to_city="Mumbai",
            to_code="BOM",
            departure_time="13:25",
            arrival_time="18:40",
            duration="3h 15m",
            price=13900,
            class_type="Economy",
            stops=0,
            available_seats=56,
            baggage="20kg",
            amenities=["Meals"]
        ),
    ],
    ("bangalore", "delhi"): [
        Flight(
            id="BLR-DEL-001",
            airline="Air India",
            flight_number="AI-805",
            from_city="Bangalore",
            from_code="BLR",
            to_city="Delhi",
            to_code="DEL",
            departure_time="10:45",
            arrival_time="13:40",
            duration="2h 55m",
            price=6100,
            class_type="Economy",
            stops=0,
            available_seats=36,
            baggage="25kg",
            amenities=["Meals", "Entertainment"]
        ),
        Flight(
            id="BLR-DEL-002",
            airline="IndiGo",
            flight_number="6E-6118",
            from_city="Bangalore",
            from_code="BLR",
            to_city="Delhi",
            to_code="DEL",
            departure_time="15:15",
            arrival_time="18:05",
            duration="2h 50m",
            price=5200,
            class_type="Economy",
            stops=0,
            available_seats=51,
            baggage="15kg",
            amenities=["Snacks"]
        ),
        Flight(
            id="BLR-DEL-003",
            airline="Vistara",
            flight_number="UK-888",
            from_city="Bangalore",
            from_code="BLR",
            to_city="Delhi",
            to_code="DEL",
            departure_time="21:00",
            arrival_time="23:50",
            duration="2h 50m",
            price=6800,
            class_type="Economy",
            stops=0,
            available_seats=28,
            baggage="20kg",
            amenities=["Meals", "Wi-Fi", "Entertainment"]
        ),
    ],
    ("delhi", "bangalore"): [
        Flight(
            id="DEL-BLR-001",
            airline="Air India",
            flight_number="AI-804",
            from_city="Delhi",
            from_code="DEL",
            to_city="Bangalore",
            to_code="BLR",
            departure_time="06:15",
            arrival_time="09:10",
            duration="2h 55m",
            price=5800,
            class_type="Economy",
            stops=0,
            available_seats=40,
            baggage="25kg",
            amenities=["Meals", "Entertainment"]
        ),
        Flight(
            id="DEL-BLR-002",
            airline="IndiGo",
            flight_number="6E-6117",
            from_city="Delhi",
            from_code="DEL",
            to_city="Bangalore",
            to_code="BLR",
            departure_time="12:30",
            arrival_time="15:20",
            duration="2h 50m",
            price=4900,
            class_type="Economy",
            stops=0,
            available_seats=55,
            baggage="15kg",
            amenities=["Snacks"]
        ),
        Flight(
            id="DEL-BLR-003",
            airline="Vistara",
            flight_number="UK-887",
            from_city="Delhi",
            from_code="DEL",
            to_city="Bangalore",
            to_code="BLR",
            departure_time="17:45",
            arrival_time="20:35",
            duration="2h 50m",
            price=6500,
            class_type="Economy",
            stops=0,
            available_seats=32,
            baggage="20kg",
            amenities=["Meals", "Wi-Fi", "Entertainment"]
        ),
    ],
}

# City name mapping
CITY_MAPPING = {
    "delhi": {"name": "Delhi", "code": "DEL"},
    "new delhi": {"name": "Delhi", "code": "DEL"},
    "newdelhi": {"name": "Delhi", "code": "DEL"},
    "mumbai": {"name": "Mumbai", "code": "BOM"},
    "bombay": {"name": "Mumbai", "code": "BOM"},
    "dubai": {"name": "Dubai", "code": "DXB"},
    "bangalore": {"name": "Bangalore", "code": "BLR"},
    "bengaluru": {"name": "Bangalore", "code": "BLR"},
    "blr": {"name": "Bangalore", "code": "BLR"},
    "goa": {"name": "Goa", "code": "GOI"},
}


# ==================== In-Memory Booking Storage ====================

# Pre-populate with demo bookings
FLIGHT_BOOKINGS: List[FlightBooking] = [
    FlightBooking(
        booking_id="FB-A1B2C3",
        flight_id="DEL-BOM-001",
        airline="Air India",
        flight_number="AI-864",
        from_city="Delhi",
        from_code="DEL",
        to_city="Mumbai",
        to_code="BOM",
        departure_time="06:00",
        arrival_time="08:15",
        duration="2h 15m",
        price=5500,
        currency="INR",
        class_type="Economy",
        passenger_name="Test User",
        booking_date=(datetime.now() - timedelta(days=5)).strftime("%Y-%m-%d %H:%M:%S"),
        status="Confirmed"
    ),
]


# ==================== SBT Agent Class ====================

class SBTAgent:
    """SBT Agent for flight operations"""

    def __init__(self):
        self.flights = MOCK_FLIGHTS
        self.bookings = FLIGHT_BOOKINGS

    def execute(self, user_message: str) -> ToolResult:
        """
        Execute SBT Agent based on user message
        
        Determines which tool to call based on message intent and executes it.
        
        Args:
            user_message: User's natural language request
            
        Returns:
            ToolResult from the appropriate tool
        """
        logger.info(f"SBT Agent executing: {user_message}")
        
        message_lower = user_message.lower()
        
        # Determine tool and extract parameters
        if "list" in message_lower and "booking" in message_lower:
            # list_flight_bookings intent
            return self.list_flight_bookings()
            
        elif "book" in message_lower and "flight" in message_lower:
            # book_flight intent
            route = self._extract_route(user_message)
            if not route:
                return self._create_error_result(
                    "book_flight",
                    "Please specify your route (e.g., 'Delhi to Dubai', 'Mumbai to Dubai')."
                )
            
            budget = self._extract_budget(user_message)
            return self.book_flight(
                from_city=route["from"],
                to_city=route["to"],
                budget=budget
            )
            
        else:
            # Default to search_flights intent
            route = self._extract_route(user_message)
            if not route:
                return self._create_error_result(
                    "search_flights",
                    "Please specify your route (e.g., 'Delhi to Dubai', 'Mumbai to Dubai', 'Delhi to Bangalore')."
                )
            
            return self.search_flights(
                from_city=route["from"],
                to_city=route["to"]
            )

    def _extract_route(self, message: str) -> Optional[Dict[str, str]]:
        """Extract route (from and to cities) from user message"""
        import re
        
        message_lower = message.lower()
        
        # Pattern 1: "from X to Y"
        pattern1 = r'\bfrom\s+([a-z\s]+?)\s+to\s+([a-z\s]+?)(?:\s|$|,|\.|for|on|flight)'
        match = re.search(pattern1, message_lower)
        if match:
            from_city = match.group(1).strip()
            to_city = match.group(2).strip()
            if self._normalize_city(from_city) and self._normalize_city(to_city):
                return {"from": from_city, "to": to_city}
        
        # Pattern 2: "X to Y" (most common)
        pattern2 = r'\b([a-z\s]+?)\s+to\s+([a-z\s]+?)(?:\s|$|,|\.|for|on|flight|flights)'
        match = re.search(pattern2, message_lower)
        if match:
            from_city = match.group(1).strip()
            to_city = match.group(2).strip()
            # Remove common words
            from_city = from_city.replace('flight', '').replace('flights', '').strip()
            to_city = to_city.replace('flight', '').replace('flights', '').strip()
            if self._normalize_city(from_city) and self._normalize_city(to_city):
                return {"from": from_city, "to": to_city}
        
        # Pattern 3: Try to extract just city names
        cities = ["delhi", "mumbai", "dubai", "bangalore", "bengaluru", "bombay"]
        found_cities = []
        for city in cities:
            if city in message_lower:
                found_cities.append(city)
        
        if len(found_cities) >= 2:
            # Assume first is from, second is to
            return {"from": found_cities[0], "to": found_cities[1]}
        
        return None

    def _extract_budget(self, message: str) -> Optional[int]:
        """Extract budget from user message"""
        import re
        
        patterns = [
            r'(?:under|below|max|budget|upto|up to)\s*₹?\s*(\d+)',
            r'₹\s*(\d+)',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, message.lower())
            if match:
                return int(match.group(1))
        
        return None

    def _normalize_city(self, city: str) -> Optional[str]:
        """Normalize city name to standard key"""
        city_lower = city.lower().strip()
        if city_lower in CITY_MAPPING:
            return city_lower
        return None

    def _get_route_key(self, from_city: str, to_city: str) -> Optional[tuple]:
        """Get route key for flight lookup"""
        from_normalized = self._normalize_city(from_city)
        to_normalized = self._normalize_city(to_city)
        
        if not from_normalized or not to_normalized:
            return None
        
        return (from_normalized, to_normalized)

    def _generate_booking_id(self) -> str:
        """Generate unique booking ID"""
        return f"FB-{uuid.uuid4().hex[:6].upper()}"

    def _generate_trace_event(
        self,
        event_id: str,
        event_type: str,
        name: str,
        agent: str,
        status: str,
        input_data: Any,
        output_summary: str,
        duration_ms: int = 100
    ) -> Dict[str, Any]:
        """Generate a trace event"""
        return {
            "id": event_id,
            "type": event_type,
            "name": name,
            "agent": agent,
            "status": status,
            "input": input_data,
            "output_summary": output_summary,
            "duration_ms": duration_ms,
            "timestamp": datetime.now().isoformat()
        }

    def _create_error_result(self, action: str, message: str) -> ToolResult:
        """Create error result with trace"""
        trace = [
            self._generate_trace_event(
                event_id="trace-1",
                event_type="orchestrator",
                name="Orchestrator",
                agent="orchestrator",
                status="completed",
                input_data={},
                output_summary="Routed to SBT Agent",
                duration_ms=50
            ),
            self._generate_trace_event(
                event_id="trace-2",
                event_type="agent",
                name="SBT Agent",
                agent="sbt_agent",
                status="failed",
                input_data={},
                output_summary="Missing required information",
                duration_ms=30
            ),
        ]
        return ToolResult(
            action=action,
            message=message,
            data=None,
            trace=trace
        )

    def search_flights(self, from_city: str, to_city: str, date: Optional[str] = None) -> ToolResult:
        """
        Search flights for a route
        
        Args:
            from_city: Origin city name
            to_city: Destination city name
            date: Travel date (optional)
            
        Returns:
            ToolResult with flight list
        """
        logger.info(f"Searching flights from {from_city} to {to_city}")
        
        trace = []
        
        # Trace: Orchestrator
        trace.append(self._generate_trace_event(
            event_id="trace-1",
            event_type="orchestrator",
            name="Orchestrator",
            agent="orchestrator",
            status="completed",
            input_data={"user_message": f"Search flights from {from_city} to {to_city}"},
            output_summary="Routed to SBT Agent",
            duration_ms=50
        ))
        
        # Trace: SBT Agent
        trace.append(self._generate_trace_event(
            event_id="trace-2",
            event_type="agent",
            name="SBT Agent",
            agent="sbt_agent",
            status="processing",
            input_data={"from_city": from_city, "to_city": to_city},
            output_summary="Executing search_flights",
            duration_ms=30
        ))
        
        # Get route key
        route_key = self._get_route_key(from_city, to_city)
        
        if not route_key or route_key not in self.flights:
            # Trace: Tool execution - no results
            trace.append(self._generate_trace_event(
                event_id="trace-3",
                event_type="tool",
                name="search_flights",
                agent="sbt_agent",
                status="completed",
                input_data={"from_city": from_city, "to_city": to_city},
                output_summary="No flights found - route not available",
                duration_ms=20
            ))
            
            # Trace: Result
            trace.append(self._generate_trace_event(
                event_id="trace-4",
                event_type="result",
                name="Result",
                agent="sbt_agent",
                status="completed",
                input_data={},
                output_summary="Route not available",
                duration_ms=10
            ))
            
            return ToolResult(
                action="search_flights",
                message=f"Sorry, no flights available from {from_city.title()} to {to_city.title()}. Try different cities like Delhi, Mumbai, Dubai, or Bangalore.",
                data={"flights": [], "count": 0},
                trace=trace
            )
        
        # Get flights
        flights = self.flights[route_key].copy()
        random.shuffle(flights)
        
        # Get city info
        from_info = CITY_MAPPING[self._normalize_city(from_city)]
        to_info = CITY_MAPPING[self._normalize_city(to_city)]
        
        # Trace: Tool execution - success
        trace.append(self._generate_trace_event(
            event_id="trace-3",
            event_type="tool",
            name="search_flights",
            agent="sbt_agent",
            status="completed",
            input_data={"from_city": from_city, "to_city": to_city, "route_key": route_key},
            output_summary=f"Found {len(flights)} flights",
            duration_ms=80
        ))
        
        # Trace: Result
        trace.append(self._generate_trace_event(
            event_id="trace-4",
            event_type="result",
            name="Result",
            agent="sbt_agent",
            status="completed",
            input_data={},
            output_summary=f"{len(flights)} flights returned",
            duration_ms=10
        ))
        
        return ToolResult(
            action="search_flights",
            message=f"Found {len(flights)} flights from {from_info['name']} ({from_info['code']}) to {to_info['name']} ({to_info['code']}).",
            data={
                "flights": [flight.model_dump() for flight in flights],
                "count": len(flights),
                "from": from_info,
                "to": to_info
            },
            trace=trace
        )

    def book_flight(
        self,
        from_city: str,
        to_city: str,
        budget: Optional[int] = None,
        passenger_name: str = "Test User",
        class_type: str = "Economy"
    ) -> ToolResult:
        """
        Book a flight within budget
        
        Args:
            from_city: Origin city name
            to_city: Destination city name
            budget: Maximum price
            passenger_name: Passenger name
            class_type: Flight class
            
        Returns:
            ToolResult with booking details
        """
        logger.info(f"Booking flight from {from_city} to {to_city} with budget {budget}")
        
        trace = []
        
        # Trace: Orchestrator
        trace.append(self._generate_trace_event(
            event_id="trace-1",
            event_type="orchestrator",
            name="Orchestrator",
            agent="orchestrator",
            status="completed",
            input_data={"user_message": f"Book flight from {from_city} to {to_city}"},
            output_summary="Routed to SBT Agent",
            duration_ms=50
        ))
        
        # Trace: SBT Agent
        trace.append(self._generate_trace_event(
            event_id="trace-2",
            event_type="agent",
            name="SBT Agent",
            agent="sbt_agent",
            status="processing",
            input_data={"from_city": from_city, "to_city": to_city, "budget": budget},
            output_summary="Executing book_flight",
            duration_ms=30
        ))
        
        # Get route key
        route_key = self._get_route_key(from_city, to_city)
        
        if not route_key or route_key not in self.flights:
            trace.append(self._generate_trace_event(
                event_id="trace-3",
                event_type="tool",
                name="book_flight",
                agent="sbt_agent",
                status="completed",
                input_data={"from_city": from_city, "to_city": to_city},
                output_summary="Route not available",
                duration_ms=20
            ))
            
            return ToolResult(
                action="book_flight",
                message=f"Sorry, no flights available from {from_city.title()} to {to_city.title()}.",
                data=None,
                trace=trace
            )
        
        # Get flights
        flights = self.flights[route_key]
        
        # Filter by budget if provided
        if budget:
            available_flights = [f for f in flights if f.price <= budget]
            if not available_flights:
                trace.append(self._generate_trace_event(
                    event_id="trace-3",
                    event_type="tool",
                    name="book_flight",
                    agent="sbt_agent",
                    status="completed",
                    input_data={"budget": budget},
                    output_summary="No flights within budget",
                    duration_ms=50
                ))
                
                return ToolResult(
                    action="book_flight",
                    message=f"No flights found from {from_city.title()} to {to_city.title()} under ₹{budget}. Try increasing your budget.",
                    data=None,
                    trace=trace
                )
        else:
            available_flights = flights
        
        # Sort by price (ascending)
        available_flights = sorted(available_flights, key=lambda f: f.price)
        selected_flight = available_flights[0]
        
        # Create booking
        booking = FlightBooking(
            booking_id=self._generate_booking_id(),
            flight_id=selected_flight.id,
            airline=selected_flight.airline,
            flight_number=selected_flight.flight_number,
            from_city=selected_flight.from_city,
            from_code=selected_flight.from_code,
            to_city=selected_flight.to_city,
            to_code=selected_flight.to_code,
            departure_time=selected_flight.departure_time,
            arrival_time=selected_flight.arrival_time,
            duration=selected_flight.duration,
            price=selected_flight.price,
            currency=selected_flight.currency,
            class_type=selected_flight.class_type,
            passenger_name=passenger_name,
            booking_date=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            status="Confirmed"
        )
        
        # Add to bookings
        self.bookings.insert(0, booking)
        
        # Trace: Tool execution - success
        trace.append(self._generate_trace_event(
            event_id="trace-3",
            event_type="tool",
            name="book_flight",
            agent="sbt_agent",
            status="completed",
            input_data={"from_city": from_city, "to_city": to_city, "budget": budget},
            output_summary=f"Flight booked: {selected_flight.airline} {selected_flight.flight_number}",
            duration_ms=120
        ))
        
        # Trace: Booking created
        trace.append(self._generate_trace_event(
            event_id="trace-4",
            event_type="booking",
            name="Booking Created",
            agent="sbt_agent",
            status="completed",
            input_data={"booking_id": booking.booking_id},
            output_summary=f"Booking {booking.booking_id} confirmed",
            duration_ms=50
        ))
        
        # Trace: Result
        trace.append(self._generate_trace_event(
            event_id="trace-5",
            event_type="result",
            name="Result",
            agent="sbt_agent",
            status="completed",
            input_data={},
            output_summary="Flight booking successful",
            duration_ms=10
        ))
        
        return ToolResult(
            action="book_flight",
            message=f"✓ Flight booked successfully! {selected_flight.airline} {selected_flight.flight_number} from {selected_flight.from_city} to {selected_flight.to_city}.",
            data={
                "booking": booking.model_dump(),
                "flight": selected_flight.model_dump()
            },
            trace=trace
        )

    def list_flight_bookings(self) -> ToolResult:
        """
        List all flight bookings
        
        Returns:
            ToolResult with bookings list
        """
        logger.info("Listing all flight bookings")
        
        trace = []
        
        # Trace: Orchestrator
        trace.append(self._generate_trace_event(
            event_id="trace-1",
            event_type="orchestrator",
            name="Orchestrator",
            agent="orchestrator",
            status="completed",
            input_data={"user_message": "List my flight bookings"},
            output_summary="Routed to SBT Agent",
            duration_ms=50
        ))
        
        # Trace: SBT Agent
        trace.append(self._generate_trace_event(
            event_id="trace-2",
            event_type="agent",
            name="SBT Agent",
            agent="sbt_agent",
            status="processing",
            input_data={},
            output_summary="Executing list_flight_bookings",
            duration_ms=30
        ))
        
        # Trace: Tool execution
        trace.append(self._generate_trace_event(
            event_id="trace-3",
            event_type="tool",
            name="list_flight_bookings",
            agent="sbt_agent",
            status="completed",
            input_data={},
            output_summary=f"Retrieved {len(self.bookings)} bookings",
            duration_ms=40
        ))
        
        # Trace: Result
        trace.append(self._generate_trace_event(
            event_id="trace-4",
            event_type="result",
            name="Result",
            agent="sbt_agent",
            status="completed",
            input_data={},
            output_summary=f"{len(self.bookings)} bookings returned",
            duration_ms=10
        ))
        
        if not self.bookings:
            return ToolResult(
                action="list_flight_bookings",
                message="No flight bookings found.",
                data={"bookings": [], "count": 0},
                trace=trace
            )
        
        return ToolResult(
            action="list_flight_bookings",
            message=f"Found {len(self.bookings)} flight booking(s).",
            data={
                "bookings": [booking.model_dump() for booking in self.bookings],
                "count": len(self.bookings)
            },
            trace=trace
        )
