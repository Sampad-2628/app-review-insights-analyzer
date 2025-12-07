import sys
import os

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app_review_insights.scraping.google_play_scraper import fetch_reviews, save_raw_reviews

def main():
    print("Starting review fetch...")
    reviews = fetch_reviews(count=1000) # Fetch plenty to ensure coverage
    save_raw_reviews(reviews)
    print("Done.")

if __name__ == "__main__":
    main()
