# generate_newsletter.py
import os
import json
from dotenv import load_dotenv
from jinja2 import Environment, FileSystemLoader
from mailchimp_marketing import Client
from mailchimp_marketing.api_client import ApiClientError
import datetime

# html file name based on today's date
# This will be used to save the local copy of the newsletter
# and also as the name for the Mailchimp campaign
# e.g. 2025-07-08.html
FILE_NAME = datetime.date.today().strftime("%d-%m-%Y") + ".html"

# === CONFIG ===
load_dotenv(dotenv_path='.env')
MAILCHIMP_API_KEY     = os.getenv("MAILCHIMP_API_KEY")     # e.g. abc123-us19
MAILCHIMP_AUDIENCE_ID = os.getenv("MAILCHIMP_AUDIENCE_ID") # your list ID
SENDER_NAME           = "Sachin Kumar Singh"
SENDER_EMAIL          = "kumarsinghsachin506@gmail.com"
CAMPAIGN_SUBJECT      = "Higher Education Regulatory Newsletter"
CAMPAIGN_TITLE        = "Higher Education Regulatory Newsletter - 8th July 2025"

# Extract datacenter prefix (e.g. 'us19') from the API key
SERVER_PREFIX = MAILCHIMP_API_KEY.split('-')[-1]

# === RENDER TEMPLATE ===
# Get the current folder path
template_path = os.path.dirname(os.path.abspath(__file__))

# Set up the environment using the current folder
env = Environment(loader=FileSystemLoader(template_path))

# Load your HTML file (not inside 'templates/')
template = env.get_template('newsletter.html')
html_content = template.render(
    pdf_url="newsletter.pdf",  # Placeholder for PDF URL
)

# === SAVE LOCAL COPY ===
with open(FILE_NAME, "w", encoding="utf-8") as f:
    f.write(html_content)

# === INITIALIZE MAILCHIMP CLIENT ===
mailchimp = Client()
mailchimp.set_config({
    "api_key": MAILCHIMP_API_KEY,
    "server": SERVER_PREFIX
})

try:
    # Create a draft campaign
    campaign = mailchimp.campaigns.create({
        "type": "regular",
        "recipients": {"list_id": MAILCHIMP_AUDIENCE_ID},
        "settings": {
            "subject_line": CAMPAIGN_SUBJECT,
            "title":        CAMPAIGN_TITLE,
            "from_name":    SENDER_NAME,
            "reply_to":     SENDER_EMAIL
        }
    })
    campaign_id = campaign["id"]
    print(f"➤ Campaign draft created: ID={campaign_id}")

    # Set the inlined-HTML content
    mailchimp.campaigns.set_content(campaign_id, {"html": html_content})
    print("➤ Inlined HTML content uploaded to campaign.")

except ApiClientError as error:
    print(f"✖ Mailchimp error: {error.text}")