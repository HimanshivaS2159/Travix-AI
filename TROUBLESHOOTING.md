# Troubleshooting Guide - Flight Booking System

## Problem: "No flights found" message

### ✅ Backend Test Results
The backend is working perfectly! Test shows:
- ✓ Delhi → Mumbai: 4 flights
- ✓ Delhi → Dubai: 4 flights  
- ✓ Mumbai → Delhi: 4 flights
- ✓ Dubai → Delhi: 3 flights
- ✓ All 8 routes working!

### 🔍 Possible Issues & Solutions

#### Issue 1: Backend Server Not Running

**Solution:**
1. Double-click `START-BACKEND.bat` file
2. Or run manually:
   ```bash
   cd apps/backend
   python -m uvicorn app.main:app --reload --port 8000
   ```
3. You should see:
   ```
   INFO:     Uvicorn running on http://127.0.0.1:8000
   INFO:     Application startup complete.
   ```

#### Issue 2: Frontend Not Connected to Backend

**Check `.env` file in `apps/backend/`:**
```env
GROQ_API_KEY=your_groq_api_key_here
```

**Check frontend API configuration:**
File: `apps/frontend/src/services/api.ts`
Should have:
```typescript
const API_BASE_URL = 'http://localhost:8000';
```

#### Issue 3: GROQ API Key Missing

The orchestrator needs a GROQ API key to route messages.

**Solution:**
1. Get API key from: https://console.groq.com/
2. Add to `apps/backend/.env`:
   ```
   GROQ_API_KEY=gsk_xxxxxxxxxxxxx
   ```
3. Restart backend server

#### Issue 4: CORS Issues

If you see CORS errors in browser console (F12):

**Solution:**
Backend already has CORS enabled in `app/main.py`. Make sure frontend is running on `localhost:5173` or `localhost:3000`.

### 🧪 Manual Testing

#### Test Backend Directly:

1. **Check if backend is running:**
   ```bash
   curl http://localhost:8000/
   ```

2. **Test flight search:**
   ```bash
   curl -X POST http://localhost:8000/api/orchestrator/execute \
     -H "Content-Type: application/json" \
     -d "{\"user_message\": \"Search flights from Delhi to Mumbai\"}"
   ```

3. **Test with Python script:**
   ```bash
   python test_flight_routes.py
   ```

#### Test Frontend:

1. Open browser console (F12)
2. Go to Network tab
3. Send a message: "Search flights Delhi to Mumbai"
4. Check if request goes to backend
5. Look for any errors in Console tab

### 📋 Step-by-Step Startup

1. **Start Backend:**
   ```bash
   cd apps/backend
   python -m uvicorn app.main:app --reload --port 8000
   ```
   Wait for: "Application startup complete"

2. **Start Frontend (in new terminal):**
   ```bash
   cd apps/frontend
   npm run dev
   ```
   Wait for: "Local: http://localhost:5173"

3. **Open Browser:**
   - Go to: http://localhost:5173
   - Login if needed
   - Go to Dashboard

4. **Test:**
   Type in chat: "Search flights from Delhi to Mumbai"

### 🎯 Expected Behavior

When you type: **"Search flights from Delhi to Mumbai"**

You should see:
1. Message appears in conversation panel (left)
2. Loading indicator shows
3. Trace events appear in Trace View
4. Flight cards appear in Result View with:
   - 4 flights listed
   - Air India, IndiGo, Vistara, SpiceJet
   - Prices from ₹4,200 to ₹6,200
   - "Select Flight" buttons

### 🔧 Common Fixes

#### Backend won't start:
```bash
# Install dependencies
cd apps/backend
pip install -r requirements.txt
```

#### Frontend won't start:
```bash
# Install dependencies
cd apps/frontend
npm install
```

#### Port already in use:
```bash
# Backend on different port
python -m uvicorn app.main:app --reload --port 8001

# Update frontend API URL to match
```

### 📞 Debug Checklist

- [ ] Backend server is running (check terminal)
- [ ] Frontend is running (check browser at localhost:5173)
- [ ] GROQ_API_KEY is set in backend/.env
- [ ] No errors in backend terminal
- [ ] No errors in browser console (F12)
- [ ] Network tab shows requests to localhost:8000
- [ ] Python test script passes (test_flight_routes.py)

### 🎉 If All Else Fails

1. Restart both servers
2. Clear browser cache
3. Check `.env` file exists with GROQ_API_KEY
4. Run: `python test_flight_routes.py` to verify backend
5. Check browser console for errors

The flight data is there and working! Just need to ensure frontend-backend connection is proper.
