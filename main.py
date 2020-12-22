#!/usr/bin/env python
import sys
import webbrowser

from converter import convert_to_full_url


def main():
    if len(sys.argv) > 0:
        full_url = convert_to_full_url(base_url=sys.argv[1], time=sys.argv[2])

        print(full_url)
        webbrowser.open(full_url, new=2)


if __name__ == '__main__':
    main()
