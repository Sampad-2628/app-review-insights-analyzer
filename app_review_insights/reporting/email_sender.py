import smtplib
import ssl
import os
from datetime import datetime
from dotenv import load_dotenv
from .. import config

# Load environment variables
load_dotenv()

def send_weekly_email(to_email: str, subject: str, body: str) -> dict:
    """
    Sends the weekly email to `to_email`.
    Returns a dict like {"ok": True/False, "message": "..."}.
    """
    sender_email = os.getenv("EMAIL_SENDER")
    sender_password = os.getenv("EMAIL_PASSWORD")
    
    # 1. Validate credentials
    if not sender_email or not sender_password:
        return {
            "ok": False,
            "message": "Missing email credentials (EMAIL_SENDER or EMAIL_PASSWORD) in environment."
        }

    # 2. Validate recipient
    if not to_email or "@" not in to_email or "." not in to_email:
        return {
            "ok": False,
            "message": "Invalid recipient email address."
        }
        
    port = 587  # For starttls
    smtp_server = "smtp.gmail.com"
    
    # Construct the message (headers + body)
    # Note: A proper email message should ideally use email.message.EmailMessage to handle headers correctly, 
    # but the prompt asks for "Subject: subject \n Body: body" style plain text sending via sendmail if possible, 
    # or just a simple format.
    # The requirement says: 
    #   Send a plain text email:
    #     From: EMAIL_SENDER
    #     To:   to_email
    #     Subject: subject
    #     Body: body
    
    email_message = f"From: {sender_email}\nTo: {to_email}\nSubject: {subject}\n\n{body}"
    
    # Create logs directory if not exists
    log_dir = os.path.join(config.OUTPUT_DIR, "email_logs")
    os.makedirs(log_dir, exist_ok=True)
    log_file = os.path.join(log_dir, "email_log.txt") # Append to single file as per Step 1 req
    
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    try:
        context = ssl.create_default_context()
        with smtplib.SMTP(smtp_server, port) as server:
            server.ehlo() # Can be omitted, called by starttls
            server.starttls(context=context)
            server.ehlo() # Can be omitted, called by login
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, to_email, email_message.encode('utf-8')) # Encode to bytes for safety
            
        # Log success
        with open(log_file, 'a', encoding='utf-8') as f:
            f.write(f"{timestamp} | {to_email} | {subject} | SUCCESS\n")
            
        return {"ok": True, "message": "Email sent"}
        
    except Exception as e:
        # Log failure
        with open(log_file, 'a', encoding='utf-8') as f:
            f.write(f"{timestamp} | {to_email} | {subject} | FAIL | {str(e)}\n")
            
        return {"ok": False, "message": str(e)}
