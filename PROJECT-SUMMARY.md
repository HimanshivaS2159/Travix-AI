# Travix - Project Summary

## What is Travix?

Travix is an intelligent travel management platform that uses AI agents to help users plan trips, book flights and hotels, manage expenses, create itineraries, and handle travel disruptions - all through natural conversation.

## Core Capabilities

### 1. Flight Management
- **Search Flights**: Find flights between cities with filters for price, timing, and airlines
- **Book Flights**: Complete flight bookings with passenger details
- **View Bookings**: Track all flight reservations in one place
- **Handle Delays**: Get compensation options when flights are delayed
- **Handle Cancellations**: Automatic rebooking with alternative flight options

### 2. Hotel Management
- **Search Hotels**: Find hotels by city with budget filtering
- **Book Hotels**: Reserve hotel rooms with dates and room preferences
- **View Bookings**: See all hotel reservations
- **Cancellation Support**: Handle hotel cancellations with refund information

### 3. Trip Planning
- **Day-Wise Schedules**: Create detailed itineraries with activities, times, and locations
- **View All Trips**: Manage multiple trip schedules
- **Local Guide**: Get recommendations for places to visit in any city
- **Optimize Itinerary**: AI suggestions to improve your travel plans

### 4. Expense Tracking
- **Log Expenses**: Track spending on flights, hotels, food, and activities
- **Create Trips**: Organize expenses by trip
- **Budget Analysis**: See spending breakdown and remaining budget
- **Expense Reports**: View detailed expense summaries

### 5. Smart Assistance
- **Review Plans**: Get AI suggestions to improve your itinerary
- **Budget Optimization**: Identify ways to save money
- **Travel Advice**: Local tips and recommendations

## Technical Architecture

### Backend (Python/FastAPI)

**7 Specialized AI Agents:**

1. **Orchestrator** - Routes user requests to the right agent
2. **SBT Agent** - Handles flight search and booking
3. **BackOffice Agent** - Manages hotel operations
4. **Expense Agent** - Tracks trip spending
5. **Itinerary Agent** - Creates and manages trip schedules
6. **Rebooking Agent** - Handles cancellations and delays
7. **Revising Agent** - Reviews and optimizes plans
8. **Local Guide Agent** - Provides city recommendations

**Technology Stack:**
- Python 3.11
- FastAPI (REST API framework)
- Groq API with Llama 3.3 70B model (AI intelligence)
- Pydantic (data validation)
- Docker (containerization)

**Key Files:**
```
apps/backend/
├── app/
│   ├── api/
│   │   └── orchestrator.py          # API endpoints
│   ├── services/
│   │   ├── groq_orchestrator.py     # AI routing logic
│   │   ├── sbt_agent.py             # Flight agent
│   │   ├── backoffice_agent.py      # Hotel agent
│   │   ├── expense_agent.py         # Expense agent
│   │   ├── itinerary_agent.py       # Trip planning agent
│   │   ├── rebooking_agent.py       # Cancellation agent
│   │   ├── revising_agent.py        # Optimization agent
│   │   └── local_guide_agent.py     # City guide agent
│   ├── config.py                    # Configuration
│   └── main.py                      # App entry point
├── tests/                           # Test files
└── requirements.txt                 # Python dependencies
```

### Frontend (React/TypeScript)

**Technology Stack:**
- React 19
- TypeScript
- Tailwind CSS
- React Router
- Vite (build tool)

**Key Components:**

**Dashboard Components:**
- `ConversationPanel.tsx` - Chat interface for talking to agents
- `SubagentsSidebar.tsx` - Shows available agents and tools
- `ResultView.tsx` - Displays agent responses

**Flight Components:**
- `FlightResultView.tsx` - Shows flight search results
- `FlightBookingModal.tsx` - Flight booking form
- `ShowFlightBookings.tsx` - List all flight bookings

**Hotel Components:**
- Hotel search and booking (integrated in BackOffice agent)

**Trip Planning Components:**
- `ScheduleForm.tsx` - Create day-by-day itineraries
- `ShowSchedules.tsx` - View all saved trips
- `LocalGuideView.tsx` - City recommendations

**Expense Components:**
- `ExpenseForm.tsx` - Log expenses
- `TripForm.tsx` - Create trip containers
- `ShowExpenses.tsx` - View expense reports
- `ShowTrips.tsx` - Manage trips

**Rebooking Components:**
- `RebookingModal.tsx` - Handle flight/hotel cancellations

**Key Files:**
```
apps/frontend/src/
├── components/
│   ├── dashboard/           # Main app components
│   ├── layout/             # Layout components
│   └── ui/                 # Reusable UI components
├── contexts/
│   └── OrchestratorContext.tsx  # Global state
├── pages/
│   ├── LoginPage.tsx       # Login screen
│   ├── HomePage.tsx        # Landing page
│   └── DashboardPage.tsx   # Main app
├── services/               # API communication
├── types/                  # TypeScript types
└── App.tsx                 # App root
```

## How It Works

### User Flow

1. **User Types a Message**: "Search flights from Delhi to Dubai"

2. **Orchestrator Analyzes**: AI determines this is a flight search request

3. **Routes to SBT Agent**: The flight agent handles the request

4. **Agent Executes**: Searches mock flight database

5. **Returns Results**: Flight options displayed in the UI

6. **User Takes Action**: Clicks "Select Flight" to book

### Three View Modes

**Trace View** - See step-by-step execution
- Shows each agent action
- Displays processing time
- Helpful for debugging

**Flow View** - Visual workflow
- Agent workflow diagram
- Shows data flow between agents
- Beautiful visualizations

**Result View** - Final output
- Forms (schedule creation, expense logging)
- Lists (flight results, hotel options)
- Modals (booking confirmations, rebooking options)

## Data Storage

**Current (Development):**
- In-memory storage (resets on restart)
- Mock data for flights, hotels, cities

**Production Ready:**
- PostgreSQL database schemas defined
- Ready for persistent storage
- User authentication prepared

## What You Can Do

### Example Conversations

**Book a Trip:**
```
You: "Search flights from Delhi to Dubai"
System: [Shows 4 flights with prices]
You: [Click "Select Flight"]
System: "Flight booked! AI-595 confirmed."
```

**Create Itinerary:**
```
You: "Create a day wise schedule"
System: [Opens schedule form]
You: [Fill trip details, add activities]
System: "Schedule saved! View it anytime."
```

**Handle Disruption:**
```
You: "My flight is delayed by 3 hours"
System: [Shows modal with options]
- Take delayed flight (₹3,000 compensation)
- Rebook on next flight
- Cancel and get refund
```

**Get Recommendations:**
```
You: "What can I do in Delhi?"
System: [Shows local guide with places]
- Red Fort, Qutub Minar, India Gate...
- With descriptions and tips
```

**Track Spending:**
```
You: "Add expense 5000 for hotel"
System: "Expense logged!"
You: "Show my expenses"
System: [Displays expense breakdown]
Total: ₹45,000
- Hotels: ₹15,000
- Flights: ₹20,000
- Food: ₹10,000
```

## Project Structure

```
Travix-AI/
├── apps/
│   ├── backend/              # Python/FastAPI server
│   │   ├── app/
│   │   │   ├── api/         # API endpoints
│   │   │   ├── services/    # AI agents
│   │   │   ├── config.py    # Settings
│   │   │   └── main.py      # Entry point
│   │   ├── tests/           # Unit tests
│   │   ├── Dockerfile       # Container config
│   │   └── requirements.txt # Dependencies
│   │
│   └── frontend/            # React web app
│       ├── src/
│       │   ├── components/  # UI components
│       │   ├── pages/       # Routes
│       │   ├── contexts/    # State management
│       │   ├── services/    # API calls
│       │   └── types/       # TypeScript types
│       ├── Dockerfile       # Container config
│       └── package.json     # Dependencies
│
├── .github/                 # GitHub templates
├── docker-compose.dev.yml   # Development setup
├── docker-compose.yml       # Production setup
├── .env.example            # Environment template
├── .gitignore              # Git ignore rules
├── LICENSE                 # License file
└── README.md               # Setup instructions
```

## Setup & Running

### Prerequisites
- Docker & Docker Compose
- Groq API key (free at console.groq.com)

### Quick Start
```bash
# 1. Clone the repo
git clone <repo-url>
cd Travix-AI

# 2. Add your API key
cp apps/backend/.env.example apps/backend/.env
# Edit apps/backend/.env and add: GROQ_API_KEY=your_key_here

# 3. Start everything
docker-compose -f docker-compose.dev.yml up

# 4. Open browser
# Frontend: http://localhost:5173
# API Docs: http://localhost:8000/docs
```

### Development Mode
```bash
# Backend only
cd apps/backend
pip install -r requirements.txt
uvicorn app.main:app --reload

# Frontend only
cd apps/frontend
npm install
npm run dev
```

## Features Summary

| Feature | Status | Agent |
|---------|--------|-------|
| Flight Search | ✅ Working | SBT Agent |
| Flight Booking | ✅ Working | SBT Agent |
| Hotel Search | ✅ Working | BackOffice Agent |
| Hotel Booking | ✅ Working | BackOffice Agent |
| Trip Schedules | ✅ Working | Itinerary Agent |
| Expense Tracking | ✅ Working | Expense Agent |
| Local Recommendations | ✅ Working | Local Guide Agent |
| Flight Delays | ✅ Working | Rebooking Agent |
| Cancellations | ✅ Working | Rebooking Agent |
| Itinerary Review | ✅ Working | Revising Agent |
| Budget Analysis | ✅ Working | Revising Agent |

## API Endpoints

### Main Endpoints
- `POST /api/orchestrator/analyze` - Route user message to agent
- `POST /api/orchestrator/execute` - Execute agent action
- `GET /api/orchestrator/agents` - List all agents
- `GET /api/orchestrator/agents/{name}/tools` - Get agent tools

### Tool Endpoints
- `POST /api/orchestrator/execute/list_hotels` - Search hotels
- `POST /api/orchestrator/execute/book_hotel` - Book hotel
- `GET /api/orchestrator/execute/list_bookings` - Get bookings

## Environment Variables

**Backend (.env):**
```env
GROQ_API_KEY=your_groq_api_key_here
GROQ_MODEL=llama-3.3-70b-versatile
ENVIRONMENT=development
```

**Frontend:**
Uses environment variables from Vite config.

## Testing

```bash
# Run backend tests
cd apps/backend
python -m pytest tests/ -v

# Tests include:
# - Agent integration tests
# - BackOffice agent tests
# - Expense agent tests
# - Local guide agent tests
```

## Future Enhancements

**Ready to Implement:**
- PostgreSQL database integration
- User authentication (JWT)
- Payment gateway integration
- Email notifications
- Mobile app (React Native)
- Real flight/hotel APIs

**Database Schemas:**
- Already designed for PostgreSQL
- Tables: users, schedules, bookings, expenses, rebookings

## Technology Highlights

**AI-Powered:**
- Uses Groq's Llama 3.3 70B model
- Natural language understanding
- Context-aware responses

**Modern Stack:**
- React 19 (latest)
- Python 3.11
- TypeScript for type safety
- Docker for easy deployment

**Developer Friendly:**
- Clear code structure
- Comprehensive error handling
- Detailed logging
- API documentation (Swagger/OpenAPI)

## Key Statistics

- **7 AI Agents** working together
- **19+ Tools** for different operations
- **14 UI Components** for user interaction
- **3 View Modes** (Trace, Flow, Result)
- **2000+ lines** of production code
- **Full TypeScript** type safety
- **Docker containerized** for deployment

## Support

**Common Issues:**
1. API key not set → Check `.env` file
2. Port already in use → Change ports in docker-compose
3. Docker not starting → Run `docker-compose down` first

**Getting Help:**
1. Check README.md for setup
2. View API docs at /docs endpoint
3. Check trace view for debugging
4. Open GitHub issue for bugs

## License

See LICENSE file for details.

---

**Built for travelers who want smart, automated trip planning and management.**
