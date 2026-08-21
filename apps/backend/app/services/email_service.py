"""
Email Service for Travix
Handles sending and receiving emails, and integrates with the orchestrator
"""

import smtplib
import imaplib
import email
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import List, Optional, Dict
from datetime import datetime
import logging
from pydantic import BaseModel

logger = logging.getLogger(__name__)


class EmailConfig(BaseModel):
    """Email configuration"""
    smtp_host: str
    smtp_port: int
    imap_host: str
    imap_port: int
    email_address: str
    email_password: str
    from_name: str = "Travix AI Assistant"


class EmailMessage(BaseModel):
    """Email message model"""
    id: Optional[str] = None
    from_address: str
    to_address: str
    subject: str
    body: str
    html_body: Optional[str] = None
    received_at: Optional[datetime] = None
    replied: bool = False


class EmailService:
    """
    Email service that integrates with Groq Orchestrator
    Sends and receives emails, processes requests through orchestrator
    """

    def __init__(self, config: EmailConfig):
        """Initialize email service"""
        self.config = config
        self.processed_emails: List[str] = []  # Track processed email IDs
        
    def send_email(
        self,
        to_address: str,
        subject: str,
        body: str,
        html_body: Optional[str] = None
    ) -> bool:
        """
        Send an email
        
        Args:
            to_address: Recipient email address
            subject: Email subject
            body: Plain text body
            html_body: HTML body (optional)
            
        Returns:
            True if sent successfully, False otherwise
        """
        try:
            # Create message
            msg = MIMEMultipart('alternative')
            msg['Subject'] = subject
            msg['From'] = f"{self.config.from_name} <{self.config.email_address}>"
            msg['To'] = to_address
            
            # Attach plain text
            text_part = MIMEText(body, 'plain')
            msg.attach(text_part)
            
            # Attach HTML if provided
            if html_body:
                html_part = MIMEText(html_body, 'html')
                msg.attach(html_part)
            
            # Send email
            with smtplib.SMTP(self.config.smtp_host, self.config.smtp_port) as server:
                server.starttls()
                server.login(self.config.email_address, self.config.email_password)
                server.send_message(msg)
            
            logger.info(f"Email sent successfully to {to_address}")
            return True
            
        except Exception as e:
            logger.error(f"Error sending email: {e}")
            return False
    
    def check_new_emails(self, limit: int = 10) -> List[EmailMessage]:
        """
        Check for new unread emails
        
        Args:
            limit: Maximum number of emails to fetch
            
        Returns:
            List of new email messages
        """
        try:
            # Connect to IMAP server
            mail = imaplib.IMAP4_SSL(self.config.imap_host, self.config.imap_port)
            mail.login(self.config.email_address, self.config.email_password)
            mail.select('INBOX')
            
            # Search for unseen emails
            status, messages = mail.search(None, 'UNSEEN')
            
            if status != 'OK' or not messages[0]:
                return []
            
            email_ids = messages[0].split()
            new_emails = []
            
            # Process emails (limit to specified number)
            for email_id in email_ids[-limit:]:
                try:
                    # Skip if already processed
                    if email_id.decode() in self.processed_emails:
                        continue
                    
                    # Fetch email
                    status, msg_data = mail.fetch(email_id, '(RFC822)')
                    
                    if status != 'OK':
                        continue
                    
                    # Parse email
                    raw_email = msg_data[0][1]
                    email_message = email.message_from_bytes(raw_email)
                    
                    # Extract details
                    from_address = email_message.get('From', '')
                    subject = email_message.get('Subject', '')
                    
                    # Extract body
                    body = ''
                    if email_message.is_multipart():
                        for part in email_message.walk():
                            if part.get_content_type() == 'text/plain':
                                body = part.get_payload(decode=True).decode('utf-8', errors='ignore')
                                break
                    else:
                        body = email_message.get_payload(decode=True).decode('utf-8', errors='ignore')
                    
                    # Create EmailMessage
                    new_email = EmailMessage(
                        id=email_id.decode(),
                        from_address=from_address,
                        to_address=self.config.email_address,
                        subject=subject,
                        body=body,
                        received_at=datetime.now(),
                        replied=False
                    )
                    
                    new_emails.append(new_email)
                    self.processed_emails.append(email_id.decode())
                    
                except Exception as e:
                    logger.error(f"Error processing email {email_id}: {e}")
                    continue
            
            mail.close()
            mail.logout()
            
            return new_emails
            
        except Exception as e:
            logger.error(f"Error checking emails: {e}")
            return []
    
    def reply_to_email(
        self,
        original_email: EmailMessage,
        reply_body: str,
        reply_html: Optional[str] = None
    ) -> bool:
        """
        Reply to an email
        
        Args:
            original_email: Original email to reply to
            reply_body: Reply text
            reply_html: Reply HTML (optional)
            
        Returns:
            True if sent successfully
        """
        # Extract sender's email from From field
        from_address = original_email.from_address
        if '<' in from_address:
            # Extract email from "Name <email@example.com>" format
            from_address = from_address.split('<')[1].split('>')[0]
        
        # Create reply subject
        subject = original_email.subject
        if not subject.startswith('Re:'):
            subject = f"Re: {subject}"
        
        return self.send_email(
            to_address=from_address,
            subject=subject,
            body=reply_body,
            html_body=reply_html
        )
    
    def format_orchestrator_response(self, response_data: Dict) -> tuple[str, str]:
        """
        Format orchestrator response for email
        
        Args:
            response_data: Response from orchestrator execution
            
        Returns:
            Tuple of (plain_text, html_text)
        """
        try:
            agent = response_data.get('agent', 'Unknown')
            result = response_data.get('result', {})
            action = result.get('action', 'unknown')
            message = result.get('message', 'Request processed successfully.')
            data = result.get('data', {})
            
            # Build plain text response
            plain_text = f"""Hello,

Thank you for contacting Travix AI Assistant!

Your request has been processed by our {agent}.

{message}

"""
            
            # Add specific data based on action
            if action == "search_flights" and data and isinstance(data, dict):
                flights = data.get('flights', [])
                if flights:
                    plain_text += "\nAvailable Flights:\n\n"
                    for i, flight in enumerate(flights[:5], 1):
                        plain_text += f"{i}. {flight.get('airline', 'N/A')} - {flight.get('flight_number', 'N/A')}\n"
                        plain_text += f"   From: {flight.get('from_city', 'N/A')} ({flight.get('departure_time', 'N/A')})\n"
                        plain_text += f"   To: {flight.get('to_city', 'N/A')} ({flight.get('arrival_time', 'N/A')})\n"
                        plain_text += f"   Price: {flight.get('currency', 'INR')} {flight.get('price', 'N/A')}\n"
                        plain_text += f"   Duration: {flight.get('duration', 'N/A')}\n\n"
            
            elif action == "list_hotels" and data and isinstance(data, dict):
                hotels = data.get('hotels', [])
                if hotels:
                    plain_text += "\nAvailable Hotels:\n\n"
                    for i, hotel in enumerate(hotels[:5], 1):
                        plain_text += f"{i}. {hotel.get('name', 'N/A')}\n"
                        plain_text += f"   Location: {hotel.get('city', 'N/A')}, {hotel.get('address', 'N/A')}\n"
                        plain_text += f"   Rating: {'⭐' * int(hotel.get('rating', 0))}\n"
                        plain_text += f"   Price: {hotel.get('currency', 'INR')} {hotel.get('price_per_night', 'N/A')}/night\n"
                        plain_text += f"   Room Types: {', '.join(hotel.get('room_types', []))}\n\n"
            
            elif action == "local_guide" and data and isinstance(data, dict):
                city = data.get('city', 'N/A')
                attractions = data.get('attractions', [])
                if attractions:
                    plain_text += f"\nTop Attractions in {city}:\n\n"
                    for i, place in enumerate(attractions[:5], 1):
                        plain_text += f"{i}. {place.get('name', 'N/A')}\n"
                        plain_text += f"   {place.get('description', '')}\n\n"
            
            plain_text += """
Best regards,
Travix AI Assistant

---
To modify your booking or ask another question, simply reply to this email!
"""
            
            # Build HTML response (simplified)
            html_text = f"""
<html>
<body style="font-family: Arial, sans-serif; color: #333;">
    <h2 style="color: #4A90E2;">Travix AI Assistant</h2>
    <p>Hello,</p>
    <p>Thank you for contacting Travix AI Assistant!</p>
    <p>Your request has been processed by our <strong>{agent}</strong>.</p>
    <p>{message}</p>
    <br>
    <p style="color: #666; font-size: 12px;">
        Best regards,<br>
        Travix AI Assistant
    </p>
    <hr style="border: 1px solid #eee;">
    <p style="color: #999; font-size: 11px;">
        To modify your booking or ask another question, simply reply to this email!
    </p>
</body>
</html>
"""
            
            return plain_text, html_text
            
        except Exception as e:
            logger.error(f"Error formatting response: {e}")
            return "Your request has been processed. Please check the Travix dashboard for details.", ""


# Global email service instance
_email_service_instance: Optional[EmailService] = None


def get_email_service(
    smtp_host: str,
    smtp_port: int,
    imap_host: str,
    imap_port: int,
    email_address: str,
    email_password: str,
    from_name: str = "Travix AI Assistant"
) -> EmailService:
    """Get or create email service instance"""
    global _email_service_instance
    
    if _email_service_instance is None:
        config = EmailConfig(
            smtp_host=smtp_host,
            smtp_port=smtp_port,
            imap_host=imap_host,
            imap_port=imap_port,
            email_address=email_address,
            email_password=email_password,
            from_name=from_name
        )
        _email_service_instance = EmailService(config)
    
    return _email_service_instance
