# 🤖 Groq API Orchestrator Setup Guide

## 📋 Overview

The Travix AI application now uses **Groq API** as the main orchestrator that intelligently routes user requests to the appropriate agent based on command analysis.

### Architecture

```
Frontend (React)
     ↓
User Types Command in Chat
     ↓
ConversationPanel (with useOrchestrator hook)
     ↓
API Service (frontend/src/services/api.ts)
     ↓
Backend FastAPI (apps/backend)
     ↓
Groq API Orchestrator Service
     ↓
Routes to: Orchestrator, SBT Agent, Expense Agent, or BackOffice Agent
     ↓
Response with Agent, Action, Confidence & Reason
     ↓
Display in Chat with Agent Card
```

---

## 🚀 Quick Start

### 1. Get Groq API Key

1. Visit [console.groq.com](https://console.groq.com)
2. Sign up / Log in
3. Go to **API Keys** section
4. Create a new API key
5. Copy your key

### 2. Set Environment Variables

#### Backend (.env)
```bash
# Copy from .env.example
cp apps/backend/.env.example apps/backend/.env

# Edit .env and add:
GROQ_API_KEY=your_groq_api_key_here
GROQ_MODEL=mixtral-8x7b-32768
```

#### Frontend (.env)
```bash
# Copy from .env.example
cp apps/frontend/.env.example apps/frontend/.env

# Already configured by default:
VITE_API_BASE_URL=http://localhost:8000
VITE_GROQ_ENABLED=true
```

### 3. Install Dependencies

```bash
# Backend
cd apps/backend
pip install -r requirements.txt

# Frontend (already has necessary packages)
cd apps/frontend
npm install
```

### 4. Run the Application

```bash
# Using Docker Compose
docker-compose up -d

# Or manually:
# Terminal 1 - Backend
cd apps/backend
uvicorn app.main:app --reload --port 8000

# Terminal 2 - Frontend
cd apps/frontend
npm run dev
```

### 5. Test It Out

1. Open http://localhost:3000/dashboard
2. Type in the chat: "I need to book a flight from Delhi to Mumbai"
3. Watch the orchestrator route to the appropriate agent!

---

## 🎯 Available Agents

### 1. **Orchestrator**
- **Icon**: O (Blue)
- **Description**: Routes users across flight and preference workflows
- **Capabilities**: 
  - `flight_search`
  - `preference_management`
  - `route_planning`
- **Tools**: search_flights, manage_preferences, create_itinerary

### 2. **SBT Agent**
- **Icon**: S (Cyan)
- **Description**: Collects flight search route preference-aware guidance
- **Capabilities**:
  - `flight_search`
  - `route_suggestions`
  - `price_analysis`
- **Tools**: search_flights, filter_routes, analyze_prices, suggest_alternatives

### 3. **Expense Agent**
- **Icon**: E (Green)
- **Description**: Handles trips, approvals, invoices and expense mutation tools
- **Capabilities**:
  - `expense_tracking`
  - `trip_management`
  - `invoice_generation`
  - `approval_workflow`
- **Tools**: create_expense, approve_expense, generate_invoice, track_trip_costs, create_trip

### 4. **BackOffice Agent**
- **Icon**: B (Blue)
- **Description**: Manages accounts, traveler policy, and request policy
- **Capabilities**:
  - `account_management`
  - `policy_configuration`
  - `request_handling`
- **Tools**: manage_user_account, configure_policy, handle_requests, generate_reports

---

## 📡 API Endpoints

### Health Check
```bash
GET /health

Response:
{
  "status": "healthy",
  "service": "travix-backend",
  "version": "0.1.0",
  "groq_configured": true
}
```

### Analyze Request (Main Endpoint)
```bash
POST /api/orchestrator/analyze

Request:
{
  "user_message": "I need to book a flight to Dubai",
  "conversation_history": []
}

Response:
{
  "agent": "sbt_agent",
  "action": "search_flights",
  "confidence": 0.92,
  "reason": "User is asking about flight booking which is handled by SBT Agent",
  "tools": ["search_flights", "filter_routes"]
}
```

### Get Available Agents
```bash
GET /api/orchestrator/agents

Response:
{
  "agents": {
    "orchestrator": {
      "name": "Orchestrator",
      "description": "Routes users across flight and preference workflows",
      "capabilities": ["flight_search", "preference_management", "route_planning"],
      "icon": "O"
    },
    ...
  },
  "total": 4
}
```

### Get Agent Tools
```bash
GET /api/orchestrator/agents/expense_agent/tools

Response:
{
  "agent": "expense_agent",
  "tools": [
    "create_expense",
    "approve_expense",
    "generate_invoice",
    "track_trip_costs",
    "create_trip"
  ],
  "tool_count": 5
}
```

---

## 🔧 Groq Models Available

The system supports different Groq models. You can change them in `.env`:

### Recommended Models

1. **mixtral-8x7b-32768** (DEFAULT) ⭐
   - Fast processing
   - Good at routing decisions
   - ~300ms average response
   - Best for production

2. **llama2-70b-4096**
   - More detailed reasoning
   - Better for complex analysis
   - ~500ms average response
   - Use for detailed reports

3. **gemma-7b-it**
   - Lightweight
   - Fastest response
   - ~200ms average response
   - Use for high volume

Change in `.env`:
```bash
GROQ_MODEL=llama2-70b-4096
```

---

## 📂 Project Structure

```
apps/
├── backend/
│   ├── app/
│   │   ├── main.py                    # FastAPI app entry point
│   │   ├── config.py                  # Configuration management
│   │   ├── services/
│   │   │   └── groq_orchestrator.py   # Groq orchestrator logic
│   │   └── api/
│   │       └── orchestrator.py        # API endpoints
│   ├── requirements.txt               # Python dependencies
│   └── .env.example                   # Backend environment template
│
├── frontend/
│   ├── src/
│   │   ├── services/
│   │   │   └── api.ts                 # API communication service
│   │   ├── hooks/
│   │   │   └── useOrchestrator.ts     # Orchestrator state management
│   │   ├── components/
│   │   │   └── dashboard/
│   │   │       └── ConversationPanel.tsx  # Updated with orchestrator
│   │   └── pages/
│   │       └── DashboardPage.tsx
│   └── .env.example                   # Frontend environment template
```

---

## 🧪 Testing

### Test 1: Flight Search
```
User: "Show me flights from Delhi to New York next week"
Expected Agent: sbt_agent or orchestrator
```

### Test 2: Expense Management
```
User: "Create an expense report for my trip to London"
Expected Agent: expense_agent
```

### Test 3: Account Management
```
User: "Update my traveler policy"
Expected Agent: backoffice_agent
```

### Test 4: Complex Request
```
User: "I need to book a flight and track expenses"
Expected Agent: orchestrator (will sub-route to other agents)
```

---

## 🐛 Troubleshooting

### Issue: "GROQ_API_KEY environment variable not set"

**Solution:**
1. Create `.env` file in `apps/backend/`
2. Add: `GROQ_API_KEY=your_key_here`
3. Restart backend service

### Issue: API returns 500 error

**Check:**
1. Groq API key is valid: `curl https://api.groq.com/health`
2. Backend is running: `curl http://localhost:8000/health`
3. Check backend logs: `docker-compose logs backend`

### Issue: Frontend can't connect to backend

**Check:**
1. Frontend `.env` has correct `VITE_API_BASE_URL`
2. Backend CORS allows frontend origin
3. Both services are running on correct ports

### Issue: Slow responses

**Solutions:**
1. Switch to faster model: `GROQ_MODEL=gemma-7b-it`
2. Check Groq API status: https://status.groq.com/
3. Clear browser cache
4. Restart backend service

---

## 🔐 Security Best Practices

1. **Never commit `.env` files** - Add to `.gitignore`
2. **Use environment variables** - Don't hardcode API keys
3. **Validate API responses** - Check confidence scores
4. **Rate limiting** - Implement in production
5. **Monitor API costs** - Groq charges per token

---

## 📊 Example Flow

```
User Types: "I need to expense my flight"

1. Frontend sends to /api/orchestrator/analyze
2. Groq API analyzes the request
3. Returns: agent=expense_agent, action=create_expense, confidence=0.95
4. Frontend displays response in green card (Expense Agent color)
5. Shows: "Expense Agent - Create Expense - 95% confidence"
6. User can then provide more details
```

---

## 🚀 Production Deployment

### Before Going Live

1. **Set strong Groq API key** in production environment
2. **Enable CORS properly** - only allow your domain
3. **Add authentication** - protect `/api/orchestrator` endpoints
4. **Implement rate limiting** - prevent API abuse
5. **Add logging** - for debugging and monitoring
6. **Set up monitoring** - track response times and errors
7. **Use async processing** - for long-running tasks

### Environment Variables (Production)

```bash
ENVIRONMENT=production
GROQ_API_KEY=prod_key_xyz
GROQ_MODEL=mixtral-8x7b-32768
CORS_ORIGINS=https://yourdomain.com
DATABASE_URL=postgresql://user:pass@prod-db:5432/db
```

---

## 📞 Support

For issues or questions:

1. Check Groq API documentation: https://console.groq.com/docs
2. Review backend logs: `docker-compose logs backend`
3. Check browser console: F12 → Console tab
4. Test API directly: Use curl or Postman

---

## 🎉 Features Enabled

✅ Intelligent agent routing via Groq API  
✅ Real-time conversation in dashboard  
✅ Confidence scoring for routing decisions  
✅ Multiple agent support (4 agents, 19 tools)  
✅ Conversation history tracking  
✅ Error handling and recovery  
✅ Responsive UI with agent-colored cards  
✅ Loading states and animations  
