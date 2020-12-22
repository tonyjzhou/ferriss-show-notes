#!/usr/bin/env python
import re

import requests
from bs4 import BeautifulSoup

from converter import convert_to_full_url


def main():
    url = 'https://tim.blog/2020/12/09/harley-finkelstein/'

    resp = requests.get(url)

    if resp.status_code == 200:
        soup = BeautifulSoup(resp.text, 'html.parser')

        notes_title = soup.find('h3', text=re.compile('SHOW NOTES'))
        # print(notes_title)

        notes = notes_title.fetchNextSiblings()[0]
        # print(notes)

        re.compile('(.+) \[(.+)\]')
        for note in notes.findAll('li'):
            regexp_1 = re.compile(r'(.+) \[(.+)\]')
            re_match = regexp_1.match(note.text)
            description, time = re_match.group(1), re_match.group(2)
            full_url = convert_to_full_url(base_url='https://www.youtube.com/watch?v=tcvzxXhSQ8o', time=time)
            print(f"<a href={full_url}>{note.text}</a>")
    else:
        print("Error")


if __name__ == '__main__':
    main()
