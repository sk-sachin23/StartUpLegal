import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import re
from datetime import datetime

# Robust static headers
def get_headers():
    return {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/114.0.0.0 Safari/537.36"
        ),
        "Accept": (
            "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8"
        ),
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "en-US,en;q=0.9",
        "Connection": "keep-alive",
        "Referer": "https://www.google.com/"
    }

# Main scraping function
def DHE():
    url = "https://www.education.gov.in/en/higher_education"
    base_url = "https://www.education.gov.in"
    tab_labels = ["Update", "Circular", "Press Releases", "Advertisement", "Achievements"]

    response = requests.get(url, headers=get_headers())
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")

    results = {label: {} for label in tab_labels}

    for i in range(len(tab_labels)):
        tab_id = f"quicktabs-tabpage-higher_education_quick_tab-{i}"
        tab_section = soup.find("div", id=tab_id)
        if not tab_section:
            continue

        list_items = tab_section.find_all("li")
        for idx, li in enumerate(list_items):
            a_tag = li.find("a", href=True)
            if not a_tag:
                continue

            raw_title = a_tag.get_text(strip=True)

            # Extract date before removing anything
            date_match = re.search(r'(\d{1,2} \w+ \d{4})', raw_title)
            if date_match:
                try:
                    raw_date = datetime.strptime(date_match.group(1), "%d %B %Y")
                    date = raw_date.strftime("%d-%m-%Y")
                except ValueError:
                    date = "Invalid Date"
            else:
                date = "N/A"

            # Clean title: remove (date + time), (MB), (KB)
            clean_title = re.sub(r'\([^)]*\d{4}[^)]*\)', '', raw_title)  # (Tuesday, 8 July 2025 - 1:36pm)
            clean_title = re.sub(r'\([^)]*(MB|KB)\)', '', clean_title)   # (2.51 MB) or (512 KB)
            title = re.sub(r'\s{2,}', ' ', clean_title).strip().rstrip('-').strip()

            link = urljoin(base_url, a_tag['href'])

            results[tab_labels[i]][idx] = {
                "Date": date,
                "Title": title,
                "Link": link
            }

    return results
