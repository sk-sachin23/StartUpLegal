from playwright.sync_api import sync_playwright
from urllib.parse import urljoin

def get_browser_headers():
    return {
        "user_agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/114.0.0.0 Safari/537.36"
        ),
        "extra_http_headers": {
            "Accept-Language": "en-US,en;q=0.9",
            "Upgrade-Insecure-Requests": "1",
            "Sec-Fetch-Site": "same-origin",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-User": "?1",
            "Sec-Fetch-Dest": "document",
        }
    }

def UGC():
    """Scrape UGC Notices page and handle multiple links properly."""
    base_url = "https://www.ugc.gov.in"

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)

        headers = get_browser_headers()
        context = browser.new_context(
            user_agent=headers["user_agent"],
            extra_http_headers=headers["extra_http_headers"]
        )

        page = context.new_page()
        page.goto("https://www.ugc.gov.in/Notices/")
        page.wait_for_selector("table.table")

        rows = page.locator("table.table tbody tr")
        data = {}
        notice_idx = 0

        for i in range(rows.count()):
            cols = rows.nth(i).locator("td")
            title_td = cols.nth(1)
            date = cols.nth(2).inner_text().strip()

            title = title_td.inner_text().split("\n")[0].strip()

            # ✅ Get all <a> tags
            link_elements = title_td.locator("a").element_handles()
            links = {}

            if len(link_elements) == 1:
                href = link_elements[0].get_attribute("href")
                if href:
                    links["View"] = urljoin(base_url, href)
            elif len(link_elements) > 1:
                for link_el in link_elements:
                    href = link_el.get_attribute("href")
                    link_text = link_el.inner_text().strip() or "Document"
                    if href:
                        links[link_text] = urljoin(base_url, href)

            if not title:
                continue

            data[str(notice_idx)] = {
                "Date": date,
                "Title": title,
                "Links": links
            }
            notice_idx += 1

        browser.close()
        return data

