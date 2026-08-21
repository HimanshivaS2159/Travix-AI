"""
Demo Script for Expense Tracker
Run this to see the expense tracker in action
"""

import requests
import json
from datetime import date, timedelta

BASE_URL = "http://localhost:8000/api/expense-tracker"

def print_response(title, response):
    """Pretty print API response"""
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}")
    print(json.dumps(response.json(), indent=2))


def main():
    print("""
╔═══════════════════════════════════════════════════════════╗
║         Trip Expense Tracker - Demo Script               ║
║     Excel-based expense tracking with FastAPI            ║
╚═══════════════════════════════════════════════════════════╝
    """)

    # Check if server is running
    try:
        response = requests.get("http://localhost:8000/health")
        print("✅ Server is running!")
    except requests.exceptions.ConnectionError:
        print("❌ Server is not running!")
        print("   Start it with: python -m uvicorn app.main:app --reload")
        return

    # 1. Get Categories
    print("\n📂 Step 1: Get Available Categories")
    response = requests.get(f"{BASE_URL}/categories")
    print_response("Available Categories", response)

    # 2. Create Goa Trip Expenses
    print("\n📝 Step 2: Creating Goa Trip Expenses...")
    
    goa_expenses = [
        {
            "trip_name": "Goa Beach Holiday 2026",
            "date": "2026-08-15",
            "category": "Travel",
            "amount": 4500.00,
            "notes": "Flight tickets Delhi to Goa"
        },
        {
            "trip_name": "Goa Beach Holiday 2026",
            "date": "2026-08-15",
            "category": "Stay",
            "amount": 3000.00,
            "notes": "Beach resort - 3 nights"
        },
        {
            "trip_name": "Goa Beach Holiday 2026",
            "date": "2026-08-16",
            "category": "Food",
            "amount": 1200.00,
            "notes": "Seafood dinner at beach shack"
        },
        {
            "trip_name": "Goa Beach Holiday 2026",
            "date": "2026-08-17",
            "category": "Shopping",
            "amount": 850.00,
            "notes": "Beach wear and souvenirs"
        }
    ]

    for expense in goa_expenses:
        response = requests.post(f"{BASE_URL}/expenses", json=expense)
        if response.json()["success"]:
            print(f"✅ Added: {expense['category']} - ₹{expense['amount']}")

    # 3. Create Mumbai Business Trip Expenses
    print("\n📝 Step 3: Creating Mumbai Business Trip Expenses...")
    
    mumbai_expenses = [
        {
            "trip_name": "Mumbai Business Meeting",
            "date": "2026-08-20",
            "category": "Travel",
            "amount": 2800.00,
            "notes": "Train ticket to Mumbai"
        },
        {
            "trip_name": "Mumbai Business Meeting",
            "date": "2026-08-20",
            "category": "Stay",
            "amount": 4000.00,
            "notes": "Hotel near office - 2 nights"
        },
        {
            "trip_name": "Mumbai Business Meeting",
            "date": "2026-08-21",
            "category": "Food",
            "amount": 2500.00,
            "notes": "Client lunch at 5-star hotel"
        }
    ]

    for expense in mumbai_expenses:
        response = requests.post(f"{BASE_URL}/expenses", json=expense)
        if response.json()["success"]:
            print(f"✅ Added: {expense['category']} - ₹{expense['amount']}")

    # 4. Get All Expenses
    print("\n📋 Step 4: Getting All Expenses")
    response = requests.get(f"{BASE_URL}/expenses")
    print_response("All Expenses", response)

    # 5. Get Summary
    print("\n📊 Step 5: Getting Summary (Grouped by Trip)")
    response = requests.get(f"{BASE_URL}/summary")
    summary_data = response.json()
    print_response("Trip Summary", response)

    # 6. Get Statistics
    print("\n📈 Step 6: Getting Detailed Statistics")
    response = requests.get(f"{BASE_URL}/stats")
    print_response("Statistics", response)

    # 7. Filter by Trip
    print("\n🔍 Step 7: Filtering Goa Trip Expenses")
    response = requests.get(f"{BASE_URL}/expenses", params={"trip_name": "Goa Beach Holiday 2026"})
    print_response("Goa Trip Expenses Only", response)

    # 8. Filter by Category
    print("\n🔍 Step 8: Filtering Food Expenses")
    response = requests.get(f"{BASE_URL}/expenses", params={"category": "Food"})
    print_response("Food Expenses Only", response)

    # 9. Update an Expense
    print("\n✏️ Step 9: Updating an Expense")
    response = requests.put(
        f"{BASE_URL}/expenses/1",
        json={
            "amount": 5000.00,
            "notes": "Flight tickets - Updated with baggage fee"
        }
    )
    print_response("Updated Expense", response)

    # 10. Get All Trip Names
    print("\n🗺️ Step 10: Getting All Trip Names")
    response = requests.get(f"{BASE_URL}/trips")
    print_response("All Trips", response)

    # 11. Delete an Expense
    print("\n🗑️ Step 11: Deleting an Expense")
    response = requests.delete(f"{BASE_URL}/expenses/4")
    print_response("Delete Result", response)

    # 12. Final Summary
    print("\n📊 Step 12: Final Summary After Changes")
    response = requests.get(f"{BASE_URL}/summary")
    print_response("Updated Summary", response)

    # Print final message
    print(f"\n{'='*60}")
    print("✅ Demo completed successfully!")
    print(f"{'='*60}")
    print("\n📂 Check the Excel file at:")
    print("   apps/backend/data/trip_expenses.xlsx")
    print("\n🌐 Interactive API docs:")
    print("   http://localhost:8000/docs")
    print(f"{'='*60}\n")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("   Make sure the server is running!")
