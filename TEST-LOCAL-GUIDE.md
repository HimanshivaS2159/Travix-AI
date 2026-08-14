# How to Test the Local Guide Agent 🧪

This guide will help you verify that the Local Guide Agent is working correctly.

## 🚀 Quick Test (30 seconds)

### Step 1: Test Backend
```bash
cd apps/backend
python tests\test_local_guide_agent.py
```

**Expected Output:**
```
============================================================
Testing Local Guide Agent
============================================================

✓ Get attractions for Delhi - PASSED
✓ Get restaurants for Mumbai - PASSED
✓ Get travel tips for Dubai - PASSED
✓ Get hidden gems for Bangalore - PASSED
✓ Complete local guide for Delhi - PASSED
✓ Unknown city handling - PASSED
✓ No city specified - PASSED

============================================================
✓ All tests completed successfully!
============================================================
```

### Step 2: Test Frontend
```bash
# Terminal 1 - Start Backend
cd apps/backend
python -m uvicorn app.main:app --reload

# Terminal 2 - Start Frontend
cd apps/frontend
npm run dev
```

Open browser: `http://localhost:5173`

### Step 3: Test Queries

Type these in the chat to test each feature:

#### Test 1: Attractions
```
Show me attractions in Delhi
```
**Expected:** Card view with 5 Delhi attractions

#### Test 2: Restaurants
```
Where can I eat in Mumbai?
```
**Expected:** 3 Mumbai restaurants with must-try dishes

#### Test 3: Travel Tips
```
Give me travel tips for Dubai
```
**Expected:** 5 categorized travel tips

#### Test 4: Hidden Gems
```
Hidden gems in Bangalore
```
**Expected:** 5 hidden gem locations

#### Test 5: Complete Guide
```
Complete local guide for Delhi
```
**Expected:** Tabbed interface with all categories

---

## 🔍 Detailed Testing

### Test Each City

#### Delhi
```
"Complete guide for Delhi"
```
Should show:
- 5 attractions (Red Fort, Qutub Minar, India Gate, Lotus Temple, Humayun's Tomb)
- 4 restaurants (Karim's, Paranthe Wali Gali, Indian Accent, Saravana Bhavan)
- 7 travel tips
- 5 hidden gems

#### Mumbai
```
"Show me everything about Mumbai"
```
Should show:
- 3 attractions (Gateway of India, Marine Drive, Elephanta Caves)
- 3 restaurants (Britannia & Co., Leopold Cafe, Trishna)
- 5 travel tips
- 5 hidden gems

#### Dubai
```
"Local guide for Dubai"
```
Should show:
- 2 attractions (Burj Khalifa, Dubai Mall)
- 2 restaurants (Al Fanar, Ravi Restaurant)
- 5 travel tips
- 5 hidden gems

#### Bangalore
```
"What to do in Bangalore?"
```
Should show:
- 2 attractions (Lalbagh Garden, Bangalore Palace)
- 2 restaurants (MTR, Vidyarthi Bhavan)
- 4 travel tips
- 5 hidden gems

### Test Natural Language Variations

Try these different phrasings:

```
"Places to visit in Delhi"
"Best food in Mumbai"
"Travel advice for Dubai"
"Secret spots in Bangalore"
"Where should I eat in Delhi?"
"What attractions are in Mumbai?"
"Give me tips for visiting Dubai"
"Show hidden places in Bangalore"
```

All should route to Local Guide Agent correctly.

### Test UI Tabs

1. Click "Attractions" tab → See attraction cards
2. Click "Restaurants" tab → See restaurant cards
3. Click "Travel Tips" tab → See categorized tips
4. Click "Hidden Gems" tab → See gem grid

### Test Error Handling

#### Unknown City
```
"Show me attractions in Paris"
```
**Expected:** Help message with available cities

#### No City Specified
```
"Show me some attractions"
```
**Expected:** "Please specify a city" message with city list

---

## ✅ Verification Checklist

### Backend
- [ ] Agent service loads without errors
- [ ] All test cases pass
- [ ] Natural language queries work
- [ ] Returns correct data for each city
- [ ] Error handling works for unknown cities

### Frontend
- [ ] LocalGuideView component renders
- [ ] All 4 tabs are clickable
- [ ] Data displays correctly in each tab
- [ ] Icons and badges show properly
- [ ] Responsive design works

### Integration
- [ ] Orchestrator routes to local guide agent
- [ ] Agent appears in sidebar
- [ ] All 5 tools listed
- [ ] Natural queries route correctly
- [ ] Results display in ResultView

### Data Quality
- [ ] All attractions have ratings, fees, tips
- [ ] All restaurants have cuisine, prices, must-try dishes
- [ ] All tips have categories and importance levels
- [ ] All hidden gems have descriptions

---

## 🎯 Expected Behavior

### Query: "Show attractions in Delhi"

**Backend Response:**
```json
{
  "action": "get_attractions",
  "message": "Found 5 top attractions in Delhi!",
  "data": {
    "city": "Delhi",
    "count": 5,
    "attractions": [
      {
        "id": "DEL-ATT-001",
        "name": "Red Fort (Lal Qila)",
        "rating": 4.6,
        "entry_fee": "₹50 (Indians), ₹600 (Foreigners)",
        // ... more fields
      }
    ]
  },
  "success": true
}
```

**Frontend Display:**
- Attractions tab active
- 5 cards showing
- Each card has: name, rating, location, fees, duration, tips
- Clean, professional layout

---

## 🐛 Common Issues

### Issue: "Module not found"
**Solution:**
```bash
cd apps/backend
pip install -r requirements.txt
```

### Issue: "Agent not found in orchestrator"
**Solution:** Verify these files were updated:
- `apps/backend/app/api/orchestrator.py`
- `apps/backend/app/services/groq_orchestrator.py`

### Issue: "Component not rendering"
**Solution:** Check browser console for errors. Verify:
- `LocalGuideView.tsx` exists
- `ResultView.tsx` imports it
- All dependencies installed

### Issue: "No data returned"
**Solution:** Check:
1. Backend is running on port 8000
2. Frontend is configured to connect to backend
3. GROQ_API_KEY is set in backend .env

---

## 📊 Performance Benchmarks

### Expected Response Times
- Backend test suite: < 2 seconds
- Attraction query: < 500ms
- Restaurant query: < 500ms
- Complete guide: < 1 second
- UI render: < 100ms

### Expected Data Sizes
- Single attraction: ~500 bytes
- Single restaurant: ~400 bytes
- Complete guide: ~10KB
- UI bundle: ~50KB

---

## 🎓 Test Scenarios

### Scenario 1: First-Time Traveler
```
User: "I'm traveling to Delhi for the first time"
Agent: Routes to local guide
Result: Complete Delhi guide with all categories
```

### Scenario 2: Food Enthusiast
```
User: "Where's the best food in Mumbai?"
Agent: Routes to local guide
Result: Restaurant recommendations with must-try dishes
```

### Scenario 3: Budget Traveler
```
User: "Free things to do in Delhi"
Agent: Routes to local guide
Result: Shows attractions with "Free" entry fee
```

### Scenario 4: Adventure Seeker
```
User: "Hidden gems in Bangalore"
Agent: Routes to local guide
Result: Off-the-beaten-path locations
```

---

## 🎉 Success Criteria

✅ **Backend Tests Pass**
- All 7 tests green
- No errors in console
- Correct data returned

✅ **Frontend Renders**
- Tabs work smoothly
- Data displays correctly
- UI is responsive

✅ **Natural Language Works**
- Different phrasings understood
- Correct agent routing
- Proper error messages

✅ **Data Quality**
- All fields populated
- Ratings accurate
- Tips are helpful

✅ **User Experience**
- Fast response times
- Beautiful UI
- Easy navigation

---

## 📝 Test Report Template

After testing, fill this out:

```
LOCAL GUIDE AGENT TEST REPORT
Date: _______________
Tester: _______________

BACKEND TESTS
[ ] All tests passing
[ ] No console errors
[ ] Data accuracy verified

FRONTEND TESTS  
[ ] UI renders correctly
[ ] Tabs work properly
[ ] Responsive design OK

INTEGRATION TESTS
[ ] Orchestrator routing works
[ ] Sidebar shows agent
[ ] Natural language queries OK

DATA QUALITY
[ ] All attractions complete
[ ] All restaurants complete
[ ] All tips complete
[ ] All gems complete

OVERALL STATUS
[ ] PASS - Ready for production
[ ] FAIL - Issues found (list below)

ISSUES FOUND:
1. _______________
2. _______________

NOTES:
_______________
```

---

## 🚀 Ready to Test!

Run through all the tests above to verify the Local Guide Agent is working perfectly. If all tests pass, congratulations! The agent is production-ready. 🎊

---

**Happy Testing! 🧪✨**
