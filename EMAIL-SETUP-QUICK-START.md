# Email Integration - Quick Start

## What Was Added

Complete email integration system that allows Travix to:
- ✅ Receive emails from users
- ✅ Process requests through Groq Orchestrator
- ✅ Send AI-powered replies automatically

## Files Created (NEW)

1. `apps/backend/app/services/email_service.py` - Email sending/receiving service
2. `apps/backend/app/api/email.py` - Email API endpoints
3. `EMAIL-INTEGRATION.md` - Complete documentation

## Files Updated

1. `apps/backend/app/main.py` - Added email router
2. `apps/backend/app/config.py` - Added email settings + **FIXED GROQ MODEL**

## Quick Setup (5 Minutes)

### Step 1: Get Gmail App Password

1. Go to https://myaccount.google.com/apppasswords
2. Create app password for "Mail"
3. Copy the 16-character password

### Step 2: Update .env File

Add to `apps/backend/.env`:

```env
# Fix the Groq model (IMPORTANT!)
GROQ_MODEL=llama-3.1-8b-instant

# Email settings
EMAIL_FROM_ADDRESS=your-email@gmail.com
EMAIL_FROM_PASSWORD=your-16-char-app-password
EMAIL_FROM_NAME=Travix AI Assistant
EMAIL_AUTO_REPLY=true
```

### Step 3: Restart Backend

```bash
docker-compose -f docker-compose.dev.yml restart backend
```

### Step 4: Test It

```bash
# Check if email is configured
curl http://localhost:8000/api/email/status

# Check for new emails
curl http://localhost:8000/api/email/check

# Send test email
curl -X POST http://localhost:8000/api/email/send \
  -H "Content-Type: application/json" \
  -d '{
    "to_address": "test@example.com",
    "subject": "Test",
    "body": "Test email from Travix"
  }'
```

## How Users Interact

### User Sends Email:
```
To: your-travix-email@gmail.com
Subject: Flight booking

Search flights from Delhi to Dubai
```

### Travix AI Replies:
```
Hello,

Thank you for contacting Travix AI Assistant!

Your request has been processed by our SBT Agent.

Available Flights:

1. Air India - AI-595
   From: Delhi (14:20)
   To: Dubai (17:15)
   Price: INR 15,200

[... more flights ...]

Best regards,
Travix AI Assistant
```

## API Endpoints

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/api/email/status` | GET | Check if email is configured |
| `/api/email/check` | GET | Check for new emails |
| `/api/email/send` | POST | Send an email |
| `/api/email/process` | POST | Process email through orchestrator |

## Automated Checking

Create a cron job to check emails every 5 minutes:

```bash
*/5 * * * * curl "http://localhost:8000/api/email/check?auto_process=true"
```

Or run the background worker:

```python
# email_worker.py
import time, requests

while True:
    requests.get("http://localhost:8000/api/email/check?auto_process=true")
    time.sleep(60)
```

## What Was Fixed

### GROQ Model Error
**Problem:** Model `llama-3.3-70b-versatile` was decommissioned

**Solution:** Updated to `llama-3.1-8b-instant` in:
- `apps/backend/app/config.py` (default value)
- Updated `.env` example files

This model is:
- ✅ Currently supported by Groq
- ✅ Ultra-fast responses
- ✅ Perfect for routing and simple tasks

## Architecture Flow

```
User Email
    ↓
IMAP (Check Inbox)
    ↓
Groq Orchestrator (Analyze intent)
    ↓
Route to Agent (Flight/Hotel/Itinerary)
    ↓
Agent Processes Request
    ↓
Format Response (Plain + HTML)
    ↓
SMTP (Send Reply)
    ↓
User Receives AI Reply
```

## Security Notes

- ✅ Use Gmail App Passwords (not main password)
- ✅ All connections encrypted (TLS/SSL)
- ✅ Credentials in .env (not in code)
- ✅ .env in .gitignore (never committed)

## Troubleshooting

**"Email configuration not set"**
→ Add EMAIL_FROM_ADDRESS and EMAIL_FROM_PASSWORD to .env

**"GROQ model error"**
→ Already fixed! Just restart backend

**"Login failed"**
→ Use App Password (16 chars), not regular password
→ Enable 2FA on Gmail first

## What You Can Do Now

1. ✅ Users can email travel requests
2. ✅ AI processes and replies automatically  
3. ✅ Supports all agents (Flight, Hotel, Itinerary, etc.)
4. ✅ Formatted responses (plain text + HTML)
5. ✅ Background processing ready

## Next Actions

1. Add email credentials to `.env`
2. Restart backend
3. Test with `/api/email/status`
4. Send test email
5. Set up automated checking (optional)

## Full Documentation

See `EMAIL-INTEGRATION.md` for complete details, examples, and advanced usage.

---

**Email integration complete! Users can now interact via email.** ✉️
