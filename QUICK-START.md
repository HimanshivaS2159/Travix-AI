# Quick Start Guide

## Current Status

### ✅ Completed
1. Email integration system created
2. Revising Agent UI components created with save functionality and popup notifications
3. Toast notification system implemented
4. `email-validator` dependency added to requirements.txt

### ⚠️ Pending Action
**Backend container needs to be rebuilt** to install the `email-validator` dependency.

## Fix Backend Container Error

The backend is crashing because it needs to rebuild with the new dependency. Run this command:

```bash
docker-compose -f docker-compose.dev.yml up -d --build backend
```

This will:
1. Rebuild the backend Docker image
2. Install `email-validator>=2.0.0`
3. Restart the backend service

## Testing the Revising Agent UI

Once the backend is running:

1. **Access the Dashboard**
   - Open http://localhost (or your configured port)
   - Navigate to the dashboard

2. **Test Each View**:

   **Itinerary Review:**
   ```
   Review my itinerary
   ```
   - Should show suggestions with checkboxes
   - Select suggestions and click "Apply Selected Changes"
   - See success popup notification

   **Booking Review:**
   ```
   Review my bookings
   ```
   - Should show confirmed bookings
   - Click "Save Booking Details"
   - See success popup notification

   **Optimize Schedule:**
   ```
   Optimize my schedule
   ```
   - Should show original vs optimized schedule
   - Click "Save Optimized Schedule"
   - See success popup notification

   **Budget Check:**
   ```
   Check my budget
   ```
   - Should show budget breakdown with progress bars
   - Click "Save Budget Details"
   - See success popup notification

## Features Overview

### Revising Agent Views

1. **Itinerary Review View**
   - Overall score display (color-coded)
   - Score breakdown by category
   - Selectable suggestions with checkboxes
   - Priority badges (High/Medium/Low)
   - Apply button with selection counter
   - Success toast on save

2. **Booking Review View**
   - Booking status banner
   - List of confirmed bookings (hotels/flights)
   - Total cost summary
   - Recommendations section
   - Save button with success toast

3. **Optimize Schedule View**
   - Time saved banner
   - Original vs. optimized schedule comparison
   - Day-by-day breakdown
   - Key improvements list
   - Save button with success toast

4. **Budget Check View**
   - Budget overview (total/spent/remaining)
   - Expense breakdown by category
   - Visual progress bars
   - Percentage calculations
   - Save button with success toast

### Toast Notifications
- ✅ Success (green) - When saving successfully
- ℹ️ Info (blue) - For informational messages
- ❌ Error (red) - For error messages
- Auto-dismiss after 3 seconds
- Multiple toasts supported
- Manual close button

## Architecture

```
User Query → Orchestrator → Revising Agent → Backend Response
                                                    ↓
Frontend ResultView → RevisingAgentView → Appropriate View Component
                                                    ↓
                                          User Clicks Save
                                                    ↓
                                          Toast Notification
```

## File Locations

**Backend:**
- `apps/backend/app/services/revising_agent.py` - Revising agent logic
- `apps/backend/app/services/email_service.py` - Email integration
- `apps/backend/app/api/email.py` - Email endpoints
- `apps/backend/requirements.txt` - Dependencies (includes email-validator)

**Frontend:**
- `apps/frontend/src/components/dashboard/RevisingAgentView.tsx` - All revising agent views
- `apps/frontend/src/components/ui/Toast.tsx` - Toast notification system
- `apps/frontend/src/components/dashboard/ResultView.tsx` - Main result view (updated)
- `apps/frontend/src/App.tsx` - App root (added ToastContainer)

## Troubleshooting

### Backend won't start
- **Issue**: `ModuleNotFoundError: No module named 'email_validator'`
- **Fix**: Rebuild backend container:
  ```bash
  docker-compose -f docker-compose.dev.yml down
  docker-compose -f docker-compose.dev.yml up -d --build backend
  ```

### Toast notifications not showing
- **Issue**: Toast container not initialized
- **Fix**: Verify `ToastContainer` is added to `App.tsx`

### Revising agent views not displaying
- **Issue**: Action type mismatch
- **Fix**: Check backend returns correct action names:
  - `review_itinerary`
  - `review_booking`
  - `optimize_schedule`
  - `check_budget`

## Next Steps

1. Rebuild backend container (see command above)
2. Test each revising agent view
3. Verify popup notifications work
4. Test email integration (if needed)
5. Consider adding:
   - Actual API persistence for saves
   - Loading states
   - Error handling
   - PDF export functionality
