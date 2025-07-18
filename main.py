#!/usr/bin/env python3
"""Command line interface for scraping and rendering the newsletter."""

import argparse
import datetime
import logging
import os
import subprocess
import sys

import extractData
import render


def list_bodies() -> list[str]:
    """Return available educational body module names."""
    edu_dir = 'EDU'
    bodies = []
    for fname in os.listdir(edu_dir):
        if fname.endswith('.py') and not fname.startswith('_'):
            bodies.append(os.path.splitext(fname)[0])
    return sorted(bodies)


def scrape_cmd(args: argparse.Namespace) -> None:
    bodies = args.bodies or list_bodies()
    logging.info("Scraping data for: %s", ", ".join(bodies))
    extractData.extractData(bodies)


def render_cmd(args: argparse.Namespace) -> None:
    logging.info("Rendering newsletter HTML from %s", args.data)
    html_path = render.render_newsletter_html(
        args.data,
        args.templates_dir,
        args.template,
        args.date,
        args.number,
        args.pdf,
        args.css,
        args.output,
    )
    logging.info("HTML written to %s", html_path)


def send_cmd(args: argparse.Namespace) -> None:
    logging.info("Running gen_news.py")
    subprocess.run([sys.executable, 'gen_news.py'])


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Newsletter utilities")
    sub = parser.add_subparsers(dest='command', required=True)

    p_scrape = sub.add_parser('scrape', help='Scrape regulatory websites')
    p_scrape.add_argument('bodies', nargs='*', help='Bodies to scrape (default: all)')
    p_scrape.set_defaults(func=scrape_cmd)

    p_render = sub.add_parser('render', help='Render newsletter HTML')
    today = datetime.date.today()
    p_render.add_argument('--data', default=f'data/{today.isoformat()}.json', help='JSON data file')
    p_render.add_argument('--templates-dir', default='templates', help='Templates directory')
    p_render.add_argument('--template', default='newsletter_base.html', help='Template file')
    p_render.add_argument('--date', default=today.strftime('%d %B %Y'), help='Edition date')
    p_render.add_argument('--number', type=int, default=1, help='Edition number')
    p_render.add_argument('--pdf', default='newsletter.pdf', help='PDF path placeholder')
    p_render.add_argument('--css', default=os.path.join('templates', 'styles.css'), help='CSS file to inline')
    p_render.add_argument('--output', default='newsletter.html', help='Output HTML file')
    p_render.set_defaults(func=render_cmd)

    p_send = sub.add_parser('send', help='Run gen_news.py to send the newsletter')
    p_send.set_defaults(func=send_cmd)

    return parser


def main(argv: list[str] | None = None) -> None:
    logging.basicConfig(level=logging.INFO, format='%(message)s')
    parser = build_parser()
    args = parser.parse_args(argv)
    args.func(args)


if __name__ == '__main__':
    main()

