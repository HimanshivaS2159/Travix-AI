# Local Guide Agent 🗺️

The **Local Guide Agent** provides comprehensive local recommendations, attractions, restaurants, travel tips, and hidden gems for cities in your travel itinerary. It helps travelers discover the best places to visit, eat, and explore like a local.

## 🌟 Features

### 1. **Tourist Attractions** 🏛️
- Curated list of top attractions with ratings
- Entry fees, timings, and visit duration
- Best time to visit recommendations
- Insider tips for each attraction

### 2. **Restaurant Recommendations** 🍽️
- Authentic local and international cuisines
- Price range indicators
- Must-try dishes highlighted
- Ratings from local reviews

### 3. **Travel Tips** 💡
- Transportation advice
- Safety guidelines
- Weather recommendations
- Local customs and cultural notes
- Money and shopping tips

### 4. **Hidden Gems** 💎
- Off-the-beaten-path locations
- Local favorites
- Secret spots tourists miss
- Unique experiences

## 🎯 Supported Cities

Currently, the Local Guide Agent provides detailed information for:
- **Delhi** (India)
- **Mumbai** (India)
- **Dubai** (UAE)
- **Bangalore** (India)

## 🚀 How to Use

### Natural Language Queries

The agent understands natural language and can respond to various query types:

```
"Show me attractions in Delhi"
"Where can I eat in Mumbai?"
"Give me travel tips for Dubai"
"What are the hidden gems in Bangalore?"
"Complete local guide for Delhi"
```

### Specific Categories

You can request specific information:

**Attractions:**
- "Show attractions in [city]"
- "Places to visit in [city]"
- "Tourist spots in [city]"

**Restaurants:**
- "Where to eat in [city]"
- "Best food in [city]"
- "Restaurants in [city]"

**Travel Tips:**
- "Travel tips for [city]"
- "Advice for visiting [city]"

**Hidden Gems:**
- "Hidden gems in [city]"
- "Secret places in [city]"
- "Off the beaten path in [city]"

## 📊 Data Structure

### Attraction Object
```json
{
  "id": "DEL-ATT-001",
  "name": "Red Fort (Lal Qila)",
  "category": "Historical Monument",
  "description": "Magnificent 17th-century fort, UNESCO World Heritage Site",
  "location": "Chandni Chowk, Old Delhi",
  "rating": 4.6,
  "visit_duration": "2-3 hours",
  "entry_fee": "₹50 (Indians), ₹600 (Foreigners)",
  "best_time": "Early morning (9-11 AM) to avoid crowds",
  "tips": [
    "Visit on weekdays to avoid weekend rush",
    "Light and sound show in evening (tickets separate)",
    "Wear comfortable shoes for walking"
  ]
}
```

### Restaurant Object
```json
{
  "id": "DEL-RES-001",
  "name": "Karim's",
  "cuisine": "Mughlai",
  "specialty": "Authentic Mughlai cuisine since 1913",
  "location": "Jama Masjid, Old Delhi",
  "rating": 4.4,
  "price_range": "₹₹ (₹300-600 per person)",
  "must_try": ["Mutton Korma", "Chicken Jahangiri", "Sheermal", "Phirni"]
}
```

### Travel Tip Object
```json
{
  "category": "Transportation",
  "tip": "Use Delhi Metro - it's clean, safe, and efficient",
  "importance": "high"
}
```

## 🔧 API Endpoints

### Execute Local Guide
**POST** `/api/orchestrator/execute/local_guide`

**Request Body:**
```json
{
  "city": "Delhi",
  "type": "complete"  // Options: attractions, restaurants, tips, gems, complete
}
```

**Response:**
```json
{
  "action": "complete_local_guide",
  "message": "Here's your complete local guide for Delhi!",
  "data": {
    "city": "Delhi",
    "attractions": [...],
    "restaurants": [...],
    "tips": [...],
    "hidden_gems": [...],
    "summary": {
      "attractions_count": 5,
      "restaurants_count": 4,
      "tips_count": 7,
      "hidden_gems_count": 5
    }
  },
  "success": true,
  "trace": [...]
}
```

## 💻 Integration

### Backend Integration

The Local Guide Agent is integrated with:
1. **Orchestrator** - Routes local guide queries
2. **Groq AI** - Natural language understanding
3. **API Endpoints** - REST API access

### Frontend Integration

The frontend displays local guide results with:
1. **LocalGuideView Component** - Beautiful tabbed interface
2. **ResultView Integration** - Automatic routing
3. **SubagentsSidebar** - Agent visibility

## 🎨 UI Components

### Attractions Tab
- Card-based layout with images placeholder
- Rating badges
- Location information
- Entry fees and timings
- Insider tips section

### Restaurants Tab
- Restaurant cards with cuisine badges
- Price range indicators
- Must-try dishes highlighted
- Ratings and specialty information

### Travel Tips Tab
- Categorized tips (Transportation, Safety, Weather, etc.)
- Priority indicators (High, Medium, Low)
- Clean, scannable layout

### Hidden Gems Tab
- Grid layout with gem icons
- Quick-view cards
- Easy-to-browse format

## 📱 Example Usage

### 1. Get Attractions
```python
from app.services.local_guide_agent import LocalGuideAgent

agent = LocalGuideAgent()
result = agent.execute("Show me attractions in Delhi")

# Result will contain:
# - 5 top attractions
# - Ratings, timings, entry fees
# - Best time to visit
# - Insider tips
```

### 2. Get Complete Guide
```python
result = agent.execute("Complete local guide for Mumbai")

# Result will contain:
# - All attractions
# - All restaurants
# - All travel tips
# - All hidden gems
# - Summary statistics
```

## 🔄 Integration with Itinerary Agent

The Local Guide Agent works seamlessly with the Itinerary Agent:
- When creating a schedule for a city, local guide suggestions can be shown
- Users can add attractions directly to their itinerary
- Restaurant recommendations for meal times
- Travel tips relevant to the trip dates

## 🌐 Future Enhancements

### Planned Features
- [ ] More cities (Paris, London, Tokyo, etc.)
- [ ] Real-time pricing from APIs
- [ ] User reviews and ratings
- [ ] Photo galleries
- [ ] Map integration
- [ ] Booking integration
- [ ] Personalized recommendations
- [ ] Distance and route planning
- [ ] Budget-based filtering
- [ ] Seasonal recommendations

### Potential Integrations
- Google Maps API for locations
- Zomato/Yelp API for restaurant data
- TripAdvisor API for reviews
- Weather API for timing suggestions
- Currency exchange API for pricing

## 🧪 Testing

Run the test suite:
```bash
cd apps/backend
python tests/test_local_guide_agent.py
```

Test coverage includes:
- ✅ Get attractions for all cities
- ✅ Get restaurants for all cities
- ✅ Get travel tips for all cities
- ✅ Get hidden gems for all cities
- ✅ Complete local guide
- ✅ Unknown city handling
- ✅ No city specified handling

## 📝 Notes

- All data is currently mock/static data
- Real-time integrations planned for future releases
- Data is curated for quality and relevance
- Regular updates to keep information current

## 🤝 Contributing

To add a new city:
1. Add city data to `LOCAL_ATTRACTIONS`, `LOCAL_RESTAURANTS`, `LOCAL_TIPS`, `HIDDEN_GEMS` in `local_guide_agent.py`
2. Update `_normalize_city()` method if needed
3. Add test cases in `test_local_guide_agent.py`
4. Update this documentation

## 📄 License

Part of the Travix-AI project. See main LICENSE file for details.

---

**Made with ❤️ by the Travix-AI Team**
