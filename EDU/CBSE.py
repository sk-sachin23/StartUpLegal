import re
from urllib.parse import urljoin
import requests
from bs4 import BeautifulSoup, Tag, NavigableString
from fake_useragent import UserAgent
from datetime import datetime


def CBSE():
    base_url = "https://www.cbse.gov.in/cbsenew/"
    root_url = "https://www.cbse.gov.in"
    page_url = urljoin(base_url, "cbse.html")

    # Generate fake user-agent
    try:
        ua = UserAgent()
        user_agent = ua.random
    except Exception:
        user_agent = (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
            "(KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
        )

    headers = {"User-Agent": user_agent}
    resp = requests.get(page_url, headers=headers, timeout=20)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.content, "html.parser")

    notices = {}
    ul = soup.find("ul")
    if not ul:
        return notices

    for idx, li in enumerate(ul.find_all("li"), start=0):
        raw_text = li.get_text(" ", strip=True)

        # Extract and format date
        m = re.search(r"\d{2}/\d{2}/\d{4}", raw_text)
        if m:
            try:
                date_obj = datetime.strptime(m.group(0), "%d/%m/%Y")
                date = date_obj.strftime("%d-%m-%Y")
            except Exception:
                date = None
        else:
            date = None

        # Extract main title before first <a>
        title = ""
        for content in li.contents:
            if isinstance(content, Tag) and content.name == "a":
                break
            if isinstance(content, NavigableString):
                title += content.strip()
            elif isinstance(content, Tag):
                title += content.get_text(strip=True)
        title = title.strip(":- ").strip()
        title = re.sub(r"\(\s*\d+(\.\d+)?\s*(KB|MB|GB)\s*\)", "", title).strip()

        # Fallback: use first <a> text if title is empty
        if not title:
            first_a = li.find("a")
            if first_a:
                title = first_a.get_text(strip=True)
                title = re.sub(r"\(\s*\d+(\.\d+)?\s*(KB|MB|GB)\s*\)", "", title).strip()

        # Extract links as dict
        links_dict = {}
        for a in li.find_all("a", href=True):
            href = a["href"].strip()
            base = root_url if href.startswith("/") else base_url
            full_url = urljoin(base, href)
            full_url = requests.utils.requote_uri(full_url)

            icon_class = a.find("i")["class"] if a.find("i") else []

            # Determine link title
            if "fa-file-pdf-o" in icon_class:
                link_title = "View-PDF"
            elif "fa-link" in icon_class:
                link_title = "URL"
            else:
                link_title = a.get_text(strip=True)
                link_title = re.sub(r"\(\s*\d+(\.\d+)?\s*(KB|MB|GB)\s*\)", "", link_title).strip()
                if not link_title:
                    link_title = "Link"

            # Handle duplicate link titles
            original_title = link_title
            counter = 2
            while link_title in links_dict:
                link_title = f"{original_title}-{counter}"
                counter += 1

            links_dict[link_title] = full_url

        notices[str(idx)] = {
            "Date": date,
            "Title": title,
            "Links": links_dict
        }

    return notices
