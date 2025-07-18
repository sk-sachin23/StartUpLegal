import requests
from urllib.parse import urlparse, quote
from datetime import datetime

def NMC():
    endpoint = "https://www.nmc.org.in/MCIRest/open/getDataFromService"
    params = {
        "service": "getLatestNewsNew"
    }
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/137.0.0.0 Safari/537.36"
        ),
        "Referer": "https://www.nmc.org.in/information-desk/all-news/",
        "X-Requested-With": "XMLHttpRequest"
    }

    try:
        resp = requests.get(endpoint, headers=headers, params=params, timeout=60)
        resp.raise_for_status()
    except Exception as e:
        print("❌ Request error:", e)
        return {}

    try:
        data_list = resp.json()
    except ValueError as e:
        print("❌ Failed to parse JSON:", e)
        return {}

    if not isinstance(data_list, list):
        print("❌ Unexpected JSON structure: expected a list at top level.")
        return {}

    base = "https://www.nmc.org.in"
    data = {}
    count = 0

    for entry in data_list:
        page_name = entry.get("pageName", "").replace('\r', '').replace('\n', '').strip()
        raw_date = entry.get("updatedDate", "").strip()
        doc_path = entry.get("docUpload", "").strip()

        # Convert date from d/m/y to d-m-y
        try:
            date_obj = datetime.strptime(raw_date, "%d/%m/%Y")
            date = date_obj.strftime("%d-%m-%Y")
        except ValueError:
            date = raw_date

        if not page_name:
            continue

        if doc_path:
            parsed = urlparse(doc_path)
            encoded_path = quote(parsed.path)
            full_link = f"{base}/MCIRest/open/getDocument?path={encoded_path}"
        else:
            full_link = ""

        data[str(count)] = {
            "Title": page_name,
            "Date": date,
            "Link": full_link
        }
        count += 1

    return data
