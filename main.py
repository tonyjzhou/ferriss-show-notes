#!/usr/bin/env python
import re

import requests
from bs4 import BeautifulSoup
from jinja2 import Environment, PackageLoader, select_autoescape

from converter import convert_to_full_url
from model.note import Note, Notes


def _extract_title(soup):
    title_tag = soup.find('h1', {"class": "entry-title"})
    return title_tag.text


def _make_notes(blog_url: str, youtube_url: str) -> list:
    resp = requests.get(blog_url)

    if resp.status_code == 200:
        soup = BeautifulSoup(resp.text, 'html.parser')

        content = _make_content(soup, youtube_url)
        title = _extract_title(soup)

        return [Notes(title=title, content=content)]
    else:
        return None


def _make_content(soup, youtube_url):
    show_notes_tag = soup.find('h3', text=re.compile('SHOW NOTES'))
    notes_tag = show_notes_tag.fetchNextSiblings()[0]
    note_regexp = re.compile(r'(.+) \[(.+)\]')
    content = []
    for note_tag in notes_tag.findAll('li'):
        note_match = note_regexp.match(note_tag.text)

        description, time = note_match.group(1), note_match.group(2)
        full_url = convert_to_full_url(base_url=youtube_url, time=time)

        content.append(Note(description=description, time=time, url=full_url))
    return content


def main():
    all_notes = _make_notes(blog_url='https://tim.blog/2020/12/09/harley-finkelstein/',
                            youtube_url='https://www.youtube.com/watch?v=tcvzxXhSQ8o')
    _save_all_notes(all_notes)


def _save_all_notes(all_notes: list):
    for notes in all_notes:
        _save_notes(notes)

    html = _render_all_notes(all_notes)
    with open(f"public/index.html", "w") as writer:
        writer.writelines(html)


def _save_notes(notes: Notes):
    html = _render_notes(notes)
    with open(f"public/{notes.filename()}", "w") as writer:
        writer.writelines(html)


def _render_all_notes(all_notes: list) -> str:
    env = Environment(
        loader=PackageLoader(package_name="jinja"),
        autoescape=select_autoescape(["html", "xml"]),
    )

    template = env.get_template("all_notes.html")
    return template.render(all_notes=all_notes)


def _render_notes(notes: Notes) -> str:
    env = Environment(
        loader=PackageLoader(package_name="jinja"),
        autoescape=select_autoescape(["html", "xml"]),
    )

    template = env.get_template("notes.html")
    return template.render(notes=notes)


if __name__ == '__main__':
    main()
