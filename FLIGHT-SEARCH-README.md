# ✈️ TRAVIX AI - Flight Search System

Complete flight search system with **300,153 real flight records** stored in PostgreSQL database.

## 🎯 Overview

The Flight Search System provides comprehensive search and filtering capabilities for flight data including:
- 6 major airlines (Vistara, Air India, Indigo, GO_FIRST, AirAsia, SpiceJet)
- 30 popular routes across India
- Multiple departure times (Morning, Afternoon, Evening, Night, Early_Morning, Late_Night)
- Various stop options (zero, one, two_or_more)
- Price range: ₹1,105 - ₹1,23,071
- Both Economy and Business class

---

## 📊 Database Statistics

- **Total Flights**: 300,153
- **Airlines**: 6
- **Routes**: 30
- **Average Price**: ₹20,890

### Top Airlines:
1. Vistara: 127,859 flights
2. Air_India: 80,892 flights
3. Indigo: 43,120 flights
4. GO_FIRST: 23,173 flights
5. AirAsia: 16,098 flights
6. SpiceJet: 9,011 flights

### Popular Routes:
1. Delhi → Mumbai: 15,289 flights
2. Mumbai → Delhi: 14,809 flights
3. Delhi → Bangalore: 14,012 flights
4. Bangalore → Delhi: 13,756 flights
5. Bangalore → Mumbai: 12,939 flights

---

## 🚀 API Endpoints

Base URL: `http://localhost:8000/api/flights`

### 1. Search Flights
**Endpoint:** `GET /api/flights/search`

Search and filter flights with multiple criteria.

**Query Parameters:**
| Parameter | Type | Description | Example |
|-----------|------|-------------|---------|
| `source_city` | string | Source city | Delhi |
| `destination_city` | string | Destination city | Mumbai |
| `airline` | string | Airline name (partial match) | Indigo |
| `max_price` | float | Maximum price filter | 10000 |
| `stops` | string | Number of stops | zero, one, two_or_more |
| `departure_time` | string | Departure time slot | Morning, Afternoon, Evening |
| `flight_class` | string | Flight class | Economy, Business |
| `page` | integer | Page number (default: 1) | 1 |
| `page_size` | integer | Results per page (default: 50, max: 500) | 100 |

**Example Request:**
```bash
GET /api/flights/search?source_city=Delhi&destination_city=Mumbai&max_price=10000&stops=zero&page=1&page_size=20
```

**Response:**
```json
{
  "success": true,
  "total": 20,
  "page": 1,
  "page_size": 20,
  "flights": [
    {
      "id": 1,
      "airline": "SpiceJet",
      "flight": "SG-8709",
      "source_city": "Delhi",
      "departure_time": "Evening",
      "stops": "zero",
      "arrival_time": "Night",
      "destination_city": "Mumbai",
      "class": "Economy",
      "duration": 2.33,
      "days_left": 47,
      "price": 2281.0
    }
  ]
}
```

---

### 2. Get Statistics
**Endpoint:** `GET /api/flights/statistics`

Get comprehensive database statistics.

**Example Request:**
```bash
GET /api/flights/statistics
```

**Response:**
```json
{
  "total_flights": 300153,
  "total_airlines": 6,
  "total_routes": 30,
  "price_range": {
    "min": 1105.0,
    "max": 123071.0,
    "avg": 20889.66
  },
  "top_airlines": [...],
  "popular_routes": [...]
}
```

---

### 3. Get Filter Options
**Endpoint:** `GET /api/flights/filters`

Get all unique values for dropdown filters.

**Example Request:**
```bash
GET /api/flights/filters
```

**Response:**
```json
{
  "cities": ["Bangalore", "Chennai", "Delhi", "Hyderabad", "Kolkata", "Mumbai"],
  "airlines": ["AirAsia", "Air_India", "GO_FIRST", "Indigo", "SpiceJet", "Vistara"],
  "stops": ["one", "two_or_more", "zero"],
  "departure_times": ["Afternoon", "Early_Morning", "Evening", "Late_Night", "Morning", "Night"],
  "classes": ["Business", "Economy"]
}
```

---

### 4. Get Cheapest Flights
**Endpoint:** `GET /api/flights/cheapest`

Get the cheapest flights for a specific route.

**Query Parameters:**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `source_city` | string | Yes | Source city |
| `destination_city` | string | Yes | Destination city |
| `limit` | integer | No | Number of results (default: 10, max: 50) |

**Example Request:**
```bash
GET /api/flights/cheapest?source_city=Delhi&destination_city=Mumbai&limit=10
```

**Response:**
```json
{
  "success": true,
  "route": "Delhi → Mumbai",
  "total": 10,
  "flights": [...]
}
```

---

### 5. Get Flights by Airline
**Endpoint:** `GET /api/flights/by-airline/{airline}`

Get all flights for a specific airline.

**Path Parameters:**
- `airline`: Airline name

**Query Parameters:**
- `page`: Page number (default: 1)
- `page_size`: Results per page (default: 50, max: 200)

**Example Request:**
```bash
GET /api/flights/by-airline/Indigo?page=1&page_size=50
```

---

### 6. Health Check
**Endpoint:** `GET /api/flights/health`

Check if the flight service is operational.

**Example Request:**
```bash
GET /api/flights/health
```

**Response:**
```json
{
  "status": "healthy",
  "total_flights": 300153
}
```

---

## 🔧 Setup & Installation

### Prerequisites
- Docker & Docker Compose
- PostgreSQL (included in docker-compose)

### Step 1: Build and Start Services
```bash
cd Travix-AI
docker-compose build backend
docker-compose up -d
```

### Step 2: Initialize Flight Database
```bash
docker exec travix-ai-backend-1 python initialize_flights.py
```

This will:
1. Create the `flights` table with proper schema
2. Load all 300,153 flight records from CSV
3. Create database indexes for fast searching
4. Display statistics

---

## 📝 Usage Examples

### Example 1: Search Direct Flights from Delhi to Mumbai
```bash
curl "http://localhost:8000/api/flights/search?source_city=Delhi&destination_city=Mumbai&stops=zero&page_size=10"
```

### Example 2: Find Cheap Vistara Flights
```bash
curl "http://localhost:8000/api/flights/search?airline=Vistara&max_price=15000&page_size=20"
```

### Example 3: Morning Flights with No Stops
```bash
curl "http://localhost:8000/api/flights/search?departure_time=Morning&stops=zero&page_size=50"
```

### Example 4: Business Class Flights
```bash
curl "http://localhost:8000/api/flights/search?flight_class=Business&page_size=20"
```

### Example 5: Get Cheapest Delhi to Bangalore Flights
```bash
curl "http://localhost:8000/api/flights/cheapest?source_city=Delhi&destination_city=Bangalore&limit=5"
```

---

## 🎨 Frontend Integration

### Using JavaScript Fetch API

```javascript
// Search flights
async function searchFlights(params) {
  const queryString = new URLSearchParams(params).toString();
  const response = await fetch(`http://localhost:8000/api/flights/search?${queryString}`);
  const data = await response.json();
  return data.flights;
}

// Example usage
const flights = await searchFlights({
  source_city: 'Delhi',
  destination_city: 'Mumbai',
  max_price: 10000,
  stops: 'zero',
  page_size: 20
});

console.log(flights);
```

### Using React

```jsx
import { useState, useEffect } from 'react';

function FlightSearch() {
  const [flights, setFlights] = useState([]);
  const [filters, setFilters] = useState({
    source_city: 'Delhi',
    destination_city: 'Mumbai',
    max_price: 10000
  });

  useEffect(() => {
    const fetchFlights = async () => {
      const params = new URLSearchParams(filters);
      const response = await fetch(`http://localhost:8000/api/flights/search?${params}`);
      const data = await response.json();
      setFlights(data.flights);
    };
    
    fetchFlights();
  }, [filters]);

  return (
    <div>
      <h2>Flight Search Results</h2>
      {flights.map(flight => (
        <div key={flight.id}>
          <h3>{flight.airline} - {flight.flight}</h3>
          <p>{flight.source_city} → {flight.destination_city}</p>
          <p>₹{flight.price}</p>
        </div>
      ))}
    </div>
  );
}
```

---

## 🗄️ Database Schema

```sql
CREATE TABLE flights (
    id SERIAL PRIMARY KEY,
    index_num INTEGER,
    airline VARCHAR(100),
    flight VARCHAR(50),
    source_city VARCHAR(100),
    departure_time VARCHAR(50),
    stops VARCHAR(20),
    arrival_time VARCHAR(50),
    destination_city VARCHAR(100),
    class VARCHAR(50),
    duration DECIMAL(10,2),
    days_left INTEGER,
    price DECIMAL(10,2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Indexes for fast searching
CREATE INDEX idx_flights_source ON flights(source_city);
CREATE INDEX idx_flights_destination ON flights(destination_city);
CREATE INDEX idx_flights_airline ON flights(airline);
CREATE INDEX idx_flights_price ON flights(price);
CREATE INDEX idx_flights_stops ON flights(stops);
CREATE INDEX idx_flights_departure ON flights(departure_time);
```

---

## 🎯 Key Features

✅ **Fast Search**: Database indexes ensure sub-second search response  
✅ **Multiple Filters**: Combine multiple filters for precise results  
✅ **Pagination**: Handle large result sets efficiently  
✅ **Real Data**: 300K+ real flight records  
✅ **RESTful API**: Standard REST endpoints with JSON responses  
✅ **Comprehensive**: All major Indian routes and airlines  
✅ **Sorted Results**: Results sorted by price (cheapest first)  

---

## 📖 API Documentation

Full interactive API documentation available at:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

---

## 🔍 Testing

Test the API using cURL, Postman, or your browser:

```bash
# Test statistics
curl http://localhost:8000/api/flights/statistics

# Test filters
curl http://localhost:8000/api/flights/filters

# Test search
curl "http://localhost:8000/api/flights/search?source_city=Delhi&destination_city=Mumbai"

# Test health
curl http://localhost:8000/api/flights/health
```

---

## 💡 Tips

1. **Use Pagination**: For large result sets, use pagination to avoid performance issues
2. **Combine Filters**: Combine multiple filters for more precise results
3. **Cache Results**: Consider caching frequently accessed routes
4. **Use Indexes**: The database has proper indexes for fast queries
5. **Monitor Performance**: Check query performance with database EXPLAIN

---

## 🐛 Troubleshooting

### Issue: No flights returned
- Check if database is initialized: `docker exec travix-ai-backend-1 python initialize_flights.py`
- Verify city names match exactly (case-insensitive): Delhi, Mumbai, Bangalore, etc.

### Issue: Slow queries
- Check database indexes are created
- Reduce page_size for faster response
- Use more specific filters to reduce result set

### Issue: Container not running
```bash
docker-compose ps
docker-compose logs backend
docker-compose restart backend
```

---

## 📞 Support

For issues or questions:
1. Check API documentation: http://localhost:8000/docs
2. View container logs: `docker-compose logs backend`
3. Test database connection: `docker exec -it travix-postgres psql -U travix -d travix_db`

---

**🎉 Your flight search system is ready to use with 300,153 flights!**
