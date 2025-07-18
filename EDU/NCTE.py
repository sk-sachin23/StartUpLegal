import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from datetime import datetime

def NCTE():
    base_url = "https://ncte.gov.in/ncte_new/page-archive-public-notice"
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/114.0.0.0 Safari/537.36"
        )
    }

    response = requests.get(base_url, headers=headers)
    response.raise_for_status()

    html_content = BeautifulSoup(response.content, "html.parser")

    announcements_div = html_content.find("div", id="vPillsCouncil")
    if not announcements_div:
        print("❌ Could not find <div id='vPillsCouncil'>.")
        return {}

    announcements_table = announcements_div.find("table", class_="table table-striped hover table-bordered")
    if not announcements_table:
        print("❌ Could not find the table inside <div id='vPillsCouncil'>.")
        return {}

    table_body = announcements_table.find("tbody")
    table_rows = table_body.find_all("tr")

    announcements_data = {}

    for index, row in enumerate(table_rows):
        columns = row.find_all("td")
        if len(columns) >= 4:
            raw_date_text = columns[1].get_text(strip=True)
            try:
                formatted_date = datetime.strptime(raw_date_text, "%d/%m/%Y").strftime("%d-%m-%Y")
            except ValueError:
                formatted_date = raw_date_text  # Leave it as-is if parsing fails

            announcement_title = columns[2].get_text(strip=True)
            link_element = columns[3].find("a")
            announcement_url = urljoin(base_url, link_element["href"].replace("\\", "/")) if link_element else ""

            announcements_data[str(index)] = {
                "Date": formatted_date,
                "Title": announcement_title,
                "Link": announcement_url
            }

    return announcements_data