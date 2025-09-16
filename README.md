# StartUpLegal Newsletter Automation

## What this project does
StartUpLegal helps you collect education-related news, turn it into a polished PDF newsletter, and send that newsletter to your Mailchimp subscribers with just a few clicks. The web page at `webapp.py` guides you through three buttons:

1. **Scrape** – runs `extractData.extractData` to pull the latest updates and save them into the `data/` folder.
2. **Render** – calls `render.render_newsletter_html` and `render.html_to_pdf_pdfkit` to turn that data into a nice-looking HTML file and a PDF using wkhtmltopdf.
3. **Send** – uses `gen_news.send_newsletter` to upload the HTML to Mailchimp and send the email campaign.

The homepage in `templates/index.html` shows each step in plain language so you always know what is happening next.

## What you need before you start
- **Python 3.10 or newer.** This is the programming language the project runs on. You can download it from [python.org](https://www.python.org/downloads/).
- **wkhtmltopdf.** This tool converts the HTML version of the newsletter into a PDF. The rendering code in `render.py` looks for the `wkhtmltopdf` program on your computer.
- **Mailchimp credentials.** You need an API key and an Audience/List ID so Mailchimp knows who you are and who to send the newsletter to.
- **Playwright with Chromium.** One of the scrapers (`EDU/UGC.py`) opens a headless Chromium browser via Playwright, so the browser files must be installed.

> **Tip for first-time users:** The commands below run in a terminal (Command Prompt on Windows, Terminal app on macOS, or any Linux shell). Type each line and press Enter before moving to the next one.

## Step-by-step setup
1. **Create a project folder (if you have not already).** Download or clone this repository into a folder you can find easily.
2. **Open a terminal in that folder.** On Windows you can right-click inside the folder and choose *Open in Terminal* or *Open PowerShell window here*. On macOS or Linux, open Terminal and use `cd` to move into the folder.
3. **Create and activate a virtual environment.** This keeps your project’s Python packages separate from the rest of your computer.
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate  # Windows users: .venv\Scripts\activate
   ```
   After activation you should see `(.venv)` at the start of your terminal prompt.
4. **Install the Python packages listed for the project.**
   ```bash
   pip install -r requirements.txt
   ```
5. **Install the Playwright browser files.** This downloads the Chromium browser that Playwright needs.
   ```bash
   playwright install chromium
   ```
6. **Install wkhtmltopdf and make sure your computer can find it.**
   - **macOS (Homebrew):** `brew install wkhtmltopdf` puts the program in `/usr/local/bin` or `/opt/homebrew/bin`, which already sit on your PATH.
   - **Windows:** Download the installer from the wkhtmltopdf website, run it, and then add the folder (for example `C:\Program Files\wkhtmltopdf\bin`) to your system `Path`. Open a new Command Prompt and run `wkhtmltopdf --version` to make sure it works.
   - **Linux:** Use your package manager (`sudo apt-get install wkhtmltopdf`) or download the binary, move it to `/usr/local/bin`, and mark it executable with `chmod +x /usr/local/bin/wkhtmltopdf`.
   If your system cannot find the program later, you can tell the app exactly where it lives using the `WKHTMLTOPDF_PATH` setting in the `.env` file (explained below).

## Fill in your settings with `.env`
Sensitive information such as API keys should not live directly in the code. Instead, this project uses a hidden file named `.env` that Flask and the helper scripts read at runtime.

1. **Copy the template file.** The repository includes a starter file named `local.env` with placeholders.
   ```bash
   cp local.env .env
   ```
2. **Open `.env` in a text editor.** You can use Notepad (Windows), TextEdit (macOS – in plain text mode), or any editor you like.
3. **Replace the placeholder text:**
   - `MAILCHIMP_API_KEY=` – paste your Mailchimp API key after the `=` sign.
   - `MAILCHIMP_AUDIENCE_ID=` – paste the ID of the audience/list you want to email.
   - `WKHTMLTOPDF_PATH=` – leave this blank if `wkhtmltopdf` is on your PATH. Otherwise paste the full path to the `wkhtmltopdf` executable, such as `C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe` (Windows) or `/usr/local/bin/wkhtmltopdf` (macOS/Linux).
4. **Save the file.** Do not share `.env` publicly—these values are private.

Any time you change `.env`, restart the Flask app (or rerun your script) so it reads the updated settings.

## Run the web app
1. Make sure your virtual environment is active (`(.venv)` should appear in your prompt).
2. Start the Flask server:
   ```bash
   python webapp.py
   ```
3. Open your browser and go to [http://127.0.0.1:5000/](http://127.0.0.1:5000/). You will see three large buttons—Scrape, Render, and Send—with a short explanation under each one.
4. Click the buttons in order:
   - **Scrape** gathers new data and writes JSON files into the `data/` folder. It also records what happened in the `logs/` folder.
   - **Render** builds the HTML newsletter and converts it into a PDF. The files are saved next to your project (for example `newsletter.html` and `newsletter.pdf`).
   - **Send** uploads the HTML version to Mailchimp using the values from `.env` and triggers the campaign.

## Where files are saved and other ways to send
- Scraped data lives in `data/` with filenames like `2024-01-15.json` so you can look back at previous runs.
- Log files such as `logs/run_YYYYMMDD_HHMMSS.log` describe what each scraping session did.
- You can send the latest newsletter without using the web page by running:
  ```bash
  python gen_news.py
  ```
  This script uses the same `.env` settings and prints out the Mailchimp campaign ID if everything worked.

## Troubleshooting tips
- **Playwright says Chromium is missing or crashes:** Rerun `playwright install chromium`. On Linux, make sure you have the required system libraries for headless Chromium.
- **wkhtmltopdf cannot be found:** Run `wkhtmltopdf --version` in your terminal. If you get an error, either reinstall wkhtmltopdf or set `WKHTMLTOPDF_PATH` in `.env` to the exact location of the executable.
- **Emails fail to send:** Double-check your Mailchimp API key and Audience ID in `.env`, and ensure the Mailchimp account has permission to send to that audience.

## License
If this repository also includes an MIT `LICENSE` file, that license applies to your use and redistribution of the code.
