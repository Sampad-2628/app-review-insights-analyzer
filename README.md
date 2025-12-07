# App Review Insights Analyzer

Automate the extraction and analysis of Google Play Store reviews to generate actionable weekly product insights and professional email reports.

## Features

- **Automated Scraping**: Fetch recent reviews from the Google Play Store (PII Redacted).
- **Intelligent Categorization**: Classify reviews into key product themes (e.g., UI/UX, Payments, Bugs).
- **Weekly Pulse Summary**: Generate a concise, insight-driven markdown report highlighting top issues and actionable steps.
- **Email Integration**: Draft and send professional weekly summary emails via Gmail SMTP.
- **Streamlit Frontend**: A clean, interactive UI to manage the entire workflow inline.
- **Console Utility**: A `main.py` CLI for running the pipeline from the terminal.

## Folder Structure

```
milestone-2/
│── app_review_insights/      # Core package
│   ├── scraping/             # Play Store & App Store scrapers
│   ├── processing/           # Data cleaning, PII redaction, categorization
│   ├── reporting/            # Weekly note & email generation
│   ├── api.py                # Action-based API layer
│   └── config.py             # Configuration settings
│
│── frontend/
│   └── app.py                # Streamlit web interface
│
│── scripts/
│   └── test_email.py         # Manual email testing script
│
│── data/                     # Raw & processed JSON reviews
│── output/                   # Generated reports & logs
│── main.py                   # CLI entry point
│── requirements.txt          # Project dependencies
└── README.md                 # Project documentation
```

## How to Run Locally

### Prerequisites
- Python 3.8+
- A Google account (for email sending features, optional)

### Installation

1.  **Clone the repository**:
    ```bash
    git clone <your-repo-url>
    cd milestone-2
    ```

2.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

3.  **Setup Environment Variables**:
    Create a `.env` file in the root directory:
    ```env
    # Required for email sending
    EMAIL_SENDER=your-email@gmail.com
    EMAIL_PASSWORD=your-app-password
    ```
    > **Note**: For Gmail, use an [App Password](https://support.google.com/accounts/answer/185833) if 2-Factor Authentication is enabled.

### Running the Application

**Option 1: Streamlit Interface (Recommended)**
Launch the web UI:
```bash
streamlit run frontend/app.py
```
This opens the dashboard in your browser where you can:
1. Paste a Play Store URL.
2. Scrape & categorize reviews.
3. View the generated "Weekly Pulse" summary.
4. Preview and send the email report.

**Option 2: CLI Runner**
Run the full pipeline from the terminal:
```bash
python main.py
```

## Frontend Usage Flow

1.  **Scrape**: Enter the app URL (e.g., Groww) and click **Scrape Reviews**. The tool fetches reviews and redacts PII automatically.
2.  **Categorize**: Click **Categorize Reviews** to group feedback into themes like "Trading", "Payments", etc.
3.  **Report**: Click **Generate Weekly Pulse Summary** to view the structured top-3 insights report.
4.  **Email**: Click **Generate Email Draft** to preview the formatted email. Enter a recipient and hit **Send Email** if configured.

## Deployment Notes

- This app is stateless but relies on local JSON files in `data/` and `output/`. For production deployment (e.g., Streamlit Cloud, Heroku), consider moving storage to a database or S3.
- Ensure `EMAIL_PASSWORD` is kept secure and handled via proper secrets management in production environments.

## Credits

Built as part of the advanced agentic coding milestone project.
