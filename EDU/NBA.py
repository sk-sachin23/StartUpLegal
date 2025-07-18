import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import re
import json
from datetime import datetime

def NBA():
    base_url = "https://www.nbaind.org"
    url = "https://www.nbaind.org/Home/latest"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                      "AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/114.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9",
        "Referer": "https://www.google.com"
    }

    response = requests.get(url, headers=headers, timeout=10)
    soup = BeautifulSoup(response.content, "html.parser")

    data = {}
    index = 0
    ol = soup.find('ol')

    if ol:
        for li in ol.find_all('li'):
            date_match = re.search(r'\d{1,2}/\d{1,2}/\d{4}', li.text)
            if date_match:
                raw_date = date_match.group(0)
                try:
                    date_obj = datetime.strptime(raw_date, "%d/%m/%Y")
                    date = date_obj.strftime("%d-%m-%Y")
                except ValueError:
                    date = raw_date
            else:
                date = ""

            a = li.find('a')
            if not a:
                continue

            title = a.get_text(strip=True)
            link = urljoin(base_url, a['href'])

            data[str(index)] = {
                "Date": date,
                "Title": title,
                "Link": link
            }
            index += 1

    return data
