from datetime import datetime, timedelta
from .. import config

import re

def sanitize_review_text(text):
    """
    Redacts PII from text:
    - Emails
    - Phone numbers (7+ digits)
    - Names (e.g., "- Name", "by Name")
    """
    if not text:
        return ""
        
    # Redact Emails
    text = re.sub(r'[\w\.-]+@[\w\.-]+\.\w+', '[EMAIL REDACTED]', text)
    
    # Redact Phone Numbers (7+ digits)
    text = re.sub(r'\b\d{7,}\b', '[PHONE REDACTED]', text)
    
    # Redact Names (Simple heuristic for "- Name", "~ Name", "by Name")
    # Matches hyphen/tilde/by followed by capitalized words
    text = re.sub(r'(?:-|~|by)\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)', '[NAME REDACTED]', text)
    
    return text

def filter_reviews(reviews_data):
    """
    Filters reviews based on date (last 8-10 weeks) and length.
    """
    filtered = []
    cutoff_date = datetime.now() - timedelta(weeks=config.WEEKS_BACK)
    
    print(f"Filtering reviews since {cutoff_date.date()}...")
    
    for r in reviews_data:
        # Parse date
        review_date_str = r.get('at') or r.get('date')
        if not review_date_str:
            continue
            
        try:
            review_date = datetime.strptime(review_date_str, "%Y-%m-%dT%H:%M:%SZ")
        except ValueError:
            # Try alternative format if needed, or skip
            continue
            
        if review_date < cutoff_date:
            continue
            
        # Length check
        content = r.get('content') or r.get('text', '')
        word_count = len(content.split())
        char_count = len(content)
        
        if word_count < config.MIN_WORD_COUNT and char_count < config.MIN_CHAR_COUNT:
            continue
            
        # PII Redaction
        sanitized_text = sanitize_review_text(content.replace("\n", " "))

        # Normalize structure
        normalized_review = {
            "platform": "Google Play",
            "app_name": config.APP_ID,
            "date": review_date_str,
            "rating": r.get('score') or r.get('rating'),
            # Drop reviewer identity as requested
            "title": "", 
            "text": sanitized_text
        }
        
        filtered.append(normalized_review)
        
    return filtered
