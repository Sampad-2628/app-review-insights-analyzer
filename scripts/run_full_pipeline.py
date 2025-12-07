import sys
import os
import json

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app_review_insights import config
from app_review_insights.scraping.google_play_scraper import fetch_reviews, save_raw_reviews
from app_review_insights.processing.filters import filter_reviews
from app_review_insights.processing.theming import theme_reviews
from app_review_insights.reporting.weekly_note import generate_weekly_note
from app_review_insights.reporting.email_draft import generate_email_draft

def main():
    print("=== Starting App Review Insights Pipeline ===")
    
    # 1. Scrape
    raw_reviews = fetch_reviews(count=500)
    save_raw_reviews(raw_reviews)
    
    # 2. Filter
    filtered_reviews = filter_reviews(raw_reviews)
    print(f"Filtered down to {len(filtered_reviews)} reviews.")
    
    with open(config.FILTERED_REVIEWS_FILE, 'w', encoding='utf-8') as f:
        json.dump(filtered_reviews, f, indent=2)
        
    # 3. Theme
    tagged_reviews = theme_reviews(filtered_reviews)
    
    with open(config.TAGGED_REVIEWS_FILE, 'w', encoding='utf-8') as f:
        json.dump(tagged_reviews, f, indent=2)
        
    # 4. Report
    generate_weekly_note(tagged_reviews)
    generate_email_draft(tagged_reviews)
    
    print("=== Pipeline Completed Successfully ===")

if __name__ == "__main__":
    main()
