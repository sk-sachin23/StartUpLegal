import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import json

def get_retry_session():
    session = requests.Session()
    retries = Retry(
        total=3,
        backoff_factor=1,
        status_forcelist=(500, 502, 503, 504),
        raise_on_status=False
    )
    adapter = HTTPAdapter(max_retries=retries)
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    session.headers.update({
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/114.0.0.0 Safari/537.36"
        ),
        "Referer": "https://vci.admissions.nic.in/"
    })
    return session

def VCI():
    base_url = "https://vci.admissions.nic.in/"
    session = get_retry_session()

    try:
        response = session.get(base_url, timeout=10)
        response.raise_for_status()
    except Exception as e:
        print("❌ Request failed:", e)
        return {}

    soup = BeautifulSoup(response.text, 'html.parser')
    gen_list_div = soup.find("div", class_="gen-list")
    data = {}
    count = 0

    if gen_list_div:
        for li in gen_list_div.find_all("li"):
            a_tag = li.find("a", href=True)
            if a_tag:
                title = a_tag.get_text(strip=True).replace('\n', '').replace('\r', '')
                link = urljoin(base_url, a_tag["href"].strip())
                data[str(count)] = {
                    "Title": title,
                    "Link": link
                }
                count += 1

    return data

"""if __name__ == "__main__":
    result = VCI()
    with open("VCI.json", "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)

    print(f"✅ Saved {len(result)} items to VCI.json")
"""