import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime

def NIEPA():
    url = "https://niepaadm.samarth.edu.in/2025/"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                      "AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/114.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9",
        "Referer": "https://www.google.com"
    }

    r = requests.get(url, headers=headers, timeout=10)
    soup = BeautifulSoup(r.content, "html.parser")

    all_tabs = soup.find_all("div", id="myTabContent")
    data = {}
    count = 0

    for tab in all_tabs:
        rows = tab.select("li.mb-6 div.row")
        for row in rows:
            date_div = row.find("div", class_="col-md-2")
            link_div = row.find("div", class_="col-md-10")

            if date_div and link_div:
                raw_date = date_div.get_text(strip=True)
                try:
                    # Convert from "04 Jul 2025" to "04-07-2025"
                    date_obj = datetime.strptime(raw_date, "%d %b %Y")
                    date = date_obj.strftime("%d-%m-%Y")
                except ValueError:
                    date = raw_date

                a_tag = link_div.find("a", href=True)
                if a_tag:
                    title = a_tag.get_text(strip=True).replace("🔗", "").strip()
                    link = a_tag["href"].strip()

                    data[str(count)] = {
                        "Date": date,
                        "Title": title,
                        "Link": link
                    }
                    count += 1

    return data
