# ✅ Groq API Orchestrator - Setup Checklist

## 📋 Pre-Setup Requirements

- [ ] Groq Console account created at https://console.groq.com
- [ ] Groq API key generated
- [ ] Docker and Docker Compose installed
- [ ] Node.js 18+ and Python 3.9+ installed
- [ ] Git configured

---

## 🔧 Step 1: Backend Configuration

- [ ] Navigate to `apps/backend/`
- [ ] Create `.env` file:
  ```bash
  cp .env.example .env
  ```
- [ ] Edit `.env` and add your Groq API key:
  ```
  GROQ_API_KEY=your_groq_api_key_here
  GROQ_MODEL=mixtral-8x7b-32768
  ```
- [ ] Verify `requirements.txt` contains:
  - [ ] `groq>=0.4.0`
  - [ ] `fastapi>=0.110.0`
  - [ ] `pydantic>=2.6.0`

---

## 🎨 Step 2: Frontend Configuration

- [ ] Navigate to `apps/frontend/`
- [ ] Create `.env` file:
  ```bash
  cp .env.example .env
  ```
- [ ] Verify `.env` contains:
  - [ ] `VITE_API_BASE_URL=http://localhost:8000`
  - [ ] `VITE_GROQ_ENABLED=true`

---

## 📦 Step 3: Install Dependencies

### Backend
- [ ] Navigate to `apps/backend/`
- [ ] Run:
  ```bash
  pip install -r requirements.txt
  ```
- [ ] Verify Groq library installed:
  ```bash
  python -c "import groq; print(groq.__version__)"
  ```

### Frontend
- [ ] Navigate to `apps/frontend/`
- [ ] Run:
  ```bash
  npm install
  ```

---

## 🚀 Step 4: Start Services

### Using Docker Compose (Recommended)
- [ ] Navigate to project root
- [ ] Run:
  ```bash
  docker-compose up -d
  ```
- [ ] Verify services:
  ```bash
  docker-compose ps
  ```
- [ ] Check backend health:
  ```bash
  curl http://localhost:8000/health
  ```

### Manual Start
- [ ] Terminal 1 - Backend:
  ```bash
  cd apps/backend
  uvicorn app.main:app --reload --port 8000
  ```
- [ ] Terminal 2 - Frontend:
  ```bash
  cd apps/frontend
  npm run dev
  ```

---

## ✨ Step 5: Verify Setup

- [ ] Frontend loads at http://localhost:3000
- [ ] Can navigate to login page
- [ ] Login page works (any credentials work for demo)
- [ ] Can access dashboard after login
- [ ] Backend health check returns `groq_configured: true`:
  ```bash
  curl http://localhost:8000/health
  ```
- [ ] Agents endpoint returns 4 agents:
  ```bash
  curl http://localhost:8000/api/orchestrator/agents
  ```

---

## 🧪 Step 6: Test Orchestrator

### Test in Browser
1. [ ] Open http://localhost:3000/dashboard
2. [ ] Click on Conversation panel
3. [ ] Type a message: "Show me flights from Delhi to Dubai"
4. [ ] Verify:
   - [ ] Message appears in chat
   - [ ] Loading spinner shows
   - [ ] Response appears with agent card
   - [ ] Agent card shows agent name, confidence, and reasoning
   - [ ] No errors in browser console

### Test API Directly
- [ ] Test with curl:
  ```bash
  curl -X POST http://localhost:8000/api/orchestrator/analyze \
    -H "Content-Type: application/json" \
    -d '{"user_message": "I need to book a flight"}'
  ```
- [ ] Verify JSON response with agent routing

---

## 🎯 Step 7: Test All Agents

Try these commands in the dashboard chat:

1. [ ] **Flight Search** (routes to: sbt_agent)
   ```
   "Show me flights from Mumbai to London next month"
   ```

2. [ ] **Expense Tracking** (routes to: expense_agent)
   ```
   "Create an expense report for my trip"
   ```

3. [ ] **Account Management** (routes to: backoffice_agent)
   ```
   "Update my traveler policy settings"
   ```

4. [ ] **Complex Request** (routes to: orchestrator)
   ```
   "I need to book a flight and track expenses"
   ```

---

## 🔍 Step 8: Verify Logs

### Backend Logs
- [ ] Check for "Analyzing request" messages:
  ```bash
  docker-compose logs backend | grep "Analyzing"
  ```
- [ ] Check for successful Groq API calls:
  ```bash
  docker-compose logs backend | grep "Groq response"
  ```

### Frontend Logs
- [ ] Open browser DevTools (F12)
- [ ] Check Console tab for:
  - [ ] No errors
  - [ ] API requests showing successful responses
  - [ ] Messages logged properly

---

## 🚨 Troubleshooting Checklist

If something doesn't work:

### Backend Won't Start
- [ ] Check Groq API key is valid
- [ ] Check Python version: `python --version` (should be 3.9+)
- [ ] Check all dependencies installed: `pip list | grep -E "groq|fastapi|pydantic"`
- [ ] Check port 8000 is not in use: `netstat -ano | findstr :8000`
- [ ] Check `.env` file exists and has `GROQ_API_KEY`

### Frontend Won't Connect to Backend
- [ ] Check `.env` has correct `VITE_API_BASE_URL`
- [ ] Check backend is running: `curl http://localhost:8000/health`
- [ ] Check CORS is configured: Look for CORS errors in browser console
- [ ] Clear browser cache: Ctrl+Shift+Delete (or Cmd+Shift+Delete on Mac)
- [ ] Check port 3000 is not in use: `netstat -ano | findstr :3000`

### Orchestrator Not Working
- [ ] Verify Groq API key is correct
- [ ] Test API directly: `curl http://localhost:8000/api/orchestrator/agents`
- [ ] Check backend logs: `docker-compose logs backend -f`
- [ ] Try different message: Some messages might not route clearly
- [ ] Check browser console for API errors

### Slow Responses
- [ ] Check internet connection
- [ ] Check Groq API status: https://status.groq.com/
- [ ] Try different model: Change `GROQ_MODEL` in `.env`
- [ ] Restart backend: `docker-compose restart backend`

---

## 📚 Documentation to Read

After setup, read these in order:

1. [ ] `ORCHESTRATOR-SETUP.md` - Complete orchestrator guide
2. [ ] `DOCKER-SETUP.md` - Docker configuration details
3. [ ] `QUICK-FIX.md` - Quick troubleshooting guide

---

## 🎉 Success Indicators

You've successfully set up the Groq API Orchestrator when:

✅ Backend starts without errors  
✅ Frontend loads dashboard  
✅ Can type in conversation panel  
✅ Messages are sent to backend  
✅ Groq API analyzes and routes to agent  
✅ Response appears with agent card and confidence score  
✅ All 4 agents are available in sidebar  
✅ Logout button works and returns to login  
✅ No errors in console or logs  

---

## 📞 Next Steps

After successful setup:

1. **Add Real Authentication**
   - Implement JWT tokens
   - Add database user management
   - Add login validation

2. **Implement Agent Logic**
   - Create actual agent services
   - Implement tools for each agent
   - Add database persistence

3. **Add Analytics**
   - Track which agent routes are most common
   - Monitor response times
   - Log user interactions

4. **Deploy to Production**
   - Set up CI/CD pipeline
   - Configure production environment
   - Set up monitoring and alerting

---

## ✅ Checklist Complete!

If you've checked all items above, you're ready to use the Groq API Orchestrator! 🚀
