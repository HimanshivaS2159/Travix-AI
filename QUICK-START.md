# ⚡ Quick Start Guide

Get Travix-AI up and running in 5 minutes!

## 📋 Prerequisites Checklist

Before you begin, ensure you have:

- [ ] **Python 3.11+** installed ([Download](https://www.python.org/downloads/))
- [ ] **Node.js 18+** installed ([Download](https://nodejs.org/))
- [ ] **Git** installed ([Download](https://git-scm.com/))
- [ ] **Groq API Key** ([Get yours free](https://console.groq.com/))
- [ ] A code editor (VS Code recommended)

---

## 🚀 3-Step Installation

### Step 1: Clone & Navigate
```bash
git clone https://github.com/yourusername/travix-ai.git
cd travix-ai
```

### Step 2: Setup Backend
```bash
cd apps/backend
python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate

pip install -r requirements.txt
copy .env.example .env
# Edit .env and add your GROQ_API_KEY
```

### Step 3: Setup Frontend
```bash
cd apps/frontend
npm install
```

---

## ▶️ Start the Application

### Option 1: Using Batch Files (Windows)

**Double-click these files:**
1. `START-BACKEND.bat` (starts backend server)
2. `START-FRONTEND.bat` (starts frontend app)

### Option 2: Manual Start

**Terminal 1 - Backend:**
```bash
cd apps/backend
python -m uvicorn app.main:app --reload --port 8000
```

**Terminal 2 - Frontend:**
```bash
cd apps/frontend
npm run dev
```

---

## 🎯 Access the Application

Once both servers are running:

| Service | URL | Description |
|---------|-----|-------------|
| 🌐 **Frontend** | http://localhost:5173 | Main application |
| 🔌 **Backend API** | http://localhost:8000 | REST API |
| 📚 **API Docs** | http://localhost:8000/docs | Swagger UI |

---

## ✨ Your First Actions

### 1️⃣ Search for Flights
Type in the chat:
```
Search flights from Delhi to Mumbai
```

### 2️⃣ Find Hotels
Type in the chat:
```
Show me hotels in Delhi
```

### 3️⃣ Book a Flight
Type in the chat:
```
Book a flight from Delhi to Dubai under ₹15000
```

### 4️⃣ Create an Itinerary
Type in the chat:
```
Create a day-wise schedule for my trip
```

---

## 🧪 Verify Installation

### Test Backend
```bash
python test_flight_routes.py
```

**Expected output:**
```
✓ Success! Found 4 flights
  1. SpiceJet SG-8937: ₹4,200
  2. IndiGo 6E-2134: ₹4,800
  3. Vistara UK-995: ₹6,200
```

### Test Frontend
1. Open http://localhost:5173
2. You should see the login page
3. Login and access the dashboard

---

## 🔧 Common Setup Issues

### Issue: "Module not found"

**Solution:**
```bash
# Backend
cd apps/backend
pip install -r requirements.txt

# Frontend
cd apps/frontend
npm install
```

### Issue: "Port already in use"

**Solution:**
```bash
# Use different port for backend
python -m uvicorn app.main:app --reload --port 8001

# Update frontend API URL in .env
VITE_API_BASE_URL=http://localhost:8001
```

### Issue: "GROQ_API_KEY not found"

**Solution:**
1. Get API key from https://console.groq.com/
2. Create/edit `apps/backend/.env`
3. Add: `GROQ_API_KEY=gsk_your_key_here`
4. Restart backend server

---

## 📱 Next Steps

Now that you're set up:

1. 📖 **Read the full [README](README.md)** for detailed documentation
2. 🧪 **Try different queries** to explore agent capabilities
3. 🎨 **Customize the UI** in `apps/frontend/src`
4. 🤖 **Add new agents** following [CONTRIBUTING.md](CONTRIBUTING.md)
5. 🐛 **Report issues** on GitHub

---

## 💡 Quick Tips

### Development Mode Features

- 🔄 **Hot Reload**: Both servers auto-reload on code changes
- 🐛 **Debug Mode**: Check browser console (F12) for errors
- 📊 **API Testing**: Use http://localhost:8000/docs for API testing
- 🔍 **Trace View**: See agent execution in real-time

### Useful Commands

```bash
# Backend
python -m uvicorn app.main:app --reload     # Start with hot reload
python test_flight_routes.py                # Run tests
pip freeze > requirements.txt               # Update dependencies

# Frontend
npm run dev                                 # Start dev server
npm run build                               # Build for production
npm run preview                             # Preview production build
npm run lint                                # Check code style
```

---

## 🎓 Learn More

- 📚 **[Full Documentation](README.md)**
- 🔌 **[API Integration Guide](API-INTEGRATION-GUIDE.md)**
- ✈️ **[Flight Booking Implementation](FLIGHT-BOOKING-IMPLEMENTATION.md)**
- 🔧 **[Troubleshooting Guide](TROUBLESHOOTING.md)**
- 🤝 **[Contributing Guidelines](CONTRIBUTING.md)**

---

## 💬 Need Help?

- 📖 Check the [Troubleshooting Guide](TROUBLESHOOTING.md)
- 💬 Join our [Discord](https://discord.gg/travix-ai)
- 🐛 Report bugs on [GitHub Issues](https://github.com/yourusername/travix-ai/issues)
- 📧 Email: support@travix-ai.com

---

## ✅ Installation Complete!

You're all set! Start exploring Travix-AI and let the AI agents handle your travel needs.

**Happy traveling! ✈️🏨**

---

<div align="center">

[⬆ Back to Top](#-quick-start-guide) • [Main README](README.md)

</div>
