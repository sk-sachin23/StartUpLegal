import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from datetime import datetime

def MoA():
    url = "https://e-aushadhi.gov.in/ayush/notifications/NA=="
    base_url = "https://e-aushadhi.gov.in"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                      "AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/114.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9",
        "Referer": "https://www.google.com"
    }

    response = requests.get(url, headers=headers, timeout=10)
    soup = BeautifulSoup(response.text, 'html.parser')

    data = {}
    table = soup.find("table", {"id": "datatable1"})

    if table:
        tbody = table.find("tbody")
        if tbody:
            rows = tbody.find_all("tr")
            idx = 0
            for row in rows:
                cols = row.find_all("td")
                if len(cols) >= 4:
                    title = cols[1].get_text(strip=True)
                    date_raw = cols[2].get_text(strip=True)

                    # Convert date from yyyy-mm-dd to dd-mm-yyyy
                    try:
                        date = datetime.strptime(date_raw, "%Y-%m-%d").strftime("%d-%m-%Y")
                    except ValueError:
                        date = date_raw  # fallback if format is unexpected

                    a_tag = cols[3].find("a")
                    if a_tag and a_tag.get("href"):
                        abs_link = urljoin(base_url, a_tag["href"])
                        data[str(idx)] = {
                            "Date": date,
                            "Title": title,
                            "Link": abs_link
                        }
                        idx += 1

    return data
