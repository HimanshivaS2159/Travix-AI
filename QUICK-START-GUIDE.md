# 🚀 Quick Start Guide - Travix AI

## Getting Started in 5 Minutes

### 1. Start the Backend
```bash
cd apps/backend
python -m uvicorn app.main:app --reload --port 8000
```

### 2. Start the Frontend
```bash
cd apps/frontend
npm run dev
```

### 3. Open Browser
Navigate to: `http://localhost:5173`

---

## 📝 Try These Commands

### Local Guide Agent

**Get Attractions**:
```
"Show attractions in Delhi"
"Show attractions in Mumbai"
```

**Get Restaurants**:
```
"Show restaurants in Dubai"
"Show restaurants in Bangalore"
```

**Get Travel Tips**:
```
"Give me travel tips for Delhi"
"Show travel tips for Mumbai"
```

**Get Hidden Gems**:
```
"Show hidden gems in Bangalore"
"What are hidden gems in Dubai"
```

**Complete Guide**:
```
"Complete local guide for Delhi"
```

---

### Trip Management

**Create a Trip**:
```
"Create a trip"
"Create a business trip"
```

Then fill the form:
- Trip Name: e.g., "Mumbai Client Meeting • August 2026"
- Start Date: 2026-08-14
- End Date: 2026-08-16
- Destination: Mumbai, India
- Purpose: Quarterly business review with key clients

**View Your Trips**:
```
"Show my trips"
"List all trips"
```

---

### Expense Management

**Create an Expense**:
```
"Create an expense"
```

Then fill the form:
- **Expense Core Details**:
  - Date: 2026-08-14
  - Category: Hotel
  - Merchant: Marriott Mumbai
  - Amount: 15000
  - Currency: INR

- **Corporate Audit & Policy**:
  - Associated Trip: Select your trip (e.g., "Mumbai Client Meeting")
  - Payment Method: Corporate Card (Ending 4090)
  - GST Amount: 2700
  - Notes: Client meeting accommodation

- **Receipt Upload** (Optional):
  - Drag & drop a receipt file (JPG, PNG, or PDF)

**View Your Expenses**:
```
"Show my expenses"
"List all expenses"
```

---

## 🔄 Complete Workflow Example

### Scenario: Business Trip with Expenses

**Step 1: Create the Trip**
```
You: "Create a business trip"
```
Fill form:
- Trip Name: "Mumbai Q4 Review • August 2026"
- Dates: Aug 14-16, 2026
- Destination: Mumbai, Maharashtra, India
- Purpose: "Quarterly business review with Mumbai team and clients"
- Click "💾 Save Trip"

**Step 2: View Trip Created**
You'll see a success confirmation with trip details.

**Step 3: Create Hotel Expense**
```
You: "Create an expense"
```
Fill form:
- Date: 2026-08-14
- Category: Hotel
- Merchant: Taj Mahal Palace Mumbai
- Amount: 25000
- Currency: INR
- Associated Trip: "Mumbai Q4 Review • August 2026"
- Payment Method: Corporate Card
- GST Amount: 4500
- Notes: "3 nights accommodation for business review"
- Click "💾 Save Expense"

**Step 4: Create Flight Expense**
```
You: "Create an expense"
```
Fill form:
- Date: 2026-08-14
- Category: Flight
- Merchant: IndiGo Airlines
- Amount: 8500
- Currency: INR
- Associated Trip: "Mumbai Q4 Review • August 2026"
- Payment Method: Corporate Card
- Click "💾 Save Expense"

**Step 5: Create Food Expense**
```
You: "Create an expense"
```
Fill form:
- Date: 2026-08-15
- Category: Food & Dining
- Merchant: Trishna Restaurant
- Amount: 4500
- Currency: INR
- Associated Trip: "Mumbai Q4 Review • August 2026"
- Payment Method: Corporate Card
- Notes: "Client dinner meeting"
- Click "💾 Save Expense"

**Step 6: View All Expenses**
```
You: "Show my expenses"
```
You'll see:
- Statistics Dashboard showing total: ₹38,000
- 3 expense cards with all details
- All marked with trip "Mumbai Q4 Review • August 2026"

**Step 7: View Trip Summary**
```
You: "Show my trips"
```
You'll see:
- Trip card for "Mumbai Q4 Review • August 2026"
- Total Expenses: ₹38,000 (auto-calculated!)
- Status: Active
- Duration: 3 days

---

## 🗺️ Planning Your Trip with Local Guide

**Before the Trip**:
```
You: "Complete local guide for Mumbai"
```

**View Different Categories**:
- Click **Attractions** tab → See Gateway of India, Marine Drive, Elephanta Caves
- Click **Restaurants** tab → See Trishna, Britannia & Co, Leopold Cafe
- Click **Travel Tips** tab → Safety tips, best time to visit, currency info
- Click **Hidden Gems** tab → Local markets, street food, authentic experiences

**Save Favorite Places**:
Take notes from the recommendations and plan your itinerary!

---

## 💡 Pro Tips

### For Trip Management:
1. **Create Trip First**: Always create the trip before adding expenses
2. **Descriptive Names**: Use format "City + Purpose + Month/Year"
3. **Accurate Dates**: Double-check start and end dates
4. **Clear Purpose**: Write detailed business purpose for approvals

### For Expense Management:
1. **Link to Trip**: Always select the associated trip from dropdown
2. **Include GST**: Add GST amount for compliant expenses
3. **Add Notes**: Include business justification in notes
4. **Upload Receipt**: Upload receipt immediately while you have it
5. **Check Totals**: Use "Show my trips" to verify trip totals are correct

### For Local Guide:
1. **Research Early**: Check local guide before your trip
2. **Save Info**: Take screenshots or notes from recommendations
3. **Check Tips**: Read travel tips for safety and cultural info
4. **Explore Gems**: Don't miss the hidden gems for authentic experiences

---

## 🎨 UI Tips

### Navigation:
- **Left Sidebar**: Select different sub-agents
- **Chat Panel**: Type natural language commands
- **Result View**: See results, forms, and data displays

### Forms:
- **Required Fields**: Marked with red asterisk (*)
- **Date Pickers**: Click calendar icon to select dates
- **Dropdowns**: Click to see all options
- **Drag & Drop**: Drag receipt files to upload area
- **Buttons**: 
  - Blue = Primary action
  - White = Secondary action
  - Gray = Disabled (processing)

### Status Badges:
- 🔵 **Blue (Active)**: Trip is active
- 🟢 **Green (Approved)**: Expense approved
- 🟡 **Yellow (Pending)**: Waiting for approval
- 🔴 **Red (Rejected/Cancelled)**: Rejected or cancelled

---

## 🐛 Troubleshooting

### "Error: Failed to save expense"
- Check all required fields are filled
- Ensure amount is a valid number
- Verify date format is correct
- Try again or refresh page

### "No trips found"
- Create a trip first using "Create a trip"
- Check if trip was saved successfully
- Try "Show my trips" to refresh

### "Backend not responding"
- Verify backend is running on port 8000
- Check GROQ_API_KEY is set in backend/.env
- Look at backend terminal for errors
- Restart backend server

### Form Not Submitting
- Check for validation errors (red text)
- Fill all required fields (marked with *)
- Wait for previous operation to complete
- Check browser console for errors

---

## 📱 Keyboard Shortcuts

- **Enter**: Send message in chat
- **Escape**: Close modals/forms
- **Tab**: Navigate between form fields
- **Ctrl/Cmd + R**: Refresh page

---

## 🎯 Best Practices

### 1. Trip Planning Workflow
```
1. Research destination with Local Guide
2. Create trip with dates and purpose
3. Add expenses as they occur
4. Review trip totals regularly
5. Submit for approval when complete
```

### 2. Expense Entry Workflow
```
1. Collect receipt immediately
2. Create expense while details are fresh
3. Link to appropriate trip
4. Upload receipt file
5. Add detailed notes
6. Submit same day
```

### 3. Organized Naming
```
✓ Good: "Mumbai Client Review • Q4 2026"
✓ Good: "Dubai Conference • Aug 2026"
✓ Good: "Bangalore Training • Sep 2026"

✗ Avoid: "Trip 1"
✗ Avoid: "Mumbai"
✗ Avoid: "Business Trip"
```

---

## 📊 Understanding Statistics

### Expense Dashboard:
- **Total Amount**: Sum of all expenses (all statuses)
- **Pending**: Expenses awaiting approval
- **Approved**: Expenses that are approved
- **Average**: Total amount ÷ number of expenses

### Trip Dashboard:
- **Total Trips**: Count of all trips
- **Active Trips**: Trips currently ongoing or upcoming
- **Total Expenses**: Sum across all trips

---

## 🔄 Data Flow

```
User Types Command
    ↓
Groq Orchestrator Analyzes
    ↓
Routes to Appropriate Agent
    ↓
Agent Executes Action
    ↓
Returns Result
    ↓
Frontend Displays Result
```

---

## 📞 Support

### Common Questions:

**Q: Can I edit an expense after creating it?**
A: Currently, you need to create a new one. Edit feature coming soon.

**Q: Can I delete a trip?**
A: Currently not available. Status can be changed to "cancelled".

**Q: Do expenses really update trip totals?**
A: Yes! Automatically when you select the associated trip.

**Q: Can I create expenses without a trip?**
A: Yes! Select "None" in Associated Trip dropdown.

**Q: How do I approve expenses?**
A: Use command "Approve expenses" (feature documented, approval flow ready).

---

## 🚀 Quick Commands Cheat Sheet

```
┌─────────────────────────────────────────────────────┐
│  LOCAL GUIDE                                        │
├─────────────────────────────────────────────────────┤
│  "Show attractions in [city]"                       │
│  "Show restaurants in [city]"                       │
│  "Give me travel tips for [city]"                   │
│  "Show hidden gems in [city]"                       │
│  "Complete local guide for [city]"                  │
└─────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────┐
│  TRIP MANAGEMENT                                    │
├─────────────────────────────────────────────────────┤
│  "Create a trip"                                    │
│  "Create a business trip"                           │
│  "Show my trips"                                    │
│  "List all trips"                                   │
└─────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────┐
│  EXPENSE MANAGEMENT                                 │
├─────────────────────────────────────────────────────┤
│  "Create an expense"                                │
│  "Show my expenses"                                 │
│  "List all expenses"                                │
└─────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────┐
│  HOTELS (Existing)                                  │
├─────────────────────────────────────────────────────┤
│  "List hotels in [city]"                            │
│  "Book a hotel in [city]"                           │
│  "Show my bookings"                                 │
└─────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────┐
│  FLIGHTS (Existing)                                 │
├─────────────────────────────────────────────────────┤
│  "Search flights from [city] to [city]"            │
│  "Book a flight"                                    │
│  "Show my flight bookings"                          │
└─────────────────────────────────────────────────────┘
```

---

## ✅ You're Ready!

You now have everything you need to:
- ✅ Plan trips with local recommendations
- ✅ Create and manage business trips
- ✅ Track expenses with receipt uploads
- ✅ Link expenses to trips automatically
- ✅ View statistics and summaries
- ✅ Use natural language for everything

**Happy traveling! 🌍✈️**
