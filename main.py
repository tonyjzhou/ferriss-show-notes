#!/usr/bin/env python
import sys


def main():
    if len(sys.argv) > 0:
        hours, minutes, seconds = sys.argv[1].split(':')

        total_seconds = int(seconds) + int(minutes) * 60 + int(hours) * 60 * 60

        print(total_seconds)


if __name__ == '__main__':
    main()
