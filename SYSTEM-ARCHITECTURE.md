# 🏗️ System Architecture - Travix AI

## System Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                         USER INTERFACE                          │
│                     (React + TypeScript)                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐        │
│  │ Chat Panel   │  │ Result View  │  │ Subagents    │        │
│  │ (Input)      │  │ (Display)    │  │ (Sidebar)    │        │
│  └──────────────┘  └──────────────┘  └──────────────┘        │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
                              │
                              │ Natural Language
                              │ Commands
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                      API SERVICE LAYER                          │
│                    (apiService.ts)                              │
├─────────────────────────────────────────────────────────────────┤
│  • executeRequest()     • saveExpense()                         │
│  • analyzeRequest()     • saveTrip()                            │
│  • listHotels()         • getExpenses()                         │
│  • bookFlight()         • getTrips()                            │
└─────────────────────────────────────────────────────────────────┘
                              │
                              │ HTTP REST API
                              │ (JSON)
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                    FASTAPI BACKEND                              │
│                   (Python + FastAPI)                            │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌───────────────────────────────────────────────────────┐    │
│  │           ORCHESTRATOR ENDPOINTS                       │    │
│  │         (/api/orchestrator/*)                          │    │
│  ├───────────────────────────────────────────────────────┤    │
│  │  POST /execute          - Unified execution            │    │
│  │  POST /analyze          - Intent analysis              │    │
│  │  GET  /agents           - List agents                  │    │
│  │  POST /execute/*        - Direct tool execution        │    │
│  └───────────────────────────────────────────────────────┘    │
│                              │                                  │
│                              ▼                                  │
│  ┌───────────────────────────────────────────────────────┐    │
│  │           GROQ ORCHESTRATOR                            │    │
│  │        (groq_orchestrator.py)                          │    │
│  ├───────────────────────────────────────────────────────┤    │
│  │  • Analyzes user intent with Groq AI                   │    │
│  │  • Routes to appropriate agent                         │    │
│  │  • Returns routing decision                            │    │
│  │                                                         │    │
│  │  Model: llama-3.1-70b-versatile                        │    │
│  └───────────────────────────────────────────────────────┘    │
│                              │                                  │
│                              ▼                                  │
│  ┌───────────────────────────────────────────────────────┐    │
│  │                    AGENT LAYER                         │    │
│  ├───────────────────────────────────────────────────────┤    │
│  │                                                         │    │
│  │  ┌──────────────────┐    ┌──────────────────┐        │    │
│  │  │ BackOffice Agent │    │   SBT Agent      │        │    │
│  │  │   (Hotels)       │    │   (Flights)      │        │    │
│  │  └──────────────────┘    └──────────────────┘        │    │
│  │                                                         │    │
│  │  ┌──────────────────┐    ┌──────────────────┐        │    │
│  │  │ LocalGuide Agent │    │ Expense Agent    │        │    │
│  │  │  (Attractions)   │    │ (Expenses/Trips) │        │    │
│  │  └──────────────────┘    └──────────────────┘        │    │
│  │                                                         │    │
│  │  ┌──────────────────┐    ┌──────────────────┐        │    │
│  │  │ Itinerary Agent  │    │ Rebooking Agent  │        │    │
│  │  │  (Schedules)     │    │  (Changes)       │        │    │
│  │  └──────────────────┘    └──────────────────┘        │    │
│  │                                                         │    │
│  │  ┌──────────────────┐                                  │    │
│  │  │  Revising Agent  │                                  │    │
│  │  │  (Optimization)  │                                  │    │
│  │  └──────────────────┘                                  │    │
│  │                                                         │    │
│  └───────────────────────────────────────────────────────┘    │
│                              │                                  │
│                              ▼                                  │
│  ┌───────────────────────────────────────────────────────┐    │
│  │              DATA STORAGE LAYER                        │    │
│  ├───────────────────────────────────────────────────────┤    │
│  │  EXPENSES = []     # In-memory array                   │    │
│  │  TRIPS = []        # In-memory array                   │    │
│  │  HOTELS = []       # In-memory array                   │    │
│  │  FLIGHTS = []      # In-memory array                   │    │
│  │  BOOKINGS = []     # In-memory array                   │    │
│  │                                                         │    │
│  │  (Future: PostgreSQL / MongoDB)                        │    │
│  └───────────────────────────────────────────────────────┘    │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## Component Architecture

### Frontend Component Tree

```
App.tsx
└─ OrchestratorProvider (Context)
   └─ Router
      └─ DashboardPage
         ├─ Navbar
         ├─ SubagentsSidebar
         │  └─ Agent Selection
         ├─ ConversationPanel
         │  ├─ Message List
         │  └─ Input Field
         └─ ResultView (Router)
            ├─ HotelListView
            ├─ FlightResultView
            ├─ FlightBookingModal
            ├─ ShowFlightBookings
            ├─ LocalGuideView ✅
            │  ├─ Attractions Tab
            │  ├─ Restaurants Tab
            │  ├─ Travel Tips Tab
            │  └─ Hidden Gems Tab
            ├─ ExpenseForm ✅
            │  ├─ Core Details Section
            │  ├─ Corporate Audit Section
            │  └─ Receipt Upload Section
            ├─ ShowExpenses ✅
            │  ├─ Statistics Cards
            │  └─ Expense Cards
            ├─ TripForm ✅
            │  └─ Trip Details
            └─ ShowTrips ✅
               ├─ Summary Cards
               └─ Trip Cards
```

---

## Data Flow

### 1. Natural Language Query Flow

```
User Types: "Create an expense"
     │
     ▼
ConversationPanel.sendMessage()
     │
     ▼
useOrchestrator.sendMessage()
     │
     ▼
apiService.executeRequest({
  user_message: "Create an expense",
  conversation_history: [...]
})
     │
     ▼
POST /api/orchestrator/execute
     │
     ▼
GroqOrchestrator.analyze_request()
     │ (Groq AI analyzes intent)
     ▼
Routes to: expense_agent
Action: create_expense
     │
     ▼
ExpenseAgent.execute("Create an expense")
     │
     ▼
ExpenseAgent.create_expense_form()
     │
     ▼
Returns ToolResult {
  action: "create_expense",
  message: "Let's create an expense",
  data: { form_type, fields, categories, ... },
  success: true,
  trace: [...]
}
     │
     ▼
Frontend receives result
     │
     ▼
ResultView displays ExpenseForm
     │
     ▼
User fills and submits form
     │
     ▼
ExpenseForm.handleSubmit()
     │
     ▼
apiService.saveExpense(expenseData)
     │
     ▼
POST /api/orchestrator/execute/save_expense
     │
     ▼
ExpenseAgent.save_expense(data)
     │
     ▼
Saves to EXPENSES array
Updates TRIPS[x].total_expenses
     │
     ▼
Returns success confirmation
     │
     ▼
Frontend shows ExpenseCreatedView
     │
     ▼
Auto-refreshes with "Show my expenses"
```

---

## Agent Communication Pattern

### Standard Agent Interface

```python
class Agent:
    def execute(self, user_message: str) -> ToolResult:
        """
        Main entry point for agent execution
        
        Args:
            user_message: Natural language command
            
        Returns:
            ToolResult with action, message, data, trace
        """
        # 1. Parse intent from message
        intent = self._parse_intent(user_message)
        
        # 2. Execute appropriate tool
        if intent == "create":
            result = self._create_tool()
        elif intent == "show":
            result = self._show_tool()
        # ...
        
        # 3. Return standardized result
        return ToolResult(
            action=action,
            message=message,
            data=data,
            success=True,
            trace=trace_events
        )
```

### ToolResult Standard Format

```python
@dataclass
class ToolResult:
    action: str              # "create_expense", "show_trips", etc.
    message: str             # Human-readable message
    data: Dict[str, Any]    # Action-specific data
    success: bool           # Operation success flag
    trace: List[Dict]       # Execution trace events

# Example:
ToolResult(
    action="expense_created",
    message="✓ Expense 'EXP-2026-001' created successfully!",
    data={
        "expense": {...},
        "total_expenses": 5
    },
    success=True,
    trace=[
        {"id": "trace-1", "type": "agent", "status": "completed", ...},
        {"id": "trace-2", "type": "tool", "status": "completed", ...},
        {"id": "trace-3", "type": "booking", "status": "completed", ...}
    ]
)
```

---

## API Endpoint Structure

### Orchestrator Endpoints

```
/api/orchestrator
├─ POST /analyze              # Analyze intent only
├─ POST /execute              # Analyze + execute
├─ GET  /agents               # List available agents
└─ GET  /agents/{name}/tools  # Get agent tools
```

### Direct Execution Endpoints

```
/api/orchestrator/execute
├─ Hotels
│  ├─ POST /list_hotels
│  ├─ POST /book_hotel
│  └─ GET  /list_bookings
│
├─ Flights
│  ├─ POST /search_flights
│  ├─ POST /book_flight
│  └─ GET  /list_flight_bookings
│
├─ Local Guide ✅
│  └─ POST /local_guide
│
└─ Expenses & Trips ✅
   ├─ POST /create_expense_form
   ├─ POST /save_expense
   ├─ GET  /show_expenses
   ├─ POST /create_trip_form
   ├─ POST /save_trip
   ├─ GET  /show_trips
   ├─ GET  /approve_expenses_form
   └─ POST /approve_expense
```

---

## State Management

### Frontend State Architecture

```
OrchestratorContext
├─ messages: Message[]
├─ loading: boolean
├─ error: string | null
├─ currentResult: ToolResult | null
├─ currentTrace: TraceEvent[]
└─ agents: AgentInfo[]

Component State (Local)
├─ Form Data (e.g., expense, trip)
├─ Validation Errors
├─ Submit Loading State
└─ Submit Error
```

### Backend State (In-Memory)

```python
# In expense_agent.py
EXPENSES: List[Dict] = [
    {
        "expense_id": "EXP-2026-001",
        "trip_id": "TRIP-001",
        "amount": 15000,
        ...
    }
]

TRIPS: List[Dict] = [
    {
        "trip_id": "TRIP-001",
        "trip_name": "Mumbai Meeting",
        "total_expenses": 15000,
        ...
    }
]
```

---

## Integration Points

### 1. Groq AI Integration

```python
# In groq_orchestrator.py
client = Groq(api_key=settings.groq_api_key)

response = client.chat.completions.create(
    model="llama-3.1-70b-versatile",
    messages=[
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user_message}
    ],
    temperature=0.3
)

# Parses response to determine agent routing
```

### 2. Frontend-Backend Integration

```typescript
// In api.ts
class APIService {
  private baseURL = 'http://localhost:8000';
  
  async executeRequest(request: OrchestratorRequest) {
    const response = await fetch(
      `${this.baseURL}/api/orchestrator/execute`,
      {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(request)
      }
    );
    return response.json();
  }
}
```

### 3. Agent-Data Integration

```python
# In expense_agent.py
def save_expense(self, expense_data: Dict) -> ToolResult:
    # Create expense
    expense = {...}
    
    # Link to trip if specified
    if expense_data.get("associated_trip"):
        for trip in self.trips:
            if trip["trip_name"] == expense_data["associated_trip"]:
                expense["trip_id"] = trip["trip_id"]
                trip["total_expenses"] += expense["amount"]
    
    # Save to storage
    self.expenses.insert(0, expense)
    
    return ToolResult(...)
```

---

## Security Architecture (Future)

```
┌─────────────────────────────────────────────────┐
│          AUTHENTICATION LAYER (Future)          │
├─────────────────────────────────────────────────┤
│  • JWT Token Authentication                     │
│  • Session Management                           │
│  • Role-Based Access Control (RBAC)             │
└─────────────────────────────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────────────┐
│          AUTHORIZATION MIDDLEWARE               │
├─────────────────────────────────────────────────┤
│  • Verify JWT Token                             │
│  • Check User Permissions                       │
│  • Rate Limiting                                │
└─────────────────────────────────────────────────┘
                    │
                    ▼
           Current API Layer
```

---

## Deployment Architecture (Future)

```
┌──────────────────────────────────────────────────────┐
│                   PRODUCTION                         │
├──────────────────────────────────────────────────────┤
│                                                      │
│  ┌─────────────┐        ┌─────────────┐            │
│  │   Nginx     │───────▶│   React     │            │
│  │  (Reverse   │        │   (Build)   │            │
│  │   Proxy)    │        └─────────────┘            │
│  └─────────────┘                                    │
│         │                                            │
│         │                                            │
│         ▼                                            │
│  ┌─────────────┐        ┌─────────────┐            │
│  │   Gunicorn  │───────▶│  FastAPI    │            │
│  │   (WSGI)    │        │   Backend   │            │
│  └─────────────┘        └─────────────┘            │
│         │                      │                     │
│         │                      │                     │
│         ▼                      ▼                     │
│  ┌─────────────┐        ┌─────────────┐            │
│  │ PostgreSQL  │        │    Redis    │            │
│  │  Database   │        │    Cache    │            │
│  └─────────────┘        └─────────────┘            │
│                                                      │
└──────────────────────────────────────────────────────┘
```

---

## Technology Stack

### Frontend
- **Framework**: React 18
- **Language**: TypeScript
- **Styling**: Tailwind CSS
- **Icons**: Lucide React
- **HTTP Client**: Fetch API
- **State**: React Context + Hooks
- **Build**: Vite
- **Routing**: React Router

### Backend
- **Framework**: FastAPI
- **Language**: Python 3.11
- **AI**: Groq API (Llama 3.1)
- **Validation**: Pydantic
- **CORS**: fastapi.middleware.cors
- **Logging**: Python logging
- **Testing**: pytest

### Development
- **Version Control**: Git
- **Package Managers**: npm, pip
- **Development Server**: Vite Dev Server, Uvicorn
- **Hot Reload**: Both frontend and backend

---

## Performance Considerations

### Current Performance
- ✅ Fast in-memory data access
- ✅ Minimal API latency
- ✅ Quick UI rendering
- ✅ Efficient state management

### Future Optimizations
- ⏳ Database indexing
- ⏳ API response caching
- ⏳ Frontend code splitting
- ⏳ Image optimization
- ⏳ Lazy loading
- ⏳ CDN for static assets

---

## Scalability Path

### Current (Development)
```
Single Server
├─ Frontend (Vite Dev)
├─ Backend (Uvicorn)
└─ In-Memory Storage
```

### Future (Production)
```
Load Balancer
├─ Frontend Servers (Multiple)
├─ Backend Servers (Multiple)
├─ Database Cluster (Primary + Replicas)
├─ Cache Layer (Redis Cluster)
└─ File Storage (S3/Cloud Storage)
```

---

## Monitoring & Logging (Future)

```
┌─────────────────────────────────────────┐
│         Application Logs                │
│  • API requests/responses               │
│  • Error traces                         │
│  • Performance metrics                  │
└─────────────────────────────────────────┘
              │
              ▼
┌─────────────────────────────────────────┐
│      Logging Service                    │
│  • ELK Stack / CloudWatch               │
│  • Log aggregation                      │
│  • Real-time alerts                     │
└─────────────────────────────────────────┘
              │
              ▼
┌─────────────────────────────────────────┐
│      Monitoring Dashboard               │
│  • Grafana / DataDog                    │
│  • Uptime monitoring                    │
│  • Performance metrics                  │
└─────────────────────────────────────────┘
```

---

## Summary

**Architecture Type**: Microservices-oriented with agent-based routing

**Communication**: RESTful API with JSON

**State Management**: Context API (frontend), In-memory (backend)

**AI Integration**: Groq API for natural language understanding

**Deployment**: Development (single server), Production (distributed)

**Scalability**: Horizontal scaling ready with stateless design

**Security**: Token-based auth ready, HTTPS for production

**Monitoring**: Logging infrastructure ready for integration

---

**Last Updated**: August 14, 2026  
**Version**: 1.0.0  
**Status**: Architecture Documented
