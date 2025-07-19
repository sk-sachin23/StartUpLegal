import os
import json
from jinja2 import Environment, FileSystemLoader
import pdfkit
import datetime

def render_newsletter_html(
    data_json: str,
    template_name: str,
    edition_date: str,
    edition_number: int,
    get_pdf: str,
    css_path: str,
    output_html: str
) -> str:
    """
    Load JSON data, render the Jinja2 template with inline CSS, and save to an HTML file.

    :param data_json: Path to the JSON data file.
    :param templates_dir: Directory containing the Jinja2 templates.
    :param template_name: Name of the newsletter template file.
    :param edition_date: Edition date string to render.
    :param edition_number: Edition number to render.
    :param css_path: Path to the styles.css file to inline.
    :param output_html: Path where the rendered HTML will be saved.
    :return: The path to the saved HTML file.
    """
    # Load data
    with open(data_json, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Render template
    env = Environment(loader=FileSystemLoader("templates"))
    template = env.get_template(template_name)
    html_content = template.render(
        data=data,
        edition_date=edition_date,
        edition_number=edition_number,
        pdf_url=get_pdf  # This will be set after PDF generation
    )

    # Inline CSS
    with open(css_path, 'r', encoding='utf-8') as css_file:
        css = css_file.read().replace('\n', ' ')
    html_content = html_content.replace(
        '</head>',
        f'<style type="text/css">{css}</style></head>'
    )

    # Save HTML file
    with open(output_html, 'w', encoding='utf-8') as f:
        f.write(html_content)

    return output_html


def html_to_pdf_pdfkit(
    input_html: str,
    output_pdf: str,
    wkhtmltopdf_path: str = None,
    options: dict = None
) -> None:
    """
    Convert an HTML file to PDF using pdfkit (wkhtmltopdf).

    :param input_html: Path to the HTML file to convert.
    :param output_pdf: Path where the PDF will be saved.
    :param wkhtmltopdf_path: Optional path to the wkhtmltopdf binary.
    :param options: Optional dict of wkhtmltopdf command-line options.
    """
    config = None
    if wkhtmltopdf_path:
        config = pdfkit.configuration(wkhtmltopdf=wkhtmltopdf_path)

    pdfkit.from_file(
        input_html,
        output_pdf,
        configuration=config,
        options=options or {
            'enable-local-file-access': None,
            'print-media-type': None,
            'margin-top': '15mm',
            'margin-bottom': '15mm',
        }
    )


if __name__ == '__main__':
    # Configuration
    DATA_JSON = f'{datetime.date.today()}.json'
    TEMPLATES_DIR = 'templates'
    TEMPLATE_NAME = 'newsletter_base.html'
    EDITION_DATE = datetime.date.today().strftime("%d %B %Y")
    EDITION_NUMBER = 1
    GET_PDF = "{{pdf_url}}"
    CSS_PATH = os.path.join(TEMPLATES_DIR, 'styles.css')
    OUTPUT_HTML = 'newsletter.html'
    OUTPUT_PDF = 'newsletter.pdf'
    # If wkhtmltopdf isn't on PATH, set this:
    WKHTMLTOPDF_PATH = "/wkhtmltopdf/bin/wkhtmltopdf.exe"  # e.g., '/usr/local/bin/wkhtmltopdf'

    # Render and convert
    render_newsletter_html(
        DATA_JSON,
        TEMPLATE_NAME,
        EDITION_DATE,
        EDITION_NUMBER,
        GET_PDF,
        CSS_PATH,
        OUTPUT_HTML
    )
    html_to_pdf_pdfkit(
        OUTPUT_HTML,
        OUTPUT_PDF,
        wkhtmltopdf_path=WKHTMLTOPDF_PATH
    )

    print(f"Generated '{OUTPUT_HTML}' and '{OUTPUT_PDF}' successfully.")
