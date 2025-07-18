import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import json
import urllib3

# Suppress SSL warning for verify=False
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def ICAR():
    base_url = "https://icar.org.in"
    url = "https://icar.org.in/en/circulars-data"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                      "AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/114.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9",
        "Referer": "https://www.google.com"
    }

    response = requests.get(url, headers=headers, verify=False, timeout=10)
    soup = BeautifulSoup(response.content, "html.parser")

    data = {}
    notice_idx = 0

    for row in soup.find_all("tr"):
        cols = row.find_all("td")
        if len(cols) < 5:
            continue  # Skip if structure is unexpected

        title = cols[1].get_text(strip=True)
        category = cols[2].get_text(strip=True)
        date = cols[3].get_text(strip=True)

        link_tag = cols[4].find("a")
        link = urljoin(base_url, link_tag['href']) if link_tag and link_tag.has_attr('href') else None

        data[str(notice_idx)] = {
            "Title": title,
            "Category": category,
            "Date": date,
            "Link": link
        }
        notice_idx += 1

    return data

"""if __name__ == "__main__":
    results = ICAR()

    with open("ICAR.json", "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)

    print(f"✅ Saved {len(results)} circulars to 'ICAR.json'")"""
