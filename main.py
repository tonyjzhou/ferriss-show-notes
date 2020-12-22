#!/usr/bin/env python
import sys
import webbrowser


def main():
    if len(sys.argv) > 0:
        total_seconds = convert_time_to_seconds(sys.argv[1])
        base_url = sys.argv[2]
        full_url = f"{base_url}&t={total_seconds}s"

        print(full_url)
        webbrowser.open(full_url, new=2)


def convert_time_to_seconds(time: str):
    hours, minutes, seconds = time.split(':')
    total_seconds = int(seconds) + int(minutes) * 60 + int(hours) * 60 * 60
    return total_seconds


if __name__ == '__main__':
    main()
