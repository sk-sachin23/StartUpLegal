import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from datetime import datetime

def DSL():
    base_url = 'https://dsel.education.gov.in/en'
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                      "AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/114.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9",
        "Referer": "https://www.google.com"
    }

    r = requests.get(base_url, headers=headers, timeout=10)
    soup = BeautifulSoup(r.content, 'html.parser')

    updt_divs = soup.select('div.updt')
    categories = ["Press Release", "Update"]
    categorized_data = {}

    for index, div in enumerate(updt_divs[:2]):  # Only process first two sections
        category = categories[index]
        entries = {}
        links = div.find_all('a')

        notice_idx = 0
        for a in links:
            title = a.get('title', '').strip()
            date_tag = a.select_one('.date')
            raw_date = date_tag.get_text(strip=True) if date_tag else ''
            href = a.get('href', '')

            # Convert "Wednesday, July 2, 2025" → "02-07-2025"
            formatted_date = ''
            try:
                parsed_date = datetime.strptime(raw_date, "%A, %B %d, %Y")
                formatted_date = parsed_date.strftime("%d-%m-%Y")
            except Exception:
                formatted_date = raw_date  # Leave as-is if format doesn't match

            if title and href:
                full_link = urljoin(base_url, href)
                if full_link == "https://dsel.education.gov.in/sites/default/files/update/List_School_Boards.pdf" : continue
                entries[str(notice_idx)] = {
                    "Title": title,
                    "Date": formatted_date,
                    "Link": full_link
                }
                notice_idx += 1

        categorized_data[category] = entries

    return categorized_data

