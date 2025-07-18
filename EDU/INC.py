import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import json

def INC():
    base_url = "https://www.indiannursingcouncil.org"
    url = f"{base_url}/notifications"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                      "AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/114.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9",
        "Referer": "https://www.google.com"
    }

    r = requests.get(url, headers=headers, timeout=10)
    soup = BeautifulSoup(r.content, "html.parser")

    notifications = soup.find_all("div", class_="notification")
    data = {}
    notice_idx = 0

    for div in notifications:
        a_tag = div.find("a", href=True)
        if not a_tag:
            continue

        relative_link = a_tag["href"]
        full_link = urljoin(base_url, relative_link)

        title = a_tag.get_text(strip=True).replace('(Click Here)', '').strip()
        if not title:
            continue

        data[str(notice_idx)] = {
            "Title": title,
            "Link": full_link
        }
        notice_idx += 1

    return data

"""if __name__ == "__main__":
    results = INC()

    with open("INC.json", "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)

    print(f"✅ Saved {len(results)} notifications to 'INC.json'")"""
