import json
from google_play_scraper import Sort, reviews
from datetime import datetime, timedelta
from .. import config

def fetch_reviews(app_id=config.APP_ID, lang=config.LANG, country=config.COUNTRY, count=500):
    """
    Fetches reviews from Google Play Store.
    """
    print(f"Fetching reviews for {app_id}...")
    
    result, _ = reviews(
        app_id,
        lang=lang,
        country=country,
        sort=Sort.NEWEST,
        count=count
    )
    
    # Convert datetime objects to strings for JSON serialization
    for r in result:
        for key, value in r.items():
            if isinstance(value, datetime):
                r[key] = value.strftime("%Y-%m-%dT%H:%M:%SZ")
            
    return result

import os

def save_raw_reviews(reviews_data, filepath=config.RAW_REVIEWS_FILE):
    print(f"DEBUG: Attempting to save reviews to {filepath}")
    
    # Ensure directory exists
    try:
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        print(f"DEBUG: Directory {os.path.dirname(filepath)} created/checked.")
    except Exception as e:
        print(f"DEBUG: Failed to create dir: {e}")
        
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(reviews_data, f, indent=2)
    print(f"Saved {len(reviews_data)} raw reviews to {filepath}")
