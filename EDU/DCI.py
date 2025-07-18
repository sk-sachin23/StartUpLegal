import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import json

def get_session_with_retries(retries=3, backoff_factor=1, status_forcelist=(500, 502, 503, 504)):
    session = requests.Session()
    retry = Retry(
        total=retries,
        read=retries,
        connect=retries,
        backoff_factor=backoff_factor,
        status_forcelist=status_forcelist,
        raise_on_status=False
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    return session

def DCI():
    url = "https://dciindia.gov.in/Notification.aspx"
    session = get_session_with_retries()

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                      "AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/114.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9",
        "Referer": "https://www.google.com"
    }

    try:
        response = session.get(url, headers=headers, timeout=10)
        response.raise_for_status()
    except requests.exceptions.HTTPError as e:
        print(f"❌ HTTP Error: {e}")
        return {}
    except requests.exceptions.RequestException as e:
        print(f"❌ Request Exception: {e}")
        return {}

    soup = BeautifulSoup(response.content, "html.parser")
    data = {}
    notice_idx = 0

    for tr in soup.find_all("tr"):
        a_tag = tr.find("a", href=True)
        if a_tag:
            title = a_tag.get_text(strip=True)
            link = urljoin(url, a_tag["href"])

            # Skip empty titles or homepage links
            if title and "Home.aspx" not in link:
                data[str(notice_idx)] = {
                    "Title": title,
                    "Link": link
                }
                notice_idx += 1

    return data

"""if __name__ == "__main__":
    results = DCI()

    with open("DCI.json", "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)

    print(f"✅ Saved {len(results)} notices to 'DCI.json'")
"""