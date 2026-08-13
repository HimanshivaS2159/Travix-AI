# Quick Start Guide - Travel Booking System

## 🚀 Get Started in 30 Seconds

### What You Can Do Now

#### 1. **Create a Day-Wise Schedule**
```
In Chat: "Create a day wise schedule"
↓
Opens form to fill:
- Trip name (e.g., "Delhi Adventure 2026")
- Start and end dates
- City selection
- Daily activities with time, location, duration

Submit → Schedule saved ✓
```

#### 2. **View All Your Schedules**
```
In Chat: "Show me my schedule" or "Show me all schedules"
↓
Displays all saved trips with:
- Trip name and city
- Date range and duration
- Expandable daily breakdown
- Copy, Edit, Delete buttons
```

#### 3. **Handle Flight Delay**
```
In Chat: "My flight is delayed by 3 hours"
↓
Shows modal with:
- Delay compensation: ₹3,000
- 3 options to choose from
- You take action immediately
```

#### 4. **Handle Flight Cancellation**
```
In Chat: "My flight was cancelled"
↓
Shows:
- Refund amount: ₹45,000
- 3 airline rebooking options
- Alternative flights with times
- You select preferred option
```

#### 5. **Handle Hotel Cancellation**
```
In Chat: "Cancel my hotel booking"
↓
Shows:
- Refund amount and policy
- 3 alternative hotels
- Prices and ratings
- You choose rebook or accept refund
```

#### 6. **Review Your Trip**
```
In Chat: "Review my itinerary"
↓
Gets 4 suggestions:
- Time pacing issues
- Better routing options
- Meal break recommendations
- Optimized timing
```

#### 7. **Optimize Your Schedule**
```
In Chat: "Optimize my schedule"
↓
Returns:
- Better daily timing
- Improved routing (45 min saved)
- Suggested changes
```

#### 8. **Check Your Budget**
```
In Chat: "Check my budget"
↓
Shows:
- Total budget breakdown
- Hotels, flights, food, activities
- Spent vs remaining
- Percentage breakdown
```

---

## 🎯 What Agents Do What?

| Agent | What It Does | Say This |
|-------|-------------|----------|
| **Itinerary** | Create schedules | "Create a day wise schedule" |
| **Itinerary** | View schedules | "Show me my schedule" |
| **Rebooking** | Handle delays | "My flight is delayed" |
| **Rebooking** | Handle cancellations | "Cancel my flight/hotel" |
| **Revising** | Review plans | "Review my itinerary" |
| **Revising** | Optimize timing | "Optimize my schedule" |
| **Revising** | Check costs | "Check my budget" |

---

## 📱 UI Components

### ScheduleForm
- Fill trip details
- Add multiple days
- Add activities per day
- Auto-save on submit

### ShowSchedules
- View all trips
- Expand/collapse days
- See all activities
- Copy schedule to clipboard

### RebookingModal
- Choose from options
- See compensation/refunds
- Accept or rebook
- Process immediately

---

## 🔧 Technical Details

### Backend Stack
- Python 3.11
- FastAPI
- Groq API (llama-3.3-70b)
- 7 AI agents

### Frontend Stack
- React 19
- TypeScript
- Tailwind CSS
- Real-time updates

### Data Storage
- In-memory (development)
- Ready for PostgreSQL (production)

---

## 📊 Example Flows

### Complete Trip Planning Flow
```
1. User: "Create a day wise schedule"
   → Opens form

2. User: Fills Delhi trip (Aug 14-16)
   → Save schedule

3. User: "Show me my schedule"
   → Displays Delhi trip

4. User: "Review my itinerary"
   → Gets 4 suggestions

5. User: "Optimize my schedule"
   → Saves time on routing

6. User: "My flight is delayed"
   → Modal with options

7. User: Selects "Rebook option"
   → Confirmed ✓

Result: Trip fully planned and rebooking handled!
```

---

## 💡 Pro Tips

1. **Be Specific**: "My flight AI-600 is delayed 3 hours" gives better results than "delayed"

2. **Use Keywords**: System recognizes:
   - "create" + "schedule" = Schedule form
   - "show" + "schedule" = List schedules
   - "delay" + "flight" = Flight delay handling
   - "cancel" + "hotel" = Hotel cancellation
   - "review" + "itinerary" = Review suggestions

3. **One Action at a Time**: Each prompt triggers one agent

4. **Check Trace View**: See exactly what happened in the "Trace View" tab

5. **Flow View**: Visualize the agent's thinking in "Flow View" tab

---

## ⚙️ Configuration

### Available Cities
- Delhi
- Mumbai
- Bangalore
- Goa
- Jaipur

### Compensation Rules
- Flight delay < 2 hours: ₹1,500
- Flight delay 2-4 hours: ₹3,000
- Flight delay > 4 hours: ₹5,000

### Refund Policies
- Full flight refund on cancellation
- 50% hotel refund if cancelled within 48 hours
- Full refund if cancelled >48 hours before check-in

---

## 🎨 UI Theme

- Dark mode (dark blue/gray)
- Light mode for result display (off-white)
- Color-coded agents:
  - Orchestrator: Blue
  - SBT Agent: Cyan
  - Expense Agent: Green
  - BackOffice Agent: Dark Blue
  - **Itinerary Agent: Purple** ← NEW
  - **Rebooking Agent: Red** ← NEW
  - **Revising Agent: Violet** ← NEW

---

## 📞 Support

### Common Issues

**Q: Schedule didn't save?**
- Check if all required fields are filled (trip name, dates, city)
- Try submitting again

**Q: Can't see rebooking options?**
- Make sure you said "delayed" or "cancelled"
- Wait for the modal to appear

**Q: Budget shows 0?**
- This is demo data - in production, it pulls from actual bookings

---

## 🚀 Next Steps

1. ✅ Try creating a schedule
2. ✅ Add multiple days
3. ✅ View and copy schedules
4. ✅ Test rebooking flows
5. ✅ Review and optimize
6. ✅ Check budget breakdown

## 🎉 You're All Set!

Everything is working. Start using the system by typing prompts in the chat box on the left!

**Tip**: Start with "Create a day wise schedule" to see the form in action.
