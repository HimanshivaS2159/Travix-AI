"""
Expense Agent Service
Handles expense creation, management, trip tracking, and approvals
"""

import logging
import uuid
from datetime import datetime
from typing import Optional, List, Dict, Any
from pydantic import BaseModel

logger = logging.getLogger(__name__)

# In-memory storage
EXPENSES = []
TRIPS = []


# ==================== Models ====================

class ExpenseItem(BaseModel):
    """Individual expense item"""
    expense_id: str
    trip_id: Optional[str] = None
    trip_name: Optional[str] = None
    date: str
    category: str
    merchant: str
    amount: float
    currency: str
    payment_method: str
    gst_amount: Optional[float] = None
    notes: Optional[str] = None
    receipt_url: Optional[str] = None
    status: str = "pending"  # pending, approved, rejected
    created_at: str
    associated_trip: Optional[str] = None
    policy_compliance: str = "compliant"  # compliant, non-compliant, under_review


class Trip(BaseModel):
    """Business trip model"""
    trip_id: str
    trip_name: str
    start_date: str
    end_date: str
    destination: str
    purpose: str
    status: str = "active"  # active, completed, cancelled
    total_expenses: float = 0.0
    currency: str = "INR"
    created_at: str


class ToolResult(BaseModel):
    """Tool result wrapper"""
    action: str
    message: str
    data: Any
    success: bool
    trace: List[Dict] = []


# ==================== Mock Categories ====================

EXPENSE_CATEGORIES = [
    "Flight",
    "Hotel",
    "Food & Dining",
    "Transportation",
    "Fuel",
    "Entertainment",
    "Office Supplies",
    "Client Meeting",
    "Conference",
    "Other"
]

PAYMENT_METHODS = [
    "Corporate Card (Ending 4090)",
    "Personal Card (Reimbursement)",
    "Cash",
    "UPI",
    "Bank Transfer"
]

CURRENCIES = ["INR", "USD", "EUR", "GBP", "AED"]


# ==================== Expense Agent Class ====================

class ExpenseAgent:
    """Agent for expense management and trip tracking"""

    def __init__(self):
        self.expenses = EXPENSES
        self.trips = TRIPS

    def execute(self, user_message: str) -> ToolResult:
        """
        Execute Expense Agent based on user message
        
        Args:
            user_message: User's natural language request
            
        Returns:
            ToolResult with expense data or form
        """
        logger.info(f"Expense Agent executing: {user_message}")
        
        message_lower = user_message.lower()
        trace = self._generate_initial_trace()

        # Determine intent
        if "create" in message_lower and "expense" in message_lower:
            return self.create_expense_form(trace)
        
        elif "show" in message_lower and "expense" in message_lower:
            return self.show_expenses(trace)
        
        elif "list" in message_lower and "expense" in message_lower:
            return self.show_expenses(trace)
        
        elif "create" in message_lower and "trip" in message_lower:
            return self.create_trip_form(trace)
        
        elif "show" in message_lower and "trip" in message_lower:
            return self.show_trips(trace)
        
        elif "approve" in message_lower and "expense" in message_lower:
            return self.approve_expenses_form(trace)
        
        else:
            return ToolResult(
                action="help",
                message="I can help you with: 1) Create expense 2) Show expenses 3) Create trip 4) Show trips 5) Approve expenses",
                data={"suggestions": [
                    "Create an expense",
                    "Show my expenses",
                    "Create a trip",
                    "Show my trips",
                    "Approve expenses"
                ]},
                success=True,
                trace=trace
            )

    def create_expense_form(self, trace: List[Dict]) -> ToolResult:
        """Return form for creating expense"""
        trace.append(self._generate_trace_event(
            "trace-2",
            "tool",
            "create_expense",
            "completed",
            "Expense creation form prepared"
        ))

        return ToolResult(
            action="create_expense",
            message="Let's create an expense. Please fill in the details:",
            data={
                "form_type": "expense_creator",
                "expense_id": f"EXP-{datetime.now().strftime('%Y')}-{len(self.expenses) + 1:03d}",
                "categories": EXPENSE_CATEGORIES,
                "payment_methods": PAYMENT_METHODS,
                "currencies": CURRENCIES,
                "trips": [{"id": trip["trip_id"], "name": trip["trip_name"]} for trip in self.trips],
                "fields": [
                    {
                        "section": "Expense Core Details",
                        "section_id": "expense_core",
                        "fields": [
                            {
                                "name": "expense_id",
                                "label": "Expense ID (Auto-generated)",
                                "type": "text",
                                "value": f"EXP-{datetime.now().strftime('%Y')}-{len(self.expenses) + 1:03d}",
                                "readonly": True,
                                "required": True
                            },
                            {
                                "name": "date",
                                "label": "Date",
                                "type": "date",
                                "placeholder": "Select date",
                                "required": True
                            },
                            {
                                "name": "category",
                                "label": "Category",
                                "type": "select",
                                "options": EXPENSE_CATEGORIES,
                                "placeholder": "Select category",
                                "required": True
                            },
                            {
                                "name": "merchant",
                                "label": "Merchant / Vendor Name",
                                "type": "text",
                                "placeholder": "e.g. Marriott Executive Suites, Indigo, Uber...",
                                "required": True
                            },
                            {
                                "name": "amount",
                                "label": "Amount",
                                "type": "number",
                                "placeholder": "e.g. 10000",
                                "required": True
                            },
                            {
                                "name": "currency",
                                "label": "Currency",
                                "type": "select",
                                "options": CURRENCIES,
                                "default": "INR",
                                "required": True
                            }
                        ]
                    },
                    {
                        "section": "Corporate Audit & Policy",
                        "section_id": "corporate_audit",
                        "description": "Policy Compliance Checklist",
                        "fields": [
                            {
                                "name": "associated_trip",
                                "label": "Associated Trip",
                                "type": "select",
                                "options": ["None"] + [trip["trip_name"] for trip in self.trips],
                                "placeholder": "Business Trip • July 2026",
                                "required": False
                            },
                            {
                                "name": "payment_method",
                                "label": "Payment Method",
                                "type": "select",
                                "options": PAYMENT_METHODS,
                                "required": True
                            },
                            {
                                "name": "gst_amount",
                                "label": "GST / Tax Amount (₹)",
                                "type": "number",
                                "placeholder": "Auto-calculated from bill",
                                "required": False
                            },
                            {
                                "name": "notes",
                                "label": "Notes / Business Purpose",
                                "type": "textarea",
                                "placeholder": "Specify client meeting details, purpose of trip, or exchange rate...",
                                "required": False
                            }
                        ]
                    },
                    {
                        "section": "Receipt & Invoice Upload",
                        "section_id": "receipt_upload",
                        "description": "Upload JPG, PNG or PDF receipts for automated line-item OCR parsing",
                        "fields": [
                            {
                                "name": "receipt",
                                "label": "Receipt Upload",
                                "type": "file",
                                "accept": ".jpg,.jpeg,.png,.pdf",
                                "placeholder": "Drag & drop receipt here, or browse file",
                                "required": False,
                                "ocr_ready": True
                            }
                        ]
                    }
                ]
            },
            success=True,
            trace=trace
        )

    def save_expense(self, expense_data: Dict) -> ToolResult:
        """Save expense to in-memory storage"""
        trace = self._generate_initial_trace()
        trace.append(self._generate_trace_event(
            "trace-2",
            "tool",
            "create_expense",
            "processing",
            "Validating expense data"
        ))

        try:
            # Validate required fields
            required_fields = ["date", "category", "merchant", "amount", "currency", "payment_method"]
            missing = [f for f in required_fields if f not in expense_data or not expense_data[f]]
            
            if missing:
                return ToolResult(
                    action="error",
                    message=f"Missing required fields: {', '.join(missing)}",
                    data={"missing_fields": missing},
                    success=False,
                    trace=trace
                )

            # Create expense object
            expense_id = expense_data.get("expense_id") or f"EXP-{datetime.now().strftime('%Y')}-{len(self.expenses) + 1:03d}"
            
            # Find associated trip if specified
            trip_id = None
            trip_name = None
            if expense_data.get("associated_trip") and expense_data["associated_trip"] != "None":
                for trip in self.trips:
                    if trip["trip_name"] == expense_data["associated_trip"]:
                        trip_id = trip["trip_id"]
                        trip_name = trip["trip_name"]
                        # Update trip total expenses
                        trip["total_expenses"] += float(expense_data["amount"])
                        break

            expense = {
                "expense_id": expense_id,
                "trip_id": trip_id,
                "trip_name": trip_name,
                "date": expense_data["date"],
                "category": expense_data["category"],
                "merchant": expense_data["merchant"],
                "amount": float(expense_data["amount"]),
                "currency": expense_data["currency"],
                "payment_method": expense_data["payment_method"],
                "gst_amount": float(expense_data.get("gst_amount", 0)) if expense_data.get("gst_amount") else None,
                "notes": expense_data.get("notes"),
                "receipt_url": expense_data.get("receipt_url"),
                "status": "pending",
                "policy_compliance": "compliant",
                "associated_trip": expense_data.get("associated_trip"),
                "created_at": datetime.now().isoformat()
            }

            trace.append(self._generate_trace_event(
                "trace-3",
                "booking",
                "create_expense",
                "completed",
                f"Expense {expense_id} created"
            ))

            # Save to in-memory storage
            self.expenses.insert(0, expense)

            return ToolResult(
                action="expense_created",
                message=f"✓ Expense '{expense_id}' created successfully!",
                data={
                    "expense": expense,
                    "total_expenses": len(self.expenses)
                },
                success=True,
                trace=trace
            )

        except Exception as e:
            logger.error(f"Error saving expense: {e}")
            trace.append(self._generate_trace_event(
                "trace-3",
                "error",
                "create_expense",
                "failed",
                str(e)
            ))
            return ToolResult(
                action="error",
                message=f"Error saving expense: {str(e)}",
                data={},
                success=False,
                trace=trace
            )

    def show_expenses(self, trace: List[Dict]) -> ToolResult:
        """Show all expenses"""
        trace.append(self._generate_trace_event(
            "trace-2",
            "tool",
            "show_expenses",
            "completed",
            f"Retrieved {len(self.expenses)} expenses"
        ))

        if not self.expenses:
            return ToolResult(
                action="show_expenses",
                message="No expenses found. Create your first expense!",
                data={"expenses": []},
                success=True,
                trace=trace
            )

        # Calculate statistics
        total_amount = sum(e["amount"] for e in self.expenses)
        pending_count = sum(1 for e in self.expenses if e["status"] == "pending")
        approved_count = sum(1 for e in self.expenses if e["status"] == "approved")

        return ToolResult(
            action="show_expenses",
            message=f"Found {len(self.expenses)} expense(s):",
            data={
                "expenses": self.expenses,
                "total": len(self.expenses),
                "statistics": {
                    "total_amount": total_amount,
                    "pending_count": pending_count,
                    "approved_count": approved_count,
                    "average_amount": total_amount / len(self.expenses) if self.expenses else 0
                }
            },
            success=True,
            trace=trace
        )

    def create_trip_form(self, trace: List[Dict]) -> ToolResult:
        """Return form for creating trip"""
        trace.append(self._generate_trace_event(
            "trace-2",
            "tool",
            "create_trip",
            "completed",
            "Trip creation form prepared"
        ))

        return ToolResult(
            action="create_trip",
            message="Let's create a business trip. Please fill in the details:",
            data={
                "form_type": "trip_creator",
                "fields": [
                    {
                        "name": "trip_name",
                        "label": "Trip Name",
                        "type": "text",
                        "placeholder": "e.g., Business Trip • July 2026",
                        "required": True
                    },
                    {
                        "name": "start_date",
                        "label": "Start Date",
                        "type": "date",
                        "required": True
                    },
                    {
                        "name": "end_date",
                        "label": "End Date",
                        "type": "date",
                        "required": True
                    },
                    {
                        "name": "destination",
                        "label": "Destination",
                        "type": "text",
                        "placeholder": "e.g., Mumbai, India",
                        "required": True
                    },
                    {
                        "name": "purpose",
                        "label": "Purpose",
                        "type": "textarea",
                        "placeholder": "Describe the purpose of the trip",
                        "required": True
                    }
                ]
            },
            success=True,
            trace=trace
        )

    def save_trip(self, trip_data: Dict) -> ToolResult:
        """Save trip to in-memory storage"""
        trace = self._generate_initial_trace()
        trace.append(self._generate_trace_event(
            "trace-2",
            "tool",
            "create_trip",
            "processing",
            "Validating trip data"
        ))

        try:
            # Create trip object
            trip_id = f"TRIP-{len(self.trips) + 1:03d}"
            
            trip = {
                "trip_id": trip_id,
                "trip_name": trip_data["trip_name"],
                "start_date": trip_data["start_date"],
                "end_date": trip_data["end_date"],
                "destination": trip_data["destination"],
                "purpose": trip_data["purpose"],
                "status": "active",
                "total_expenses": 0.0,
                "currency": "INR",
                "created_at": datetime.now().isoformat()
            }

            trace.append(self._generate_trace_event(
                "trace-3",
                "booking",
                "create_trip",
                "completed",
                f"Trip {trip_id} created"
            ))

            # Save to in-memory storage
            self.trips.insert(0, trip)

            return ToolResult(
                action="trip_created",
                message=f"✓ Trip '{trip_data['trip_name']}' created successfully!",
                data={"trip": trip},
                success=True,
                trace=trace
            )

        except Exception as e:
            logger.error(f"Error saving trip: {e}")
            return ToolResult(
                action="error",
                message=f"Error saving trip: {str(e)}",
                data={},
                success=False,
                trace=trace
            )

    def show_trips(self, trace: List[Dict]) -> ToolResult:
        """Show all trips"""
        trace.append(self._generate_trace_event(
            "trace-2",
            "tool",
            "show_trips",
            "completed",
            f"Retrieved {len(self.trips)} trips"
        ))

        if not self.trips:
            return ToolResult(
                action="show_trips",
                message="No trips found. Create your first trip!",
                data={"trips": []},
                success=True,
                trace=trace
            )

        return ToolResult(
            action="show_trips",
            message=f"Found {len(self.trips)} trip(s):",
            data={
                "trips": self.trips,
                "total": len(self.trips)
            },
            success=True,
            trace=trace
        )

    def approve_expenses_form(self, trace: List[Dict]) -> ToolResult:
        """Show pending expenses for approval"""
        trace.append(self._generate_trace_event(
            "trace-2",
            "tool",
            "approve_expenses",
            "completed",
            "Loaded pending expenses"
        ))

        pending_expenses = [e for e in self.expenses if e["status"] == "pending"]

        return ToolResult(
            action="approve_expenses",
            message=f"Found {len(pending_expenses)} expense(s) pending approval:",
            data={
                "expenses": pending_expenses,
                "total_pending": len(pending_expenses)
            },
            success=True,
            trace=trace
        )

    def approve_expense(self, expense_id: str, status: str, notes: Optional[str] = None) -> ToolResult:
        """Approve or reject an expense"""
        trace = self._generate_initial_trace()
        
        for expense in self.expenses:
            if expense["expense_id"] == expense_id:
                expense["status"] = status
                if notes:
                    expense["approval_notes"] = notes
                expense["approved_at"] = datetime.now().isoformat()
                
                trace.append(self._generate_trace_event(
                    "trace-2",
                    "approval",
                    "approve_expense",
                    "completed",
                    f"Expense {expense_id} {status}"
                ))
                
                return ToolResult(
                    action="expense_approved",
                    message=f"✓ Expense {expense_id} has been {status}!",
                    data={"expense": expense},
                    success=True,
                    trace=trace
                )
        
        return ToolResult(
            action="error",
            message=f"Expense {expense_id} not found",
            data={},
            success=False,
            trace=trace
        )

    def _generate_initial_trace(self) -> List[Dict]:
        """Generate initial trace event"""
        return [
            self._generate_trace_event(
                "trace-1",
                "agent",
                "expense_agent",
                "completed",
                "Expense Agent processing started"
            )
        ]

    def _generate_trace_event(self, event_id: str, event_type: str, name: str, 
                             status: str, output: str) -> Dict:
        """Generate a trace event"""
        return {
            "id": event_id,
            "type": event_type,
            "name": name,
            "agent": "expense_agent",
            "status": status,
            "output_summary": output,
            "duration_ms": 50,
            "timestamp": datetime.now().isoformat()
        }
