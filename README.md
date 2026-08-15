# Travix - Travel Management System

A smart travel booking and management platform that helps you plan trips, book flights and hotels, manage expenses, and handle travel disruptions.

## What Does This Do?

Travix is your personal travel assistant that can:

- **Search and book flights** between cities
- **Find and reserve hotels** within your budget
- **Create detailed trip schedules** with day-by-day activities
- **Track and manage expenses** for your trips
- **Handle flight delays and cancellations** with automatic rebooking options
- **Review and optimize** your itineraries to save time and money

## Getting Started

### What You Need

- Docker and Docker Compose installed on your computer
- A Groq API key (free at [console.groq.com](https://console.groq.com))

### Installation

1. **Get the code**
   ```bash
   git clone <your-repo-url>
   cd Travix-AI
   ```

2. **Set up your API key**
   ```bash
   # Copy the example environment file
   cp apps/backend/.env.example apps/backend/.env
   
   # Edit apps/backend/.env and add your Groq API key
   GROQ_API_KEY=your_actual_api_key_here
   ```

3. **Start the application**
   ```bash
   docker-compose -f docker-compose.dev.yml up
   ```

4. **Open in your browser**
   - Main app: http://localhost:5173
   - API docs: http://localhost:8000/docs

That's it! You're ready to start planning your trips.

## How to Use

### Book a Flight

Just type in the chat:
- "Search flights from Delhi to Dubai"
- "Find me cheap flights to Mumbai next week"

You'll see available flights with prices, timings, and airlines. Click "Select Flight" to book.

### Find a Hotel

Tell the system what you need:
- "Find hotels in Delhi under 30000"
- "Book a hotel in Goa near the beach"

Browse through options with photos, amenities, and ratings.

### Create a Trip Schedule

Get organized with a day-by-day plan:
- "Create a day wise schedule"
- Fill in your trip name, dates, and city
- Add activities for each day with times and locations
- Save and view anytime with "Show me my schedule"

### Handle Travel Issues

When things don't go as planned:
- "My flight is delayed by 3 hours" → Get compensation options
- "My flight was cancelled" → See rebooking alternatives instantly
- "Cancel my hotel booking" → View refund policy and alternatives

### Get Smart Recommendations

- "Review my itinerary" → Get suggestions to improve your trip
- "Optimize my schedule" → Save time with better routing
- "Check my budget" → See a breakdown of all expenses

## Project Structure

```
Travix-AI/
├── apps/
│   ├── backend/          # Python/FastAPI server
│   │   ├── app/
│   │   │   ├── api/      # API endpoints
│   │   │   └── services/ # Core logic (agents)
│   │   └── tests/        # Test files
│   │
│   └── frontend/         # React web app
│       └── src/
│           ├── components/ # UI components
│           ├── pages/      # Main pages
│           └── types/      # TypeScript types
│
├── docker-compose.dev.yml  # Development setup
└── .env.example            # Example configuration
```

## Tech Stack

**Backend:**
- Python 3.11
- FastAPI (web framework)
- Groq API (AI intelligence)

**Frontend:**
- React 19
- TypeScript
- Tailwind CSS

**Infrastructure:**
- Docker & Docker Compose
- PostgreSQL (production ready)

## Development

### Running Locally Without Docker

**Backend:**
```bash
cd apps/backend
pip install -r requirements.txt
uvicorn app.main:app --reload
```

**Frontend:**
```bash
cd apps/frontend
npm install
npm run dev
```

### Environment Variables

Create `apps/backend/.env` with:

```env
GROQ_API_KEY=your_groq_api_key
GROQ_MODEL=llama-3.3-70b-versatile
ENVIRONMENT=development
```

## Features in Detail

### Smart Agents

The system uses specialized agents that understand what you need:

1. **Orchestrator** - Routes your requests to the right agent
2. **Flight Agent** - Handles all flight searches and bookings
3. **Hotel Agent** - Manages hotel searches and reservations
4. **Expense Agent** - Tracks your trip spending
5. **Itinerary Agent** - Creates and manages trip schedules
6. **Rebooking Agent** - Handles cancellations and delays
7. **Advisor Agent** - Reviews and optimizes your plans

### Three Views

**Trace View** - See exactly what the system is doing step-by-step

**Flow View** - Visualize how your request moves through different agents

**Result View** - See the final output with forms, lists, or booking confirmations

## Common Questions

**Q: Do I need to pay for anything?**
A: The Groq API has a free tier. The app itself is free to use.

**Q: Where is my data stored?**
A: Currently in memory (resets on restart). You can configure PostgreSQL for permanent storage.

**Q: Can I customize the agents?**
A: Yes! Check the files in `apps/backend/app/services/` to modify agent behavior.

**Q: The system isn't showing results**
A: Make sure your Groq API key is set correctly in `apps/backend/.env` and restart Docker.

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## Support

Having issues? Check these first:

1. Is Docker running?
2. Is the Groq API key set in `.env`?
3. Are ports 5173 and 8000 available?
4. Try `docker-compose down` then `docker-compose -f docker-compose.dev.yml up --build`

Still stuck? Open an issue on GitHub.

## License

[Add your license here]

## Acknowledgments

Built with modern tools and frameworks:
- FastAPI for the robust Python backend
- React for the interactive frontend
- Groq for the intelligent AI capabilities
- Docker for easy deployment

---

**Made with care for travelers who want hassle-free trip planning.**
