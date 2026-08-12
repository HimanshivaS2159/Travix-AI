"""
BackOffice Agent Service
Handles hotel-related workflows: list_hotels, book_hotel, list_bookings
"""

import logging
import random
import uuid
from datetime import datetime, timedelta
from typing import Optional, List, Dict, Any
from pydantic import BaseModel

logger = logging.getLogger(__name__)


# ==================== Models ====================

class Hotel(BaseModel):
    """Hotel model"""
    id: str
    name: str
    city: str
    address: str
    rating: float
    price_per_night: int
    currency: str = "INR"
    room_types: List[str]
    amenities: List[str]


class Booking(BaseModel):
    """Hotel booking model"""
    booking_id: str
    hotel_id: str
    hotel_name: str
    city: str
    address: str
    rating: float
    price_per_night: int
    currency: str
    room_type: str
    check_in: str
    check_out: str
    nights: int
    total_price: int
    booked_at: str


class ToolResult(BaseModel):
    """Result from tool execution"""
    action: str
    message: str
    data: Optional[Any] = None
    trace: List[Dict[str, Any]]


# ==================== Mock Hotel Data ====================

MOCK_HOTELS = {
    "delhi": [
        Hotel(
            id="DEL-001",
            name="The Imperial Delhi",
            city="Delhi",
            address="Janpath, Connaught Place, New Delhi",
            rating=4.8,
            price_per_night=8500,
            room_types=["Standard", "Deluxe", "Suite"],
            amenities=["Wi-Fi", "Breakfast", "Pool", "Gym", "Spa"]
        ),
        Hotel(
            id="DEL-002",
            name="Leela Palace New Delhi",
            city="Delhi",
            address="Diplomatic Enclave, Chanakyapuri, New Delhi",
            rating=4.7,
            price_per_night=12000,
            room_types=["Deluxe", "Suite", "Presidential"],
            amenities=["Wi-Fi", "Breakfast", "Pool", "Gym", "Spa", "Restaurant"]
        ),
        Hotel(
            id="DEL-003",
            name="Hotel Godwin Deluxe",
            city="Delhi",
            address="Arakashan Road, Paharganj, New Delhi",
            rating=4.2,
            price_per_night=3500,
            room_types=["Standard", "Deluxe"],
            amenities=["Wi-Fi", "Breakfast", "Restaurant"]
        ),
        Hotel(
            id="DEL-004",
            name="The Oberoi New Delhi",
            city="Delhi",
            address="Dr Zakir Hussain Marg, New Delhi",
            rating=4.9,
            price_per_night=15000,
            room_types=["Deluxe", "Premier", "Suite"],
            amenities=["Wi-Fi", "Breakfast", "Pool", "Gym", "Spa", "Restaurant", "Bar"]
        ),
        Hotel(
            id="DEL-005",
            name="Hotel City Star",
            city="Delhi",
            address="Karol Bagh, New Delhi",
            rating=4.0,
            price_per_night=2800,
            room_types=["Standard", "Deluxe"],
            amenities=["Wi-Fi", "Breakfast"]
        ),
        Hotel(
            id="DEL-006",
            name="ITC Maurya New Delhi",
            city="Delhi",
            address="Sardar Patel Marg, Diplomatic Enclave, New Delhi",
            rating=4.6,
            price_per_night=10000,
            room_types=["Deluxe", "Executive", "Suite"],
            amenities=["Wi-Fi", "Breakfast", "Pool", "Gym", "Spa", "Restaurant"]
        ),
    ],
    "mumbai": [
        Hotel(
            id="MUM-001",
            name="The Taj Mahal Palace",
            city="Mumbai",
            address="Apollo Bunder, Colaba, Mumbai",
            rating=4.9,
            price_per_night=18000,
            room_types=["Deluxe", "Premium", "Suite"],
            amenities=["Wi-Fi", "Breakfast", "Pool", "Gym", "Spa", "Restaurant", "Bar"]
        ),
        Hotel(
            id="MUM-002",
            name="Hotel Suba Palace",
            city="Mumbai",
            address="Colaba Causeway, Mumbai",
            rating=4.1,
            price_per_night=4500,
            room_types=["Standard", "Deluxe"],
            amenities=["Wi-Fi", "Breakfast", "Restaurant"]
        ),
        Hotel(
            id="MUM-003",
            name="The Oberoi Mumbai",
            city="Mumbai",
            address="Nariman Point, Mumbai",
            rating=4.8,
            price_per_night=16000,
            room_types=["Deluxe", "Premier", "Suite"],
            amenities=["Wi-Fi", "Breakfast", "Pool", "Gym", "Spa", "Restaurant"]
        ),
    ],
    "bangalore": [
        Hotel(
            id="BLR-001",
            name="The Leela Palace Bengaluru",
            city="Bangalore",
            address="23 HAL Old Airport Road, Bangalore",
            rating=4.7,
            price_per_night=11000,
            room_types=["Deluxe", "Grand", "Royal Suite"],
            amenities=["Wi-Fi", "Breakfast", "Pool", "Gym", "Spa", "Restaurant"]
        ),
        Hotel(
            id="BLR-002",
            name="Hotel Empire International",
            city="Bangalore",
            address="Cunningham Road, Bangalore",
            rating=4.0,
            price_per_night=3200,
            room_types=["Standard", "Deluxe"],
            amenities=["Wi-Fi", "Breakfast"]
        ),
        Hotel(
            id="BLR-003",
            name="The Oberoi Bengaluru",
            city="Bangalore",
            address="MG Road, Bangalore",
            rating=4.8,
            price_per_night=13000,
            room_types=["Deluxe", "Premier", "Luxury Suite"],
            amenities=["Wi-Fi", "Breakfast", "Pool", "Gym", "Spa", "Restaurant", "Bar"]
        ),
    ],
    "goa": [
        Hotel(
            id="GOA-001",
            name="Taj Exotica Resort & Spa",
            city="Goa",
            address="Calwaddo, Benaulim, South Goa",
            rating=4.6,
            price_per_night=9500,
            room_types=["Deluxe", "Premium", "Villa"],
            amenities=["Wi-Fi", "Breakfast", "Pool", "Gym", "Spa", "Beach Access", "Restaurant"]
        ),
        Hotel(
            id="GOA-002",
            name="Hotel Fidalgo",
            city="Goa",
            address="18th June Road, Panjim, North Goa",
            rating=4.2,
            price_per_night=4000,
            room_types=["Standard", "Deluxe"],
            amenities=["Wi-Fi", "Breakfast", "Pool", "Restaurant"]
        ),
        Hotel(
            id="GOA-003",
            name="Park Hyatt Goa Resort and Spa",
            city="Goa",
            address="Arossim Beach, South Goa",
            rating=4.7,
            price_per_night=12000,
            room_types=["Deluxe", "Pool Villa", "Suite"],
            amenities=["Wi-Fi", "Breakfast", "Pool", "Gym", "Spa", "Beach Access", "Restaurant", "Bar"]
        ),
    ],
}

# City aliases for normalization
CITY_ALIASES = {
    "delhi": ["delhi", "new delhi", "newdelhi"],
    "mumbai": ["mumbai", "bombay"],
    "bangalore": ["bangalore", "bengaluru", "blr"],
    "goa": ["goa"],
}


# ==================== In-Memory Booking Storage ====================

# Pre-populate with demo bookings
BOOKINGS: List[Booking] = [
    Booking(
        booking_id="BK-A1B2C3",
        hotel_id="MUM-002",
        hotel_name="Hotel Suba Palace",
        city="Mumbai",
        address="Colaba Causeway, Mumbai",
        rating=4.1,
        price_per_night=4500,
        currency="INR",
        room_type="Deluxe",
        check_in=(datetime.now() - timedelta(days=5)).strftime("%Y-%m-%d"),
        check_out=(datetime.now() - timedelta(days=3)).strftime("%Y-%m-%d"),
        nights=2,
        total_price=9000,
        booked_at=(datetime.now() - timedelta(days=10)).strftime("%Y-%m-%d %H:%M:%S")
    ),
    Booking(
        booking_id="BK-D4E5F6",
        hotel_id="GOA-002",
        hotel_name="Hotel Fidalgo",
        city="Goa",
        address="18th June Road, Panjim, North Goa",
        rating=4.2,
        price_per_night=4000,
        currency="INR",
        room_type="Standard",
        check_in=(datetime.now() + timedelta(days=15)).strftime("%Y-%m-%d"),
        check_out=(datetime.now() + timedelta(days=18)).strftime("%Y-%m-%d"),
        nights=3,
        total_price=12000,
        booked_at=(datetime.now() - timedelta(days=2)).strftime("%Y-%m-%d %H:%M:%S")
    ),
]


# ==================== BackOffice Agent Class ====================

class BackOfficeAgent:
    """BackOffice Agent for hotel operations"""

    def __init__(self):
        self.hotels = MOCK_HOTELS
        self.bookings = BOOKINGS

    def execute(self, user_message: str) -> ToolResult:
        """
        Execute BackOffice Agent based on user message
        
        Determines which tool to call based on message intent and executes it.
        
        Args:
            user_message: User's natural language request
            
        Returns:
            ToolResult from the appropriate tool
        """
        logger.info(f"BackOffice Agent executing: {user_message}")
        
        message_lower = user_message.lower()
        
        # Determine tool and extract parameters
        if "list" in message_lower and "booking" in message_lower:
            # list_bookings intent
            return self.list_bookings()
            
        elif "book" in message_lower:
            # book_hotel intent
            # Extract city
            city_match = self._extract_city(user_message)
            if not city_match:
                # Return error result with trace
                trace = [
                    self._generate_trace_event(
                        event_id="trace-1",
                        event_type="orchestrator",
                        name="Orchestrator",
                        agent="orchestrator",
                        status="completed",
                        input_data={"user_message": user_message},
                        output_summary="Routed to BackOffice Agent",
                        duration_ms=50
                    ),
                    self._generate_trace_event(
                        event_id="trace-2",
                        event_type="agent",
                        name="BackOffice Agent",
                        agent="backoffice_agent",
                        status="failed",
                        input_data={"user_message": user_message},
                        output_summary="Could not determine city",
                        duration_ms=30
                    ),
                    self._generate_trace_event(
                        event_id="trace-3",
                        event_type="result",
                        name="Result",
                        agent="backoffice_agent",
                        status="completed",
                        input_data={},
                        output_summary="Missing city information",
                        duration_ms=10
                    )
                ]
                return ToolResult(
                    action="book_hotel",
                    message="Please specify which city you'd like to book a hotel in (e.g., Delhi, Mumbai, Bangalore, Goa).",
                    data=None,
                    trace=trace
                )
            
            # Extract budget
            budget_info = self._extract_budget(user_message)
            
            return self.book_hotel(
                city=city_match,
                budget_info=budget_info
            )
            
        else:
            # Default to list_hotels intent
            city_match = self._extract_city(user_message)
            if not city_match:
                # Return error result with trace
                trace = [
                    self._generate_trace_event(
                        event_id="trace-1",
                        event_type="orchestrator",
                        name="Orchestrator",
                        agent="orchestrator",
                        status="completed",
                        input_data={"user_message": user_message},
                        output_summary="Routed to BackOffice Agent",
                        duration_ms=50
                    ),
                    self._generate_trace_event(
                        event_id="trace-2",
                        event_type="agent",
                        name="BackOffice Agent",
                        agent="backoffice_agent",
                        status="failed",
                        input_data={"user_message": user_message},
                        output_summary="Could not determine city",
                        duration_ms=30
                    ),
                    self._generate_trace_event(
                        event_id="trace-3",
                        event_type="result",
                        name="Result",
                        agent="backoffice_agent",
                        status="completed",
                        input_data={},
                        output_summary="Missing city information",
                        duration_ms=10
                    )
                ]
                return ToolResult(
                    action="list_hotels",
                    message="Please specify which city you'd like to see hotels in (e.g., Delhi, Mumbai, Bangalore, Goa).",
                    data=[],
                    trace=trace
                )
            
            return self.list_hotels(city=city_match)

    def _extract_city(self, message: str) -> Optional[str]:
        """Extract city name from user message"""
        message_lower = message.lower()
        
        # Check for explicit patterns
        import re
        patterns = [
            r'\b(?:in|at|to|for|near)\s+([a-z]+)\b',
            r'\b(delhi|mumbai|bangalore|bengaluru|goa)\b'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, message_lower)
            if match:
                city = match.group(1) if match.lastindex else match.group(0)
                # Validate it's a known city
                normalized = self._normalize_city(city)
                if normalized:
                    return city
        
        # Fallback: check if message ends with a city name
        words = message.split()
        if words:
            last_word = words[-1].lower().strip('.,!?')
            normalized = self._normalize_city(last_word)
            if normalized:
                return last_word
        
        return None

    def _extract_budget(self, message: str) -> Optional[dict]:
        """
        Extract budget from user message
        
        Returns dict with:
        - 'amount': int - the budget amount
        - 'type': 'total' or 'nightly' - budget interpretation
        """
        import re
        
        # Check for explicit "per night" patterns
        nightly_patterns = [
            r'(?:under|below|max|budget|upto|up to)\s*₹?\s*(\d+)\s*(?:per night|/night|a night|each night)',
            r'₹\s*(\d+)\s*(?:per night|/night|a night|each night)',
        ]
        
        for pattern in nightly_patterns:
            match = re.search(pattern, message.lower())
            if match:
                return {
                    'amount': int(match.group(1)),
                    'type': 'nightly'
                }
        
        # Default: interpret as total budget
        total_patterns = [
            r'(?:under|below|max|budget|upto|up to)\s*₹?\s*(\d+)',
            r'₹\s*(\d+)',
        ]
        
        for pattern in total_patterns:
            match = re.search(pattern, message.lower())
            if match:
                return {
                    'amount': int(match.group(1)),
                    'type': 'total'
                }
        
        return None

    def _normalize_city(self, city: str) -> Optional[str]:
        """Normalize city name to standard key"""
        city_lower = city.lower().strip()
        for standard_name, aliases in CITY_ALIASES.items():
            if city_lower in aliases:
                return standard_name
        return None

    def _generate_booking_id(self) -> str:
        """Generate unique booking ID"""
        return f"BK-{uuid.uuid4().hex[:6].upper()}"

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

    def list_hotels(self, city: str) -> ToolResult:
        """
        List hotels in a requested city
        
        Args:
            city: City name to search hotels
            
        Returns:
            ToolResult with hotel list
        """
        logger.info(f"Listing hotels in {city}")
        
        trace = []
        
        # Trace: Orchestrator
        trace.append(self._generate_trace_event(
            event_id="trace-1",
            event_type="orchestrator",
            name="Orchestrator",
            agent="orchestrator",
            status="completed",
            input_data={"user_message": f"Show me hotels in {city}"},
            output_summary="Routed to BackOffice Agent",
            duration_ms=50
        ))
        
        # Trace: BackOffice Agent
        trace.append(self._generate_trace_event(
            event_id="trace-2",
            event_type="agent",
            name="BackOffice Agent",
            agent="backoffice_agent",
            status="processing",
            input_data={"city": city},
            output_summary="Executing list_hotels",
            duration_ms=30
        ))
        
        # Normalize city
        normalized_city = self._normalize_city(city)
        
        if not normalized_city or normalized_city not in self.hotels:
            # Trace: Tool execution - no results
            trace.append(self._generate_trace_event(
                event_id="trace-3",
                event_type="tool",
                name="list_hotels",
                agent="backoffice_agent",
                status="completed",
                input_data={"city": city},
                output_summary="No hotels found - unsupported city",
                duration_ms=20
            ))
            
            # Trace: Result
            trace.append(self._generate_trace_event(
                event_id="trace-4",
                event_type="result",
                name="Result",
                agent="backoffice_agent",
                status="completed",
                input_data={},
                output_summary="City not supported",
                duration_ms=10
            ))
            
            return ToolResult(
                action="list_hotels",
                message=f"Sorry, we don't have hotel data for {city}. Supported cities are: Delhi, Mumbai, Bangalore, and Goa.",
                data=[],
                trace=trace
            )
        
        # Get hotels and randomize order
        hotels = self.hotels[normalized_city].copy()
        random.shuffle(hotels)
        
        # Trace: Tool execution - success
        trace.append(self._generate_trace_event(
            event_id="trace-3",
            event_type="tool",
            name="list_hotels",
            agent="backoffice_agent",
            status="completed",
            input_data={"city": city, "normalized_city": normalized_city},
            output_summary=f"Found {len(hotels)} hotels",
            duration_ms=80
        ))
        
        # Trace: Result
        trace.append(self._generate_trace_event(
            event_id="trace-4",
            event_type="result",
            name="Result",
            agent="backoffice_agent",
            status="completed",
            input_data={},
            output_summary=f"{len(hotels)} hotels returned",
            duration_ms=10
        ))
        
        return ToolResult(
            action="list_hotels",
            message=f"Found {len(hotels)} hotels in {city.title()}.",
            data=[hotel.model_dump() for hotel in hotels],
            trace=trace
        )

    def book_hotel(
        self,
        city: str,
        budget_info: Optional[dict] = None,
        room_type: Optional[str] = None,
        check_in: Optional[str] = None,
        check_out: Optional[str] = None
    ) -> ToolResult:
        """
        Book a hotel within budget
        
        Args:
            city: City name
            budget_info: Dict with 'amount' and 'type' ('total' or 'nightly')
            room_type: Preferred room type
            check_in: Check-in date (YYYY-MM-DD)
            check_out: Check-out date (YYYY-MM-DD)
            
        Returns:
            ToolResult with booking details
        """
        logger.info(f"Booking hotel in {city} with budget_info {budget_info}")
        
        trace = []
        
        # Trace: Orchestrator
        trace.append(self._generate_trace_event(
            event_id="trace-1",
            event_type="orchestrator",
            name="Orchestrator",
            agent="orchestrator",
            status="completed",
            input_data={"user_message": f"Book a hotel in {city}"},
            output_summary="Routed to BackOffice Agent",
            duration_ms=50
        ))
        
        # Trace: BackOffice Agent
        trace.append(self._generate_trace_event(
            event_id="trace-2",
            event_type="agent",
            name="BackOffice Agent",
            agent="backoffice_agent",
            status="processing",
            input_data={"city": city, "budget_info": budget_info},
            output_summary="Executing book_hotel",
            duration_ms=30
        ))
        
        # Check budget provided
        if budget_info is None:
            trace.append(self._generate_trace_event(
                event_id="trace-3",
                event_type="tool",
                name="book_hotel",
                agent="backoffice_agent",
                status="failed",
                input_data={"city": city, "budget": None},
                output_summary="Budget not provided",
                duration_ms=10
            ))
            
            trace.append(self._generate_trace_event(
                event_id="trace-4",
                event_type="result",
                name="Result",
                agent="backoffice_agent",
                status="completed",
                input_data={},
                output_summary="Asked for budget",
                duration_ms=10
            ))
            
            return ToolResult(
                action="book_hotel",
                message="Please specify your budget per night (e.g., 'under ₹4000').",
                data=None,
                trace=trace
            )
        
        # Normalize city
        normalized_city = self._normalize_city(city)
        
        if not normalized_city or normalized_city not in self.hotels:
            trace.append(self._generate_trace_event(
                event_id="trace-3",
                event_type="tool",
                name="book_hotel",
                agent="backoffice_agent",
                status="completed",
                input_data={"city": city},
                output_summary="City not supported",
                duration_ms=20
            ))
            
            trace.append(self._generate_trace_event(
                event_id="trace-4",
                event_type="result",
                name="Result",
                agent="backoffice_agent",
                status="completed",
                input_data={},
                output_summary="City not supported",
                duration_ms=10
            ))
            
            return ToolResult(
                action="book_hotel",
                message=f"Sorry, we don't have hotels in {city}. Supported cities are: Delhi, Mumbai, Bangalore, and Goa.",
                data=None,
                trace=trace
            )
        
        # Determine dates and calculate nights
        if not check_in:
            check_in = (datetime.now() + timedelta(days=7)).strftime("%Y-%m-%d")
        if not check_out:
            check_out = (datetime.now() + timedelta(days=10)).strftime("%Y-%m-%d")
        
        # Calculate nights
        try:
            check_in_date = datetime.strptime(check_in, "%Y-%m-%d")
            check_out_date = datetime.strptime(check_out, "%Y-%m-%d")
            nights = (check_out_date - check_in_date).days
            if nights <= 0:
                nights = 3
        except:
            nights = 3
        
        # Extract budget amount and type
        budget_amount = budget_info['amount']
        budget_type = budget_info['type']
        
        # Filter hotels based on budget type
        hotels = self.hotels[normalized_city]
        
        if budget_type == 'nightly':
            # Budget is per night - filter by nightly price
            available_hotels = [h for h in hotels if h.price_per_night <= budget_amount]
            budget_description = f"₹{budget_amount} per night"
        else:
            # Budget is total - filter by total price
            max_nightly_price = budget_amount / nights
            available_hotels = [h for h in hotels if h.price_per_night <= max_nightly_price]
            budget_description = f"₹{budget_amount} total for {nights} nights"
        
        if not available_hotels:
            trace.append(self._generate_trace_event(
                event_id="trace-3",
                event_type="tool",
                name="book_hotel",
                agent="backoffice_agent",
                status="completed",
                input_data={"city": city, "budget_info": budget_info, "nights": nights},
                output_summary="No hotels within budget",
                duration_ms=50
            ))
            
            trace.append(self._generate_trace_event(
                event_id="trace-4",
                event_type="result",
                name="Result",
                agent="backoffice_agent",
                status="completed",
                input_data={},
                output_summary="Budget too low",
                duration_ms=10
            ))
            
            if budget_type == 'nightly':
                message = f"No hotels found in {city.title()} under ₹{budget_amount} per night. Try increasing your budget."
            else:
                message = f"I couldn't find a hotel in {city.title()} within your total budget of ₹{budget_amount} for {nights} nights. The cheapest option would cost more. Try increasing your budget."
            
            return ToolResult(
                action="book_hotel",
                message=message,
                data=None,
                trace=trace
            )
        
        # Sort by rating (desc), then by price (asc)
        available_hotels.sort(key=lambda h: (-h.rating, h.price_per_night))
        selected_hotel = available_hotels[0]
        
        # Determine room type
        final_room_type = room_type if room_type in selected_hotel.room_types else selected_hotel.room_types[0]
        
        # Calculate total price
        total_price = selected_hotel.price_per_night * nights
        
        # Create booking
        booking = Booking(
            booking_id=self._generate_booking_id(),
            hotel_id=selected_hotel.id,
            hotel_name=selected_hotel.name,
            city=selected_hotel.city,
            address=selected_hotel.address,
            rating=selected_hotel.rating,
            price_per_night=selected_hotel.price_per_night,
            currency=selected_hotel.currency,
            room_type=final_room_type,
            check_in=check_in,
            check_out=check_out,
            nights=nights,
            total_price=total_price,
            booked_at=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        )
        
        # Add to bookings
        self.bookings.insert(0, booking)
        
        # Trace: Tool execution - success
        trace.append(self._generate_trace_event(
            event_id="trace-3",
            event_type="tool",
            name="book_hotel",
            agent="backoffice_agent",
            status="completed",
            input_data={"city": city, "budget_info": budget_info, "nights": nights},
            output_summary=f"Hotel booked: {selected_hotel.name}",
            duration_ms=120
        ))
        
        # Trace: Booking created
        trace.append(self._generate_trace_event(
            event_id="trace-4",
            event_type="booking",
            name="Booking Created",
            agent="backoffice_agent",
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
            agent="backoffice_agent",
            status="completed",
            input_data={},
            output_summary="Booking successful",
            duration_ms=10
        ))
        
        return ToolResult(
            action="book_hotel",
            message=f"Hotel booked successfully! Booking ID: {booking.booking_id}",
            data=booking.model_dump(),
            trace=trace
        )

    def list_bookings(self) -> ToolResult:
        """
        List all bookings
        
        Returns:
            ToolResult with booking list
        """
        logger.info("Listing all bookings")
        
        trace = []
        
        # Trace: Orchestrator
        trace.append(self._generate_trace_event(
            event_id="trace-1",
            event_type="orchestrator",
            name="Orchestrator",
            agent="orchestrator",
            status="completed",
            input_data={"user_message": "Show my hotel bookings"},
            output_summary="Routed to BackOffice Agent",
            duration_ms=50
        ))
        
        # Trace: BackOffice Agent
        trace.append(self._generate_trace_event(
            event_id="trace-2",
            event_type="agent",
            name="BackOffice Agent",
            agent="backoffice_agent",
            status="processing",
            input_data={},
            output_summary="Executing list_bookings",
            duration_ms=30
        ))
        
        # Trace: Tool execution
        trace.append(self._generate_trace_event(
            event_id="trace-3",
            event_type="tool",
            name="list_bookings",
            agent="backoffice_agent",
            status="completed",
            input_data={},
            output_summary=f"Retrieved {len(self.bookings)} bookings",
            duration_ms=60
        ))
        
        # Trace: Result
        trace.append(self._generate_trace_event(
            event_id="trace-4",
            event_type="result",
            name="Result",
            agent="backoffice_agent",
            status="completed",
            input_data={},
            output_summary=f"{len(self.bookings)} bookings returned",
            duration_ms=10
        ))
        
        # Bookings are already sorted newest first (inserted at index 0)
        return ToolResult(
            action="list_bookings",
            message=f"Found {len(self.bookings)} booking(s).",
            data=[booking.model_dump() for booking in self.bookings],
            trace=trace
        )
