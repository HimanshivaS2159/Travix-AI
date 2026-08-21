# 🚀 Trip Expense Tracker - Complete Setup Guide

## Overview

A complete **Excel-based expense tracking system** built with:
- **Backend**: FastAPI + Python + openpyxl
- **Storage**: Excel (.xlsx) files
- **Features**: CRUD operations, filtering, statistics, trip grouping

---

## ✅ Quick Start (5 Minutes)

### 1. Install Dependencies

```bash
cd apps/backend
pip install openpyxl
```

### 2. Start the Server

```bash
python -m uvicorn app.main:app --reload --port 8000
```

### 3. Run the Demo

Open a new terminal:

```bash
cd apps/backend
python demo_expense_tracker.py
```

### 4. Check the Excel File

Open the generated file:
```
apps/backend/data/trip_expenses.xlsx
```

---

## 📋 What Was Built

### Backend Files Created

```
apps/backend/
├── app/
│   ├── services/
│   │   └── expense_tracker.py          # Excel operations (openpyxl)
│   └── api/
│       └── expense_tracker.py          # REST API endpoints
├── tests/
│   └── test_expense_tracker.py         # Pytest tests
├── demo_expense_tracker.py             # Demo script
├── EXPENSE-TRACKER-README.md           # API documentation
└── data/
    └── trip_expenses.xlsx              # Auto-created Excel file
```

### Features Implemented

✅ **CRUD Operations**
- Create expense entries
- Read all expenses (with filters)
- Update existing expenses
- Delete expenses

✅ **Excel Storage**
- Automatic file creation with headers
- Styled headers (blue background, white text)
- Currency formatting (₹#,##0.00)
- Auto-save on every operation
- Persistent data across server restarts

✅ **Filtering**
- Filter by trip name
- Filter by category
- Filter by date range

✅ **Statistics & Summaries**
- Trip-wise totals
- Category-wise totals
- Grand total
- Highest/lowest expenses
- Most expensive trip
- Average expense

✅ **Data Validation**
- Category validation (Food, Travel, Stay, Shopping, Other)
- Amount validation (must be positive)
- Date format validation

---

## 🔌 API Endpoints Summary

### Base URL
```
http://localhost:8000/api/expense-tracker
```

### Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/categories` | Get available categories |
| POST | `/expenses` | Create new expense |
| GET | `/expenses` | Get all expenses (with filters) |
| GET | `/expenses/{id}` | Get specific expense |
| PUT | `/expenses/{id}` | Update expense |
| DELETE | `/expenses/{id}` | Delete expense |
| GET | `/summary` | Get trip-wise summary |
| GET | `/stats` | Get detailed statistics |
| GET | `/trips` | Get all trip names |

---

## 📊 Excel File Structure

**Location:** `apps/backend/data/trip_expenses.xlsx`

**Columns:**
| Column | Type | Example |
|--------|------|---------|
| ID | Auto-increment | 1, 2, 3... |
| Trip Name | Text | "Goa Beach Holiday 2026" |
| Date | Date (YYYY-MM-DD) | "2026-08-15" |
| Category | Text | "Food", "Travel", "Stay" |
| Amount | Currency | ₹1,500.50 |
| Notes | Text | "Dinner at beach restaurant" |

**Features:**
- Blue header row with white text
- Auto-adjusted column widths
- Currency formatting for amounts
- Persistent storage (survives server restart)

---

## 🧪 Testing

### Run Tests

```bash
cd apps/backend
pytest tests/test_expense_tracker.py -v
```

**Test Coverage:**
- File creation
- Add expense
- Get all expenses
- Get by ID
- Update expense
- Delete expense
- Filter by trip
- Filter by category
- Filter by date range
- Summary calculation
- Statistics
- Invalid category handling
- ID auto-increment
- Data persistence

---

## 📝 Example Usage

### Using cURL

```bash
# Create expense
curl -X POST http://localhost:8000/api/expense-tracker/expenses \
  -H "Content-Type: application/json" \
  -d '{
    "trip_name": "Goa Trip",
    "date": "2026-08-15",
    "category": "Food",
    "amount": 1500.50,
    "notes": "Beach dinner"
  }'

# Get all expenses
curl http://localhost:8000/api/expense-tracker/expenses

# Get summary
curl http://localhost:8000/api/expense-tracker/summary

# Filter by trip
curl "http://localhost:8000/api/expense-tracker/expenses?trip_name=Goa%20Trip"

# Update expense
curl -X PUT http://localhost:8000/api/expense-tracker/expenses/1 \
  -H "Content-Type: application/json" \
  -d '{"amount": 1800.00}'

# Delete expense
curl -X DELETE http://localhost:8000/api/expense-tracker/expenses/1
```

### Using Python

```python
import requests

BASE = "http://localhost:8000/api/expense-tracker"

# Create
response = requests.post(f"{BASE}/expenses", json={
    "trip_name": "Goa Trip",
    "date": "2026-08-15",
    "category": "Food",
    "amount": 1500.50,
    "notes": "Beach dinner"
})
print(response.json())

# Read
response = requests.get(f"{BASE}/expenses")
expenses = response.json()["expenses"]

# Summary
response = requests.get(f"{BASE}/summary")
summary = response.json()["summary"]
print(f"Grand Total: ₹{summary['grand_total']}")
```

---

## 🌐 Interactive API Documentation

Once server is running, visit:

**Swagger UI:** http://localhost:8000/docs  
**ReDoc:** http://localhost:8000/redoc

Try all endpoints directly in the browser!

---

## 📈 Demo Script Output

When you run `python demo_expense_tracker.py`, you'll see:

```
╔═══════════════════════════════════════════════════════════╗
║         Trip Expense Tracker - Demo Script               ║
║     Excel-based expense tracking with FastAPI            ║
╚═══════════════════════════════════════════════════════════╝

✅ Server is running!

📂 Step 1: Get Available Categories
============================================================
  Available Categories
============================================================
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

📝 Step 2: Creating Goa Trip Expenses...
✅ Added: Travel - ₹4500.0
✅ Added: Stay - ₹3000.0
✅ Added: Food - ₹1200.0
✅ Added: Shopping - ₹850.0

📝 Step 3: Creating Mumbai Business Trip Expenses...
✅ Added: Travel - ₹2800.0
✅ Added: Stay - ₹4000.0
✅ Added: Food - ₹2500.0

📋 Step 4: Getting All Expenses
============================================================
  All Expenses
============================================================
{
  "success": true,
  "expenses": [...],
  "count": 7
}

📊 Step 5: Getting Summary (Grouped by Trip)
============================================================
  Trip Summary
============================================================
{
  "success": true,
  "summary": {
    "trips": {
      "Goa Beach Holiday 2026": {
        "total": 9550.0,
        "count": 4
      },
      "Mumbai Business Meeting": {
        "total": 9300.0,
        "count": 3
      }
    },
    "grand_total": 18850.0,
    "total_expenses": 7
  }
}
```

---

## 🎯 Use Cases

### 1. Personal Travel Expenses
Track expenses for vacation trips with family or friends.

### 2. Business Travel
Manage corporate travel expenses with proper categorization.

### 3. Expense Reports
Generate trip-wise expense reports from Excel data.

### 4. Budget Planning
Analyze spending patterns by category and trip.

### 5. Reimbursement Claims
Submit Excel file for expense reimbursement.

---

## 🔧 Configuration

### Change Excel File Location

Edit `apps/backend/app/services/expense_tracker.py`:

```python
# Change this line
EXCEL_FILE_PATH = "data/trip_expenses.xlsx"

# To your preferred location
EXCEL_FILE_PATH = "/path/to/your/expenses.xlsx"
```

### Add Custom Categories

Edit `expense_tracker.py`:

```python
CATEGORIES = ["Food", "Travel", "Stay", "Shopping", "Other", "Entertainment", "Medical"]
```

### Change Currency Symbol

Edit `expense_tracker.py` in the `add_expense` method:

```python
# Change this line
cell.number_format = '₹#,##0.00'

# To your currency
cell.number_format = '$#,##0.00'  # Dollar
cell.number_format = '€#,##0.00'  # Euro
cell.number_format = '£#,##0.00'  # Pound
```

---

## 🚀 Next Steps

### Frontend Integration

1. **Create React Component** (already in your project)
2. **Add API calls** using the expense tracker endpoints
3. **Display data** in tables with filters
4. **Add charts** using Chart.js or Recharts

### PDF Export (Future)

Use libraries like:
- `reportlab` - Python PDF generation
- `pypdf` - PDF manipulation
- `weasyprint` - HTML to PDF

Example:
```python
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

def export_to_pdf(expenses):
    pdf = canvas.Canvas("expense_report.pdf", pagesize=letter)
    # Add expense data to PDF
    pdf.save()
```

### Charts/Graphs (Future)

Add endpoint to generate chart data:

```python
@router.get("/chart-data")
async def get_chart_data():
    summary = expense_tracker.get_trip_summary()
    return {
        "pie": summary["categories"],  # Category pie chart
        "bar": summary["trips"]         # Trip bar chart
    }
```

---

## 📚 Documentation

- **API README**: `apps/backend/EXPENSE-TRACKER-README.md`
- **API Docs (Swagger)**: http://localhost:8000/docs
- **Source Code**: `apps/backend/app/services/expense_tracker.py`
- **Tests**: `apps/backend/tests/test_expense_tracker.py`

---

## 🐛 Troubleshooting

### Server Won't Start

**Error:** `ModuleNotFoundError: No module named 'openpyxl'`  
**Solution:** `pip install openpyxl`

### Excel File Not Created

**Error:** Permission denied  
**Solution:** Check write permissions on `data/` directory

### Demo Script Fails

**Error:** Connection refused  
**Solution:** Make sure server is running first

### Tests Fail

**Error:** Import errors  
**Solution:** Install pytest: `pip install pytest`

---

## ✅ Verification Checklist

- [ ] Server starts without errors
- [ ] Excel file created at `data/trip_expenses.xlsx`
- [ ] API docs accessible at http://localhost:8000/docs
- [ ] Demo script runs successfully
- [ ] Tests pass with `pytest`
- [ ] Can create/read/update/delete expenses
- [ ] Excel file updates in real-time
- [ ] Filters work correctly
- [ ] Summary shows correct totals

---

## 🎉 Success!

You now have a fully functional **Excel-based Trip Expense Tracker**!

### What You Can Do:

1. ✅ Add expenses via API
2. ✅ View expenses in Excel
3. ✅ Filter by trip, category, date
4. ✅ Get statistics and summaries
5. ✅ Update/delete expenses
6. ✅ Export Excel for sharing

### Excel File Benefits:

- ✅ Can be opened in Excel/LibreOffice/Google Sheets
- ✅ Can be emailed directly
- ✅ Easy backup (just copy the file)
- ✅ No database required
- ✅ Human-readable format

---

**Version:** 1.0.0  
**Status:** ✅ Ready to Use  
**Last Updated:** August 14, 2026
