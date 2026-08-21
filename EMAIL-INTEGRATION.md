# Email Integration for Travix

Complete email integration that connects with the Groq Orchestrator to process travel requests via email.

## Overview

The email system allows users to:
1. **Send travel requests via email** (e.g., "Search flights from Delhi to Dubai")
2. **Receive AI-powered responses** from the orchestrator
3. **Get automatic replies** with booking details, recommendations, etc.

## How It Works

```
User sends email
    ↓
Travix checks inbox
    ↓
Email processed through Groq Orchestrator
    ↓
Routed to appropriate agent (Flight/Hotel/Itinerary)
    ↓
Agent processes request
    ↓
AI-formatted reply sent back to user
```

## Setup Instructions

### 1. Configure Gmail App Password

**For Gmail users:**

1. Go to Google Account → Security
2. Enable 2-Factor Authentication
3. Go to App Passwords: https://myaccount.google.com/apppasswords
4. Create new app password for "Mail"
5. Copy the 16-character password

### 2. Update Environment Variables

Add these to `apps/backend/.env`:

```env
# Email Configuration
EMAIL_SMTP_HOST=smtp.gmail.com
EMAIL_SMTP_PORT=587
EMAIL_IMAP_HOST=imap.gmail.com
EMAIL_IMAP_PORT=993
EMAIL_FROM_ADDRESS=your-email@gmail.com
EMAIL_FROM_PASSWORD=your-16-char-app-password
EMAIL_FROM_NAME=Travix AI Assistant

# Email Agent Settings
EMAIL_CHECK_INTERVAL=60
EMAIL_AUTO_REPLY=true
```

### 3. Fix the Groq Model

The model name in config was outdated. It's already been updated to:
```env
GROQ_MODEL=llama-3.1-8b-instant
```

### 4. Restart Backend

```bash
docker-compose -f docker-compose.dev.yml restart backend
```

## API Endpoints

### 1. Send Email
```http
POST /api/email/send
Content-Type: application/json

{
  "to_address": "user@example.com",
  "subject": "Your Travel Itinerary",
  "body": "Here are your flight details...",
  "html_body": "<h1>Flight Details</h1>..."
}
```

### 2. Check New Emails
```http
GET /api/email/check?limit=10&auto_process=true
```

**Response:**
```json
{
  "success": true,
  "count": 3,
  "emails": [
    {
      "id": "12345",
      "from": "customer@example.com",
      "subject": "Book flight to Dubai",
      "body": "I need to book a flight from Delhi to Dubai...",
      "received_at": "2026-08-21T10:30:00"
    }
  ],
  "processed": 3
}
```

### 3. Process Email (Manual)
```http
POST /api/email/process
Content-Type: application/json

{
  "from_address": "customer@example.com",
  "subject": "Flight booking request",
  "body": "Search flights from Delhi to Mumbai next week",
  "auto_reply": true
}
```

### 4. Email Status
```http
GET /api/email/status
```

**Response:**
```json
{
  "configured": true,
  "smtp_host": "smtp.gmail.com",
  "imap_host": "imap.gmail.com",
  "from_address": "travix@example.com",
  "message": "Email service is ready"
}
```

## Usage Examples

### Example 1: Customer Sends Flight Request

**Customer Email:**
```
To: travix@example.com
Subject: Flight booking

Hi, I need to book a flight from Delhi to Dubai for next week.
What options are available?
```

**Travix AI Reply:**
```
Hello,

Thank you for contacting Travix AI Assistant!

Your request has been processed by our SBT Agent.

We found 4 available flights for your route.

Available Flights:

1. Air India - AI-595
   From: Delhi (14:20)
   To: Dubai (17:15)
   Price: INR 15,200
   Duration: 3h 50min

2. Emirates - EK-512
   From: Delhi (10:30)
   To: Dubai (13:45)
   Price: INR 18,500
   Duration: 3h 15min

[... more flights ...]

Best regards,
Travix AI Assistant

---
To book or ask another question, simply reply to this email!
```

### Example 2: Hotel Search Request

**Customer Email:**
```
To: travix@example.com
Subject: Hotel needed

Find me hotels in Goa under 20000 per night
```

**Travix AI Reply:**
```
Hello,

Thank you for contacting Travix AI Assistant!

Your request has been processed by our BackOffice Agent.

Available Hotels:

1. The Oberoi New Delhi
   Location: Goa, Beach Road
   Rating: ⭐⭐⭐⭐⭐
   Price: INR 15,000/night
   Room Types: Deluxe, Premier, Suite

[... more hotels ...]
```

### Example 3: Itinerary Request

**Customer Email:**
```
To: travix@example.com
Subject: Trip planning

Create a 3-day itinerary for Delhi
```

**Travix AI Reply:**
```
Hello,

Thank you for contacting Travix AI Assistant!

Your request has been processed by our Itinerary Agent.

A day-wise schedule form has been created for you. 
Please visit the Travix dashboard to complete your itinerary details.

Or reply with specific activities you'd like to include!
```

## Automated Email Checking

### Set up Scheduled Email Checking

Create a cron job or scheduled task to check emails periodically:

**Linux/Mac (crontab):**
```bash
# Check emails every 5 minutes
*/5 * * * * curl -X GET "http://localhost:8000/api/email/check?auto_process=true"
```

**Windows (Task Scheduler):**
1. Create new task
2. Trigger: Every 5 minutes
3. Action: Start program
4. Program: `curl`
5. Arguments: `-X GET "http://localhost:8000/api/email/check?auto_process=true"`

### Python Background Worker

Create `apps/backend/email_worker.py`:

```python
import time
import requests
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

API_URL = "http://localhost:8000/api/email/check"

while True:
    try:
        response = requests.get(
            API_URL,
            params={"limit": 10, "auto_process": True}
        )
        
        if response.status_code == 200:
            data = response.json()
            logger.info(f"Checked emails: {data['count']} new, {data['processed']} processed")
        else:
            logger.error(f"Error checking emails: {response.status_code}")
    
    except Exception as e:
        logger.error(f"Error: {e}")
    
    # Wait 60 seconds before next check
    time.sleep(60)
```

Run with:
```bash
python apps/backend/email_worker.py
```

## Email Response Formats

The system automatically formats responses based on the agent action:

### Flight Search Results
- Lists up to 5 flights
- Shows airline, route, price, duration
- Formatted for easy reading

### Hotel Search Results
- Lists up to 5 hotels
- Shows location, rating, price
- Includes amenities

### Local Guide
- City attractions with descriptions
- Restaurant recommendations
- Travel tips

### Expense/Trip Management
- Confirmation messages
- Summary of created items
- Next steps

## Security Considerations

1. **Use App Passwords**: Never use your main Gmail password
2. **Environment Variables**: Keep email credentials in .env (never commit to git)
3. **Rate Limiting**: Gmail has sending limits (500/day for free accounts)
4. **SSL/TLS**: All connections are encrypted
5. **Email Validation**: System validates email addresses

## Troubleshooting

### "Email configuration not set"
- Check `.env` file has `EMAIL_FROM_ADDRESS` and `EMAIL_FROM_PASSWORD`
- Restart backend after updating .env

### "Login failed"
- Verify app password is correct (16 characters, no spaces)
- Check 2FA is enabled on Gmail account
- Ensure "Less secure app access" is OFF (use app password instead)

### "No new emails found"
- Check inbox has unread emails
- System only processes UNSEEN emails
- Emails are marked as processed to avoid duplicates

### "GROQ model error"
- Model updated to `llama-3.1-8b-instant` in config.py
- Restart backend to apply changes

## Testing

### Test Email Sending
```bash
curl -X POST http://localhost:8000/api/email/send \
  -H "Content-Type: application/json" \
  -d '{
    "to_address": "test@example.com",
    "subject": "Test Email",
    "body": "This is a test email from Travix"
  }'
```

### Test Email Checking
```bash
curl http://localhost:8000/api/email/check?limit=5
```

### Test Email Processing
```bash
curl -X POST http://localhost:8000/api/email/process \
  -H "Content-Type: application/json" \
  -d '{
    "from_address": "customer@example.com",
    "subject": "Test",
    "body": "Search flights from Delhi to Mumbai",
    "auto_reply": true
  }'
```

### Check Email Status
```bash
curl http://localhost:8000/api/email/status
```

## Integration with Frontend

Add email management UI to the dashboard:

```typescript
// Check email status
const checkEmailStatus = async () => {
  const response = await fetch('/api/email/status');
  const data = await response.json();
  console.log('Email configured:', data.configured);
};

// Manually check for emails
const checkNewEmails = async () => {
  const response = await fetch('/api/email/check?auto_process=true');
  const data = await response.json();
  console.log(`Found ${data.count} new emails`);
};
```

## Architecture

```
┌─────────────────┐
│   User Email    │
│  (Gmail/etc)    │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Email Service  │
│  (IMAP Check)   │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Groq Orchestr.  │
│ (Route Request) │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Agent Execute  │
│ (SBT/Hotel/etc) │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Format Response │
│  (Plain + HTML) │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Send Reply     │
│  (SMTP Send)    │
└─────────────────┘
```

## Files Created

1. **`apps/backend/app/services/email_service.py`**
   - EmailService class
   - Send/receive email functions
   - Response formatting
   - SMTP and IMAP handling

2. **`apps/backend/app/api/email.py`**
   - REST API endpoints
   - Integration with orchestrator
   - Background task processing

3. **`apps/backend/app/config.py`** (Updated)
   - Email configuration settings
   - Model name fixed

4. **`apps/backend/app/main.py`** (Updated)
   - Email router included
   - New endpoints listed

## Next Steps

1. Set up email credentials in `.env`
2. Test with `/api/email/status`
3. Send test email with `/api/email/send`
4. Set up automated checking (cron/scheduler)
5. Monitor logs for email processing

## Support

For issues:
1. Check logs: `docker-compose -f docker-compose.dev.yml logs backend`
2. Verify email status: `http://localhost:8000/api/email/status`
3. Test SMTP manually: Use tools like Thunderbird to verify credentials
4. Check Groq API key is valid

---

**Email integration is now complete and ready to use!**
