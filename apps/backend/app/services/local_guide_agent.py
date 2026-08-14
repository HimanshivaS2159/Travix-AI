"""
Local Guide Agent Service
Provides local recommendations, attractions, food spots, and travel tips
"""

import logging
from typing import List, Dict, Any, Optional
from datetime import datetime
from pydantic import BaseModel

logger = logging.getLogger(__name__)


# ==================== Models ====================

class Attraction(BaseModel):
    """Tourist attraction model"""
    id: str
    name: str
    category: str
    description: str
    location: str
    rating: float
    visit_duration: str
    entry_fee: str
    best_time: str
    tips: List[str]


class Restaurant(BaseModel):
    """Restaurant/food spot model"""
    id: str
    name: str
    cuisine: str
    specialty: str
    location: str
    rating: float
    price_range: str
    must_try: List[str]


class LocalTip(BaseModel):
    """Local travel tip"""
    category: str
    tip: str
    importance: str  # high, medium, low


class ToolResult(BaseModel):
    """Tool result wrapper"""
    action: str
    message: str
    data: Any
    trace: List[Dict]


# ==================== Mock Local Data ====================

LOCAL_ATTRACTIONS = {
    "delhi": [
        Attraction(
            id="DEL-ATT-001",
            name="Red Fort (Lal Qila)",
            category="Historical Monument",
            description="Magnificent 17th-century fort, UNESCO World Heritage Site",
            location="Chandni Chowk, Old Delhi",
            rating=4.6,
            visit_duration="2-3 hours",
            entry_fee="₹50 (Indians), ₹600 (Foreigners)",
            best_time="Early morning (9-11 AM) to avoid crowds",
            tips=[
                "Visit on weekdays to avoid weekend rush",
                "Light and sound show in evening (tickets separate)",
                "Wear comfortable shoes for walking"
            ]
        ),
        Attraction(
            id="DEL-ATT-002",
            name="Qutub Minar",
            category="Historical Monument",
            description="73m tall minaret, UNESCO World Heritage Site",
            location="Mehrauli, South Delhi",
            rating=4.5,
            visit_duration="1-2 hours",
            entry_fee="₹40 (Indians), ₹600 (Foreigners)",
            best_time="Morning or late afternoon",
            tips=[
                "Great for photography enthusiasts",
                "Explore Iron Pillar and other ruins",
                "Avoid midday in summer (very hot)"
            ]
        ),
        Attraction(
            id="DEL-ATT-003",
            name="India Gate",
            category="Memorial",
            description="War memorial dedicated to Indian soldiers",
            location="Rajpath, Central Delhi",
            rating=4.7,
            visit_duration="1 hour",
            entry_fee="Free",
            best_time="Evening (5-8 PM) or early morning",
            tips=[
                "Perfect for evening walk and picnic",
                "Beautifully lit at night",
                "Street food vendors nearby"
            ]
        ),
        Attraction(
            id="DEL-ATT-004",
            name="Lotus Temple",
            category="Religious Site",
            description="Bahá'í House of Worship, stunning lotus-shaped architecture",
            location="Kalkaji, South Delhi",
            rating=4.8,
            visit_duration="1-1.5 hours",
            entry_fee="Free",
            best_time="Morning (9-11 AM) for meditation",
            tips=[
                "Maintain silence inside",
                "No photography inside temple",
                "Remove shoes before entering"
            ]
        ),
        Attraction(
            id="DEL-ATT-005",
            name="Humayun's Tomb",
            category="Historical Monument",
            description="Mughal Emperor's tomb, UNESCO World Heritage Site",
            location="Nizamuddin, South Delhi",
            rating=4.6,
            visit_duration="2 hours",
            entry_fee="₹40 (Indians), ₹600 (Foreigners)",
            best_time="Early morning or late afternoon",
            tips=[
                "Beautiful gardens for photography",
                "Less crowded than other monuments",
                "Combine with nearby Hazrat Nizamuddin Dargah"
            ]
        ),
    ],
    "mumbai": [
        Attraction(
            id="MUM-ATT-001",
            name="Gateway of India",
            category="Monument",
            description="Iconic arch monument overlooking Arabian Sea",
            location="Apollo Bunder, Colaba",
            rating=4.5,
            visit_duration="1 hour",
            entry_fee="Free",
            best_time="Early morning or sunset",
            tips=[
                "Take ferry to Elephanta Caves from here",
                "Street photographers available",
                "Avoid monsoon season for photos"
            ]
        ),
        Attraction(
            id="MUM-ATT-002",
            name="Marine Drive",
            category="Seafront Promenade",
            description="6 km long boulevard, Queen's Necklace at night",
            location="South Mumbai",
            rating=4.7,
            visit_duration="1-2 hours",
            entry_fee="Free",
            best_time="Sunset or evening",
            tips=[
                "Perfect for evening walks",
                "Try street food at Chowpatty",
                "Beautiful at night with lights"
            ]
        ),
        Attraction(
            id="MUM-ATT-003",
            name="Elephanta Caves",
            category="Historical Site",
            description="Ancient cave temples, UNESCO World Heritage Site",
            location="Elephanta Island",
            rating=4.4,
            visit_duration="3-4 hours (including ferry)",
            entry_fee="₹40 + ferry ₹200",
            best_time="October to March",
            tips=[
                "Take morning ferry from Gateway",
                "Steep climb with 120 steps",
                "Avoid during monsoon"
            ]
        ),
    ],
    "dubai": [
        Attraction(
            id="DXB-ATT-001",
            name="Burj Khalifa",
            category="Skyscraper",
            description="World's tallest building with observation decks",
            location="Downtown Dubai",
            rating=4.8,
            visit_duration="2-3 hours",
            entry_fee="AED 149+ (varies by level)",
            best_time="Sunset time (book in advance)",
            tips=[
                "Book tickets online in advance",
                "Sunset slots most expensive",
                "Visit Dubai Mall afterward"
            ]
        ),
        Attraction(
            id="DXB-ATT-002",
            name="Dubai Mall",
            category="Shopping",
            description="World's largest shopping mall",
            location="Downtown Dubai",
            rating=4.7,
            visit_duration="3-5 hours",
            entry_fee="Free (attractions separate)",
            best_time="Weekday evenings",
            tips=[
                "See Dubai Fountain show (free)",
                "Visit Dubai Aquarium inside",
                "Many dining options available"
            ]
        ),
    ],
    "bangalore": [
        Attraction(
            id="BLR-ATT-001",
            name="Lalbagh Botanical Garden",
            category="Garden",
            description="240-acre garden with glass house and rare plants",
            location="South Bangalore",
            rating=4.6,
            visit_duration="2-3 hours",
            entry_fee="₹20",
            best_time="Early morning (6-9 AM)",
            tips=[
                "Perfect for morning walk",
                "Flower shows twice a year",
                "Great for photography"
            ]
        ),
        Attraction(
            id="BLR-ATT-002",
            name="Bangalore Palace",
            category="Historical Palace",
            description="Tudor-style palace with beautiful architecture",
            location="Vasanth Nagar",
            rating=4.5,
            visit_duration="1-2 hours",
            entry_fee="₹280",
            best_time="Morning or afternoon",
            tips=[
                "Audio guide available",
                "Beautiful grounds for photos",
                "Allow photography inside"
            ]
        ),
    ],
}

LOCAL_RESTAURANTS = {
    "delhi": [
        Restaurant(
            id="DEL-RES-001",
            name="Karim's",
            cuisine="Mughlai",
            specialty="Authentic Mughlai cuisine since 1913",
            location="Jama Masjid, Old Delhi",
            rating=4.4,
            price_range="₹₹ (₹300-600 per person)",
            must_try=["Mutton Korma", "Chicken Jahangiri", "Sheermal", "Phirni"]
        ),
        Restaurant(
            id="DEL-RES-002",
            name="Paranthe Wali Gali",
            cuisine="North Indian",
            specialty="Famous street with multiple paratha shops",
            location="Chandni Chowk",
            rating=4.3,
            price_range="₹ (₹100-200 per person)",
            must_try=["Stuffed Parathas", "Rabri", "Lassi"]
        ),
        Restaurant(
            id="DEL-RES-003",
            name="Indian Accent",
            cuisine="Modern Indian",
            specialty="Fine dining with innovative Indian flavors",
            location="The Lodhi Hotel",
            rating=4.7,
            price_range="₹₹₹₹ (₹4000+ per person)",
            must_try=["Meetha Achaar Pork Ribs", "Blue Cheese Naan", "Mishti Doi"]
        ),
        Restaurant(
            id="DEL-RES-004",
            name="Saravana Bhavan",
            cuisine="South Indian",
            specialty="Authentic vegetarian South Indian food",
            location="Connaught Place (multiple locations)",
            rating=4.3,
            price_range="₹ (₹200-400 per person)",
            must_try=["Masala Dosa", "Filter Coffee", "Idli Sambar", "Rava Masala Dosa"]
        ),
    ],
    "mumbai": [
        Restaurant(
            id="MUM-RES-001",
            name="Britannia & Co.",
            cuisine="Parsi",
            specialty="Iconic Parsi restaurant since 1923",
            location="Ballard Estate",
            rating=4.5,
            price_range="₹₹ (₹400-700 per person)",
            must_try=["Berry Pulao", "Sali Boti", "Caramel Custard"]
        ),
        Restaurant(
            id="MUM-RES-002",
            name="Leopold Cafe",
            cuisine="Continental",
            specialty="Historic cafe, popular with tourists",
            location="Colaba",
            rating=4.2,
            price_range="₹₹ (₹500-800 per person)",
            must_try=["Breakfast Platters", "Beer", "Continental dishes"]
        ),
        Restaurant(
            id="MUM-RES-003",
            name="Trishna",
            cuisine="Seafood",
            specialty="Famous for butter garlic crab",
            location="Kala Ghoda",
            rating=4.6,
            price_range="₹₹₹ (₹1500-2500 per person)",
            must_try=["Butter Garlic Crab", "Prawns Koliwada", "Bombil Fry"]
        ),
    ],
    "dubai": [
        Restaurant(
            id="DXB-RES-001",
            name="Al Fanar Restaurant",
            cuisine="Emirati",
            specialty="Traditional Emirati cuisine",
            location="Dubai Festival City Mall",
            rating=4.5,
            price_range="AED 80-150 per person",
            must_try=["Machboos", "Harees", "Luqaimat", "Karak Tea"]
        ),
        Restaurant(
            id="DXB-RES-002",
            name="Ravi Restaurant",
            cuisine="Pakistani",
            specialty="Budget-friendly authentic Pakistani food",
            location="Satwa",
            rating=4.4,
            price_range="AED 20-40 per person",
            must_try=["Chicken Tikka", "Biryani", "Naan", "Lassi"]
        ),
    ],
    "bangalore": [
        Restaurant(
            id="BLR-RES-001",
            name="MTR (Mavalli Tiffin Room)",
            cuisine="South Indian",
            specialty="Iconic restaurant since 1924",
            location="Lalbagh Road",
            rating=4.4,
            price_range="₹₹ (₹250-500 per person)",
            must_try=["Rava Idli", "Masala Dosa", "Filter Coffee", "Khara Bath"]
        ),
        Restaurant(
            id="BLR-RES-002",
            name="Vidyarthi Bhavan",
            cuisine="South Indian",
            specialty="Famous for crispy dosas",
            location="Gandhi Bazaar",
            rating=4.3,
            price_range="₹ (₹100-250 per person)",
            must_try=["Set Dosa", "Masala Dosa", "Coffee"]
        ),
    ],
}

LOCAL_TIPS = {
    "delhi": [
        LocalTip(category="Transportation", tip="Use Delhi Metro - it's clean, safe, and efficient", importance="high"),
        LocalTip(category="Safety", tip="Avoid isolated areas after 10 PM, especially for solo travelers", importance="high"),
        LocalTip(category="Weather", tip="October to March is best time. Avoid May-July (very hot)", importance="high"),
        LocalTip(category="Food", tip="Try street food but from busy, popular stalls", importance="medium"),
        LocalTip(category="Shopping", tip="Bargain at markets like Sarojini, Janpath. Fixed prices at malls", importance="medium"),
        LocalTip(category="Culture", tip="Dress modestly when visiting religious sites", importance="medium"),
        LocalTip(category="Money", tip="Keep cash for small vendors. Most places accept UPI/cards", importance="low"),
    ],
    "mumbai": [
        LocalTip(category="Transportation", tip="Local trains are fastest but crowded during peak hours", importance="high"),
        LocalTip(category="Safety", tip="Mumbai is generally safe, but avoid deserted areas at night", importance="high"),
        LocalTip(category="Weather", tip="Avoid monsoon (June-September) for sightseeing", importance="high"),
        LocalTip(category="Food", tip="Must try vada pav, pav bhaji from street vendors", importance="medium"),
        LocalTip(category="Culture", tip="South Mumbai for heritage, Bandra for modern vibe", importance="medium"),
    ],
    "dubai": [
        LocalTip(category="Culture", tip="Respect local customs. Dress modestly in public places", importance="high"),
        LocalTip(category="Weather", tip="November to March is best. Summer is extremely hot", importance="high"),
        LocalTip(category="Transportation", tip="Dubai Metro is efficient and connects major areas", importance="high"),
        LocalTip(category="Money", tip="Carry some cash. Most places accept cards but not everywhere", importance="medium"),
        LocalTip(category="Shopping", tip="Haggle at souks but not in malls", importance="medium"),
    ],
    "bangalore": [
        LocalTip(category="Transportation", tip="Traffic is heavy. Use Metro or Uber/Ola during peak hours", importance="high"),
        LocalTip(category="Weather", tip="Pleasant year-round. Mild winters, no extreme heat", importance="medium"),
        LocalTip(category="Food", tip="Try authentic South Indian breakfast at local restaurants", importance="medium"),
        LocalTip(category="Culture", tip="Known as Silicon Valley of India - tech hub", importance="low"),
    ],
}

HIDDEN_GEMS = {
    "delhi": [
        "Hauz Khas Village - Bohemian cafes and art galleries",
        "Lodhi Art District - Open-air street art gallery",
        "Dilli Haat - Affordable handicrafts from all over India",
        "Majnu Ka Tilla - Little Tibet with authentic Tibetan food",
        "Agrasen Ki Baoli - Ancient stepwell, great for photos",
    ],
    "mumbai": [
        "Bandra Fort - Sunset views, less crowded",
        "Sassoon Docks - Mumbai's largest fish market (morning)",
        "Chor Bazaar - Antique market, bargain paradise",
        "Khotachiwadi - Portuguese heritage village",
        "Mahim Beach - Local vibe, evening street food",
    ],
    "dubai": [
        "Al Fahidi Historical District - Old Dubai charm",
        "Dubai Creek - Traditional abra boat ride",
        "Gold Souk - Traditional gold market",
        "La Mer Beach - Trendy beach with food trucks",
        "Alserkal Avenue - Art galleries and creative spaces",
    ],
    "bangalore": [
        "Ulsoor Lake - Peaceful boating spot",
        "Commercial Street - Shopping paradise",
        "Toit - Microbrewery, popular among young crowd",
        "Bangalore Fort - Historic fort, less touristy",
        "Cubbon Park - Green lung of the city",
    ],
}


# ==================== Local Guide Agent Class ====================

class LocalGuideAgent:
    """Agent for providing local recommendations and travel tips"""

    def __init__(self):
        self.attractions = LOCAL_ATTRACTIONS
        self.restaurants = LOCAL_RESTAURANTS
        self.tips = LOCAL_TIPS
        self.hidden_gems = HIDDEN_GEMS

    def execute(self, user_message: str) -> ToolResult:
        """
        Execute Local Guide Agent based on user message
        
        Args:
            user_message: User's natural language request
            
        Returns:
            ToolResult with recommendations
        """
        logger.info(f"Local Guide Agent executing: {user_message}")
        
        message_lower = user_message.lower()
        trace = self._generate_initial_trace()

        # Extract city from message
        city = self._extract_city(user_message)
        
        if not city:
            return ToolResult(
                action="local_guide_help",
                message="Please specify a city to get local recommendations (e.g., Delhi, Mumbai, Dubai, Bangalore).",
                data={"available_cities": list(self.attractions.keys())},
                trace=trace
            )

        # Determine intent
        if "attraction" in message_lower or "place" in message_lower or "visit" in message_lower:
            return self.get_attractions(city, trace)
        elif "food" in message_lower or "restaurant" in message_lower or "eat" in message_lower:
            return self.get_restaurants(city, trace)
        elif "tip" in message_lower or "advice" in message_lower:
            return self.get_local_tips(city, trace)
        elif "hidden" in message_lower or "gem" in message_lower or "secret" in message_lower:
            return self.get_hidden_gems(city, trace)
        else:
            # Return complete guide
            return self.get_complete_guide(city, trace)

    def get_attractions(self, city: str, trace: List[Dict] = None) -> ToolResult:
        """Get tourist attractions for a city"""
        if trace is None:
            trace = self._generate_initial_trace()
        
        trace.append(self._generate_trace_event(
            "trace-2",
            "tool",
            "get_attractions",
            "local_guide_agent",
            "completed",
            f"Retrieved attractions for {city}"
        ))

        city_normalized = self._normalize_city(city)
        attractions = self.attractions.get(city_normalized, [])

        if not attractions:
            return ToolResult(
                action="get_attractions",
                message=f"No attraction data available for {city}.",
                data={"attractions": []},
                trace=trace
            )

        return ToolResult(
            action="get_attractions",
            message=f"Found {len(attractions)} top attractions in {city.title()}!",
            data={
                "city": city.title(),
                "attractions": [attr.model_dump() for attr in attractions],
                "count": len(attractions)
            },
            trace=trace
        )

    def get_restaurants(self, city: str, trace: List[Dict] = None) -> ToolResult:
        """Get restaurant recommendations for a city"""
        if trace is None:
            trace = self._generate_initial_trace()
        
        trace.append(self._generate_trace_event(
            "trace-2",
            "tool",
            "get_restaurants",
            "local_guide_agent",
            "completed",
            f"Retrieved restaurants for {city}"
        ))

        city_normalized = self._normalize_city(city)
        restaurants = self.restaurants.get(city_normalized, [])

        if not restaurants:
            return ToolResult(
                action="get_restaurants",
                message=f"No restaurant data available for {city}.",
                data={"restaurants": []},
                trace=trace
            )

        return ToolResult(
            action="get_restaurants",
            message=f"Found {len(restaurants)} amazing food spots in {city.title()}!",
            data={
                "city": city.title(),
                "restaurants": [rest.model_dump() for rest in restaurants],
                "count": len(restaurants)
            },
            trace=trace
        )

    def get_local_tips(self, city: str, trace: List[Dict] = None) -> ToolResult:
        """Get local travel tips for a city"""
        if trace is None:
            trace = self._generate_initial_trace()
        
        trace.append(self._generate_trace_event(
            "trace-2",
            "tool",
            "get_local_tips",
            "local_guide_agent",
            "completed",
            f"Retrieved travel tips for {city}"
        ))

        city_normalized = self._normalize_city(city)
        tips = self.tips.get(city_normalized, [])

        if not tips:
            return ToolResult(
                action="get_local_tips",
                message=f"No travel tips available for {city}.",
                data={"tips": []},
                trace=trace
            )

        return ToolResult(
            action="get_local_tips",
            message=f"Here are {len(tips)} essential travel tips for {city.title()}:",
            data={
                "city": city.title(),
                "tips": [tip.model_dump() for tip in tips],
                "count": len(tips)
            },
            trace=trace
        )

    def get_hidden_gems(self, city: str, trace: List[Dict] = None) -> ToolResult:
        """Get hidden gems for a city"""
        if trace is None:
            trace = self._generate_initial_trace()
        
        trace.append(self._generate_trace_event(
            "trace-2",
            "tool",
            "get_hidden_gems",
            "local_guide_agent",
            "completed",
            f"Retrieved hidden gems for {city}"
        ))

        city_normalized = self._normalize_city(city)
        gems = self.hidden_gems.get(city_normalized, [])

        if not gems:
            return ToolResult(
                action="get_hidden_gems",
                message=f"No hidden gems data available for {city}.",
                data={"gems": []},
                trace=trace
            )

        return ToolResult(
            action="get_hidden_gems",
            message=f"Discovered {len(gems)} hidden gems in {city.title()}!",
            data={
                "city": city.title(),
                "gems": gems,
                "count": len(gems)
            },
            trace=trace
        )

    def get_complete_guide(self, city: str, trace: List[Dict] = None) -> ToolResult:
        """Get complete local guide for a city"""
        if trace is None:
            trace = self._generate_initial_trace()
        
        trace.append(self._generate_trace_event(
            "trace-2",
            "tool",
            "get_complete_guide",
            "local_guide_agent",
            "completed",
            f"Generated complete guide for {city}"
        ))

        city_normalized = self._normalize_city(city)
        
        attractions = self.attractions.get(city_normalized, [])
        restaurants = self.restaurants.get(city_normalized, [])
        tips = self.tips.get(city_normalized, [])
        gems = self.hidden_gems.get(city_normalized, [])

        return ToolResult(
            action="complete_local_guide",
            message=f"Here's your complete local guide for {city.title()}!",
            data={
                "city": city.title(),
                "attractions": [attr.model_dump() for attr in attractions],
                "restaurants": [rest.model_dump() for rest in restaurants],
                "tips": [tip.model_dump() for tip in tips],
                "hidden_gems": gems,
                "summary": {
                    "attractions_count": len(attractions),
                    "restaurants_count": len(restaurants),
                    "tips_count": len(tips),
                    "hidden_gems_count": len(gems)
                }
            },
            trace=trace
        )

    def _extract_city(self, message: str) -> Optional[str]:
        """Extract city name from message"""
        message_lower = message.lower()
        cities = ["delhi", "mumbai", "dubai", "bangalore", "bengaluru"]
        
        for city in cities:
            if city in message_lower:
                return city
        
        return None

    def _normalize_city(self, city: str) -> str:
        """Normalize city name"""
        city_lower = city.lower().strip()
        if city_lower in ["bengaluru", "blr"]:
            return "bangalore"
        return city_lower

    def _generate_initial_trace(self) -> List[Dict]:
        """Generate initial trace event"""
        return [
            self._generate_trace_event(
                "trace-1",
                "agent",
                "local_guide_agent",
                "local_guide_agent",
                "completed",
                "Local Guide Agent processing started"
            )
        ]

    def _generate_trace_event(self, event_id: str, event_type: str, name: str, 
                             agent: str, status: str, output: str) -> Dict:
        """Generate a trace event"""
        return {
            "id": event_id,
            "type": event_type,
            "name": name,
            "agent": agent,
            "status": status,
            "output_summary": output,
            "duration_ms": 50,
            "timestamp": datetime.now().isoformat()
        }
