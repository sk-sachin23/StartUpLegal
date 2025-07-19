import os
import datetime
from dotenv import load_dotenv
from mailchimp_marketing import Client
from mailchimp_marketing.api_client import ApiClientError


load_dotenv(dotenv_path='.env')

MAILCHIMP_API_KEY = os.getenv("MAILCHIMP_API_KEY")
SENDER_NAME = "Sachin Kumar Singh"
SENDER_EMAIL = "kumarsinghsachin506@gmail.com"
SERVER_PREFIX = MAILCHIMP_API_KEY.split('-')[-1] if MAILCHIMP_API_KEY else ''


def send_newsletter(html_path: str, audience_id: str) -> str:
    """Send the rendered newsletter HTML to the given Mailchimp audience."""
    with open(html_path, 'r', encoding='utf-8') as f:
        html_content = f.read()

    mailchimp = Client()
    mailchimp.set_config({"api_key": MAILCHIMP_API_KEY, "server": SERVER_PREFIX})

    subject = "Higher Education Regulatory Newsletter"
    title = f"Newsletter - {datetime.date.today().isoformat()}"

    try:
        campaign = mailchimp.campaigns.create({
            "type": "regular",
            "recipients": {"list_id": audience_id},
            "settings": {
                "subject_line": subject,
                "title": title,
                "from_name": SENDER_NAME,
                "reply_to": SENDER_EMAIL,
            },
        })
        campaign_id = campaign["id"]

        mailchimp.campaigns.set_content(campaign_id, {"html": html_content})
        mailchimp.campaigns.actions.send(campaign_id)
        return campaign_id
    except ApiClientError as error:
        raise RuntimeError(f"Mailchimp error: {error.text}")


if __name__ == "__main__":
    audience = os.getenv("MAILCHIMP_AUDIENCE_ID")
    cid = send_newsletter("newsletter.html", audience)
    print(f"Newsletter sent. Campaign ID: {cid}")

