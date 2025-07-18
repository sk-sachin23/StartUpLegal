# StartUpLegal Newsletter Tools

This project scrapes regulatory websites, builds a newsletter and can
optionally send it via Mailchimp. The entry point is `main.py` which
provides a small CLI.

## Usage

```bash
python main.py scrape               # scrape all educational bodies
python main.py scrape AICTE BCI     # scrape only specific bodies

python main.py render --data data/2025-07-12.json \
                  --date "12 July 2025" --number 1

python main.py send                # run gen_news.py to send newsletter
```

The `render` command outputs an HTML newsletter using the templates in the
`templates/` folder and the JSON data produced by `scrape`.

`send` simply runs `gen_news.py`. Configure that script with your Mailchimp
credentials if you wish to distribute the generated newsletter.

