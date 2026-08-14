"""
Test Expense Agent
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.services.expense_agent import ExpenseAgent


def test_expense_agent():
    """Test Expense Agent"""
    print("\n" + "="*60)
    print("Testing Expense Agent")
    print("="*60)
    
    agent = ExpenseAgent()
    
    # Test 1: Create expense form
    print("\n1. Testing: Create expense form")
    print("-" * 60)
    result = agent.execute("Create an expense")
    print(f"Action: {result.action}")
    print(f"Message: {result.message}")
    print(f"Form type: {result.data.get('form_type')}")
    print(f"Categories: {len(result.data.get('categories', []))}")
    print(f"Payment methods: {len(result.data.get('payment_methods', []))}")
    
    # Test 2: Save expense
    print("\n2. Testing: Save expense")
    print("-" * 60)
    expense_data = {
        "date": "2026-08-13",
        "category": "Flight",
        "merchant": "Air India",
        "amount": 15000,
        "currency": "INR",
        "payment_method": "Corporate Card (Ending 4090)",
        "gst_amount": 2700,
        "notes": "Business trip to Mumbai"
    }
    result = agent.save_expense(expense_data)
    print(f"Action: {result.action}")
    print(f"Message: {result.message}")
    print(f"Expense ID: {result.data['expense']['expense_id']}")
    print(f"Amount: {result.data['expense']['currency']} {result.data['expense']['amount']}")
    
    # Test 3: Show expenses
    print("\n3. Testing: Show expenses")
    print("-" * 60)
    result = agent.execute("Show my expenses")
    print(f"Action: {result.action}")
    print(f"Message: {result.message}")
    print(f"Total expenses: {result.data['total']}")
    if result.data['statistics']:
        print(f"Total amount: ₹{result.data['statistics']['total_amount']}")
        print(f"Pending: {result.data['statistics']['pending_count']}")
    
    # Test 4: Create trip form
    print("\n4. Testing: Create trip form")
    print("-" * 60)
    result = agent.execute("Create a trip")
    print(f"Action: {result.action}")
    print(f"Message: {result.message}")
    print(f"Form type: {result.data.get('form_type')}")
    
    # Test 5: Save trip
    print("\n5. Testing: Save trip")
    print("-" * 60)
    trip_data = {
        "trip_name": "Mumbai Business Visit • August 2026",
        "start_date": "2026-08-20",
        "end_date": "2026-08-23",
        "destination": "Mumbai, India",
        "purpose": "Client meeting and product demo"
    }
    result = agent.save_trip(trip_data)
    print(f"Action: {result.action}")
    print(f"Message: {result.message}")
    print(f"Trip ID: {result.data['trip']['trip_id']}")
    print(f"Trip name: {result.data['trip']['trip_name']}")
    
    # Test 6: Save expense with trip
    print("\n6. Testing: Save expense with associated trip")
    print("-" * 60)
    expense_data2 = {
        "date": "2026-08-20",
        "category": "Hotel",
        "merchant": "Taj Hotel Mumbai",
        "amount": 8500,
        "currency": "INR",
        "payment_method": "Corporate Card (Ending 4090)",
        "associated_trip": "Mumbai Business Visit • August 2026"
    }
    result = agent.save_expense(expense_data2)
    print(f"Action: {result.action}")
    print(f"Message: {result.message}")
    print(f"Associated trip: {result.data['expense']['trip_name']}")
    
    # Test 7: Show trips
    print("\n7. Testing: Show trips")
    print("-" * 60)
    result = agent.execute("Show my trips")
    print(f"Action: {result.action}")
    print(f"Message: {result.message}")
    print(f"Total trips: {result.data['total']}")
    if result.data['trips']:
        trip = result.data['trips'][0]
        print(f"Trip: {trip['trip_name']}")
        print(f"Total expenses: ₹{trip['total_expenses']}")
    
    # Test 8: Approve expenses form
    print("\n8. Testing: Approve expenses form")
    print("-" * 60)
    result = agent.execute("Approve expenses")
    print(f"Action: {result.action}")
    print(f"Message: {result.message}")
    print(f"Pending expenses: {result.data['total_pending']}")
    
    # Test 9: Approve expense
    print("\n9. Testing: Approve expense")
    print("-" * 60)
    if agent.expenses:
        expense_id = agent.expenses[0]["expense_id"]
        result = agent.approve_expense(expense_id, "approved", "Looks good!")
        print(f"Action: {result.action}")
        print(f"Message: {result.message}")
        print(f"New status: {result.data['expense']['status']}")
    
    print("\n" + "="*60)
    print("✓ All tests completed successfully!")
    print("="*60 + "\n")


if __name__ == "__main__":
    test_expense_agent()
