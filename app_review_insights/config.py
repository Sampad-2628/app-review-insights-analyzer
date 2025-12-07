import os
from datetime import datetime, timedelta

# App Configuration
APP_ID = "com.nextbillion.groww"
LANG = "en"
COUNTRY = "in"

# Filtering Configuration
WEEKS_BACK = 10
MIN_WORD_COUNT = 10
MIN_CHAR_COUNT = 20

# Theming Configuration
MAX_THEMES = 5
THEME_LIST = [
    "App Performance & Bugs",
    "Trading & Features",
    "Customer Support",
    "Pricing & Charges",
    "User Experience"
]

# Paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
OUTPUT_DIR = os.path.join(BASE_DIR, "output")

RAW_REVIEWS_FILE = os.path.join(DATA_DIR, "reviews_raw.json")
FILTERED_REVIEWS_FILE = os.path.join(DATA_DIR, "reviews_filtered.json")
TAGGED_REVIEWS_FILE = os.path.join(DATA_DIR, "reviews_tagged.json")

WEEKLY_REPORT_FILE = os.path.join(OUTPUT_DIR, "weekly_pulse_groww.md")
EMAIL_DRAFT_FILE = os.path.join(OUTPUT_DIR, "email_draft_groww.txt")
THEME_LEGEND_FILE = os.path.join(OUTPUT_DIR, "theme_legend_groww.md")

# LLM Configuration (Placeholder for future use)
LLM_PROVIDER = "mock" # or "openai", "gemini"
