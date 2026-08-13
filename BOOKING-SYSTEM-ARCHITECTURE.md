# 🏨 Travix AI - Complete Booking System Architecture

## 📊 SYSTEM OVERVIEW

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                        TRAVIX AI BOOKING SYSTEM                             │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                               │
│   ┌──────────────────────────────────────────────────────────────────────┐  │
│   │                    FRONTEND (React + TypeScript)                    │  │
│   │                                                                      │  │
│   │  ┌─────────────────────────────────────────────────────────────┐   │  │
│   │  │  Dashboard (DashboardPage.tsx)                              │   │  │
│   │  │                                                              │   │  │
│   │  │  Left Panel          Center Panel         Right Panel       │   │  │
│   │  │  ┌──────────┐       ┌───────────┐       ┌──────────────┐   │   │  │
│   │  │  │Convers-  │       │ Trace/   │       │ Subagents   │   │   │  │
│   │  │  │ation     │       │ Flow/    │       │ & Tools     │   │   │  │
│   │  │  │ Panel    │───────│ Result   │───────│ Sidebar     │   │   │  │
│   │  │  │ (Chat)   │       │ Views    │       │             │   │   │  │
│   │  │  └──────────┘       └───────────┘       └──────────────┘   │   │  │
│   │  │                                                              │   │  │
│   │  │  [User Types: "Book hotel in Delhi under ₹5000"]            │   │  │
│   │  │           ↓                                                 │   │  │
│   │  │  [useOrchestrator Hook - State Management]                  │   │  │
│   │  │           ↓                                                 │   │  │
│   │  │  [apiService.executeRequest()]                             │   │  │
│   │  └─────────────────────────────────────────────────────────────┘   │  │
│   │                                                                      │  │
│   └──────────────────────────────────────────────────────────────────────┘  │
│                                   ↓↑                                         │
│                    [API: /api/orchestrator/execute]                         │
│                                   ↓↑                                         │
│   ┌──────────────────────────────────────────────────────────────────────┐  │
│   │                   BACKEND (FastAPI + Python)                        │  │
│   │                                                                      │  │
│   │  ┌──────────────────────────────────────────────────────────────┐   │  │
│   │  │  Groq Orchestrator Service                                  │   │  │
│   │  │  • Receives: user_message + conversation_history            │   │  │
│   │  │  • Calls Groq API (llama-3.3-70b-versatile)                 │   │  │
│   │  │  • Analyzes intent: "book hotel in Delhi under ₹5000"       │   │  │
│   │  │  • Routes to: BackOfficeAgent                               │   │  │
│   │  │  • Returns: {agent, action, confidence, reason}             │   │  │
│   │  └──────────────────────────────────────────────────────────────┘   │  │
│   │                           ↓                                          │  │
│   │  ┌──────────────────────────────────────────────────────────────┐   │  │
│   │  │  BackOffice Agent                                           │   │  │
│   │  │  • Determines action: "book_hotel"                          │   │  │
│   │  │  • Extracts parameters: city="Delhi", budget="₹5000"        │   │  │
│   │  │  • Executes 3 steps:                                        │   │  │
│   │  │    1. list_hotels("Delhi") → [Hotel[], TraceEvent[]]        │   │  │
│   │  │    2. filter_by_budget(Hotels[], 5000) → [Hotel[]]          │   │  │
│   │  │    3. select_best_hotel() → Hotel                           │   │  │
│   │  │    4. create_booking() → {Booking, TraceEvent[]}            │   │  │
│   │  └──────────────────────────────────────────────────────────────┘   │  │
│   │                                                                      │  │
│   │  Available Tools (executed sequentially):                           │  │
│   │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐             │  │
│   │  │ list_hotels  │→ │ book_hotel   │→ │list_bookings │             │  │
│   │  │              │  │              │  │              │             │  │
│   │  │ Input:       │  │ Input:       │  │ Input:       │             │  │
│   │  │ • city       │  │ • city       │  │ • none       │             │  │
│   │  │              │  │ • budget     │  │              │             │  │
│   │  │ Output:      │  │ • room_type  │  │ Output:      │             │  │
│   │  │ • Hotel[]    │  │ • dates      │  │ • Booking[]  │             │  │
│   │  │ • Trace[]    │  │              │  │ • Trace[]    │             │  │
│   │  │              │  │ Output:      │  │              │             │  │
│   │  │              │  │ • Booking    │  │              │             │  │
│   │  │              │  │ • Trace[]    │  │              │             │  │
│   │  └──────────────┘  └──────────────┘  └──────────────┘             │  │
│   │                                                                      │  │
│   └──────────────────────────────────────────────────────────────────────┘  │
│                                                                               │
│                    Response: {ToolResult + Trace[]}                         │
│                                                                               │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 🔄 COMPLETE BOOKING FLOW (Step by Step)

### **Step 1: User Input**
```
User Types: "Book a 5-star hotel in Delhi for under ₹5000"
            ↓
ConversationPanel captures input
            ↓
Sends to useOrchestrator hook
```

---

### **Step 2: Message Processing**
```
useOrchestrator.sendMessage() {
  • Create Message object: {role: 'user', content: '...', timestamp}
  • Add to messages[] array
  • Add to conversationHistoryRef
  • Set loading = true
}
```

---

### **Step 3: API Request**
```
const request = {
  user_message: "Book a 5-star hotel in Delhi for under ₹5000",
  conversation_history: [
    {role: 'user', content: '...'},
    {role: 'assistant', content: '...'},
    ...
  ]
}

apiService.executeRequest(request)
  ↓
POST /api/orchestrator/execute
```

---

### **Step 4: Backend Orchestration**
```
Backend receives request:
  ↓
GroqOrchestrator.analyze_request() {
  • Build system prompt with agent definitions
  • Call Groq API: llama-3.3-70b-versatile
  • Groq analyzes intent
  • Returns: {
      agent: "backoffice_agent",
      action: "book_hotel",
      confidence: 0.92,
      reason: "User wants to book hotel in Delhi within budget"
    }
}
  ↓
Execute routing decision:
  • Agent = backoffice_agent ✓
  • Create trace event: "Orchestrator routing decision"
```

---

### **Step 5: Agent Execution**
```
BackOfficeAgent.execute(user_message) {
  
  1. Intent Classification:
     message_lower = "book a 5-star hotel in delhi for under ₹5000"
     ↓
     Detects: "book" keyword
     Action: book_hotel
     ↓
  
  2. Parameter Extraction:
     city = _extract_city(message) → "Delhi"
     budget = _extract_budget(message) → 5000
     rating = _extract_rating(message) → 5
     ↓
     Trace Event 1: "Parameter extraction completed"
  
  3. List Hotels (Step 1 of booking):
     hotels = list_hotels("Delhi")
     ↓
     Returns 6 hotels in Delhi:
     [
       {name: "Taj Luxury", rating: 5, price: 12000, amenities: [...]}
       {name: "Oberoi", rating: 5, price: 10000, amenities: [...]}
       {name: "ITC Grand", rating: 4, price: 8500, amenities: [...]}
       {name: "Park Inn", rating: 4, price: 5500, amenities: [...]}
       {name: "Royal Palace", rating: 4, price: 3800, amenities: [...]}
       {name: "Budget Stay", rating: 3, price: 2800, amenities: [...]}
     ]
     ↓
     Trace Event 2: "Listed 6 hotels in Delhi"
  
  4. Filter by Budget:
     filtered_hotels = [h for h in hotels if h.price <= 5000]
     ↓
     Result: [
       {name: "Park Inn", price: 5500}  ✗ exceeds budget
       {name: "Royal Palace", price: 3800}  ✓
       {name: "Budget Stay", price: 2800}  ✓
     ]
     ↓
     Trace Event 3: "Filtered to 2 hotels under ₹5000"
  
  5. Filter by Rating:
     filtered_hotels = [h for h in filtered if h.rating >= 4]
     ↓
     Result: [
       {name: "Royal Palace", rating: 4, price: 3800}  ✓
       {name: "Budget Stay", rating: 3, price: 2800}  ✗ rating < 4
     ]
     ↓
     Trace Event 4: "Filtered to 1 hotel with rating ≥ 4"
  
  6. Select Best Match:
     best_hotel = filtered_hotels[0] → Royal Palace
     ↓
     Trace Event 5: "Selected best hotel: Royal Palace"
  
  7. Create Booking:
     booking = {
       booking_id: "BK-20260812-001",
       hotel: "Royal Palace",
       city: "Delhi",
       check_in: "2026-08-14",  # auto-generated
       check_out: "2026-08-15",  # auto-generated
       total_price: 3800,
       status: "confirmed",
       timestamp: "2026-08-12T12:07:53Z"
     }
     ↓
     BOOKINGS.insert(0, booking)  # Add to in-memory storage
     ↓
     Trace Event 6: "Booking created: BK-20260812-001"
  
  8. Generate ToolResult:
     return ToolResult {
       action: "book_hotel",
       message: "Successfully booked Royal Palace in Delhi. Booking ID: BK-20260812-001",
       data: booking,
       trace: [Trace Event 1-6],
       success: true
     }
}
```

---

### **Step 6: Response Preparation**
```
Backend returns ToolResult with trace:
{
  "action": "book_hotel",
  "message": "Successfully booked Royal Palace in Delhi...",
  "data": {
    "booking_id": "BK-20260812-001",
    "hotel": "Royal Palace",
    "total_price": 3800,
    ...
  },
  "trace": [
    {id: "trace-1", type: "orchestrator", name: "Analyze intent", ...},
    {id: "trace-2", type: "agent", name: "List hotels", ...},
    {id: "trace-3", type: "tool", name: "list_hotels", ...},
    {id: "trace-4", type: "filter", name: "Filter by budget", ...},
    {id: "trace-5", type: "select", name: "Select best", ...},
    {id: "trace-6", type: "booking", name: "Create booking", ...},
  ]
}
```

---

### **Step 7: Frontend State Update**
```
useOrchestrator receives response:
  
  1. Update messages array:
     messages.push({
       role: 'assistant',
       content: "Successfully booked Royal Palace in Delhi...",
       agent: "backoffice_agent",
       action: "book_hotel",
       timestamp: new Date()
     })
  
  2. Update result state:
     currentResult = ToolResult {
       action: "book_hotel",
       data: booking,
       trace: trace[]
     }
  
  3. Update trace state:
     currentTrace = trace[]  # For Trace View display
  
  4. Update loading:
     loading = false
  
  5. Add to conversation history:
     conversationHistoryRef.push({
       role: 'assistant',
       content: "Successfully booked..."
     })
```

---

### **Step 8: Display Results**

#### **A. Trace View (Tab 1)**
```
Shows execution timeline:

┌─────────────────────────────────────────────┐
│ EXECUTION TRACE                             │
├─────────────────────────────────────────────┤
│                                             │
│ 1. Orchestrator - Analyze intent    [50ms] │
│    Status: ✓ Completed                     │
│    Output: Routed to backoffice_agent      │
│                                             │
│ 2. BackOffice Agent - Process       [30ms] │
│    Status: ✓ Completed                     │
│    Output: Detected action: book_hotel     │
│                                             │
│ 3. Tool - list_hotels               [80ms] │
│    Status: ✓ Completed                     │
│    Output: Found 6 hotels in Delhi         │
│                                             │
│ 4. Filter - by budget               [20ms] │
│    Status: ✓ Completed                     │
│    Output: 2 hotels under ₹5000            │
│                                             │
│ 5. Filter - by rating               [15ms] │
│    Status: ✓ Completed                     │
│    Output: 1 hotel with 4+ rating         │
│                                             │
│ 6. Booking - Create                 [50ms] │
│    Status: ✓ Completed                     │
│    Output: BK-20260812-001 created         │
│                                             │
│                Total Time: 245ms            │
│                                             │
└─────────────────────────────────────────────┘
```

---

#### **B. Flow View (Tab 2)**
```
Shows agent workflow visualization:

         [User Input]
             ↓
    ┌─────────────────┐
    │ Orchestrator    │
    │ Analyze Intent  │  ← Routes decision
    └─────────────────┘
             ↓
    ┌──────────────────────┐
    │ BackOffice Agent     │
    │ book_hotel action    │
    └──────────────────────┘
        ↙         ↙         ↙
    ┌─────────┐ ┌────────┐ ┌──────────┐
    │ Extract │ │ Extract│ │ Extract  │
    │ City    │ │ Budget │ │ Rating   │
    └─────────┘ └────────┘ └──────────┘
         ↓         ↓          ↓
    ┌─────────────────────────┐
    │  list_hotels(Delhi)     │
    │  Returns: 6 hotels      │
    └─────────────────────────┘
             ↓
    ┌─────────────────────────┐
    │  Filter by Budget       │
    │  ₹5000 max              │
    │  Result: 2 hotels       │
    └─────────────────────────┘
             ↓
    ┌─────────────────────────┐
    │  Filter by Rating       │
    │  4+ stars               │
    │  Result: 1 hotel        │
    └─────────────────────────┘
             ↓
    ┌─────────────────────────┐
    │  Select Best Hotel      │
    │  Royal Palace Selected  │
    └─────────────────────────┘
             ↓
    ┌─────────────────────────┐
    │  Create Booking         │
    │  BK-20260812-001        │
    └─────────────────────────┘
             ↓
        [Booking Confirmed]
```

---

#### **C. Result View (Tab 3)**
```
Shows final booking result:

┌────────────────────────────────────────────┐
│ ✓ BOOKING CONFIRMED                        │
├────────────────────────────────────────────┤
│                                            │
│ Booking ID: BK-20260812-001                │
│                                            │
│ Hotel: Royal Palace                        │
│ Location: Delhi                            │
│ Rating: ⭐⭐⭐⭐ (4 stars)                    │
│                                            │
│ Check-in: 2026-08-14                       │
│ Check-out: 2026-08-15                      │
│ Nights: 1                                  │
│                                            │
│ Room Type: Standard                        │
│ Amenities: WiFi, AC, Parking               │
│                                            │
│ Price Breakdown:                           │
│ • Nightly Rate: ₹3,800                     │
│ • Taxes: ₹0 (included)                     │
│ • Total: ₹3,800                            │
│                                            │
│ Status: Confirmed ✓                        │
│ Payment: Completed                         │
│                                            │
│ [View Booking Details] [Modify] [Cancel]   │
│                                            │
└────────────────────────────────────────────┘
```

---

## 📋 DATA MODELS & STRUCTURES

### **1. Hotel Model**
```typescript
interface Hotel {
  id: string;
  name: string;
  city: string;
  rating: number;          // 1-5 stars
  price_per_night: number; // in rupees
  amenities: string[];
  room_types: string[];
  description: string;
  available: boolean;
}
```

### **2. Booking Model**
```typescript
interface Booking {
  booking_id: string;
  hotel_id: string;
  hotel_name: string;
  city: string;
  check_in: string;        // ISO date
  check_out: string;       // ISO date
  room_type: string;
  num_nights: number;
  rate_per_night: number;
  total_price: number;
  status: 'confirmed' | 'pending' | 'cancelled';
  created_at: string;      // ISO timestamp
}
```

### **3. TraceEvent Model**
```typescript
interface TraceEvent {
  id: string;
  type: 'orchestrator' | 'agent' | 'tool' | 'filter' | 'booking' | 'result';
  name: string;
  agent: string;
  status: 'completed' | 'processing' | 'failed';
  input: any;
  output_summary: string;
  duration_ms: number;
  timestamp: string;
}
```

### **4. ToolResult Model**
```typescript
interface ToolResult {
  action: string;          // list_hotels, book_hotel, list_bookings
  message: string;         // User-friendly message
  data: any;              // Hotels[], Booking, Bookings[]
  trace: TraceEvent[];    // Execution trace
  success: boolean;
}
```

---

## 🏗️ COMPONENT HIERARCHY

```
App
 └─ DashboardPage
    ├─ Header (Logout button)
    ├─ ConversationPanel
    │  ├─ Messages Display
    │  │  ├─ User Message
    │  │  ├─ Assistant Message (colored by agent)
    │  │  └─ System Error Message
    │  └─ Input Form
    │     └─ useOrchestrator hook (state management)
    │
    ├─ Views Container
    │  ├─ TraceView
    │  │  └─ TraceEvent List
    │  │     ├─ Event Timeline
    │  │     ├─ Duration Badge
    │  │     └─ Status Indicator
    │  │
    │  ├─ FlowView
    │  │  └─ Workflow Diagram
    │  │     ├─ Connected Nodes
    │  │     ├─ Agent Paths
    │  │     └─ Data Flow Arrows
    │  │
    │  └─ ResultView
    │     ├─ HotelListView
    │     │  ├─ Hotel Cards
    │     │  ├─ Rating Display
    │     │  ├─ Price Display
    │     │  └─ Book Button
    │     │
    │     ├─ BookingConfirmationView
    │     │  ├─ Success Banner
    │     │  ├─ Booking Details
    │     │  ├─ Booking ID
    │     │  └─ Action Buttons
    │     │
    │     └─ BookingsListView
    │        ├─ Booking Table/Cards
    │        ├─ Status Badges
    │        ├─ Edit Option
    │        └─ Cancel Option
    │
    └─ SubagentsSidebar
       ├─ Agent Search
       ├─ Agent List
       │  ├─ Orchestrator Card
       │  ├─ SBT Agent Card
       │  ├─ Expense Agent Card
       │  └─ BackOffice Agent Card
       └─ Tools List
```

---

## 🔌 API ENDPOINTS FLOW

```
Client → Backend API Endpoints:

1. POST /api/orchestrator/execute
   Input: {user_message, conversation_history}
   Output: {action, message, data, trace, success}
   
2. GET /api/orchestrator/agents
   Input: None
   Output: {agents: {name, description, icon, capabilities}}
   
3. POST /api/orchestrator/execute/list_hotels
   Input: {city}
   Output: {hotels: Hotel[], trace: TraceEvent[]}
   
4. POST /api/orchestrator/execute/book_hotel
   Input: {city, budget_info, room_type, check_in, check_out}
   Output: {booking: Booking, trace: TraceEvent[]}
   
5. GET /api/orchestrator/execute/list_bookings
   Input: None
   Output: {bookings: Booking[], trace: TraceEvent[]}
```

---

## 🎯 KEY FEATURES BY VIEW

### **Trace View**
- ✅ Shows all execution steps
- ✅ Displays duration for each step
- ✅ Color-coded by event type
- ✅ Status indicators (completed/failed)
- ✅ Chronological timeline

### **Flow View**
- ✅ Visual workflow diagram
- ✅ Node-based representation
- ✅ Connected agent paths
- ✅ Decision points
- 🔲 Could add: Conditional branching, tool I/O visualization

### **Result View**
- ✅ Hotel list with details
- ✅ Booking confirmation
- ✅ All bookings list
- 🔲 Could add: Hotel comparison, booking modification, date picker

---

## 📈 SUPPORTED CITIES & PRICING

```
Delhi (6 hotels)
├─ Taj Luxury: ₹12,000/night (5⭐)
├─ Oberoi: ₹10,000/night (5⭐)
├─ ITC Grand: ₹8,500/night (4⭐)
├─ Park Inn: ₹5,500/night (4⭐)
├─ Royal Palace: ₹3,800/night (4⭐)
└─ Budget Stay: ₹2,800/night (3⭐)

Mumbai (3 hotels)
├─ Taj Beachfront: ₹18,000/night (5⭐)
├─ Oberoi Mumbai: ₹14,000/night (4⭐)
└─ Sea Breeze: ₹4,500/night (3⭐)

Bangalore (3 hotels)
├─ Taj MG Road: ₹13,000/night (5⭐)
├─ Leela: ₹9,500/night (4⭐)
└─ Bangalore Inn: ₹3,200/night (3⭐)

Goa (3 hotels)
├─ Taj Fort Aguada: ₹12,000/night (5⭐)
├─ Leela: ₹8,500/night (4⭐)
└─ Beach Cottage: ₹4,000/night (3⭐)
```

---

## 🎨 COLOR CODING

```
Agent Colors:
• Orchestrator: Blue (#3b82f6)
• SBT Agent: Cyan (#06b6d4)
• Expense Agent: Emerald (#10b981)
• BackOffice Agent: Blue-600 (#2563eb)

Event Type Colors (Trace View):
• Orchestrator: Blue
• Agent: Purple
• Tool: Teal
• Filter: Amber
• Booking: Green
• Result: Indigo

Status Colors:
• Completed: Green ✓
• Processing: Yellow ⚙
• Failed: Red ✗
```

---

## 📝 READY FOR YOUR REQUIREMENTS!

Now that you understand the complete architecture:

1. **Trace View** - Shows detailed execution logs and timings
2. **Flow View** - Visualizes agent routing and workflow
3. **Result View** - Displays booking confirmation and details

I'm ready to build exactly what you need! 

**Tell me:**
- What enhancements do you want?
- New views?
- Modified flows?
- Additional agents?
- Backend modifications?

I'll build it exactly following this architecture! 🚀
