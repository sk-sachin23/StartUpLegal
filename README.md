# StartUpLegal

Utilities for scraping education-related websites and generating a newsletter.

## Setup

1. **Python dependencies**

   ```bash
   pip install -r requirements.txt
   ```

   After installing Playwright, download its browser binaries:

   ```bash
   playwright install
   ```

2. **External tools**

   `render.py` uses [wkhtmltopdf](https://wkhtmltopdf.org/) via `pdfkit` to generate PDFs. Install `wkhtmltopdf` separately and ensure the binary is on your `PATH`.

3. **Environment variables**

   Some scripts expect Mailchimp credentials and other settings in a `.env` file. See `gen_news.py` for the variables used.

## Running

Use `extractData.py` to collect data from education bodies. Render the newsletter with `render.py` and optionally send it using Mailchimp via `gen_news.py`.

