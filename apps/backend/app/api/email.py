"""
Email API Endpoints
Handles email sending, receiving, and processing through orchestrator
"""

from fastapi import APIRouter, HTTPException, Depends, BackgroundTasks
from typing import Optional, List
import logging
from pydantic import BaseModel, EmailStr
from ..services.email_service import EmailService, get_email_service, EmailMessage
from ..services.groq_orchestrator import GroqOrchestrator, OrchestratorRequest
from ..services.backoffice_agent import BackOfficeAgent
from ..services.sbt_agent import SBTAgent
from ..services.itinerary_agent import ItineraryAgent
from ..services.rebooking_agent import RebookingAgent
from ..services.revising_agent import RevisingAgent
from ..services.local_guide_agent import LocalGuideAgent
from ..services.expense_agent import ExpenseAgent
from ..config import get_settings

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/email", tags=["email"])

# Global instances
_email_service: Optional[EmailService] = None
_orchestrator: Optional[GroqOrchestrator] = None
_agents = {}


def get_email_service_instance() -> EmailService:
    """Get email service instance"""
    global _email_service
    
    if _email_service is None:
        settings = get_settings()
        
        # Get email settings from environment
        smtp_host = getattr(settings, 'email_smtp_host', 'smtp.gmail.com')
        smtp_port = getattr(settings, 'email_smtp_port', 587)
        imap_host = getattr(settings, 'email_imap_host', 'imap.gmail.com')
        imap_port = getattr(settings, 'email_imap_port', 993)
        email_address = getattr(settings, 'email_from_address', '')
        email_password = getattr(settings, 'email_from_password', '')
        from_name = getattr(settings, 'email_from_name', 'Travix AI Assistant')
        
        if not email_address or not email_password:
            raise HTTPException(
                status_code=500,
                detail="Email configuration not set. Please configure EMAIL_FROM_ADDRESS and EMAIL_FROM_PASSWORD"
            )
        
        _email_service = get_email_service(
            smtp_host=smtp_host,
            smtp_port=smtp_port,
            imap_host=imap_host,
            imap_port=imap_port,
            email_address=email_address,
            email_password=email_password,
            from_name=from_name
        )
    
    return _email_service


def get_orchestrator_instance() -> GroqOrchestrator:
    """Get orchestrator instance"""
    global _orchestrator
    
    if _orchestrator is None:
        settings = get_settings()
        if not settings.groq_api_key:
            raise HTTPException(
                status_code=500,
                detail="GROQ_API_KEY not set"
            )
        _orchestrator = GroqOrchestrator(
            api_key=settings.groq_api_key,
            model=settings.groq_model
        )
    
    return _orchestrator


def get_agents():
    """Get all agent instances"""
    global _agents
    
    if not _agents:
        _agents = {
            'backoffice_agent': BackOfficeAgent(),
            'sbt_agent': SBTAgent(),
            'itinerary_agent': ItineraryAgent(),
            'rebooking_agent': RebookingAgent(),
            'revising_agent': RevisingAgent(),
            'local_guide_agent': LocalGuideAgent(),
            'expense_agent': ExpenseAgent()
        }
    
    return _agents


# ==================== Request/Response Models ====================

class SendEmailRequest(BaseModel):
    """Request to send an email"""
    to_address: EmailStr
    subject: str
    body: str
    html_body: Optional[str] = None


class ProcessEmailRequest(BaseModel):
    """Request to process an email through orchestrator"""
    from_address: EmailStr
    subject: str
    body: str
    auto_reply: bool = True


class EmailResponse(BaseModel):
    """Email response"""
    success: bool
    message: str
    email_id: Optional[str] = None


class CheckEmailsResponse(BaseModel):
    """Response with new emails"""
    success: bool
    count: int
    emails: List[dict]
    processed: int = 0


# ==================== API Endpoints ====================

@router.post("/send", response_model=EmailResponse)
async def send_email(
    request: SendEmailRequest,
    email_service: EmailService = Depends(get_email_service_instance)
) -> EmailResponse:
    """
    Send an email
    
    Args:
        request: Email details (to, subject, body)
        
    Returns:
        Success status and message
    """
    try:
        logger.info(f"Sending email to {request.to_address}")
        
        success = email_service.send_email(
            to_address=request.to_address,
            subject=request.subject,
            body=request.body,
            html_body=request.html_body
        )
        
        if success:
            return EmailResponse(
                success=True,
                message=f"Email sent successfully to {request.to_address}"
            )
        else:
            return EmailResponse(
                success=False,
                message="Failed to send email"
            )
            
    except Exception as e:
        logger.error(f"Error sending email: {e}")
        raise HTTPException(status_code=500, detail=f"Error sending email: {str(e)}")


@router.get("/check", response_model=CheckEmailsResponse)
async def check_emails(
    limit: int = 10,
    auto_process: bool = False,
    background_tasks: BackgroundTasks = None,
    email_service: EmailService = Depends(get_email_service_instance)
) -> CheckEmailsResponse:
    """
    Check for new emails
    
    Args:
        limit: Maximum emails to fetch
        auto_process: Automatically process emails through orchestrator
        
    Returns:
        List of new emails
    """
    try:
        logger.info(f"Checking for new emails (limit: {limit})")
        
        new_emails = email_service.check_new_emails(limit=limit)
        
        # Convert to dict for response
        emails_data = []
        for email_msg in new_emails:
            emails_data.append({
                'id': email_msg.id,
                'from': email_msg.from_address,
                'subject': email_msg.subject,
                'body': email_msg.body[:200] + '...' if len(email_msg.body) > 200 else email_msg.body,
                'received_at': email_msg.received_at.isoformat() if email_msg.received_at else None
            })
        
        # Auto-process if requested
        processed = 0
        if auto_process and background_tasks:
            for email_msg in new_emails:
                background_tasks.add_task(process_email_task, email_msg)
                processed += 1
        
        return CheckEmailsResponse(
            success=True,
            count=len(new_emails),
            emails=emails_data,
            processed=processed
        )
        
    except Exception as e:
        logger.error(f"Error checking emails: {e}")
        raise HTTPException(status_code=500, detail=f"Error checking emails: {str(e)}")


@router.post("/process", response_model=EmailResponse)
async def process_email(
    request: ProcessEmailRequest,
    email_service: EmailService = Depends(get_email_service_instance),
    orchestrator: GroqOrchestrator = Depends(get_orchestrator_instance)
) -> EmailResponse:
    """
    Process an email through orchestrator and optionally reply
    
    Args:
        request: Email details to process
        
    Returns:
        Processing result
    """
    try:
        logger.info(f"Processing email from {request.from_address}: {request.subject}")
        
        # Step 1: Route through orchestrator
        orchestrator_request = OrchestratorRequest(
            user_message=request.body,
            conversation_history=None
        )
        routing = orchestrator.analyze_request(orchestrator_request)
        
        logger.info(f"Email routed to {routing.agent}: {routing.action}")
        
        # Step 2: Execute agent
        agents = get_agents()
        result = None
        
        if routing.agent in agents:
            agent = agents[routing.agent]
            result = agent.execute(request.body)
        else:
            result = type('obj', (object,), {
                'action': routing.action,
                'message': f"Routed to {routing.agent}",
                'data': None,
                'success': False
            })()
        
        # Step 3: Format and send reply if auto_reply is enabled
        if request.auto_reply:
            response_data = {
                'agent': routing.agent,
                'result': {
                    'action': result.action,
                    'message': result.message,
                    'data': result.data if hasattr(result, 'data') else None
                }
            }
            
            plain_text, html_text = email_service.format_orchestrator_response(response_data)
            
            # Create email message object for reply
            email_msg = EmailMessage(
                from_address=request.from_address,
                to_address=email_service.config.email_address,
                subject=request.subject,
                body=request.body
            )
            
            reply_sent = email_service.reply_to_email(
                original_email=email_msg,
                reply_body=plain_text,
                reply_html=html_text
            )
            
            if reply_sent:
                return EmailResponse(
                    success=True,
                    message=f"Email processed and reply sent to {request.from_address}"
                )
            else:
                return EmailResponse(
                    success=False,
                    message="Email processed but reply failed"
                )
        else:
            return EmailResponse(
                success=True,
                message=f"Email processed by {routing.agent}"
            )
            
    except Exception as e:
        logger.error(f"Error processing email: {e}")
        raise HTTPException(status_code=500, detail=f"Error processing email: {str(e)}")


async def process_email_task(email_msg: EmailMessage):
    """
    Background task to process an email
    
    Args:
        email_msg: Email message to process
    """
    try:
        email_service = get_email_service_instance()
        orchestrator = get_orchestrator_instance()
        
        # Route through orchestrator
        orchestrator_request = OrchestratorRequest(
            user_message=email_msg.body,
            conversation_history=None
        )
        routing = orchestrator.analyze_request(orchestrator_request)
        
        # Execute agent
        agents = get_agents()
        if routing.agent in agents:
            agent = agents[routing.agent]
            result = agent.execute(email_msg.body)
            
            # Format response
            response_data = {
                'agent': routing.agent,
                'result': {
                    'action': result.action,
                    'message': result.message,
                    'data': result.data if hasattr(result, 'data') else None
                }
            }
            
            plain_text, html_text = email_service.format_orchestrator_response(response_data)
            
            # Send reply
            email_service.reply_to_email(
                original_email=email_msg,
                reply_body=plain_text,
                reply_html=html_text
            )
            
            logger.info(f"Processed and replied to email {email_msg.id}")
            
    except Exception as e:
        logger.error(f"Error in background email processing: {e}")


@router.post("/reply/{email_id}")
async def reply_to_email_endpoint(
    email_id: str,
    reply_body: str,
    reply_html: Optional[str] = None,
    email_service: EmailService = Depends(get_email_service_instance)
) -> EmailResponse:
    """
    Reply to a specific email
    
    Args:
        email_id: ID of email to reply to
        reply_body: Reply text
        reply_html: Reply HTML (optional)
        
    Returns:
        Success status
    """
    try:
        # Note: This is a simplified version
        # In production, you'd store emails and retrieve them by ID
        return EmailResponse(
            success=False,
            message="Feature not fully implemented. Use /process endpoint instead."
        )
        
    except Exception as e:
        logger.error(f"Error replying to email: {e}")
        raise HTTPException(status_code=500, detail=f"Error replying to email: {str(e)}")


@router.get("/status")
async def email_status() -> dict:
    """Get email service status"""
    try:
        settings = get_settings()
        
        email_configured = bool(
            getattr(settings, 'email_from_address', None) and
            getattr(settings, 'email_from_password', None)
        )
        
        return {
            "configured": email_configured,
            "smtp_host": getattr(settings, 'email_smtp_host', 'smtp.gmail.com'),
            "imap_host": getattr(settings, 'email_imap_host', 'imap.gmail.com'),
            "from_address": getattr(settings, 'email_from_address', 'Not configured'),
            "message": "Email service is ready" if email_configured else "Email service not configured"
        }
        
    except Exception as e:
        logger.error(f"Error getting email status: {e}")
        return {
            "configured": False,
            "message": f"Error: {str(e)}"
        }
