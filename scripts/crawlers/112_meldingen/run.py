#!/usr/bin/env python

import argparse

from crawler_112meldingen import run


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-v", "--verbose", default=False, action="store_true",
                        help="Print output to screen")
    parser.add_argument("-d", "--date",
                        help="Start date. Format: DD-MM-YYYY")

    args = parser.parse_args()
    return args


def format_date(date_arg):
    day, month, year = date_arg.split("-")
    return {
        "day": int(day),
        "month": int(month),
        "year": int(year),
        "submitSettingDate": "opslaan"
    }


if __name__ == "__main__":
    args = parse_args()

    date_settings = None
    if args.date:
        date_settings = format_date(args.date)

    run(args.verbose, date_settings)
