import requests
from datetime import datetime

def BCI(limit=6):
    base_url = "https://www.barcouncilofindia.org"
    endpoint = f"{base_url}/server/api/feed/list"

    query_params = {
        "limit": limit,
        "latest": "true",
        "onlyAnnouncements": "true"
    }

    response = requests.get(endpoint, params=query_params)
    response.raise_for_status()
    announcements = response.json().get("payload", [])

    result = {}
    for idx, item in enumerate(announcements):
        title = item.get("title", "").strip()
        post_id = item.get("_id")
        url = f"{base_url}/info/{post_id}" if post_id else None

        raw_schedule = item.get("scheduleDateTime", "")
        try:
            dt_obj = datetime.strptime(raw_schedule, "%Y-%m-%d %H:%M:%S")
            formatted_date = dt_obj.strftime("%d-%m-%Y")
        except ValueError:
            formatted_date = raw_schedule

        result[str(idx)] = {
            "title": title,
            "date": formatted_date,
            "url": url
        }

    return result
