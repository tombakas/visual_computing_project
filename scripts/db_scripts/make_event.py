#!/usr/bin/env python3

import csv
import sqlite3
import argparse


DB_NAME = "./calls_20200328.db"


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-p", "--path", default=".", help="Path to directory with batches"
    )
    args = parser.parse_args()
    return args


def create_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute(
        """
        CREATE TABLE IF NOT EXISTS events
       (id INTEGER PRIMARY KEY,
        date TEXT,
        name TEXT,
        location TEXT,
        city TEXT)""")

    conn.commit()
    conn.close()


def process_entry(entry):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    command = """
       INSERT INTO events
       (date, name, location, city)
       VALUES(?, ?, ?, ?)
       """

    c.execute(command, entry)
    conn.commit()
    conn.close()


def main():
    create_db()

    with open("./event-data_2.csv") as csv_file:
        csv_file.readline() # Skip header
        csv_reader = csv.reader(csv_file, delimiter=",")
        for row in csv_reader:
            date_parts = row[0].split("/")
            row[0] = "-".join(reversed(date_parts))
            process_entry(row)

if __name__ == "__main__":
    main()
