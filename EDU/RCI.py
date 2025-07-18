import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, quote
import json
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

def get_retry_session():
    session = requests.Session()
    retry = Retry(
        total=3,
        backoff_factor=1,
        status_forcelist=(500, 502, 503, 504),
        raise_on_status=False
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount("https://", adapter)
    session.mount("http://", adapter)

    session.headers.update({
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/114.0.0.0 Safari/537.36"
        ),
        "Referer": "https://rehabcouncil.nic.in"
    })
    return session

def RCI():
    base_url = "https://rehabcouncil.nic.in"
    url = f"{base_url}/notices-circulars"
    session = get_retry_session()

    try:
        r = session.get(url, timeout=10, verify=False)  # SSL verification disabled
        r.raise_for_status()
    except requests.exceptions.RequestException as e:
        print("❌ Error fetching RCI page:", e)
        return {}

    soup = BeautifulSoup(r.content, "html.parser")
    rows = soup.find_all('tr')[1:]  # Skip header row
    data = {}

    count = 0
    for tr in rows:
        try:
            title = tr.find('td', class_='views-field-title').get_text(strip=True).replace('\r', '').replace('\n', '')
            date = tr.find('td', class_='views-field-field-publish-date').get_text(strip=True)
            relative_link = tr.find('a')['href'].strip()
            full_link = urljoin(base_url, quote(relative_link))

            data[str(count)] = {
                "Title": title,
                "Date": date,
                "Link": full_link
            }
            count += 1
        except Exception as e:
            print(f"⚠️ Skipping one row due to error: {e}")
            continue

    return data

"""if __name__ == "__main__":
    result = RCI()
    with open("RCI.json", "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)

    print(f"✅ Saved {len(result)} notices to RCI.json")
"""