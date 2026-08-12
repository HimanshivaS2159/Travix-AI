# 🔧 Backend Fix - Missing pydantic-settings

## Issue
```
ModuleNotFoundError: No module named 'pydantic_settings'
```

## Solution

### Step 1: Update requirements.txt
✅ Already done! The file now includes:
```
pydantic-settings>=2.0.0,<3.0.0
```

### Step 2: Rebuild Backend

#### Option A: Automated Script (Recommended)
1. Double-click: `rebuild-backend.bat`
2. Wait for rebuild to complete
3. Done!

#### Option B: Manual Commands
```bash
# Stop the backend
docker-compose down backend

# Remove old image
docker rmi travix-ai-backend 2>nul

# Rebuild
docker-compose build --no-cache backend

# Start
docker-compose up -d backend
```

#### Option C: Full Docker Reset
If Option A/B doesn't work:
```bash
# Stop all services
docker-compose down

# Clean everything
docker system prune -a

# Rebuild all
docker-compose build --no-cache

# Start all
docker-compose up -d
```

### Step 3: Verify It Works
```bash
# Check backend is running
docker-compose ps

# Check logs for errors
docker-compose logs backend

# Test health endpoint
curl http://localhost:8000/health

# Should return:
# {
#   "status": "healthy",
#   "service": "travix-backend",
#   "version": "0.1.0",
#   "groq_configured": false
# }
```

### Step 4: Set Groq API Key
```bash
# Edit apps/backend/.env and add:
GROQ_API_KEY=your_key_here
```

### Step 5: Restart with API Key
```bash
docker-compose restart backend
```

---

## ✅ Success Indicators

Backend is working when:
- ✓ Container starts without errors
- ✓ Health check returns success
- ✓ No "ModuleNotFoundError" in logs
- ✓ `groq_configured: true` in health response (after adding API key)

---

## 🆘 Still Having Issues?

1. **Check Python version in container**
   ```bash
   docker-compose exec backend python --version
   ```

2. **Check if pydantic-settings installed**
   ```bash
   docker-compose exec backend pip list | grep pydantic
   ```

3. **View full logs**
   ```bash
   docker-compose logs backend -f
   ```

4. **Rebuild from scratch**
   ```bash
   docker-compose down
   docker system prune -a
   docker-compose build --no-cache
   docker-compose up -d
   ```

---

## 📦 What Was Fixed

**File: `apps/backend/requirements.txt`**
- Added: `pydantic-settings>=2.0.0,<3.0.0`
- Reason: Pydantic v2 moved settings to separate package

**File: `apps/backend/app/config.py`**
- Already correct! Uses: `from pydantic_settings import BaseSettings`

---

## 🎉 After Fix

You'll be able to:
- ✅ Start backend without errors
- ✅ Use Groq API orchestrator
- ✅ Send messages from frontend to backend
- ✅ Get intelligent agent routing

---

## 📞 Questions?

Check:
1. Backend logs: `docker-compose logs backend`
2. Frontend logs: Browser console (F12)
3. Documentation: `ORCHESTRATOR-SETUP.md`
