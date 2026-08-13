# API Integration Guide

## 🔌 Backend API Endpoints (To Be Implemented)

All endpoints should return the standard response format with trace events and action data.

### Schedule Management Endpoints

#### 1. Create Schedule
```http
POST /api/schedules
Content-Type: application/json

{
  "trip_name": "Delhi Adventure",
  "start_date": "2026-08-14",
  "end_date": "2026-08-16",
  "city": "Delhi",
  "daily_schedules": [
    {
      "day": 1,
      "title": "Day 1 - Exploration",
      "items": [
        {
          "time": "08:00",
          "activity": "Breakfast",
          "location": "Hotel",
          "duration": "1 hour",
          "notes": "At hotel restaurant"
        }
      ]
    }
  ]
}

Response:
{
  "success": true,
  "schedule_id": "SCH-001",
  "trip_name": "Delhi Adventure",
  "message": "Schedule saved successfully",
  "trace": [...]
}
```

#### 2. Get All Schedules
```http
GET /api/schedules

Response:
{
  "success": true,
  "schedules": [
    {
      "id": "SCH-001",
      "trip_name": "Delhi Adventure",
      "city": "Delhi",
      "start_date": "2026-08-14",
      "end_date": "2026-08-16",
      "daily_schedules": [...],
      "created_at": "2026-08-13T10:30:00",
      "status": "active"
    }
  ],
  "total": 1
}
```

#### 3. Get Single Schedule
```http
GET /api/schedules/{schedule_id}

Response:
{
  "success": true,
  "schedule": {
    "id": "SCH-001",
    "trip_name": "Delhi Adventure",
    ...
  }
}
```

#### 4. Update Schedule
```http
PUT /api/schedules/{schedule_id}
Content-Type: application/json

{
  "trip_name": "Delhi Adventure 2",
  "daily_schedules": [...]
}

Response:
{
  "success": true,
  "message": "Schedule updated successfully",
  "schedule": {...}
}
```

#### 5. Delete Schedule
```http
DELETE /api/schedules/{schedule_id}

Response:
{
  "success": true,
  "message": "Schedule deleted successfully"
}
```

---

### Rebooking Endpoints

#### 1. Process Rebooking Request
```http
POST /api/rebookings
Content-Type: application/json

{
  "booking_id": "BK-12345",
  "type": "flight_delay",
  "delay_hours": 3,
  "original_flight": "AI-600",
  "original_date": "2026-08-14"
}

Response:
{
  "success": true,
  "rebooking_id": "RBK-001",
  "type": "flight_delay",
  "compensation": "₹3,000",
  "options": [
    "Take delayed flight with compensation",
    "Rebook on next available flight",
    "Full refund + rebooking voucher"
  ],
  "trace": [...]
}
```

#### 2. Confirm Rebooking Action
```http
POST /api/rebookings/{rebooking_id}/confirm
Content-Type: application/json

{
  "action": "rebook",
  "selected_option": 1
}

Response:
{
  "success": true,
  "message": "Rebooking confirmed",
  "rebooking": {...}
}
```

#### 3. Get All Rebookings
```http
GET /api/rebookings

Response:
{
  "success": true,
  "rebookings": [
    {
      "id": "RBK-001",
      "type": "flight_delay",
      "status": "processed",
      "created_at": "2026-08-13T12:00:00"
    }
  ],
  "total": 1
}
```

---

### Revising/Analysis Endpoints

#### 1. Review Itinerary
```http
POST /api/analyze/review-itinerary
Content-Type: application/json

{
  "schedule_id": "SCH-001"
}

Response:
{
  "success": true,
  "action": "review_itinerary",
  "suggestions": [
    {
      "issue": "Time constraint on Day 2",
      "current": "Red Fort (2h) + Chandni Chowk (2h) = 4 hours",
      "suggestion": "Split activities across 2 days",
      "impact": "Better pacing, no rushing",
      "priority": "High"
    }
  ],
  "overall_score": 7.5,
  "trace": [...]
}
```

#### 2. Optimize Schedule
```http
POST /api/analyze/optimize-schedule
Content-Type: application/json

{
  "schedule_id": "SCH-001"
}

Response:
{
  "success": true,
  "action": "optimize_schedule",
  "optimized_schedule": {
    "Day 1": {
      "original": "8:00 AM - 6:00 PM (continuous)",
      "optimized": "8:00 AM - 6:00 PM (with breaks)",
      "time_saved": "45 minutes"
    }
  },
  "improvements": [...]
}
```

#### 3. Check Budget
```http
POST /api/analyze/check-budget
Content-Type: application/json

{
  "schedule_id": "SCH-001"
}

Response:
{
  "success": true,
  "action": "check_budget",
  "total_budget": "₹50,000",
  "breakdown": {
    "hotels": {"amount": "₹11,400", "percentage": 22.8},
    "flights": {"amount": "₹11,000", "percentage": 22.0},
    "food": {"amount": "₹6,000", "percentage": 12.0},
    ...
  },
  "spent": "₹38,500",
  "remaining": "₹11,500",
  "status": "within_budget"
}
```

---

## 📡 Frontend API Integration

### Current Implementation

The frontend is ready to call these endpoints. Update `src/services/api.ts`:

```typescript
// Schedule API calls
export const scheduleAPI = {
  create: (data: ScheduleFormData) => 
    api.post('/schedules', data),
  
  getAll: () => 
    api.get('/schedules'),
  
  getOne: (id: string) => 
    api.get(`/schedules/${id}`),
  
  update: (id: string, data: ScheduleFormData) => 
    api.put(`/schedules/${id}`, data),
  
  delete: (id: string) => 
    api.delete(`/schedules/${id}`)
};

// Rebooking API calls
export const rebookingAPI = {
  process: (data: RebookingRequest) => 
    api.post('/rebookings', data),
  
  confirm: (id: string, action: any) => 
    api.post(`/rebookings/${id}/confirm`, action),
  
  getAll: () => 
    api.get('/rebookings')
};

// Analysis API calls
export const analysisAPI = {
  reviewItinerary: (scheduleId: string) => 
    api.post('/analyze/review-itinerary', { schedule_id: scheduleId }),
  
  optimizeSchedule: (scheduleId: string) => 
    api.post('/analyze/optimize-schedule', { schedule_id: scheduleId }),
  
  checkBudget: (scheduleId: string) => 
    api.post('/analyze/check-budget', { schedule_id: scheduleId })
};
```

### Connected Frontend Components

#### ScheduleForm.tsx
```typescript
async function handleSubmit(data: ScheduleFormData) {
  const result = await scheduleAPI.create(data);
  // Display result.schedule_id and message
}
```

#### ShowSchedules.tsx
```typescript
async function loadSchedules() {
  const result = await scheduleAPI.getAll();
  // Set schedules from result.schedules
}
```

#### RebookingModal.tsx
```typescript
async function handleConfirm(action: string) {
  const result = await rebookingAPI.confirm(rebooking_id, action);
  // Show confirmation
}
```

---

## 🔄 Agent Integration (Backend)

### Updated Orchestrator Routes Requests

The Groq Orchestrator routes user messages to agents:

```python
# In groq_orchestrator.py
def analyze_request(self, request: OrchestratorRequest) -> OrchestratorResponse:
    # Analyzes user message
    # Returns routing decision: {agent, action, confidence}
```

### Agent Response Format

All agents return `ToolResult` with consistent structure:

```python
@dataclass
class ToolResult:
    action: str              # "schedule_making_tool", "rebooking_tool", etc.
    message: str             # Human-readable message
    data: dict              # Action-specific data
    success: bool           # True/False
    trace: List[Dict]       # Execution trace events
```

### Updated orchestrator.py Integration

```python
from ..services.itinerary_agent import ItineraryAgent
from ..services.rebooking_agent import RebookingAgent
from ..services.revising_agent import RevisingAgent

@router.post("/api/orchestrator/execute/schedule_making_tool")
async def execute_schedule_tool(request: RequestModel):
    agent = ItineraryAgent()
    result = agent.save_schedule(request.data)
    return result.dict()

@router.post("/api/orchestrator/execute/show_schedule")
async def execute_show_schedule():
    agent = ItineraryAgent()
    result = agent.show_schedules([])
    return result.dict()

@router.post("/api/orchestrator/execute/rebooking_tool")
async def execute_rebooking_tool(request: RequestModel):
    agent = RebookingAgent()
    result = agent.execute(request.user_message)
    return result.dict()
```

---

## 🗄️ Database Schema (For Production)

### Schedules Table
```sql
CREATE TABLE schedules (
  id VARCHAR(50) PRIMARY KEY,
  trip_name VARCHAR(255) NOT NULL,
  city VARCHAR(100) NOT NULL,
  start_date DATE NOT NULL,
  end_date DATE NOT NULL,
  daily_schedules JSONB NOT NULL,
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW(),
  status VARCHAR(50) DEFAULT 'active',
  user_id VARCHAR(50),
  FOREIGN KEY (user_id) REFERENCES users(id)
);

CREATE TABLE schedule_items (
  id VARCHAR(50) PRIMARY KEY,
  schedule_id VARCHAR(50) NOT NULL,
  day INTEGER NOT NULL,
  time TIME NOT NULL,
  activity VARCHAR(255),
  location VARCHAR(255),
  duration VARCHAR(50),
  notes TEXT,
  FOREIGN KEY (schedule_id) REFERENCES schedules(id)
);
```

### Rebookings Table
```sql
CREATE TABLE rebookings (
  id VARCHAR(50) PRIMARY KEY,
  booking_id VARCHAR(100),
  type VARCHAR(50) NOT NULL,
  status VARCHAR(50) NOT NULL,
  original_flight VARCHAR(100),
  original_booking VARCHAR(100),
  delay_hours INTEGER,
  compensation VARCHAR(100),
  refund_amount VARCHAR(100),
  created_at TIMESTAMP DEFAULT NOW(),
  processed_at TIMESTAMP,
  user_id VARCHAR(50),
  FOREIGN KEY (user_id) REFERENCES users(id)
);
```

---

## 🧪 Testing Endpoints

### cURL Examples

#### Create Schedule
```bash
curl -X POST http://localhost:8000/api/schedules \
  -H "Content-Type: application/json" \
  -d '{
    "trip_name": "Test Trip",
    "start_date": "2026-08-14",
    "end_date": "2026-08-16",
    "city": "Delhi",
    "daily_schedules": []
  }'
```

#### Get All Schedules
```bash
curl http://localhost:8000/api/schedules
```

#### Process Rebooking
```bash
curl -X POST http://localhost:8000/api/rebookings \
  -H "Content-Type: application/json" \
  -d '{
    "booking_id": "BK-123",
    "type": "flight_delay",
    "delay_hours": 3
  }'
```

---

## ✅ Implementation Checklist

- [ ] Create database schema for schedules and rebookings
- [ ] Implement `/api/schedules/*` endpoints
- [ ] Implement `/api/rebookings/*` endpoints  
- [ ] Implement `/api/analyze/*` endpoints
- [ ] Update `src/services/api.ts` with actual API calls
- [ ] Connect DashboardPage state management to API
- [ ] Add error handling and loading states
- [ ] Implement user authentication checks
- [ ] Add input validation on backend
- [ ] Test complete flows end-to-end
- [ ] Deploy to production

---

## 🚀 Deployment Notes

1. **Backend**: Replace in-memory SCHEDULES and REBOOKINGS with database calls
2. **Frontend**: Replace API mock calls with real endpoint calls
3. **Authentication**: Add user_id validation to all endpoints
4. **Validation**: Add comprehensive input validation
5. **Error Handling**: Add try-catch blocks and error logging
6. **Monitoring**: Add APM for production monitoring

All infrastructure is ready - just implement the endpoints!
