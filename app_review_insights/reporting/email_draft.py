import os
from .. import config

def generate_email_draft(tagged_reviews, output_file=config.EMAIL_DRAFT_FILE):
    """
    Generates a formal, professional email draft including the weekly summary.
    """
    # Read the weekly report content
    report_content = ""
    if os.path.exists(config.WEEKLY_REPORT_FILE):
        with open(config.WEEKLY_REPORT_FILE, 'r', encoding='utf-8') as f:
            report_content = f.read()
    else:
        report_content = "(Weekly report not found. Please generate it first.)"

    subject = f"Market pulse: {config.APP_ID} | Weekly User Feedback Analysis"
    
    body_text = "Hi Team,\n\n"
    body_text += f"Attached is the weekly analysis of user feedback for the {config.APP_ID} Android app, covering the last {config.WEEKS_BACK} weeks. This report synthesizes recent Play Store reviews to highlight key themes, emerging pain points, and strategic opportunities for product improvement.\n\n"
    body_text += "Overview of Key Insights:\n"
    body_text += report_content + "\n\n"
    body_text += "We recommend prioritizing the high-impact action items identified above to enhance user satisfaction and retention in the coming sprint.\n\n"
    body_text += "Please let us know if you require further data segmentation or specific user verbatims.\n\n"
    body_text += "Best regards,\n"
    body_text += "Product Insights Team"

    full_content = f"Subject: {subject}\n\n{body_text}"

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(full_content)
        
    print(f"Email draft generated at {output_file}")
    return subject, body_text
