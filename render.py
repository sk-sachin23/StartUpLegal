import os
import json
from jinja2 import Environment, FileSystemLoader
import pdfkit
import datetime
import shutil

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
    :param template_name: Name of the newsletter template file.
    :param edition_date: Edition date string to render.
    :param edition_number: Edition number to render.
    :param get_pdf: URL or filename placeholder for the generated PDF.
    :param css_path: Path to the styles.css file to inline.
    :param output_html: Path where the rendered HTML will be saved.
    :return: The path to the saved HTML file.
    """
    # Read JSON data
    with open(data_json, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Render HTML via Jinja2
    env = Environment(loader=FileSystemLoader("templates"))
    template = env.get_template(template_name)
    html_content = template.render(
        data=data,
        edition_date=edition_date,
        edition_number=edition_number,
        pdf_url=get_pdf
    )

    # Inline CSS
    with open(css_path, 'r', encoding='utf-8') as css_file:
        css = css_file.read().replace('\n', ' ')
    html_content = html_content.replace(
        '</head>',
        f'<style type="text/css">{css}</style></head>'
    )

    # Save HTML
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
    Tries an explicit path, then searches system PATH.

    :param input_html: Path to the HTML file to convert.
    :param output_pdf: Path where the PDF will be saved.
    :param wkhtmltopdf_path: Optional explicit path to wkhtmltopdf.
    :param options: Optional dict of wkhtmltopdf command-line options.
    """
    # Determine executable path
    exe_path = None
    if wkhtmltopdf_path and wkhtmltopdf_path.strip():
        exe_path = wkhtmltopdf_path.strip()
    else:
        env_path = os.environ.get('WKHTMLTOPDF_PATH', '').strip()
        if env_path:
            exe_path = env_path

    if not exe_path:
        exe_path = shutil.which('wkhtmltopdf') or shutil.which('wkhtmltopdf.exe')

    # Validate executable
    if not exe_path or not os.path.isfile(exe_path) or not os.access(exe_path, os.X_OK):
        raise RuntimeError(
            f"wkhtmltopdf executable not found. "
            f"Tried: WKHTMLTOPDF_PATH='{os.environ.get('WKHTMLTOPDF_PATH')}', "
            f"PATH lookup gave '{exe_path}'."
        )

    # Configure pdfkit
    config = pdfkit.configuration(wkhtmltopdf=exe_path)
    print(f"[ℹ️] Using wkhtmltopdf executable: {exe_path}")

    # Convert HTML to PDF
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
    print(f"[✅] PDF generated at {output_pdf}")


if __name__ == '__main__':
    # Example standalone invocation
    DATA_JSON = f"{datetime.date.today().strftime('%Y-%m-%d')}.json"
    TEMPLATE_NAME = 'newsletter_base.html'
    EDITION_DATE = datetime.date.today().strftime("%d %B %Y")
    EDITION_NUMBER = 1
    GET_PDF = '{{pdf_url}}'
    CSS_PATH = os.path.join('templates', 'styles.css')
    OUTPUT_HTML = 'newsletter.html'
    OUTPUT_PDF = 'newsletter.pdf'

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
        OUTPUT_PDF
    )
    print(f"Generated '{OUTPUT_HTML}' and '{OUTPUT_PDF}' successfully.")
