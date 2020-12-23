#!/usr/bin/env python
import re

import requests
from bs4 import BeautifulSoup
from jinja2 import Environment, PackageLoader, select_autoescape

from converter import convert_to_full_url
from model.note import Note, Notes


def url_to_notes(blog_url: str, youtube_url: str):
    resp = requests.get(blog_url)

    if resp.status_code == 200:
        soup = BeautifulSoup(resp.text, 'html.parser')

        show_notes_tag = soup.find('h3', text=re.compile('SHOW NOTES'))

        notes_tag = show_notes_tag.fetchNextSiblings()[0]

        note_regexp = re.compile(r'(.+) \[(.+)\]')

        content = []
        for note_tag in notes_tag.findAll('li'):
            note_match = note_regexp.match(note_tag.text)

            description, time = note_match.group(1), note_match.group(2)
            full_url = convert_to_full_url(base_url=youtube_url, time=time)

            content.append(Note(description=description, time=time, url=full_url))

        return Notes(title="blah", content=content)
    else:
        return None


def main():
    notes = url_to_notes(blog_url='https://tim.blog/2020/12/09/harley-finkelstein/',
                         youtube_url='https://www.youtube.com/watch?v=tcvzxXhSQ8o')
    make_notes(notes)


def make_notes(notes: list):
    html = render_notes(notes)
    with open(f"public/{notes.title}", "w") as writer:
        writer.writelines(html)


def render_notes(notes: list) -> str:
    env = Environment(
        loader=PackageLoader(package_name="jinja"),
        autoescape=select_autoescape(["html", "xml"]),
    )

    template = env.get_template("note.html")
    return template.render(notes=notes)


if __name__ == '__main__':
    main()
