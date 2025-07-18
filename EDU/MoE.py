import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import re
import json
from datetime import datetime

def parse_date_to_dmy(date_str):
    formats = ["%d-%B-%Y", "%d %B %Y"]
    for fmt in formats:
        try:
            return datetime.strptime(date_str, fmt).strftime("%d-%m-%Y")
        except ValueError:
            continue
    return date_str

def clean_title(raw_title):
    cleaned = re.sub(r"\([^)]*?\d{1,2}[- ]?[A-Za-z]+[- ]?\d{4}[^)]*?\)", "", raw_title)
    cleaned = re.sub(r"\(\s*\d+(\.\d+)?\s*(KB|MB)\s*\)", "", cleaned, flags=re.IGNORECASE)
    return cleaned.strip(" -")

def MoE():
    base_url = "https://www.education.gov.in/en"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                      "AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/114.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9",
        "Referer": "https://www.google.com"
    }

    resp = requests.get(base_url, headers=headers, timeout=10)
    soup = BeautifulSoup(resp.text, "html.parser")

    container = soup.find("div", id="quicktabs-container-home_quick_tab")

    tab_names = {
        0: "Update",
        1: "Circular",
        2: "Press Releases",
        3: "Advertisement",
        4: "Achievements"
    }

    date_pattern = re.compile(r"\b\d{1,2}[- ]?[A-Za-z]+[- ]?\d{4}\b")
    tabs_data = {}

    for i in range(5):
        tab_key = tab_names[i]
        tab_id = f"quicktabs-tabpage-home_quick_tab-{i}"
        tab_div = container.find("div", id=tab_id)
        if not tab_div:
            continue

        entries = {}
        notice_idx = 0
        for a in tab_div.find_all("a", class_="pdfIcon", href=True):
            raw_title = a.get_text(strip=True)
            cleaned_title = clean_title(raw_title)

            date_match = date_pattern.search(raw_title)
            date_raw = date_match.group(0) if date_match else "N/A"
            date_formatted = parse_date_to_dmy(date_raw) if date_match else "N/A"

            link = urljoin(base_url, a['href'].strip())

            entries[str(notice_idx)] = {
                "Title": cleaned_title,
                "Date": date_formatted,
                "Link": link
            }
            notice_idx += 1

        tabs_data[tab_key] = entries

    return tabs_data
