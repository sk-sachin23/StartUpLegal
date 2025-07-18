import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from fake_useragent import UserAgent
from datetime import datetime

def AICTE():
    base_url = 'https://www.aicte.gov.in'
    url = f'{base_url}/bulletins/circulars'
    headers = {
        'User-Agent': UserAgent().chrome
    }

    resp = requests.get(url, headers=headers, timeout=10)
    soup = BeautifulSoup(resp.text, 'html.parser')

    data = {}
    notice_idx = 0

    main_div = soup.select_one("div.advertisementContentBox")
    if not main_div:
        return data

    rows = main_div.select('div.views-row')
    for row in rows:
        title_tag = row.select_one('p.titleText > a')
        date_tag = row.select_one('time.datetime')
        pdf_link_tag = row.select_one('div.advertisementLinkBtn > a')

        title = title_tag.get_text(strip=True) if title_tag else 'N/A'
        
        if date_tag and date_tag.has_attr('datetime'):
            try:
                iso_date = date_tag['datetime'].split('T')[0]
                date_obj = datetime.strptime(iso_date, '%Y-%m-%d')
                formatted_date = date_obj.strftime('%d-%m-%Y')
            except:
                formatted_date = 'N/A'
        else:
            formatted_date = 'N/A'

        link = urljoin(base_url, pdf_link_tag['href']) if pdf_link_tag else 'N/A'

        data[str(notice_idx)] = {
            "Date": formatted_date,
            "Title": title,
            "Link": link
        }
        notice_idx += 1

    return data