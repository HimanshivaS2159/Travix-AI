# 📊 Trip Expense Tracker - Excel-Based API

A complete expense tracking system with Excel (.xlsx) file storage, built with FastAPI and openpyxl.

## Features

✅ **CRUD Operations** - Create, Read, Update, Delete expenses
✅ **Excel Storage** - All data persists in `trip_expenses.xlsx`
✅ **Trip Grouping** - Organize expenses by trip name
✅ **Category Tracking** - 5 categories (Food, Travel, Stay, Shopping, Other)
✅ **Advanced Filtering** - Filter by trip, category, or date range
✅ **Real-time Statistics** - Trip summaries, category totals, grand total
✅ **Auto-Save** - Every operation immediately saves to Excel
✅ **Currency Formatting** - Rupee (₹) formatting in Excel

---

## Installation

### 1. Install Dependencies

```bash
cd apps/backend
pip install -r requirements.txt
```

This will install:
- `fastapi` - Web framework
- `uvicorn` - ASGI server
- `openpyxl` - Excel read/write library
- `pydantic` - Data validation

### 2. Start the Server

```bash
python -m uvicorn app.main:app --reload --port 8000
```

The Excel file `data/trip_expenses.xlsx` will be created automatically on first run.

---

## API Endpoints

Base URL: `http://localhost:8000/api/expense-tracker`

### 📝 Create Expense
```http
POST /api/expense-tracker/expenses
Content-Type: application/json

{
  "trip_name": "Goa Trip 2026",
  "date": "2026-08-15",
  "category": "Food",
  "amount": 1500.50,
  "notes": "Dinner at beach restaurant"
}
```

**Response:**
```json
{
  "success": true,
  "message": "Expense added successfully with ID 1",
  "expense": {
    "id": 1,
    "trip_name": "Goa Trip 2026",
    "date": "2026-08-15",
    "category": "Food",
    "amount": 1500.50,
    "notes": "Dinner at beach restaurant"
  }
}
```

---

### 📋 Get All Expenses
```http
GET /api/expense-tracker/expenses
```

**Response:**
```json
{
  "success": true,
  "expenses": [
    {
      "id": 1,
      "trip_name": "Goa Trip 2026",
      "date": "2026-08-15",
      "category": "Food",
      "amount": 1500.50,
      "notes": "Dinner at beach restaurant"
    }
  ],
  "count": 1
}
```

---

### 🔍 Filter Expenses

**By Trip:**
```http
GET /api/expense-tracker/expenses?trip_name=Goa%20Trip%202026
```

**By Category:**
```http
GET /api/expense-tracker/expenses?category=Food
```

**By Date Range:**
```http
GET /api/expense-tracker/expenses?start_date=2026-08-01&end_date=2026-08-31
```

---

### 📌 Get Single Expense
```http
GET /api/expense-tracker/expenses/1
```

**Response:**
```json
{
  "success": true,
  "expense": {
    "id": 1,
    "trip_name": "Goa Trip 2026",
    "date": "2026-08-15",
    "category": "Food",
    "amount": 1500.50,
    "notes": "Dinner at beach restaurant"
  }
}
```

---

### ✏️ Update Expense
```http
PUT /api/expense-tracker/expenses/1
Content-Type: application/json

{
  "amount": 1800.00,
  "notes": "Updated amount after tip"
}
```

**Note:** Only provide fields you want to update. Others remain unchanged.

**Response:**
```json
{
  "success": true,
  "message": "Expense ID 1 updated successfully",
  "expense": {
    "id": 1,
    "trip_name": "Goa Trip 2026",
    "date": "2026-08-15",
    "category": "Food",
    "amount": 1800.00,
    "notes": "Updated amount after tip"
  }
}
```

---

### 🗑️ Delete Expense
```http
DELETE /api/expense-tracker/expenses/1
```

**Response:**
```json
{
  "success": true,
  "message": "Expense ID 1 deleted successfully"
}
```

---

### 📊 Get Summary
```http
GET /api/expense-tracker/summary
```

**Response:**
```json
{
  "success": true,
  "summary": {
    "trips": {
      "Goa Trip 2026": {
        "total": 5420.50,
        "count": 4,
        "expenses": [...]
      },
      "Mumbai Business Trip": {
        "total": 12450.00,
        "count": 7,
        "expenses": [...]
      }
    },
    "categories": {
      "Food": 4500.00,
      "Travel": 8500.00,
      "Stay": 4000.00,
      "Shopping": 870.50,
      "Other": 0.00
    },
    "grand_total": 17870.50,
    "total_expenses": 11
  }
}
```

---

### 🎯 Get Statistics
```http
GET /api/expense-tracker/stats
```

**Response:**
```json
{
  "success": true,
  "stats": {
    "total_expenses": 11,
    "grand_total": 17870.50,
    "average_expense": 1624.59,
    "by_trip": {
      "Goa Trip 2026": 5420.50,
      "Mumbai Business Trip": 12450.00
    },
    "by_category": {
      "Food": 4500.00,
      "Travel": 8500.00,
      "Stay": 4000.00,
      "Shopping": 870.50,
      "Other": 0.00
    },
    "highest_expense": {
      "id": 5,
      "trip_name": "Mumbai Business Trip",
      "amount": 4000.00,
      "category": "Stay"
    },
    "lowest_expense": {
      "id": 8,
      "trip_name": "Goa Trip 2026",
      "amount": 250.00,
      "category": "Food"
    },
    "most_expensive_trip": {
      "name": "Mumbai Business Trip",
      "total": 12450.00,
      "count": 7
    }
  }
}
```

---

### 🗺️ Get All Trip Names
```http
GET /api/expense-tracker/trips
```

**Response:**
```json
{
  "success": true,
  "trips": [
    "Goa Trip 2026",
    "Mumbai Business Trip"
  ],
  "count": 2
}
```

---

### 📂 Get Categories
```http
GET /api/expense-tracker/categories
```

**Response:**
```json
{
  "categories": [
    "Food",
    "Travel",
    "Stay",
    "Shopping",
    "Other"
  ],
  "count": 5
}
```

---

## Excel File Structure

**File Location:** `apps/backend/data/trip_expenses.xlsx`

**Sheet Name:** `Expenses`

**Columns:**
| Column | Type | Description |
|--------|------|-------------|
| ID | Integer | Auto-incremented unique identifier |
| Trip Name | String | Name of the trip |
| Date | String | Date in YYYY-MM-DD format |
| Category | String | One of: Food, Travel, Stay, Shopping, Other |
| Amount | Number | Expense amount (formatted as ₹#,##0.00) |
| Notes | String | Optional notes about the expense |

**Example:**
| ID | Trip Name | Date | Category | Amount | Notes |
|----|-----------|------|----------|--------|-------|
| 1 | Goa Trip 2026 | 2026-08-15 | Food | ₹1,500.50 | Dinner at beach restaurant |
| 2 | Goa Trip 2026 | 2026-08-16 | Travel | ₹2,000.00 | Taxi to airport |
| 3 | Mumbai Business Trip | 2026-08-20 | Stay | ₹4,000.00 | Hotel for 2 nights |

---

## Testing with cURL

### Add an Expense
```bash
curl -X POST http://localhost:8000/api/expense-tracker/expenses \
  -H "Content-Type: application/json" \
  -d '{
    "trip_name": "Goa Trip 2026",
    "date": "2026-08-15",
    "category": "Food",
    "amount": 1500.50,
    "notes": "Dinner at beach restaurant"
  }'
```

### Get All Expenses
```bash
curl http://localhost:8000/api/expense-tracker/expenses
```

### Filter by Trip
```bash
curl "http://localhost:8000/api/expense-tracker/expenses?trip_name=Goa%20Trip%202026"
```

### Update an Expense
```bash
curl -X PUT http://localhost:8000/api/expense-tracker/expenses/1 \
  -H "Content-Type: application/json" \
  -d '{
    "amount": 1800.00
  }'
```

### Delete an Expense
```bash
curl -X DELETE http://localhost:8000/api/expense-tracker/expenses/1
```

### Get Summary
```bash
curl http://localhost:8000/api/expense-tracker/summary
```

---

## Testing with Python

```python
import requests

BASE_URL = "http://localhost:8000/api/expense-tracker"

# Create expense
response = requests.post(f"{BASE_URL}/expenses", json={
    "trip_name": "Goa Trip 2026",
    "date": "2026-08-15",
    "category": "Food",
    "amount": 1500.50,
    "notes": "Dinner"
})
print(response.json())

# Get all expenses
response = requests.get(f"{BASE_URL}/expenses")
print(response.json())

# Get summary
response = requests.get(f"{BASE_URL}/summary")
print(response.json())
```

---

## Interactive API Documentation

Once the server is running, visit:

**Swagger UI:** http://localhost:8000/docs  
**ReDoc:** http://localhost:8000/redoc

These provide interactive API documentation where you can test all endpoints directly in the browser.

---

## Data Persistence

### How It Works
1. **First Run**: Excel file created with headers at `data/trip_expenses.xlsx`
2. **Add Expense**: New row appended to Excel, auto-incremented ID
3. **Update Expense**: Specific row modified in Excel
4. **Delete Expense**: Row removed from Excel
5. **Read Operations**: Data loaded from Excel on each request

### File Management
- Excel file is created automatically if missing
- All operations immediately save to disk
- No in-memory caching - always reads from Excel
- **Backup recommended**: Copy `trip_expenses.xlsx` before major operations

---

## Categories

The system supports 5 predefined categories:

1. **Food** - Restaurant meals, snacks, groceries
2. **Travel** - Flights, trains, taxis, fuel
3. **Stay** - Hotels, hostels, Airbnb
4. **Shopping** - Souvenirs, clothes, shopping
5. **Other** - Miscellaneous expenses

---

## Error Handling

### Common Errors

**400 Bad Request** - Invalid data
```json
{
  "detail": "Invalid category. Must be one of: Food, Travel, Stay, Shopping, Other"
}
```

**404 Not Found** - Expense doesn't exist
```json
{
  "detail": "Expense with ID 999 not found"
}
```

**500 Internal Server Error** - Server/Excel error
```json
{
  "detail": "Failed to create expense"
}
```

---

## Performance Considerations

### Current Implementation
- **Read Operations**: Loads entire Excel file into memory
- **Write Operations**: Reads file, modifies, saves back
- **Suitable For**: Up to ~10,000 expenses
- **Not Recommended For**: Real-time, high-frequency operations

### Optimization Tips
1. **Batch Operations**: Group multiple updates together
2. **Caching**: Cache trip names and categories
3. **Indexing**: For large files, consider database migration
4. **File Locking**: Single-user access recommended

---

## Migration to Database (Future)

If Excel becomes too slow, migrate to SQLite/PostgreSQL:

```sql
CREATE TABLE expenses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    trip_name VARCHAR(100) NOT NULL,
    date DATE NOT NULL,
    category VARCHAR(20) NOT NULL,
    amount DECIMAL(10, 2) NOT NULL,
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_trip_name ON expenses(trip_name);
CREATE INDEX idx_category ON expenses(category);
CREATE INDEX idx_date ON expenses(date);
```

---

## Security Considerations

### Current State
- ⚠️ No authentication required
- ⚠️ No authorization checks
- ⚠️ File system access not restricted

### Production Recommendations
1. Add JWT authentication
2. Implement user-specific expense files
3. Add rate limiting
4. Validate file paths (prevent directory traversal)
5. Use environment-based file locations
6. Implement audit logging

---

## Troubleshooting

### Excel File Not Created
**Problem:** `data/trip_expenses.xlsx` doesn't exist  
**Solution:** Check write permissions on `data/` directory

### Permission Denied
**Problem:** Cannot write to Excel file  
**Solution:** 
- Close Excel if file is open
- Check file permissions
- Ensure `data/` directory exists

### Data Not Persisting
**Problem:** Changes not saved to Excel  
**Solution:**
- Check logs for errors
- Verify Excel file path
- Ensure sufficient disk space

### Invalid Category Error
**Problem:** "Invalid category" error  
**Solution:** Use exact category names: Food, Travel, Stay, Shopping, Other

---

## Next Steps

### Frontend Integration

Create a React component to interact with this API:

```typescript
// ExpenseTrackerService.ts
const API_BASE = "http://localhost:8000/api/expense-tracker";

export const expenseAPI = {
  getExpenses: () => fetch(`${API_BASE}/expenses`).then(r => r.json()),
  
  createExpense: (data) => 
    fetch(`${API_BASE}/expenses`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data)
    }).then(r => r.json()),
  
  updateExpense: (id, data) =>
    fetch(`${API_BASE}/expenses/${id}`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data)
    }).then(r => r.json()),
  
  deleteExpense: (id) =>
    fetch(`${API_BASE}/expenses/${id}`, {
      method: 'DELETE'
    }).then(r => r.json()),
  
  getSummary: () => fetch(`${API_BASE}/summary`).then(r => r.json())
};
```

---

## License

Part of Travix AI - Travel & Expense Management System

---

## Support

- **API Docs**: http://localhost:8000/docs
- **Excel File**: `apps/backend/data/trip_expenses.xlsx`
- **Logs**: Check console output for errors

---

**Version:** 1.0.0  
**Last Updated:** August 14, 2026  
**Status:** ✅ Production Ready
