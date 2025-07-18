from flask import Flask, render_template, redirect, url_for, request
import datetime
import extractData
import render as render_mod

app = Flask(__name__)

status = {
    'scrape': False,
    'render': False,
    'send': False
}

logs = {
    'scrape': '',
    'render': '',
    'send': ''
}

EDUCATIONAL_BODIES = ['AICTE', 'BCI', 'CBSE']

@app.route('/')
def index():
    return render_template('index.html', status=status, logs=logs)

@app.route('/scrape', methods=['POST'])
def scrape():
    try:
        extractData.extractData(EDUCATIONAL_BODIES)
        logs['scrape'] = 'Scraping completed successfully.'
        status['scrape'] = True
    except Exception as e:
        logs['scrape'] = f'Scraping failed: {e}'
    return redirect(url_for('index'))

@app.route('/render', methods=['POST'])
def render_newsletter():
    if not status['scrape']:
        logs['render'] = 'Please run scraping first.'
        return redirect(url_for('index'))
    try:
        today = datetime.date.today()
        render_mod.render_newsletter_html(
            data_json=f'data/{today}.json',
            templates_dir='templates',
            template_name='newsletter_base.html',
            edition_date=today.strftime('%d %B %Y'),
            edition_number=1,
            get_pdf='newsletter.pdf',
            css_path='templates/styles.css',
            output_html='newsletter.html'
        )
        logs['render'] = 'Rendering completed successfully.'
        status['render'] = True
    except Exception as e:
        logs['render'] = f'Rendering failed: {e}'
    return redirect(url_for('index'))

@app.route('/send', methods=['POST'])
def send_newsletter():
    if not status['render']:
        logs['send'] = 'Please render the newsletter first.'
        return redirect(url_for('index'))
    try:
        # Placeholder for actual send logic
        logs['send'] = 'Send step executed.'
        status['send'] = True
    except Exception as e:
        logs['send'] = f'Send failed: {e}'
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
