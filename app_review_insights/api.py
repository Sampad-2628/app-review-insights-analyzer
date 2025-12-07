import sys
import os
import json
import pandas as pd
from datetime import datetime

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app_review_insights import config
from app_review_insights.scraping.google_play_scraper import fetch_reviews, save_raw_reviews
from app_review_insights.processing.filters import filter_reviews
from app_review_insights.processing.theming import theme_reviews
from app_review_insights.reporting.weekly_note import generate_weekly_note
from app_review_insights.reporting.email_draft import generate_email_draft

def scrape_reviews_action(app_url):
    """ACTION A: SCRAPE_REVIEWS"""
    # Extract app_id from URL (simple parsing)
    try:
        app_id = app_url.split("id=")[1].split("&")[0]
    except IndexError:
        return {"status": "error", "message": "Invalid URL format"}

    # Update config (runtime override)
    config.APP_ID = app_id
    
    raw_reviews = fetch_reviews(app_id=app_id, count=500)
    save_raw_reviews(raw_reviews)
    
    filtered_reviews = filter_reviews(raw_reviews)
    os.makedirs(os.path.dirname(config.FILTERED_REVIEWS_FILE), exist_ok=True)
    with open(config.FILTERED_REVIEWS_FILE, 'w', encoding='utf-8') as f:
        json.dump(filtered_reviews, f, indent=2)
        
    # Save to CSV
    df = pd.DataFrame(filtered_reviews)
    csv_path = os.path.join(config.OUTPUT_DIR, "reviews_latest.csv")
    df.to_csv(csv_path, index=False)
        
    return {
        "action_performed": "SCRAPE_REVIEWS",
        "status": "success",
        "next_available_actions": ["CATEGORIZE_REVIEWS"],
        "data_preview": {
            "review_count": len(filtered_reviews),
            "app_id": app_id,
            "csv_path": csv_path
        }
    }

def categorize_reviews_action():
    """ACTION B: CATEGORIZE_REVIEWS"""
    if not os.path.exists(config.FILTERED_REVIEWS_FILE):
        return {"status": "error", "message": "No filtered reviews found. Run scrape first."}
        
    with open(config.FILTERED_REVIEWS_FILE, 'r', encoding='utf-8') as f:
        filtered_reviews = json.load(f)
        
    tagged_reviews = theme_reviews(filtered_reviews)
    
    os.makedirs(os.path.dirname(config.TAGGED_REVIEWS_FILE), exist_ok=True)
    with open(config.TAGGED_REVIEWS_FILE, 'w', encoding='utf-8') as f:
        json.dump(tagged_reviews, f, indent=2)
        
    themes = list(set(r['theme'] for r in tagged_reviews))
    
    return {
        "action_performed": "CATEGORIZE_REVIEWS",
        "status": "success",
        "next_available_actions": ["GENERATE_WEEKLY_NOTE"],
        "data_preview": {
            "themes": themes,
            "tagged_count": len(tagged_reviews)
        }
    }

def generate_weekly_note_action():
    """ACTION C: GENERATE_WEEKLY_NOTE"""
    if not os.path.exists(config.TAGGED_REVIEWS_FILE):
        return {"status": "error", "message": "No tagged reviews found. Run categorize first."}
        
    with open(config.TAGGED_REVIEWS_FILE, 'r', encoding='utf-8') as f:
        tagged_reviews = json.load(f)
        
    generate_weekly_note(tagged_reviews)
    
    with open(config.WEEKLY_REPORT_FILE, 'r', encoding='utf-8') as f:
        report_content = f.read()
        
    return {
        "action_performed": "GENERATE_WEEKLY_NOTE",
        "status": "success",
        "next_available_actions": ["CREATE_EMAIL_DRAFT"],
        "data_preview": {
            "report_preview": report_content[:500] + "..."
        }
    }

def create_email_draft_action():
    """ACTION D: CREATE_EMAIL_DRAFT"""
    if not os.path.exists(config.TAGGED_REVIEWS_FILE):
        return {"status": "error", "message": "No tagged reviews found."}
        
    with open(config.TAGGED_REVIEWS_FILE, 'r', encoding='utf-8') as f:
        tagged_reviews = json.load(f)
        
    generate_email_draft(tagged_reviews)
    
    with open(config.EMAIL_DRAFT_FILE, 'r', encoding='utf-8') as f:
        email_content = f.read()
        
    # Parse subject/body roughly for preview (or update generate_email_draft to return structured)
    lines = email_content.split('\n')
    subject = lines[0].replace("Subject: ", "")
    body = "\n".join(lines[1:])
    
    return {
        "action_performed": "CREATE_EMAIL_DRAFT",
        "status": "success",
        "next_available_actions": ["SEND_EMAIL"],
        "data_preview": {
            "subject": subject,
            "body_preview": body[:200] + "..."
        }
    }

def send_email_action(to_address):
    """ACTION E: SEND_EMAIL"""
    if not os.path.exists(config.EMAIL_DRAFT_FILE):
        return {"status": "error", "message": "No email draft found."}
        
    # Placeholder for actual email sending logic
    print(f"Sending email to {to_address}...")
    
    return {
        "action_performed": "SEND_EMAIL",
        "status": "success",
        "next_available_actions": [],
        "data_preview": {
            "recipient": to_address,
            "status": "Sent"
        }
    }

if __name__ == "__main__":
    # Simple CLI for testing actions
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("action", choices=["scrape", "categorize", "report", "draft", "send"])
    parser.add_argument("--url", help="App URL for scrape")
    parser.add_argument("--email", help="Email address for send")
    
    args = parser.parse_args()
    
    if args.action == "scrape":
        print(json.dumps(scrape_reviews_action(args.url or "https://play.google.com/store/apps/details?id=com.nextbillion.groww"), indent=2))
    elif args.action == "categorize":
        print(json.dumps(categorize_reviews_action(), indent=2))
    elif args.action == "report":
        print(json.dumps(generate_weekly_note_action(), indent=2))
    elif args.action == "draft":
        print(json.dumps(create_email_draft_action(), indent=2))
    elif args.action == "send":
        print(json.dumps(send_email_action(args.email or "test@example.com"), indent=2))
