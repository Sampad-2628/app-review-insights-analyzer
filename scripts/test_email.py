import os
import sys
from dotenv import load_dotenv

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app_review_insights.reporting.email_sender import send_weekly_email

def test_email():
    # Load environment variables
    load_dotenv()
    
    sender = os.getenv("EMAIL_SENDER")
    if not sender:
        print("Error: EMAIL_SENDER not found in environment variables.")
        return

    print(f"Sender detected: {sender}")
    
    # Ask for recipient
    recipient = input(f"Enter recipient email (default: {sender}): ").strip()
    if not recipient:
        recipient = sender
        
    subject = "Test - App Review Insights Email Integration"
    body = "This is a test email from the milestone 2 project.\n\nIf you received this, the SMTP integration is working correctly."
    
    print(f"\nSending email to: {recipient}...")
    print("-" * 30)
    
    result = send_weekly_email(recipient, subject, body)
    
    print("-" * 30)
    print("Result:", result)
    
    if result["ok"]:
        print("\n✅ Email sent successfully!")
    else:
        print(f"\n❌ Failed to send email: {result['message']}")

if __name__ == "__main__":
    test_email()
