import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import re
import json

def NIRF():
    url = "https://www.nirfindia.org/Home/Advertisement"
    base_url = "https://www.nirfindia.org"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                      "AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/114.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9",
        "Referer": "https://www.google.com"
    }

    response = requests.get(url, headers=headers, timeout=10)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, 'html.parser')
    main_content = soup.find("div", id="mainContent")

    data = {}
    count = 0

    if main_content:
        for li in main_content.find_all("li"):
            a_tag = li.find("a")
            if a_tag and a_tag.get("href"):
                title_raw = a_tag.get_text(strip=True)
                title = title_raw.replace('\r', '').replace('\n', '').replace('/r', '').replace('/n', '').strip()
                link = urljoin(base_url, a_tag.get("href").strip())

                match = re.search(r"\b(\d{2}-\d{2}-\d{4})\b", title)
                date = match.group(1) if match else ""

                data[str(count)] = {
                    "Date": date,
                    "Title": title,
                    "Link": link
                }
                count += 1

    return data

"""if __name__ == "__main__":
    result = NIRF()

    with open("NIRF.json", "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)

    print(f"✅ Saved {len(result)} items to 'NIRF.json'")
"""