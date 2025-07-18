# StartUpLegal Newsletter

This project collects regulatory notices from Indian higher education bodies and assembles them into a newsletter. Scrapers inside the `EDU/` package fetch the latest updates, `render.py` creates a styled HTML/PDF newsletter, and `gen_news.py` can upload the newsletter to Mailchimp.

## Installation

1. Create a Python virtual environment and activate it:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```
2. Install the required Python packages:
   ```bash
   pip install playwright requests beautifulsoup4 fake-useragent jinja2 pdfkit mailchimp-marketing python-dotenv
   ```
   You may also need the `wkhtmltopdf` system package for PDF generation.

## Environment Variables

Create a `.env` file in the project root containing your Mailchimp credentials:

```
MAILCHIMP_API_KEY=<your-api-key>
MAILCHIMP_AUDIENCE_ID=<your-audience-id>
```

These variables are used by `gen_news.py` when sending the newsletter.

## Running the Scripts

### extractData.py

Run the scraper by calling `extractData()` with a list of educational body modules to load:

```bash
python -c "from extractData import extractData; extractData(['AICTE','UGC','BCI'])"
```

This writes a dated JSON file in the `data/` folder and saves a log in `logs/`.

### render.py

Generate an HTML newsletter and convert it to PDF:

```bash
python render.py
```

The script reads the JSON file for today's date from `data/` and outputs `newsletter.html` and `newsletter.pdf`.

### gen_news.py

Create a Mailchimp draft campaign using the rendered newsletter:

```bash
python gen_news.py
```

This requires the environment variables above and produces `file.html` locally. The Mailchimp upload portion of the script is commented out; uncomment it to send the campaign.

## Folder Structure

```
StartUpLegal/
├── data/           # JSON data files (YYYY-MM-DD.json)
├── logs/           # Run logs (run_YYYYMMDD_HHMMSS.log)
├── templates/      # Jinja2 templates and CSS
├── EDU/            # Individual scrapers for each body
└── ...
```

The `data/` and `logs/` directories are created automatically when running the scraper.

# StartUpLegal Newsletter Workflow

This project includes a small Flask application that allows you to run the newsletter generation tasks manually from a web interface.

## Starting the server

Run the following command from the repository root:

```bash
python3 webapp.py
```

The app will be available on `http://127.0.0.1:5000/` by default.

