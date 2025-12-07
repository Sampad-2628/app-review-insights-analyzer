import json
import pandas as pd
from datetime import datetime, timedelta
from app_store_scraper import AppStore
from .. import config
import os
import time

def fetch_ios_reviews(app_name, app_id, country='in', count=500):
    """
    Fetches reviews from iOS App Store using app_store_scraper.
    """
    print(f"Fetching iOS reviews for {app_name} (ID: {app_id})...")
    
    try:
        # Initialize scraper
        scraper = AppStore(country=country, app_name=app_name, app_id=app_id)
        
        # Fetch reviews
        scraper.review(how_many=count)
        
        reviews_data = scraper.reviews
        print(f"Fetched {len(reviews_data)} reviews.")
        
        # Normalize data to match Google Play structure
        normalized_reviews = []
        
        for r in reviews_data:
            # app_store_scraper returns: 'date', 'review', 'rating', 'isEdited', 'title', 'userName'
            
            # Parse date
            review_date = r.get('date')
            if isinstance(review_date, datetime):
                date_str = review_date.strftime("%Y-%m-%dT%H:%M:%SZ")
            else:
                date_str = str(review_date) # Fallback
                
            normalized_review = {
                "platform": "iOS App Store",
                "app_name": app_name, 
                "date": date_str,
                "rating": r.get('rating'),
                "title": r.get('title', ''),
                "text": r.get('review', '').replace("\n", " ")
            }
            normalized_reviews.append(normalized_review)
                
        return normalized_reviews
    except Exception as e:
        print(f"Error fetching reviews: {e}")
        return []

def filter_and_save_ios_reviews(reviews_data, app_name="Groww"):
    """
    Filters iOS reviews and saves them to JSON and CSV.
    """
    filtered = []
    cutoff_date = datetime.now() - timedelta(weeks=config.WEEKS_BACK)
    
    print(f"Filtering iOS reviews since {cutoff_date.date()}...")
    
    for r in reviews_data:
        # Date check
        try:
            review_date = datetime.strptime(r['date'], "%Y-%m-%dT%H:%M:%SZ")
        except ValueError:
            continue
            
        if review_date < cutoff_date:
            continue
            
        # Length check
        content = r['text']
        word_count = len(content.split())
        char_count = len(content)
        
        if word_count < config.MIN_WORD_COUNT and char_count < config.MIN_CHAR_COUNT:
            continue
            
        filtered.append(r)
        
    print(f"Filtered down to {len(filtered)} iOS reviews.")

    # Save JSON
    json_path = os.path.join(config.DATA_DIR, "ios_reviews_filtered.json")
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(filtered, f, indent=2)
    print(f"Saved filtered JSON to {json_path}")

    # Save CSV
    if filtered:
        df = pd.DataFrame(filtered)
        csv_path = os.path.join(config.OUTPUT_DIR, "ios_reviews_latest.csv")
        df.to_csv(csv_path, index=False)
        print(f"Saved CSV to {csv_path}")
    
    return filtered

if __name__ == "__main__":
    # Test run for Groww
    # Groww iOS ID: 1351630927
    # Name: groww-stocks-mutual-fund
    reviews = fetch_ios_reviews(app_name="groww-stocks-mutual-fund", app_id=1351630927)
    filter_and_save_ios_reviews(reviews)
