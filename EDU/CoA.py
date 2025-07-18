import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, quote
import json
import urllib3

# Suppress SSL warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def CoA():
    base_url = "https://www.coa.gov.in"
    url = "https://www.coa.gov.in/notification_list.php"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                      "AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/114.0.0.0 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Connection": "keep-alive",
        "Referer": "https://www.google.com"
    }

    r = requests.get(url, headers=headers, verify=False)
    soup = BeautifulSoup(r.content, "html.parser")

    data = {}
    items = soup.select("ul.notification-listing li")

    for idx, item in enumerate(items):
        try:
            publish_date = item.find_all("a")[1].get_text(strip=True).split(":")[-1].strip()
            title = item.find("span").contents[0].strip()

            relative_link = item.find("a")["href"]
            encoded_relative_link = quote(relative_link)
            full_link = urljoin(base_url, encoded_relative_link)

            data[str(idx)] = {
                "Date": publish_date,
                "Title": title,
                "Link": full_link
            }
        except Exception:
            continue  # Skip if structure is unexpected

    return data

"""if __name__ == "__main__":
    notifications = CoA()

    with open("CoA.json", "w", encoding="utf-8") as f:
        json.dump(notifications, f, indent=2, ensure_ascii=False)

    print(f"Saved {len(notifications)} notifications to 'CoA.json'")
"""