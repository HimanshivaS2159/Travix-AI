# ✈️ Travix-AI - Intelligent Travel Management System

<div align="center">

![Travix-AI Banner](https://via.placeholder.com/1200x300/667eea/ffffff?text=Travix-AI+-+AI-Powered+Travel+Management)

**An AI-powered multi-agent travel management platform featuring intelligent flight booking, hotel reservations, expense tracking, and itinerary planning.**

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/)
[![React](https://img.shields.io/badge/React-18.0+-61DAFB.svg)](https://reactjs.org/)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.0+-3178C6.svg)](https://www.typescriptlang.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-009688.svg)](https://fastapi.tiangolo.com/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

[Features](#-features) • [Demo](#-demo) • [Quick Start](#-quick-start) • [Architecture](#-architecture) • [Documentation](#-documentation)

</div>

---

## 🎯 Overview

Travix-AI is a comprehensive travel management platform that leverages multiple AI agents to handle complex travel workflows. Built with modern technologies and powered by Groq's LLM orchestration, it provides an intuitive conversational interface for managing all aspects of business and leisure travel.

### 🌟 Key Highlights

- 🤖 **7 Specialized AI Agents** - Each agent is an expert in specific travel domains
- ✈️ **Smart Flight Booking** - Real-time flight search across 27+ routes
- 🏨 **Hotel Reservations** - Intelligent hotel recommendations and booking
- 💰 **Expense Management** - Track, approve, and manage travel expenses
- 📅 **Itinerary Planning** - AI-powered day-wise schedule creation
- 🔄 **Rebooking & Cancellations** - Handle flight delays and changes seamlessly
- 📊 **Real-time Analytics** - Visual trace view of agent execution

---

## 📸 Demo

### Flight Booking Interface
![Flight Search](https://via.placeholder.com/1200x700/667eea/ffffff?text=Flight+Search+Results)
*Search and book flights with AI-powered recommendations*

### Hotel Selection
![Hotel Booking](https://via.placeholder.com/1200x700/48bb78/ffffff?text=Hotel+Booking+Interface)
*Smart hotel recommendations based on budget and preferences*

### Expense Management
![Expense Tracking](https://via.placeholder.com/1200x700/f6993f/ffffff?text=Expense+Management)
*Track and manage travel expenses with AI assistance*

### Agent Orchestration
![Agent Flow](https://via.placeholder.com/1200x700/9b59b6/ffffff?text=Multi-Agent+Orchestration)
*Visual representation of agent workflow and trace events*

---

## ✨ Features

### 🛫 Flight Booking System

- **27+ Flight Routes** across major cities (Delhi, Mumbai, Dubai, Bangalore)
- **Multiple Airlines** - Air India, IndiGo, Vistara, SpiceJet, Emirates, FlyDubai
- **Smart Filtering** - Budget-based search, class preferences, stops
- **Real-time Availability** - Live seat availability and pricing
- **Instant Booking** - One-click flight reservations with confirmation

### 🏨 Hotel Management

- **6 Cities** with curated hotel options
- **Budget-Aware Recommendations** - Hotels matching your price range
- **Detailed Information** - Ratings, amenities, room types
- **Booking History** - Track all your hotel reservations

### 💼 Expense Agent

- **Trip Management** - Create and manage business trips
- **Expense Tracking** - Log expenses with categories
- **Approval Workflow** - Multi-level approval system
- **Invoice Generation** - Automated invoice creation
- **Receipt Upload** - OCR-based receipt parsing

### 📅 Itinerary Planning

- **Day-wise Schedules** - Detailed daily itineraries
- **Activity Management** - Time, location, duration tracking
- **Smart Optimization** - AI-powered schedule optimization
- **Budget Analysis** - Real-time budget tracking

### 🔄 Rebooking & Revisions

- **Flight Delay Handling** - Automatic compensation calculation
- **Cancellation Management** - Easy cancellation with refund processing
- **Schedule Revisions** - AI-powered itinerary improvements
- **Policy Compliance** - Automatic policy checking

---

## 🏗️ Architecture

### Technology Stack

#### Frontend
- **React 18** with TypeScript
- **Vite** for blazing-fast development
- **TailwindCSS** for modern UI
- **React Router** for navigation
- **Lucide Icons** for beautiful icons

#### Backend
- **FastAPI** - High-performance Python framework
- **Pydantic** - Data validation and serialization
- **Groq API** - LLM orchestration and routing
- **Uvicorn** - Lightning-fast ASGI server

### Multi-Agent System

```
┌─────────────────────────────────────────────────────────┐
│                    Groq Orchestrator                     │
│          (Intelligent Request Routing via LLM)           │
└──────────────────┬──────────────────────────────────────┘
                   │
       ┌───────────┼───────────┐
       │           │           │
       ▼           ▼           ▼
┌──────────┐ ┌──────────┐ ┌──────────┐
│   SBT    │ │BackOffice│ │ Expense  │
│  Agent   │ │  Agent   │ │  Agent   │
├──────────┤ ├──────────┤ ├──────────┤
│ Flights  │ │  Hotels  │ │ Expenses │
│ Booking  │ │ Bookings │ │  Trips   │
└──────────┘ └──────────┘ └──────────┘
       │           │           │
       ▼           ▼           ▼
┌──────────┐ ┌──────────┐ ┌──────────┐
│Itinerary │ │Rebooking │ │ Revising │
│  Agent   │ │  Agent   │ │  Agent   │
├──────────┤ ├──────────┤ ├──────────┤
│Schedules │ │ Delays   │ │ Analysis │
│ Planning │ │Cancellat.│ │Optimizat.│
└──────────┘ └──────────┘ └──────────┘
```

### Agent Capabilities

| Agent | Purpose | Key Tools |
|-------|---------|-----------|
| **Orchestrator** | Routes requests to appropriate agents | Groq LLM routing |
| **SBT Agent** | Flight search and booking | `search_flights`, `book_flight`, `list_bookings` |
| **BackOffice Agent** | Hotel management | `list_hotels`, `book_hotel`, `list_bookings` |
| **Expense Agent** | Expense and trip tracking | `create_expense`, `approve_expense`, `create_trip` |
| **Itinerary Agent** | Schedule planning | `schedule_making_tool`, `show_schedule` |
| **Rebooking Agent** | Handle changes and delays | `rebooking_tool`, `handle_cancellation` |
| **Revising Agent** | Optimize and analyze | `review_itinerary`, `optimize_schedule`, `check_budget` |

---

## 🚀 Quick Start

### Prerequisites

- **Python 3.11+** - [Download](https://www.python.org/downloads/)
- **Node.js 18+** - [Download](https://nodejs.org/)
- **npm** or **yarn**
- **Groq API Key** - [Get yours here](https://console.groq.com/)

### Installation

#### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/travix-ai.git
cd travix-ai
```

#### 2. Backend Setup
```bash
cd apps/backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
copy .env.example .env

# Add your Groq API key to .env
# GROQ_API_KEY=gsk_your_api_key_here
```

#### 3. Frontend Setup
```bash
cd apps/frontend

# Install dependencies
npm install

# Create .env file (if needed)
copy .env.example .env
```

### Running the Application

#### Option 1: Using Batch Files (Windows)
```bash
# Start Backend
START-BACKEND.bat

# Start Frontend (in new terminal)
START-FRONTEND.bat
```

#### Option 2: Manual Start
```bash
# Terminal 1 - Backend
cd apps/backend
python -m uvicorn app.main:app --reload --port 8000

# Terminal 2 - Frontend
cd apps/frontend
npm run dev
```

### Access the Application

- **Frontend**: http://localhost:5173
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

---

## 📖 Documentation

### API Documentation

#### Flight Booking Endpoints

**Search Flights**
```http
POST /api/orchestrator/execute/search_flights
Content-Type: application/json

{
  "from_city": "Delhi",
  "to_city": "Mumbai",
  "date": "2026-08-15"
}
```

**Book Flight**
```http
POST /api/orchestrator/execute/book_flight
Content-Type: application/json

{
  "from_city": "Delhi",
  "to_city": "Dubai",
  "budget": 15000,
  "passenger_name": "John Doe",
  "class_type": "Economy"
}
```

#### Hotel Booking Endpoints

**List Hotels**
```http
POST /api/orchestrator/execute/list_hotels
Content-Type: application/json

{
  "city": "Mumbai"
}
```

**Book Hotel**
```http
POST /api/orchestrator/execute/book_hotel
Content-Type: application/json

{
  "city": "Delhi",
  "budget": 5000,
  "room_type": "Deluxe",
  "check_in": "2026-08-15",
  "check_out": "2026-08-18"
}
```

#### Unified Orchestrator Endpoint

**Execute Any Request**
```http
POST /api/orchestrator/execute
Content-Type: application/json

{
  "user_message": "Search flights from Delhi to Mumbai",
  "conversation_history": []
}
```

### Natural Language Examples

The system understands natural language queries:

```
✈️ Flight Booking:
- "Search flights from Delhi to Dubai"
- "Book a flight from Mumbai to Delhi under ₹5000"
- "Show me my flight bookings"

🏨 Hotel Booking:
- "Find hotels in Mumbai"
- "Book a hotel in Delhi under ₹4000 per night"
- "Show my hotel bookings"

📅 Itinerary:
- "Create a day-wise schedule for my trip"
- "Show my saved schedules"

💰 Expenses:
- "Create an expense sheet"
- "Show my expenses"

🔄 Rebooking:
- "My flight is delayed by 3 hours"
- "Cancel my hotel booking"
```

---

## 🗺️ Supported Routes

### Flight Routes (27 Flights Total)

#### Delhi Hub
- Delhi ↔ Mumbai (4 flights each way) - ₹4,200 - ₹6,500
- Delhi ↔ Dubai (3-4 flights each way) - ₹12,800 - ₹19,500
- Delhi ↔ Bangalore (3 flights each way) - ₹4,900 - ₹6,800

#### Mumbai Hub
- Mumbai ↔ Delhi (4 flights each way) - ₹4,500 - ₹6,500
- Mumbai ↔ Dubai (3 flights each way) - ₹12,900 - ₹17,200

#### Dubai Hub
- Dubai ↔ Delhi (3 flights each way) - ₹13,800 - ₹19,500
- Dubai ↔ Mumbai (3 flights each way) - ₹13,900 - ₹17,200

### Hotel Locations (20+ Hotels)

- **Delhi** - 6 hotels (₹2,800 - ₹15,000/night)
- **Mumbai** - 3 hotels (₹4,500 - ₹18,000/night)
- **Bangalore** - 3 hotels (₹3,200 - ₹13,000/night)
- **Goa** - 3 hotels (₹4,000 - ₹12,000/night)

---

## 🧪 Testing

### Backend Tests

**Run Flight Route Tests**
```bash
python test_flight_routes.py
```

**Expected Output:**
```
✓ Success! Found 4 flights
  1. SpiceJet SG-8937: ₹4,200
  2. IndiGo 6E-2134: ₹4,800
  3. Vistara UK-995: ₹6,200
```

### Manual API Testing

**Using cURL:**
```bash
curl -X POST http://localhost:8000/api/orchestrator/execute \
  -H "Content-Type: application/json" \
  -d '{"user_message": "Search flights from Delhi to Mumbai"}'
```

**Using Python:**
```python
import requests

response = requests.post(
    "http://localhost:8000/api/orchestrator/execute",
    json={"user_message": "Search flights from Delhi to Dubai"}
)
print(response.json())
```

---

## 🎨 UI/UX Features

### Modern Design
- **Clean Interface** - Minimalist design inspired by modern travel platforms
- **Dark/Light Theme** - Automatic theme based on system preferences
- **Responsive Layout** - Works on desktop, tablet, and mobile
- **Smooth Animations** - Delightful micro-interactions

### Interactive Components
- **Real-time Updates** - Live booking status and availability
- **Visual Feedback** - Loading states, success/error messages
- **Agent Visualization** - See which agent is handling your request
- **Trace View** - Debug and understand agent workflow

### Accessibility
- **Keyboard Navigation** - Full keyboard support
- **Screen Reader Friendly** - ARIA labels and semantic HTML
- **High Contrast** - WCAG AA compliant color schemes
- **Focus Indicators** - Clear focus states for all interactive elements

---

## 🔧 Configuration

### Environment Variables

#### Backend (`.env`)
```env
# Groq API Configuration
GROQ_API_KEY=gsk_your_api_key_here
GROQ_MODEL=llama-3.3-70b-versatile

# Server Configuration
HOST=0.0.0.0
PORT=8000
DEBUG=True

# CORS Settings
ALLOWED_ORIGINS=http://localhost:5173,http://localhost:3000
```

#### Frontend (`.env`)
```env
# API Configuration
VITE_API_BASE_URL=http://localhost:8000

# App Configuration
VITE_APP_NAME=Travix-AI
VITE_APP_ENV=development
```

### Adding New Flight Routes

Edit `apps/backend/app/services/sbt_agent.py`:

```python
MOCK_FLIGHTS = {
    ("your_city", "destination"): [
        Flight(
            id="UNIQUE-ID",
            airline="Airline Name",
            flight_number="XX-123",
            from_city="Your City",
            from_code="YCC",
            to_city="Destination",
            to_code="DST",
            departure_time="10:00",
            arrival_time="12:00",
            duration="2h",
            price=5000,
            class_type="Economy",
            stops=0,
            available_seats=50,
            baggage="20kg",
            amenities=["Wi-Fi", "Meals"]
        ),
    ]
}
```

### Adding New Hotels

Edit `apps/backend/app/services/backoffice_agent.py`:

```python
MOCK_HOTELS = {
    "your_city": [
        Hotel(
            id="CITY-001",
            name="Hotel Name",
            city="Your City",
            address="Full Address",
            rating=4.5,
            price_per_night=5000,
            room_types=["Standard", "Deluxe"],
            amenities=["Wi-Fi", "Breakfast", "Pool"]
        ),
    ]
}
```

---

## 📊 Project Structure

```
travix-ai/
├── apps/
│   ├── backend/                 # FastAPI Backend
│   │   ├── app/
│   │   │   ├── api/            # API Routes
│   │   │   │   └── orchestrator.py
│   │   │   ├── services/       # Agent Services
│   │   │   │   ├── groq_orchestrator.py
│   │   │   │   ├── sbt_agent.py
│   │   │   │   ├── backoffice_agent.py
│   │   │   │   ├── expense_agent.py
│   │   │   │   ├── itinerary_agent.py
│   │   │   │   ├── rebooking_agent.py
│   │   │   │   └── revising_agent.py
│   │   │   ├── config.py       # Configuration
│   │   │   └── main.py         # FastAPI App
│   │   ├── requirements.txt
│   │   └── .env
│   │
│   └── frontend/               # React Frontend
│       ├── src/
│       │   ├── components/     # UI Components
│       │   │   ├── dashboard/
│       │   │   │   ├── ConversationPanel.tsx
│       │   │   │   ├── FlightResultView.tsx
│       │   │   │   ├── FlightBookingModal.tsx
│       │   │   │   ├── ResultView.tsx
│       │   │   │   └── SubagentsSidebar.tsx
│       │   │   └── ui/         # Reusable UI Components
│       │   ├── contexts/       # React Contexts
│       │   ├── hooks/          # Custom Hooks
│       │   ├── pages/          # Page Components
│       │   ├── services/       # API Services
│       │   └── types/          # TypeScript Types
│       ├── package.json
│       └── vite.config.ts
│
├── docs/                       # Documentation
│   ├── API-INTEGRATION-GUIDE.md
│   ├── FLIGHT-BOOKING-IMPLEMENTATION.md
│   └── TROUBLESHOOTING.md
│
├── test_flight_routes.py      # Backend Tests
├── START-BACKEND.bat          # Windows Startup
├── START-FRONTEND.bat
└── README.md                  # This file
```

---

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

### Development Workflow

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Run tests (`python test_flight_routes.py`)
5. Commit your changes (`git commit -m 'Add amazing feature'`)
6. Push to the branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

### Code Style

- **Python**: Follow PEP 8 guidelines
- **TypeScript/React**: Follow Airbnb style guide
- **Commits**: Use conventional commit messages

---

## 🐛 Troubleshooting

### Common Issues

**Issue: "No flights found"**
- ✅ Ensure backend server is running on port 8000
- ✅ Check GROQ_API_KEY is set in `.env`
- ✅ Verify frontend is connecting to correct API URL

**Issue: CORS errors**
- ✅ Check ALLOWED_ORIGINS in backend `.env`
- ✅ Ensure frontend URL is in allowed origins list

**Issue: Module not found**
- ✅ Install backend: `pip install -r requirements.txt`
- ✅ Install frontend: `npm install`

See [TROUBLESHOOTING.md](TROUBLESHOOTING.md) for detailed solutions.

---

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- **Groq** - For powerful LLM orchestration
- **FastAPI** - For the amazing Python framework
- **React Team** - For the excellent frontend library
- **TailwindCSS** - For beautiful utility-first CSS

---

## 📞 Support

- **Documentation**: [docs/](docs/)
- **Issues**: [GitHub Issues](https://github.com/yourusername/travix-ai/issues)
- **Email**: support@travix-ai.com

---

## 🗺️ Roadmap

### Version 1.1 (Upcoming)
- [ ] Real-time flight price tracking
- [ ] Email notifications for bookings
- [ ] PDF ticket generation
- [ ] Payment gateway integration
- [ ] User authentication & profiles

### Version 1.2 (Future)
- [ ] Mobile app (React Native)
- [ ] Car rental integration
- [ ] Train booking
- [ ] Multi-currency support
- [ ] Social sharing features

### Version 2.0 (Long-term)
- [ ] Real API integrations (Amadeus, Booking.com)
- [ ] Advanced ML-based price prediction
- [ ] Personalized recommendations
- [ ] Group travel management
- [ ] Corporate travel dashboard

---

<div align="center">

**Built with ❤️ by the Travix-AI Team**

[⬆ Back to Top](#-travix-ai---intelligent-travel-management-system)

</div>
