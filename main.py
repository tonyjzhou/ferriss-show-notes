#!/usr/bin/env python
import sys
import webbrowser


def main():
    if len(sys.argv) > 0:
        full_url = convert_to_full_url(base_url=sys.argv[1], time=sys.argv[2])

        print(full_url)
        webbrowser.open(full_url, new=2)


def convert_to_full_url(base_url: str, time: str):
    total_seconds = convert_time_to_seconds(time=time)
    full_url = f"{base_url}&t={total_seconds}s"
    return full_url


def convert_time_to_seconds(time: str):
    time_slice = [int(t) for t in time.split(':')]
    if len(time_slice) <= 0:
        hours, minutes, seconds = 0, 0, 0
    elif len(time_slice) == 1:
        hours, minutes, seconds = [0, 0] + time_slice
    elif len(time_slice) == 2:
        hours, minutes, seconds = [0] + time_slice
    elif len(time_slice) >= 3:
        hours, minutes, seconds = time_slice[:3]

    total_seconds = seconds + minutes * 60 + hours * 60 * 60
    return total_seconds


if __name__ == '__main__':
    main()
