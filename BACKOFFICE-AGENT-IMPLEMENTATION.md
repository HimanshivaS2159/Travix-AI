# BackOffice Agent Implementation

This document describes the BackOffice Agent implementation for hotel functionality in Travix-AI.

## Overview

The BackOffice Agent handles hotel-related workflows including:
- Listing hotels in supported cities
- Booking hotels within budget
- Managing booking history

## Architecture

### Backend

#### Files Modified/Created:

1. **`apps/backend/app/services/backoffice_agent.py`** (NEW)
   - Core agent logic with three tools: `list_hotels`, `book_hotel`, `list_bookings`
   - Mock hotel data for Delhi, Mumbai, Bangalore, and Goa
   - In-memory booking storage with pre-populated demo bookings
   - Trace event generation for execution flow

2. **`apps/backend/app/services/groq_orchestrator.py`** (MODIFIED)
   - Updated BackOffice Agent description to reflect hotel capabilities
   - Updated tools list to include: `list_hotels`, `book_hotel`, `list_bookings`

3. **`apps/backend/app/api/orchestrator.py`** (MODIFIED)
   - Added BackOffice agent dependency injection
   - Added three new endpoints:
     - `POST /api/orchestrator/execute/list_hotels`
     - `POST /api/orchestrator/execute/book_hotel`
     - `GET /api/orchestrator/execute/list_bookings`

4. **`apps/backend/requirements.txt`** (MODIFIED)
   - Added `pytest>=7.4.0,<8.0.0` for testing

5. **`apps/backend/tests/test_backoffice_agent.py`** (NEW)
   - Comprehensive test suite covering:
     - Hotel listing for all supported cities
     - City name normalization (e.g., Bengaluru → Bangalore)
     - Hotel booking with various budget scenarios
     - Booking history management
     - Trace generation

6. **`apps/backend/tests/__init__.py`** (NEW)
   - Tests package initialization

### Frontend

#### Files Modified/Created:

1. **`apps/frontend/src/types/index.ts`** (MODIFIED)
   - Added `Hotel` interface
   - Added `Booking` interface
   - Added `TraceEvent` interface
   - Added `ToolResult` interface

2. **`apps/frontend/src/services/api.ts`** (MODIFIED)
   - Added `listHotels()` method
   - Added `bookHotel()` method
   - Added `listBookings()` method

3. **`apps/frontend/src/hooks/useOrchestrator.ts`** (MODIFIED)
   - Added `currentResult` state for tool execution results
   - Added `currentTrace` state for execution trace
   - Enhanced `sendMessage()` to execute BackOffice tools based on routing
   - Added `executeBackofficeAgent()` helper with smart parameter extraction
   - Updated return type to include result and trace data

4. **`apps/frontend/src/components/dashboard/ResultView.tsx`** (MODIFIED)
   - Complete rewrite with dynamic rendering based on action type
   - Added `HotelListView` component for displaying hotel cards
   - Added `BookingConfirmationView` component for booking confirmation
   - Added `BookingsListView` component for booking history
   - Rich UI with icons, ratings, amenities, and pricing

5. **`apps/frontend/src/pages/DashboardPage.tsx`** (MODIFIED)
   - Added `TraceView` component for displaying execution trace
   - Added `FlowView` component for visualizing agent workflow
   - Dynamic badge counts on tabs based on data availability
   - Integrated with orchestrator hook for trace and result data

6. **`apps/frontend/src/components/dashboard/SubagentsSidebar.tsx`** (MODIFIED)
   - Updated BackOffice Agent description to reflect hotel capabilities

## Hotel Data

### Supported Cities:
- **Delhi**: 6 hotels (₹2,800 - ₹15,000 per night)
- **Mumbai**: 3 hotels (₹4,500 - ₹18,000 per night)
- **Bangalore**: 3 hotels (₹3,200 - ₹13,000 per night)
- **Goa**: 3 hotels (₹4,000 - ₹12,000 per night)

### City Normalization:
- Delhi, New Delhi → delhi
- Mumbai, Bombay → mumbai
- Bangalore, Bengaluru, BLR → bangalore
- Goa → goa

### Hotel Properties:
- `id`: Unique identifier (e.g., "DEL-001")
- `name`: Hotel name
- `city`: City name
- `address`: Full address
- `rating`: Float rating (0-5)
- `price_per_night`: Integer price in INR
- `currency`: "INR"
- `room_types`: List of available room types
- `amenities`: List of hotel amenities

### Booking Properties:
- `booking_id`: Unique booking ID (e.g., "BK-A1B2C3")
- `hotel_id`, `hotel_name`, `city`, `address`, `rating`: Hotel details
- `price_per_night`, `currency`: Pricing
- `room_type`: Selected room type
- `check_in`, `check_out`: Date strings (YYYY-MM-DD)
- `nights`: Number of nights
- `total_price`: Total booking price
- `booked_at`: Booking timestamp

## Tool Behavior

### list_hotels

**Input**: `city` (string)

**Behavior**:
1. Normalizes city name
2. Retrieves hotels from mock data
3. Randomizes order for variety
4. Returns hotel list with trace

**Output**:
```json
{
  "action": "list_hotels",
  "message": "Found 6 hotels in Delhi.",
  "data": [/* array of hotels */],
  "trace": [/* execution trace */]
}
```

**Error Cases**:
- Unsupported city: Returns empty list with helpful message

### book_hotel

**Input**: 
- `city` (string, required)
- `budget` (int, optional)
- `room_type` (string, optional)
- `check_in` (string, optional)
- `check_out` (string, optional)

**Behavior**:
1. Validates budget is provided
2. Normalizes city name
3. Filters hotels by budget
4. Selects highest-rated hotel (tie-break by lowest price)
5. Creates booking with generated ID
6. Adds to booking history (newest first)
7. Returns booking details with trace

**Default Values**:
- `check_in`: 7 days from now
- `check_out`: 10 days from now
- `nights`: Calculated from dates (default: 3)
- `room_type`: First available room type

**Output**:
```json
{
  "action": "book_hotel",
  "message": "Hotel booked successfully! Booking ID: BK-X1Y2Z3",
  "data": {/* booking object */},
  "trace": [/* execution trace */]
}
```

**Error Cases**:
- No budget: Asks user to provide budget
- Budget too low: Returns no-match message
- Unsupported city: Returns city not supported message

### list_bookings

**Input**: None

**Behavior**:
1. Retrieves all bookings from in-memory storage
2. Returns sorted newest first
3. Includes trace

**Output**:
```json
{
  "action": "list_bookings",
  "message": "Found 3 booking(s).",
  "data": [/* array of bookings */],
  "trace": [/* execution trace */]
}
```

## Trace Events

Each tool execution generates a trace with events:

1. **Orchestrator** (type: "orchestrator")
   - Receives user message
   - Routes to BackOffice Agent

2. **BackOffice Agent** (type: "agent")
   - Receives routing decision
   - Executes appropriate tool

3. **Tool Execution** (type: "tool")
   - Executes: list_hotels, book_hotel, or list_bookings
   - Returns results

4. **Booking Created** (type: "booking", book_hotel only)
   - Confirms booking creation

5. **Result** (type: "result")
   - Final result returned to user

### Trace Event Structure:
```typescript
{
  id: string;           // e.g., "trace-1"
  type: string;         // "orchestrator" | "agent" | "tool" | "booking" | "result"
  name: string;         // Display name
  agent: string;        // Agent identifier
  status: string;       // "completed" | "processing" | "failed"
  input: any;           // Input data
  output_summary: string; // Human-readable summary
  duration_ms: number;  // Execution duration
  timestamp: string;    // ISO timestamp
}
```

## Frontend Views

### Result View

**List Hotels**: Grid of hotel cards with:
- Hotel name and star rating
- Address with map pin icon
- Price per night
- Room types (badges)
- Amenities with icons

**Book Hotel**: Confirmation card with:
- Success banner with checkmark
- Hotel details with rating
- Check-in/check-out dates
- Room type
- Price breakdown (per night × nights = total)
- Booking ID (monospace)

**List Bookings**: List of booking cards with:
- Hotel name and location
- Booking ID (monospace)
- Star rating
- Check-in, check-out, room type
- Total price

### Trace View

Timeline of execution events showing:
- Event type (badge)
- Event name
- Status (colored badge)
- Output summary
- Agent name and duration

### Flow View

Visual flow diagram showing:
- Vertical flow from top to bottom
- Each step as a card
- Arrows between steps
- Step name, type, and summary

## Orchestrator Routing

The Groq-powered orchestrator routes hotel-related queries to `backoffice_agent`:

**Routing Examples**:
- "Show me hotels in Delhi" → backoffice_agent
- "List hotels in Mumbai" → backoffice_agent
- "Book a hotel in Delhi under ₹4000" → backoffice_agent
- "Show my bookings" → backoffice_agent
- "Show my hotel booking history" → backoffice_agent

The frontend hook (`useOrchestrator`) then:
1. Parses the user message
2. Extracts parameters (city, budget)
3. Calls the appropriate API endpoint
4. Updates result and trace state

## Testing

### Backend Tests

Run tests with:
```bash
cd apps/backend
pytest tests/test_backoffice_agent.py -v
```

**Test Coverage**:
- Hotel listing for all supported cities
- City name aliases (Bengaluru → Bangalore)
- Unsupported city handling
- Booking with valid budget
- Booking without budget
- Booking with insufficient budget
- Booking in unsupported city
- Booking history
- New bookings appear in history
- Trace generation
- Hotel selection logic (highest rating preference)

## Demo Prompts

### List Hotels
```
Show me hotels in Delhi
```
```
List hotels in Mumbai
```
```
Hotels in Bangalore
```

### Book Hotel
```
Book a hotel in Delhi under ₹4000
```
```
Book a hotel in Goa under ₹10000
```
```
Book a hotel in Mumbai under ₹5000
```

### List Bookings
```
Show my hotel bookings
```
```
Show my booking history
```
```
List all my bookings
```

## Notes

- All data is mock/in-memory (no database)
- Bookings persist for the application session only
- Hotel list order is randomized on each query
- Pre-populated with 2 demo bookings
- Currency is INR for all hotels
- Dates default to 7-10 days from current date
- Booking selection prefers highest rating, then lowest price
