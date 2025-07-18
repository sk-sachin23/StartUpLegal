import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import json

def NCERT():
    base_url = "https://ncert.nic.in/"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                      "AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/114.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9",
        "Referer": "https://www.google.com"
    }

    r = requests.get(base_url, headers=headers, timeout=10)
    soup = BeautifulSoup(r.content, "html.parser")

    activity_boxes = soup.find_all("div", class_="activity-box")
    if len(activity_boxes) < 2:
        return {}

    target_box = activity_boxes[1]  # second box
    ul = target_box.find("ul", class_="list")
    items = ul.find_all("li") if ul else []

    data = {}
    count = 0  # Manual counter for valid entries only

    for li in items:
        a = li.find("a")
        if a and a.get("href"):
            raw_title = a.get_text(strip=True)
            title = raw_title.replace('\r', '').replace('\n', '').replace('/r', '').replace('/n', '').strip()
            link = urljoin(base_url, a["href"])

            data[str(count)] = {
                "Title": title,
                "Link": link
            }
            count += 1  # Only increment if added

    return data

"""if __name__ == "__main__":
    result = NCERT()

    with open("NCERT.json", "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)

    print(f"✅ Saved {len(result)} items to 'NCERT.json'")
"""