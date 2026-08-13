# Flight Booking System Implementation

## ✈️ Overview
Complete flight booking system has been added to your Travix-AI project, similar to the hotel booking functionality. The system works with the SBT Agent and supports flight search, booking, and viewing bookings.

## 🎯 Features Implemented

### Backend (Python/FastAPI)

#### 1. **SBT Agent** (`apps/backend/app/services/sbt_agent.py`)
- **search_flights**: Search flights from one city to another
- **book_flight**: Book a flight with budget constraints
- **list_flight_bookings**: List all flight bookings

**Supported Routes:**
- Delhi ↔ Dubai
- Delhi ↔ Mumbai  
- Delhi ↔ Bangalore
- Mumbai ↔ Dubai

**Flight Data Includes:**
- Multiple airlines (Emirates, Air India, IndiGo, Vistara, SpiceJet, FlyDubai)
- Real pricing in INR
- Flight timings, duration
- Baggage allowance
- Amenities (Wi-Fi, Meals, Entertainment)
- Available seats

#### 2. **API Endpoints** (Updated `apps/backend/app/api/orchestrator.py`)
- `POST /api/orchestrator/execute/search_flights`
- `POST /api/orchestrator/execute/book_flight`
- `GET /api/orchestrator/execute/list_flight_bookings`
- Integrated SBT Agent into main execute endpoint

#### 3. **Groq Orchestrator** (Updated `apps/backend/app/services/groq_orchestrator.py`)
- Updated SBT Agent description for flight booking capabilities
- Added flight booking tools to agent capabilities

### Frontend (React/TypeScript)

#### 1. **Flight Types** (Updated `apps/frontend/src/types/index.ts`)
```typescript
interface Flight {
  id, airline, flight_number, from_city, from_code, to_city, to_code,
  departure_time, arrival_time, duration, price, currency, class_type,
  stops, available_seats, baggage, amenities
}

interface FlightBooking {
  booking_id, flight_id, airline, flight_number, from_city, from_code,
  to_city, to_code, departure_time, arrival_time, duration, price,
  currency, class_type, passenger_name, booking_date, status
}
```

#### 2. **FlightResultView Component** (`apps/frontend/src/components/dashboard/FlightResultView.tsx`)
- Beautiful flight cards with:
  - Airline logo/icon
  - Departure/arrival times and cities
  - Flight duration with visual indicator
  - Price display
  - Stop information (non-stop, 1 stop, etc.)
  - Class type, baggage, seats available
  - Amenities badges
  - Select flight button

#### 3. **ShowFlightBookings Component** (`apps/frontend/src/components/dashboard/ShowFlightBookings.tsx`)
- Display all flight bookings
- Booking cards with:
  - Airline and flight number
  - Booking ID and status badge
  - Route information (from/to cities with codes)
  - Departure and arrival times
  - Passenger name and class
  - Total price
  - Download ticket and view details buttons

#### 4. **ResultView Component** (Updated `apps/frontend/src/components/dashboard/ResultView.tsx`)
- Integrated flight search results
- Integrated flight booking confirmation
- Integrated flight bookings list
- Flight booking confirmation view with complete details

## 🚀 How to Use

### Search for Flights
Simply type natural language queries in the conversation panel:

```
"Search flights from Delhi to Dubai"
"Show me flights from Mumbai to Dubai"
"Find flights Delhi to Bangalore"
"Delhi to Mumbai flights"
```

The system will:
1. Route to SBT Agent
2. Parse the route (from/to cities)
3. Return available flights with pricing
4. Display beautiful flight cards

### Book a Flight
```
"Book a flight from Delhi to Dubai"
"Book a flight from Mumbai to Dubai under ₹15000"
"Book Delhi to Bangalore flight"
```

The system will:
1. Find the cheapest available flight (within budget if specified)
2. Create a booking
3. Show booking confirmation with all details

### View Flight Bookings
```
"Show my flight bookings"
"List my flight bookings"
"My flight bookings"
```

## 📊 Sample Flight Data

### Delhi → Dubai (4 flights)
- Emirates EK-511: ₹18,500 (4h 10m, Non-stop)
- Air India AI-995: ₹15,200 (3h 55m, Non-stop)
- IndiGo 6E-1135: ₹12,800 (3h 45m, Non-stop)
- FlyDubai FZ-433: ₹13,500 (4h 05m, Non-stop)

### Delhi → Mumbai (4 flights)
- Air India AI-864: ₹5,500 (2h 15m, Non-stop)
- IndiGo 6E-2134: ₹4,800 (2h 10m, Non-stop)
- Vistara UK-995: ₹6,200 (2h 15m, Non-stop)
- SpiceJet SG-8937: ₹4,200 (2h 15m, Non-stop)

### Mumbai → Dubai (3 flights)
- Emirates EK-502: ₹16,200 (3h 25m, Non-stop)
- Air India AI-979: ₹14,500 (3h 15m, Non-stop)
- IndiGo 6E-1401: ₹12,900 (3h 15m, Non-stop)

### Delhi → Bangalore (3 flights)
- Air India AI-804: ₹5,800 (2h 55m, Non-stop)
- IndiGo 6E-6117: ₹4,900 (2h 50m, Non-stop)
- Vistara UK-887: ₹6,500 (2h 50m, Non-stop)

## 🎨 UI Features

### Flight Search Results
- ✅ Clean, modern card layout
- ✅ Airline branding (color-coded icons)
- ✅ Visual flight route display with duration
- ✅ Price prominently displayed
- ✅ Flight details (stops, class, baggage, seats)
- ✅ Amenities as badges (Wi-Fi, Meals, Entertainment)
- ✅ Hover effects for better UX

### Flight Booking Confirmation
- ✅ Green success banner
- ✅ Complete flight details
- ✅ Route visualization with plane icon
- ✅ Passenger and booking information
- ✅ Booking ID for reference

### Flight Bookings List
- ✅ All bookings in organized cards
- ✅ Status badges (Confirmed, etc.)
- ✅ Quick view of route and timing
- ✅ Action buttons (View Details, Download Ticket)

## 🔧 Integration Points

### Orchestrator Flow
```
User Message → Groq Orchestrator → SBT Agent → Flight Tool → Result
```

### Data Flow
```
1. User: "Delhi to Dubai flights"
2. Orchestrator routes to sbt_agent
3. SBT Agent parses: from="delhi", to="dubai"
4. search_flights() returns 4 flights
5. Frontend displays FlightResultView
```

## 📝 Testing

### Test Searches
```bash
# Search
curl -X POST http://localhost:8000/api/orchestrator/execute \
  -H "Content-Type: application/json" \
  -d '{"user_message": "Search flights from Delhi to Dubai"}'

# Book
curl -X POST http://localhost:8000/api/orchestrator/execute \
  -H "Content-Type: application/json" \
  -d '{"user_message": "Book a flight from Delhi to Mumbai under 5000"}'

# List Bookings
curl -X POST http://localhost:8000/api/orchestrator/execute \
  -H "Content-Type: application/json" \
  -d '{"user_message": "Show my flight bookings"}'
```

## 🎯 Pattern Matching

The SBT Agent understands various natural language patterns:

### Route Extraction
- "from [city] to [city]"
- "[city] to [city]"
- Works with: Delhi, Mumbai, Dubai, Bangalore, New Delhi, Bombay, Bengaluru

### Budget Extraction
- "under ₹5000"
- "below ₹10000"
- "max ₹15000"
- "budget ₹8000"

## 🚦 Agent Routing

The Groq Orchestrator automatically routes flight-related queries to SBT Agent based on:
- Keywords: flight, fly, air, airline, Delhi, Mumbai, Dubai, etc.
- Intent: search, book, list
- Context from conversation history

## ✅ What Works

1. ✅ **Flight Search**: Natural language search for any supported route
2. ✅ **Price Filtering**: Automatically finds cheapest flights within budget
3. ✅ **Flight Booking**: Books flights and creates booking records
4. ✅ **Booking Management**: View all flight bookings
5. ✅ **Beautiful UI**: Professional flight cards and booking displays
6. ✅ **Trace System**: Full visibility into agent execution
7. ✅ **Multiple Airlines**: Realistic airline data with pricing
8. ✅ **Route Support**: Delhi, Mumbai, Dubai, Bangalore

## 🎓 Code Structure

```
apps/
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   └── orchestrator.py (Updated: SBT endpoints)
│   │   └── services/
│   │       ├── sbt_agent.py (NEW: Flight booking agent)
│   │       └── groq_orchestrator.py (Updated: SBT capabilities)
│
└── frontend/
    └── src/
        ├── components/
        │   └── dashboard/
        │       ├── FlightResultView.tsx (NEW)
        │       ├── ShowFlightBookings.tsx (NEW)
        │       └── ResultView.tsx (Updated: Flight views)
        └── types/
            └── index.ts (Updated: Flight types)
```

## 🌟 Example Conversation

**User:** "Search flights from Delhi to Dubai"

**System:** Routes to SBT Agent → Executes search_flights

**Result:** Displays 4 flights from Delhi to Dubai with prices ranging from ₹12,800 to ₹18,500

**User:** "Book a flight under ₹14000"

**System:** Books IndiGo 6E-1135 (₹12,800)

**Result:** Shows booking confirmation with Booking ID

---

## 🎉 Complete!

Your flight booking system is now fully integrated and works exactly like the hotel booking system. Users can search for flights, book them, and view their bookings through natural language conversation with the SBT Agent.
