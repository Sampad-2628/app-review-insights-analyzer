import streamlit as st
import sys
import os
import json
import pandas as pd
from datetime import datetime

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import backend actions via API
from app_review_insights.api import (
    scrape_reviews_action,
    categorize_reviews_action,
    generate_weekly_note_action,
    create_email_draft_action
)
# Import email sender directly
from app_review_insights.reporting.email_sender import send_weekly_email
from app_review_insights import config

# Page Config
st.set_page_config(
    page_title="App Review Insights Analyzer",
    page_icon="📊",
    layout="wide"
)

# Title & Description
st.title("📊 App Review Insights Analyzer")
st.markdown("""
This tool automates the process of gathering user feedback from the Google Play Store, 
analyzing it for key themes, and generating actionable weekly reports.

**Workflow:**
1. **Scrape:** Fetch recent reviews (PII redacted).
2. **Categorize:** Cluster reviews into product themes.
3. **Report:** Generate "Weekly Pulse" summary (Top 3 Categories).
4. **Email:** Create and send a professional email draft.
""")

# --- Helper Function for Insights (Updated for quote-free display) ---
def get_theme_insight(theme_name, reviews_df):
    """Generate a mock insight summary based on theme stats."""
    theme_df = reviews_df[reviews_df['theme'] == theme_name]
    count = len(theme_df)
    if count == 0:
        return f"**{theme_name}**: No reviews found."
        
    avg_rating = theme_df['rating'].mean()
    
    # Base sentiment
    sentiment = "Mixed feedback"
    if avg_rating >= 4.0: sentiment = "Positive sentiment"
    elif avg_rating <= 2.5: sentiment = "Critical feedback"
    
    # Condensed descriptors for bullet points (No quotes)
    if "Support" in theme_name:
        summary = "Issues with response time vs helpful FAQs."
    elif "Trading" in theme_name:
        summary = "Stock variety appreciated; F&O features needed."
    elif "Performance" in theme_name:
        summary = "Stable mostly; lags during market open."
    elif "Pricing" in theme_name:
        summary = "Zero MF commission is key; F&O charges high."
    elif "Experience" in theme_name:
        summary = "Mobile UI praised; Desktop needs refresh."
    else:
        summary = "General feedback breakdown available in report."
        
    return f"**{theme_name}** ({count} reviews, {avg_rating:.1f}⭐) — {summary}"

# --- Step 1: App URL & Scraping ---
st.header("1. App URL & Scraping")

default_url = "https://play.google.com/store/apps/details?id=com.nextbillion.groww"
app_url = st.text_input("Google Play Store App URL", value=default_url)

if st.button("Scrape Reviews"):
    if not app_url or "play.google.com" not in app_url or "id=" not in app_url:
        st.error("Please enter a valid Google Play Store URL.")
    else:
        with st.spinner("Scraping reviews (and redacting PII)..."):
            result = scrape_reviews_action(app_url)
            
        if result["status"] == "success":
            st.success(f"Successfully scraped {result['data_preview']['review_count']} reviews!")
            st.info(f"App ID: {result['data_preview']['app_id']}")
            
            # Show preview (redacted)
            if os.path.exists(result['data_preview'].get('csv_path', '')):
                df = pd.read_csv(result['data_preview']['csv_path'])
                # Ensure no user names in preview if columns exist
                cols_to_show = ['date', 'rating', 'text', 'theme'] if 'theme' in df.columns else ['date', 'rating', 'text']
                # Filter strictly to avoid accidental name display
                display_cols = [c for c in cols_to_show if c in df.columns]
                st.dataframe(df[display_cols].head(5), use_container_width=True)
            else:
                st.warning("Preview data not available.")
        else:
            st.error(f"Scraping failed: {result.get('message', 'Unknown error')}")

# --- Step 2: Categorize Reviews ---
st.header("2. Categorize Reviews")

if st.button("Categorize Reviews"):
    if not os.path.exists(config.FILTERED_REVIEWS_FILE):
        st.error("No scraped data found. Please run Step 1 first.")
    else:
        with st.spinner("Categorizing reviews into themes..."):
            result = categorize_reviews_action()
            
        if result["status"] == "success":
            st.success(f"Categorized {result['data_preview']['tagged_count']} reviews!")
            
            # Load tagged data for insights
            with open(config.TAGGED_REVIEWS_FILE, 'r', encoding='utf-8') as f:
                tagged_data = json.load(f)
            df = pd.DataFrame(tagged_data)
            
            st.subheader("Category Summaries")
            
            # Get unique themes and toggle list
            themes = df['theme'].unique()
            for i, theme in enumerate(themes, 1):
                insight = get_theme_insight(theme, df)
                st.markdown(f"{i}. {insight}")
                
        else:
            st.error(f"Categorization failed: {result.get('message', 'Unknown error')}")

# --- Step 3: Weekly Pulse Summary ---
st.header("3. Weekly Pulse Summary")

if st.button("Generate Weekly Pulse Summary"):
    if not os.path.exists(config.TAGGED_REVIEWS_FILE):
        st.error("No categorized data found. Please run Step 2 first.")
    else:
        with st.spinner("Generating weekly report..."):
            result = generate_weekly_note_action()
            
        if result["status"] == "success":
            st.success("Weekly report generated!")
            
            # Display Report with new format directly
            st.markdown(result['data_preview']['report_preview'])
            
            # NO DOWNLOAD BUTTON
        else:
            st.error(f"Report generation failed: {result.get('message', 'Unknown error')}")

# --- Step 4: Generate Email Draft ---
st.header("4. Generate Email Draft")

if st.button("Generate Email Draft"):
    if not os.path.exists(config.TAGGED_REVIEWS_FILE): # Draft needs tagged data
        st.error("Please complete previous steps first.")
    else:
        with st.spinner("Drafting email..."):
            draft_result = create_email_draft_action()
            
        if draft_result["status"] == "success":
            st.success("Email draft prepared!")
            
            # Parse subject and body from the draft file or preview
            try:
                with open(config.EMAIL_DRAFT_FILE, 'r', encoding='utf-8') as f:
                    content = f.read()
                    lines = content.split('\n')
                    subject = lines[0].replace("Subject: ", "").strip()
                    body = "\n".join(lines[1:]).strip()
            except Exception as e:
                st.warning(f"Could not read draft file, using preview. Error: {e}")
                subject = draft_result['data_preview']['subject']
                body = draft_result['data_preview']['body_preview']
            
            # Store in session state to persist for sending step
            st.session_state['email_subject'] = subject
            st.session_state['email_body'] = body

            st.subheader("Email Draft Preview")
            st.write(f"**Subject:** {subject}")
            st.text_area("Body (Includes Weekly Report):", body, height=400)
        else:
            st.error(f"Draft generation failed: {draft_result.get('message')}")

# --- Step 5: Send Email ---
st.header("5. Send Email")

recipient_email = st.text_input("Enter recipient email")

if st.button("Send Email"):
    if 'email_subject' not in st.session_state or 'email_body' not in st.session_state:
        st.warning("Please generate the email draft first (Step 4).")
    elif not recipient_email or "@" not in recipient_email:
        st.error("Please enter a valid recipient email address.")
    else:
        subject = st.session_state['email_subject']
        body = st.session_state['email_body']
        
        with st.spinner(f"Sending email to {recipient_email}..."):
            result = send_weekly_email(recipient_email, subject, body)
            
        if result["ok"]:
            st.success("Email sent successfully.")
        else:
            st.error(f"Failed to send email: {result['message']}")

# Sidebar info REMOVED completely
