"""
Expense Tracker API Endpoints
RESTful API for Excel-based expense tracking
"""

from fastapi import APIRouter, HTTPException, Query
from typing import Optional, List
from pydantic import BaseModel, Field
from datetime import date
import logging

from ..services.expense_tracker import expense_tracker, CATEGORIES

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/expense-tracker", tags=["expense-tracker"])


# ==================== Request Models ====================

class ExpenseCreate(BaseModel):
    """Model for creating a new expense"""
    trip_name: str = Field(..., min_length=1, max_length=100, description="Name of the trip")
    date: str = Field(..., description="Date in YYYY-MM-DD format")
    category: str = Field(..., description="Expense category")
    amount: float = Field(..., gt=0, description="Expense amount (must be positive)")
    notes: Optional[str] = Field("", max_length=500, description="Optional notes")

    class Config:
        json_schema_extra = {
            "example": {
                "trip_name": "Goa Trip 2026",
                "date": "2026-08-15",
                "category": "Food",
                "amount": 1500.50,
                "notes": "Dinner at beach restaurant"
            }
        }


class ExpenseUpdate(BaseModel):
    """Model for updating an expense"""
    trip_name: Optional[str] = Field(None, min_length=1, max_length=100)
    date: Optional[str] = None
    category: Optional[str] = None
    amount: Optional[float] = Field(None, gt=0)
    notes: Optional[str] = Field(None, max_length=500)

    class Config:
        json_schema_extra = {
            "example": {
                "amount": 1800.00,
                "notes": "Updated amount after tip"
            }
        }


# ==================== Endpoints ====================

@router.get("/categories")
async def get_categories():
    """Get list of available expense categories"""
    return {
        "categories": CATEGORIES,
        "count": len(CATEGORIES)
    }


@router.post("/expenses")
async def create_expense(expense: ExpenseCreate):
    """
    Create a new expense entry
    
    - **trip_name**: Name of the trip
    - **date**: Date in YYYY-MM-DD format
    - **category**: One of: Food, Travel, Stay, Shopping, Other
    - **amount**: Expense amount (positive number)
    - **notes**: Optional notes about the expense
    """
    try:
        result = expense_tracker.add_expense(
            trip_name=expense.trip_name,
            date=expense.date,
            category=expense.category,
            amount=expense.amount,
            notes=expense.notes
        )
        return {
            "success": True,
            "message": f"Expense added successfully with ID {result['id']}",
            "expense": result
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Error creating expense: {e}")
        raise HTTPException(status_code=500, detail="Failed to create expense")


@router.get("/expenses")
async def get_expenses(
    trip_name: Optional[str] = Query(None, description="Filter by trip name"),
    category: Optional[str] = Query(None, description="Filter by category"),
    start_date: Optional[str] = Query(None, description="Start date (YYYY-MM-DD)"),
    end_date: Optional[str] = Query(None, description="End date (YYYY-MM-DD)")
):
    """
    Get all expenses with optional filters
    
    - **trip_name**: Filter by specific trip name
    - **category**: Filter by expense category
    - **start_date**: Filter expenses from this date onwards
    - **end_date**: Filter expenses up to this date
    """
    try:
        # Apply filters
        if trip_name:
            expenses = expense_tracker.get_expenses_by_trip(trip_name)
        elif category:
            if category not in CATEGORIES:
                raise HTTPException(status_code=400, detail=f"Invalid category. Must be one of: {', '.join(CATEGORIES)}")
            expenses = expense_tracker.get_expenses_by_category(category)
        elif start_date and end_date:
            expenses = expense_tracker.get_expenses_by_date_range(start_date, end_date)
        else:
            expenses = expense_tracker.get_all_expenses()

        return {
            "success": True,
            "expenses": expenses,
            "count": len(expenses)
        }
    except Exception as e:
        logger.error(f"Error getting expenses: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve expenses")


@router.get("/expenses/{expense_id}")
async def get_expense(expense_id: int):
    """Get a specific expense by ID"""
    try:
        expense = expense_tracker.get_expense_by_id(expense_id)
        if expense is None:
            raise HTTPException(status_code=404, detail=f"Expense with ID {expense_id} not found")
        
        return {
            "success": True,
            "expense": expense
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting expense {expense_id}: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve expense")


@router.put("/expenses/{expense_id}")
async def update_expense(expense_id: int, expense: ExpenseUpdate):
    """
    Update an existing expense
    
    Only provide the fields you want to update. Other fields will remain unchanged.
    """
    try:
        # Check if expense exists
        existing = expense_tracker.get_expense_by_id(expense_id)
        if existing is None:
            raise HTTPException(status_code=404, detail=f"Expense with ID {expense_id} not found")

        # Update expense
        result = expense_tracker.update_expense(
            expense_id=expense_id,
            trip_name=expense.trip_name,
            date=expense.date,
            category=expense.category,
            amount=expense.amount,
            notes=expense.notes
        )

        return {
            "success": True,
            "message": f"Expense ID {expense_id} updated successfully",
            "expense": result
        }
    except HTTPException:
        raise
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Error updating expense {expense_id}: {e}")
        raise HTTPException(status_code=500, detail="Failed to update expense")


@router.delete("/expenses/{expense_id}")
async def delete_expense(expense_id: int):
    """Delete an expense by ID"""
    try:
        success = expense_tracker.delete_expense(expense_id)
        if not success:
            raise HTTPException(status_code=404, detail=f"Expense with ID {expense_id} not found")
        
        return {
            "success": True,
            "message": f"Expense ID {expense_id} deleted successfully"
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting expense {expense_id}: {e}")
        raise HTTPException(status_code=500, detail="Failed to delete expense")


@router.get("/summary")
async def get_summary():
    """
    Get expense summary
    
    Returns:
    - Summary grouped by trip (total, count, expenses list)
    - Summary grouped by category (total per category)
    - Grand total of all expenses
    - Total number of expenses
    """
    try:
        summary = expense_tracker.get_trip_summary()
        return {
            "success": True,
            "summary": summary
        }
    except Exception as e:
        logger.error(f"Error getting summary: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve summary")


@router.get("/trips")
async def get_trips():
    """Get list of all unique trip names"""
    try:
        trips = expense_tracker.get_all_trip_names()
        return {
            "success": True,
            "trips": trips,
            "count": len(trips)
        }
    except Exception as e:
        logger.error(f"Error getting trips: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve trips")


@router.get("/stats")
async def get_statistics():
    """
    Get detailed statistics
    
    Returns comprehensive statistics including:
    - Total expenses by trip
    - Total expenses by category
    - Average expense amount
    - Highest and lowest expenses
    - Most expensive trip
    """
    try:
        expenses = expense_tracker.get_all_expenses()
        summary = expense_tracker.get_trip_summary()

        if not expenses:
            return {
                "success": True,
                "stats": {
                    "total_expenses": 0,
                    "grand_total": 0,
                    "average_expense": 0,
                    "by_trip": {},
                    "by_category": {},
                    "highest_expense": None,
                    "lowest_expense": None,
                    "most_expensive_trip": None
                }
            }

        # Calculate additional stats
        amounts = [e["amount"] for e in expenses]
        average = sum(amounts) / len(amounts)

        # Find highest and lowest
        highest = max(expenses, key=lambda x: x["amount"])
        lowest = min(expenses, key=lambda x: x["amount"])

        # Find most expensive trip
        most_expensive_trip = max(summary["trips"].items(), key=lambda x: x[1]["total"])

        return {
            "success": True,
            "stats": {
                "total_expenses": len(expenses),
                "grand_total": summary["grand_total"],
                "average_expense": round(average, 2),
                "by_trip": {k: v["total"] for k, v in summary["trips"].items()},
                "by_category": summary["categories"],
                "highest_expense": {
                    "id": highest["id"],
                    "trip_name": highest["trip_name"],
                    "amount": highest["amount"],
                    "category": highest["category"]
                },
                "lowest_expense": {
                    "id": lowest["id"],
                    "trip_name": lowest["trip_name"],
                    "amount": lowest["amount"],
                    "category": lowest["category"]
                },
                "most_expensive_trip": {
                    "name": most_expensive_trip[0],
                    "total": most_expensive_trip[1]["total"],
                    "count": most_expensive_trip[1]["count"]
                }
            }
        }
    except Exception as e:
        logger.error(f"Error getting statistics: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve statistics")
