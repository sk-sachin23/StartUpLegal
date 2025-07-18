import json
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from datetime import datetime

BASE_URL = "https://pci.gov.in"
URL = f"{BASE_URL}/en/blog/?category=Circulars"
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/114.0.0.0 Safari/537.36"
    )
}

def format_date(date_str):
    try:
        return datetime.strptime(date_str, "%B %d, %Y").strftime("%d-%m-%Y")
    except:
        return date_str

def PCI():
    session = requests.Session()
    session.headers.update(HEADERS)

    try:
        res = session.get(URL, timeout=15)
        res.raise_for_status()
    except Exception as e:
        print(f"❌ Failed to fetch main page: {e}")
        return {}

    soup = BeautifulSoup(res.text, "html.parser")
    articles = soup.select("div.divide-y article")

    data = {}
    for i, article in enumerate(articles):
        a_tag = article.select_one("h2 a[href]")
        time_tag = article.select_one("time")

        if not a_tag or not time_tag:
            continue

        title = a_tag.get_text(strip=True)
        url = urljoin(BASE_URL, a_tag["href"])
        date = format_date(time_tag.get_text(strip=True))

        data[str(i)] = {
            "Date": date,
            "Title": title,
            "Link": url
        }

    return data
