from flask import Flask, render_template, redirect, url_for, request
import datetime
import os
import extractData
import render as render_mod
import gen_news

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

EDUCATIONAL_BODIES = sorted([
    f.split('.')[0]
    for f in os.listdir('EDU')
    if f.endswith('.py') and f != '__init__.py'
])

last_data_file = None

@app.route('/')
def index():
    return render_template('index.html', status=status, logs=logs, bodies=EDUCATIONAL_BODIES)

@app.route('/scrape', methods=['POST'])
def scrape():
    global last_data_file
    try:
        selected = request.form.getlist('bodies')
        if not selected or 'all' in selected:
            selected = EDUCATIONAL_BODIES

        exec_time, data_file = extractData.extractData(selected)
        status['scrape'] = True
        if data_file:
            last_data_file = data_file
        logs['scrape'] = f'Scraping finished in {exec_time:.1f}s.'
        if data_file:
            logs['scrape'] += f' Saved to {data_file}.'
        else:
            logs['scrape'] += ' No new data file.'
    except Exception as e:
        logs['scrape'] = f'Scraping failed: {e}'
    return redirect(url_for('index'))

@app.route('/render', methods=['POST'])
def render_newsletter():
    global last_data_file
    if not status['scrape'] or not last_data_file:
        logs['render'] = 'Please run scraping first.'
        return redirect(url_for('index'))
    try:
        edition_number = int(request.form.get('edition_number', 1))
        output_pdf = request.form.get('output_pdf', 'newsletter.pdf')
        today = datetime.date.today()
        render_mod.render_newsletter_html(
            data_json=last_data_file,
            template_name='newsletter_base.html',
            edition_date=today.strftime('%d %B %Y'),
            edition_number=edition_number,
            get_pdf=output_pdf,
            css_path='templates/styles.css',
            output_html='newsletter.html'
        )
        render_mod.html_to_pdf_pdfkit('newsletter.html', output_pdf)
        logs['render'] = f'Rendered newsletter and {output_pdf}.'
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
        audience_id = request.form.get('audience_id')
        if not audience_id:
            logs['send'] = 'Audience ID required.'
            return redirect(url_for('index'))

        campaign_id = gen_news.send_newsletter('newsletter.html', audience_id)
        logs['send'] = f'Sent campaign {campaign_id}.'
        status['send'] = True
    except Exception as e:
        logs['send'] = f'Send failed: {e}'
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
