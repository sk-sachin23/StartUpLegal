import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import json

def ICAI():
    url = "https://www.icai.org/category/announcements"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                      "AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/114.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9",
        "Referer": "https://www.google.com"
    }

    resp = requests.get(url, headers=headers, timeout=10)
    soup = BeautifulSoup(resp.text, "html.parser")

    data = {}
    notice_idx = 0

    for li in soup.select("li.list-group-item"):
        a = li.find("a", href=True)
        if not a:
            continue

        href = a['href']
        link = href if bool(urlparse(href).netloc) else urljoin(url, href)
        text = a.get_text(strip=True)

        # Extract date if available
        if text.endswith(')') and '(' in text:
            date = text[text.rfind('(')+1:-1].strip()
            title = text[:text.rfind('(')].strip()
        else:
            date = ""
            title = text.strip()

        if title.endswith("-"):
            title = title[:-1].strip()

        data[str(notice_idx)] = {
            "Date": date,
            "Title": title,
            "Link": link
        }
        notice_idx += 1

    return data

"""if __name__ == "__main__":
    results = ICAI()

    with open("ICAI.json", "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)

    print(f"✅ Saved {len(results)} announcements to 'ICAI.json'")
"""