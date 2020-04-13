#!/usr/bin/env python3
import os
import json
import sqlite3
import argparse

from glob import glob
from hashlib import md5


DB_NAME = "./calls.db"


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
        CREATE TABLE IF NOT EXISTS calls
            (id INTEGER PRIMARY KEY,
            datetime DATETIME,
            link VARCHAR(255),
            service VARCHAR(10),
            notification VARCHAR(255),
            urgency VARCHAR(1),
            region VARCHAR(100),
            hash VARCHAR(32) UNIQUE)
        """)

    c.execute(
        """
        CREATE TABLE IF NOT EXISTS units
            (id INTEGER UNIQUE,
            description VARCHAR(255))
        """)

    c.execute(
        """
        CREATE TABLE IF NOT EXISTS call_to_unit
            (
            call_id INTEGER,
            unit_id INTEGER
            )
        """)
    conn.commit()
    conn.close()


def create_unit(unit):
    conn = sqlite3.connect(DB_NAME)

    unit_id = int(unit.split()[0])
    unit_desc = " ".join(unit.split(" ")[1:]).strip()

    c = conn.cursor()
    try:
        c.execute(
            """
            INSERT INTO units values (?, ?)
            """, (unit_id, unit_desc,)
        )
        conn.commit()
    except sqlite3.IntegrityError:
        pass

    conn.close()


def make_date_time(call):
    d, m, y = call["date"].split("-")
    date = "-".join(("20" + y, m, d))
    return " ".join((date, call["time"]))


def make_call_hash(call):
    return md5(
        bytes(call["date"] + call["time"] + call["notification"], "utf-8")
    ).hexdigest()


def create_call(call):
    call_hash = make_call_hash(call)
    date_time = make_date_time(call)

    call_id = None

    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    try:
        c.execute(
            """
            INSERT INTO calls(datetime, link, service, notification, urgency, region, hash) values (?, ?, ?, ?, ?, ?, ?)
            """, (
                date_time,
                call.get("link"),
                call["service"],
                call["notification"],
                call.get("urgency", " ")[0],
                call["region"],
                call_hash
            )
        )
        conn.commit()
        call_id = c.lastrowid
    except sqlite3.IntegrityError:
        pass

    conn.close()
    return call_id


def link_call_unit(call_id, units):
    unit_ids = [int(u.split()[0]) for u in units]

    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    for unit_id in unit_ids:
        c.execute(
            """
            INSERT INTO call_to_unit values (?, ?)
            """, ((call_id, unit_id))
        )
        conn.commit()

    conn.close()


def process_entry(entry):
    units = entry.pop("units")

    for unit in units:
        create_unit(unit)

    call_id = create_call(entry)
    if call_id:
        link_call_unit(call_id, units)


def process_batch(batch):
    entries = json.loads(batch)
    for entry in entries:
        process_entry(entry)


def main():
    create_db()

    args = parse_args()
    batches = glob(os.path.join(args.path, "*json"))

    for i, batch in enumerate(batches):
        print("Processing batch {:>4} of {}".format(i, len(batches)))
        with open(batch, "r") as f:
            process_batch(f.read())


if __name__ == "__main__":
    main()
