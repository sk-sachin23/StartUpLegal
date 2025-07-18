import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import json

def NTA():
    base_url = "https://www.nta.ac.in/"
    url = "https://www.nta.ac.in/NoticeBoardArchive"

    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/114.0.0.0 Safari/537.36"
        ),
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9",
        "Referer": "https://www.google.com"
    }

    response = requests.get(url, headers=headers, timeout=10)
    soup = BeautifulSoup(response.content, "html.parser")

    rows = soup.find_all("tr")
    data = {}
    count = 0

    for row in rows:
        content_tag = row.find("content")
        a_tag = row.find("a", href=True)

        if content_tag and a_tag:
            raw_title = content_tag.get_text(strip=True)
            title = raw_title.replace('\r', '').replace('\n', '').replace('/r', '').replace('/n', '').strip()

            relative_link = a_tag["href"]
            absolute_link = urljoin(base_url, relative_link)

            data[str(count)] = {
                "Title": title,
                "Link": absolute_link
            }
            count += 1

    return data

"""if __name__ == "__main__":
    result = NTA()

    with open("NTA.json", "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)

    print(f"✅ Saved {len(result)} items to 'NTA.json'")
"""