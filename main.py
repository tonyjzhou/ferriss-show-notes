#!/usr/bin/env python
import re

import requests
from bs4 import BeautifulSoup
from jinja2 import Environment, PackageLoader, select_autoescape

from converter import convert_to_full_url
from model.note import Note, Notes, InputUrl


def _extract_title(soup):
    title_tag = soup.find('h1', {"class": "entry-title"})
    return title_tag.text


def _make_all_notes(urls: list) -> list:
    all_notes = []

    for u in urls:
        all_notes.extend(_make_notes(blog_url=u.blog, youtube_url=u.youtube, time_prefix=u.time_prefix))

    return all_notes


def _make_notes(blog_url: str, youtube_url: str, time_prefix) -> list:
    resp = requests.get(blog_url)

    if resp.status_code == 200:
        soup = BeautifulSoup(resp.text, 'html.parser')

        content = _make_content(soup, youtube_url, time_prefix=time_prefix)
        title = time_prefix + _extract_title(soup)

        return [Notes(title=title, content=content)]
    else:
        return None


def _make_content(soup, youtube_url, time_prefix):
    show_notes_tag = soup.find('h3', text=re.compile('SHOW NOTES', flags=re.IGNORECASE))
    notes_tag = next(nt for nt in (show_notes_tag.fetchNextSiblings()) if len(nt.findAll('li')) > 0)

    note_regexp = re.compile(rf'(.+) \[{time_prefix}(.+)\]')
    content = []
    for note_tag in notes_tag.findAll('li'):
        note_match = note_regexp.match(note_tag.text)
        if note_match is not None:
            description, time = note_match.group(1), note_match.group(2)
            full_url = convert_to_full_url(base_url=youtube_url, time=time)

            content.append(Note(description=description, time=time, url=full_url))
    return content


def main():
    all_notes = _make_all_notes([
        # Entrepreneurs

        InputUrl(blog='https://tim.blog/2017/01/18/arnold-schwarzenegger-part-2-bodybuilding-investing-and-online-battles/',
                 youtube='https://www.youtube.com/watch?v=zSggztqUYaY'),

        InputUrl(blog='https://tim.blog/2017/10/09/richard-branson/',
                 youtube='https://www.youtube.com/watch?v=KxL1B_3_KHk'),

        InputUrl(blog='https://tim.blog/2018/06/07/one-person-businesses-that-make-1m-per-year/',
                 youtube='https://www.youtube.com/watch?v=AhVEGIVAGco'),

        InputUrl(blog='https://tim.blog/2018/08/27/drew-houston/',
                 youtube='https://www.youtube.com/watch?v=A_E1t7FgAcU'),

        InputUrl(blog='https://tim.blog/2018/12/20/patrick-collison/',
                 youtube='https://www.youtube.com/watch?v=l73FKkh29yE'),

        InputUrl(blog='https://tim.blog/2019/02/07/tobi-lutke-shopify/',
                 youtube='https://www.youtube.com/watch?v=PQRXssjlk9U'),

        InputUrl(blog='https://tim.blog/2019/04/09/eric-schmidt/',
                 youtube='https://www.youtube.com/watch?v=O1IgduDUzIY'),

        InputUrl(blog='https://tim.blog/2020/12/03/daniel-ek/#more-53852',
                 youtube='https://www.youtube.com/watch?v=DICLqGAELMc'),

        InputUrl(blog='https://tim.blog/2020/12/09/harley-finkelstein/',
                 youtube='https://www.youtube.com/watch?v=tcvzxXhSQ8o'),

        # Investors

        InputUrl(blog='https://tim.blog/2015/08/18/the-evolutionary-angel-naval-ravikant/',
                 youtube='https://www.youtube.com/watch?v=-7J-Gwc9pVg'),

        InputUrl(blog='https://tim.blog/2016/01/30/naval-ravikant-on-happiness-hacks/',
                 youtube='https://www.youtube.com/watch?v=I53WciFh6ik'),

        InputUrl(blog='https://tim.blog/2017/02/13/mr-money-mustache/',
                 youtube='https://www.youtube.com/watch?v=-FlLj64dI1Q'),

        InputUrl(blog='https://tim.blog/2017/09/13/ray-dalio/',
                 youtube='https://www.youtube.com/watch?v=hRM7Gsyn4H4'),

        InputUrl(blog='https://tim.blog/2018/01/18/lessons-and-warnings-from-successful-risk-takers/',
                 youtube='https://www.youtube.com/watch?v=VebV1tctnEk'),

        InputUrl(
            blog='https://tim.blog/2018/02/28/how-to-secure-financial-freedom-maximize-productivity-and-protect-your-health/',
            youtube='https://www.youtube.com/watch?v=QBjM-G_d2RY'),

        InputUrl(blog='https://tim.blog/2018/09/25/howard-marks/',
                 youtube='https://www.youtube.com/watch?v=9qeWQz7qCW4'),

        InputUrl(blog='https://tim.blog/2020/05/11/howard-marks-2/',
                 youtube='https://www.youtube.com/watch?v=H0_ZscgTGXE'),

        InputUrl(blog='https://tim.blog/2020/09/22/richard-koch/',
                 youtube='https://www.youtube.com/watch?v=JznCRpl9wp4'),

        InputUrl(blog='https://tim.blog/2020/10/14/naval/',
                 youtube='https://www.youtube.com/watch?v=HiYo14wylQw'),

        # Ferris

        InputUrl(blog='https://tim.blog/2016/01/22/the-tao-of-seneca/',
                 youtube='https://www.youtube.com/watch?v=8DJJO-QoHs8'),

        InputUrl(blog='https://tim.blog/2016/03/04/how-to-10x-your-results/',
                 youtube='https://www.youtube.com/watch?v=-kD_NperbrE'),

        InputUrl(blog='https://tim.blog/2017/07/19/morning-routines-and-strategies/',
                 youtube='https://www.youtube.com/watch?v=-2PQ4eQ6EKc'),

        InputUrl(blog='https://tim.blog/2018/01/14/how-the-best-overcome-fear/',
                 youtube='https://www.youtube.com/watch?v=Fyow4sqGti0'),

        InputUrl(blog='https://tim.blog/2018/01/26/best-investments-bad-advice-to-avoid-and-other-life-lessons/',
                 youtube='https://www.youtube.com/watch?v=x3oxwAQDS7U'),

        InputUrl(blog='https://tim.blog/2018/02/02/the-4-hour-workweek-revisited/',
                 youtube='https://www.youtube.com/watch?v=4u3HZ9WduqE'),

        InputUrl(blog='https://tim.blog/2019/03/11/tea-time-with-tim/',
                 youtube='https://www.youtube.com/watch?v=LMSYbv1GBTw'),

        InputUrl(blog='https://tim.blog/2020/01/30/random-show-new-years-resolutions-2010-2019-lessons/',
                 youtube='https://www.youtube.com/watch?v=BC5lBL3PsKw'),

        InputUrl(blog='https://tim.blog/2020/02/13/ryan-holiday-interviews-tim-ferriss/',
                 youtube='https://www.youtube.com/watch?v=p3Yjx4PKIkk'),

        # MISC

        InputUrl(
            blog='https://tim.blog/2014/10/15/money-master-the-game/',
            youtube='https://www.youtube.com/watch?v=A7jOqYWJUKg',
            time_prefix='Ep1-'),

        InputUrl(
            blog='https://tim.blog/2014/10/15/money-master-the-game/',
            youtube='https://www.youtube.com/watch?v=-21OntkYTcM',
            time_prefix='Ep2-'),

        InputUrl(
            blog='https://tim.blog/2015/09/07/the-iceman-wim-hof/',
            youtube='https://www.youtube.com/watch?v=XiQ7ka11QnQ'),

        InputUrl(
            blog='https://tim.blog/2015/09/22/scott-adams-the-man-behind-dilbert/',
            youtube='https://www.youtube.com/watch?v=3KFgzvC-ao8'),

        InputUrl(
            blog='https://tim.blog/2018/06/10/how-to-succeed-in-high-stress-situations/',
            youtube='https://www.youtube.com/watch?v=jTbRx2B03WU'),

        InputUrl(blog='https://tim.blog/2019/12/05/adam-grant/',
                 youtube='https://www.youtube.com/watch?v=fbdfMn6phDw'),

        InputUrl(
            blog='https://tim.blog/2020/02/27/josh-waitzkin-beginners-mind-self-actualization-advice-from-your-future-self/',
            youtube='https://www.youtube.com/watch?v=ZXjKNFD9cvo'),

        InputUrl(blog='https://tim.blog/2020/12/08/jerry-seinfeld/',
                 youtube='https://www.youtube.com/watch?v=yNTmFORn3xQ'),

        InputUrl(
            blog='https://tim.blog/2020/12/16/martine-rothblatt/#more-54007',
            youtube='https://www.youtube.com/watch?v=S1rExMw-13A'),

        InputUrl(
            blog='https://tim.blog/2020/12/21/leo-babauta/#more-54052',
            youtube='https://www.youtube.com/watch?v=rjtg9KDpQD8'),

        InputUrl(
            blog='https://tim.blog/2021/01/06/stefi-cohen/#more-54185',
            youtube='https://www.youtube.com/watch?v=usIslVQ-Pd8'),

        InputUrl(
            blog='https://tim.blog/2021/01/21/michael-phelps-grant-hackett/#more-54432',
            youtube='https://www.youtube.com/watch?v=aG5pLBH4-9s'),

        InputUrl(
            blog='https://tim.blog/2021/03/08/vitalik-buterin-naval-ravikant/#more-55095',
            youtube='https://www.youtube.com/watch?v=42uhsP4vvCE'),

        InputUrl(
            blog='https://tim.blog/2017/06/04/nick-szabo/',
            youtube='https://www.youtube.com/watch?v=3FA3UjA0igY'),

    ])
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
