"""
Tests for Expense Tracker
"""

import pytest
import os
from app.services.expense_tracker import ExpenseTracker, CATEGORIES

# Use a test file
TEST_FILE_PATH = "data/test_expenses.xlsx"


@pytest.fixture
def tracker():
    """Create tracker with test file"""
    original_path = ExpenseTracker().file_path
    tracker = ExpenseTracker()
    tracker.file_path = TEST_FILE_PATH
    tracker._ensure_excel_file()
    yield tracker
    # Cleanup
    if os.path.exists(TEST_FILE_PATH):
        os.remove(TEST_FILE_PATH)


def test_create_expense_file(tracker):
    """Test that Excel file is created"""
    assert os.path.exists(TEST_FILE_PATH)


def test_add_expense(tracker):
    """Test adding an expense"""
    result = tracker.add_expense(
        trip_name="Test Trip",
        date="2026-08-15",
        category="Food",
        amount=1000.00,
        notes="Test expense"
    )
    
    assert result["id"] == 1
    assert result["trip_name"] == "Test Trip"
    assert result["amount"] == 1000.00


def test_get_all_expenses(tracker):
    """Test getting all expenses"""
    # Add multiple expenses
    tracker.add_expense("Trip 1", "2026-08-15", "Food", 1000.00)
    tracker.add_expense("Trip 2", "2026-08-16", "Travel", 2000.00)
    
    expenses = tracker.get_all_expenses()
    assert len(expenses) == 2
    assert expenses[0]["trip_name"] == "Trip 1"
    assert expenses[1]["trip_name"] == "Trip 2"


def test_get_expense_by_id(tracker):
    """Test getting a specific expense"""
    result = tracker.add_expense("Test Trip", "2026-08-15", "Food", 1000.00)
    expense_id = result["id"]
    
    expense = tracker.get_expense_by_id(expense_id)
    assert expense is not None
    assert expense["id"] == expense_id
    assert expense["trip_name"] == "Test Trip"


def test_update_expense(tracker):
    """Test updating an expense"""
    # Add expense
    result = tracker.add_expense("Test Trip", "2026-08-15", "Food", 1000.00)
    expense_id = result["id"]
    
    # Update it
    updated = tracker.update_expense(
        expense_id=expense_id,
        amount=1500.00,
        notes="Updated"
    )
    
    assert updated["amount"] == 1500.00
    assert updated["notes"] == "Updated"
    assert updated["trip_name"] == "Test Trip"  # Unchanged


def test_delete_expense(tracker):
    """Test deleting an expense"""
    # Add expense
    result = tracker.add_expense("Test Trip", "2026-08-15", "Food", 1000.00)
    expense_id = result["id"]
    
    # Delete it
    success = tracker.delete_expense(expense_id)
    assert success is True
    
    # Verify it's gone
    expense = tracker.get_expense_by_id(expense_id)
    assert expense is None


def test_get_expenses_by_trip(tracker):
    """Test filtering by trip name"""
    tracker.add_expense("Goa Trip", "2026-08-15", "Food", 1000.00)
    tracker.add_expense("Mumbai Trip", "2026-08-16", "Travel", 2000.00)
    tracker.add_expense("Goa Trip", "2026-08-17", "Stay", 3000.00)
    
    goa_expenses = tracker.get_expenses_by_trip("Goa Trip")
    assert len(goa_expenses) == 2
    assert all(e["trip_name"] == "Goa Trip" for e in goa_expenses)


def test_get_expenses_by_category(tracker):
    """Test filtering by category"""
    tracker.add_expense("Trip 1", "2026-08-15", "Food", 1000.00)
    tracker.add_expense("Trip 2", "2026-08-16", "Food", 2000.00)
    tracker.add_expense("Trip 3", "2026-08-17", "Travel", 3000.00)
    
    food_expenses = tracker.get_expenses_by_category("Food")
    assert len(food_expenses) == 2
    assert all(e["category"] == "Food" for e in food_expenses)


def test_get_expenses_by_date_range(tracker):
    """Test filtering by date range"""
    tracker.add_expense("Trip 1", "2026-08-10", "Food", 1000.00)
    tracker.add_expense("Trip 2", "2026-08-15", "Travel", 2000.00)
    tracker.add_expense("Trip 3", "2026-08-20", "Stay", 3000.00)
    
    filtered = tracker.get_expenses_by_date_range("2026-08-12", "2026-08-18")
    assert len(filtered) == 1
    assert filtered[0]["date"] == "2026-08-15"


def test_get_trip_summary(tracker):
    """Test getting summary grouped by trip"""
    tracker.add_expense("Goa Trip", "2026-08-15", "Food", 1000.00)
    tracker.add_expense("Goa Trip", "2026-08-16", "Travel", 2000.00)
    tracker.add_expense("Mumbai Trip", "2026-08-17", "Stay", 3000.00)
    
    summary = tracker.get_trip_summary()
    
    assert summary["grand_total"] == 6000.00
    assert summary["total_expenses"] == 3
    assert "Goa Trip" in summary["trips"]
    assert summary["trips"]["Goa Trip"]["total"] == 3000.00
    assert summary["trips"]["Mumbai Trip"]["total"] == 3000.00


def test_get_all_trip_names(tracker):
    """Test getting unique trip names"""
    tracker.add_expense("Goa Trip", "2026-08-15", "Food", 1000.00)
    tracker.add_expense("Mumbai Trip", "2026-08-16", "Travel", 2000.00)
    tracker.add_expense("Goa Trip", "2026-08-17", "Stay", 3000.00)
    
    trip_names = tracker.get_all_trip_names()
    assert len(trip_names) == 2
    assert "Goa Trip" in trip_names
    assert "Mumbai Trip" in trip_names


def test_invalid_category(tracker):
    """Test that invalid category raises error"""
    with pytest.raises(ValueError, match="Invalid category"):
        tracker.add_expense("Test Trip", "2026-08-15", "InvalidCategory", 1000.00)


def test_category_totals(tracker):
    """Test category totals in summary"""
    tracker.add_expense("Trip 1", "2026-08-15", "Food", 1000.00)
    tracker.add_expense("Trip 2", "2026-08-16", "Food", 500.00)
    tracker.add_expense("Trip 3", "2026-08-17", "Travel", 2000.00)
    
    summary = tracker.get_trip_summary()
    
    assert summary["categories"]["Food"] == 1500.00
    assert summary["categories"]["Travel"] == 2000.00
    assert summary["categories"].get("Stay", 0) == 0


def test_auto_increment_id(tracker):
    """Test that IDs auto-increment"""
    result1 = tracker.add_expense("Trip 1", "2026-08-15", "Food", 1000.00)
    result2 = tracker.add_expense("Trip 2", "2026-08-16", "Travel", 2000.00)
    result3 = tracker.add_expense("Trip 3", "2026-08-17", "Stay", 3000.00)
    
    assert result1["id"] == 1
    assert result2["id"] == 2
    assert result3["id"] == 3


def test_persistence_across_instances(tracker):
    """Test that data persists across tracker instances"""
    # Add expense
    tracker.add_expense("Test Trip", "2026-08-15", "Food", 1000.00)
    
    # Create new tracker instance
    new_tracker = ExpenseTracker()
    new_tracker.file_path = TEST_FILE_PATH
    
    # Verify data is still there
    expenses = new_tracker.get_all_expenses()
    assert len(expenses) == 1
    assert expenses[0]["trip_name"] == "Test Trip"
