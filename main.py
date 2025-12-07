import sys
import argparse
from app_review_insights.api import (
    scrape_reviews_action,
    categorize_reviews_action,
    generate_weekly_note_action,
    create_email_draft_action
)

def run_pipeline(url=None):
    print("🚀 Starting App Review Insights Pipeline...")
    
    # 1. Scrape
    print("\n--- Step 1: Scraping Reviews ---")
    if not url:
        url = input("Enter Google Play Store App URL (or press Enter for default): ").strip()
    if not url:
        url = "https://play.google.com/store/apps/details?id=com.nextbillion.groww"
        
    res = scrape_reviews_action(url)
    if res['status'] != 'success':
        print(f"❌ Scraping failed: {res.get('message')}")
        return
    print(f"✅ Scraped {res['data_preview']['review_count']} reviews.")
    
    # 2. Categorize
    print("\n--- Step 2: Categorizing Reviews ---")
    res = categorize_reviews_action()
    if res['status'] != 'success':
        print(f"❌ Categorization failed: {res.get('message')}")
        return
    print(f"✅ Categorized {res['data_preview']['tagged_count']} reviews.")
    
    # 3. Report
    print("\n--- Step 3: Generating Weekly Pulse ---")
    res = generate_weekly_note_action()
    if res['status'] != 'success':
        print(f"❌ Report generation failed: {res.get('message')}")
        return
    print("✅ Weekly report generated.")
    
    # 4. Email Draft
    print("\n--- Step 4: Drafting Email ---")
    res = create_email_draft_action()
    if res['status'] != 'success':
        print(f"❌ Draft creation failed: {res.get('message')}")
        return
    print("✅ Email draft created.")
    
    print("\n✨ Pipeline Completed Successfully! ✨")
    print("Check the 'output/' directory for results.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run the App Review Insights pipeline.")
    parser.add_argument("--url", help="Google Play Store App URL")
    args = parser.parse_args()
    
    run_pipeline(args.url)
