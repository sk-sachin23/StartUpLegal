import importlib
import json
import time
import os
import traceback
from itertools import islice
from datetime import datetime, timedelta

def extractData(educational_bodies):
    start_time = time.time()

    # --- Create log and data folders ---
    os.makedirs('logs', exist_ok=True)
    os.makedirs('data', exist_ok=True)
    log_filename = f"logs/run_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"

    def write_log(message):
        with open(log_filename, 'a', encoding='utf-8') as log_file:
            log_file.write(f"{datetime.now().isoformat()} — {message}\n")

    write_log("Script started.")

    # Date file names
    today_str = datetime.now().strftime('%Y-%m-%d')
    today_file = f"data/{today_str}.json"
    yesterday_str = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
    yesterday_file = f"data/{yesterday_str}.json"

    # Try to load yesterday's data, if exists
    def read_json_safe(filename):
        if not os.path.exists(filename):
            return {}
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            write_log(f"Could not read {filename}: {e}")
            return {}

    prev_data = read_json_safe(yesterday_file)

    changed_data = {}

    for body in educational_bodies:
        try:
            # Import and run the scraping function
            write_log(f"Importing module: EDU.{body}")
            mod = importlib.import_module(f"EDU.{body}")
            func = getattr(mod, body)
            result = func()

            # Only keep 2/3 items as per your rules
            if body in ("DSL", "MoE", "DHE"):
                trimmed = {section: dict(islice(rows.items(), 2)) for section, rows in result.items()}
            else:
                trimmed = dict(list(result.items())[:3])

            prev_body_data = prev_data.get(body, {})

            # Special handling for BCI: compare only the set of URLs
            if body == "BCI":
                def get_urls(d):
                    if not isinstance(d, dict):
                        return []
                    urls = []
                    for k, v in d.items():
                        if isinstance(v, dict) and "url" in v:
                            urls.append(v["url"])
                    return sorted(urls)

                urls_today = get_urls(trimmed)
                urls_prev = get_urls(prev_body_data)
                if urls_today != urls_prev:
                    changed_data[body] = trimmed
                    write_log(f"{body}: 'url' fields changed, will be written to {today_file}")
                    write_log(f"{body}: Previous URLs: {urls_prev}")
                    write_log(f"{body}: Current URLs: {urls_today}")
                else:
                    write_log(f"{body}: No change in 'url' fields, skipping.")

            # For all others, full data compare
            else:
                if trimmed != prev_body_data:
                    changed_data[body] = trimmed
                    write_log(f"{body}: Data changed, will be written to {today_file}")
                else:
                    write_log(f"{body}: No change from previous data, skipping.")

        except Exception as e:
            write_log(f"Error processing {body}: {e}")
            tb = traceback.format_exc()
            write_log(tb)

    # Write changed data if there is any change
    output_path = None
    if changed_data:
        with open(today_file, "w", encoding="utf-8") as f:
            json.dump(changed_data, f, indent=2, ensure_ascii=False)
        write_log(f"Written changed data to {today_file}")
        print(f"Changed data written to {today_file}")
        output_path = today_file
    else:
        write_log("No changes detected for any educational body. No file written.")
        print("No changes detected. No new data file written.")
        if os.path.exists(yesterday_file):
            output_path = yesterday_file
            write_log(f"Using yesterday's file: {yesterday_file}")

    end_time = time.time()
    exec_time = end_time - start_time
    write_log(f"Execution time: {exec_time:.2f} seconds")
    print("Execution time:", exec_time, "seconds")
    print(f"Log file saved at {log_filename}")

    return exec_time, output_path
    

