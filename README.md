# Travix AI

An enterprise-grade AI Travel Concierge built for high-performance intelligent travel planning and concierge services.

## Current Status
✅ Foundation Setup Complete

Upcoming Phases:
- Dashboard
- Chat Interface
- Multi-Agent Architecture
- Planner Agent
- Flight Agent
- Hotel Agent
- Weather Agent
- Budget Agent
- Local Guide Agent
- Result View

---

## Tech Stack

### Frontend
- **Framework**: React 19 + Vite + TypeScript
- **Styling**: Tailwind CSS v4
- **State Management**: Zustand
- **Routing**: React Router v7
- **Animations**: Framer Motion
- **Tooling**: ESLint + Prettier

### Backend
- **Framework**: Python 3.11 + FastAPI
- **Server**: Uvicorn
- **Validation**: Pydantic v2
- **Infrastructure**: Docker, Docker Compose, PostgreSQL 16, Redis 7

---

## Monorepo Structure

```
travix-ai/
├── apps/
│   ├── frontend/        # React + Vite + TypeScript web app
│   └── backend/         # FastAPI Python application
├── packages/            # Shared libraries and packages
├── docs/                # Project documentation
├── docker/              # Shared docker scripts and configurations
├── .github/             # GitHub Workflows & Actions templates
├── .env.example         # Root environment template
├── .gitignore           # Global git ignore configuration
├── docker-compose.yml   # Multi-container orchestration
└── README.md            # Project overview & documentation
```

---

## Getting Started

### Prerequisites
- Node.js >= 20.x
- npm >= 10.x
- Python >= 3.11
- Docker & Docker Compose (optional for containerized setup)

---

### Local Development Setup

#### 1. Backend Setup
```bash
cd apps/backend
python -m venv venv

# On Windows:
venv\Scripts\activate
# On macOS/Linux:
# source venv/bin/activate

pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```
Backend health check will be available at: `http://localhost:8000/health`

#### 2. Frontend Setup
```bash
cd apps/frontend
npm install
npm run dev
```
Frontend development server will be running at: `http://localhost:5173`

---

### Docker Compose Setup
To spin up all services (Frontend, Backend, PostgreSQL, Redis) simultaneously:

```bash
docker-compose up --build
```
- Frontend: `http://localhost:3000`
- Backend: `http://localhost:8000`
- Backend Health Check: `http://localhost:8000/health`
