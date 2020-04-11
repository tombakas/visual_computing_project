import sqlite3

from glob import glob
from datetime import datetime

from flask import g


DATABASE = glob("./db/*.db")[0]


def get_db():
    db = getattr(g, "_database", None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db


def extract_column_names(query):
    line = (
        next(filter(lambda a: "SELECT" in a, query.split("\n")))
        .replace("SELECT", "")
        .strip()
    )
    column_names = [
        n.strip() if "as" not in n else n.split("as")[-1].strip()
        for n in line.split(", ")
    ]

    column_names = [column_name if "count" not in column_name else "count"
                    for column_name in column_names]
    return column_names


def build_json_response(db_response, keys):
    json_response = []
    for row in db_response:
        d = {}

        for i, key in enumerate(keys):
            if key in ["lat", "lon"]:
                d[key] = float(row[i])
            elif key == "datetime":
                d[key] = datetime.strptime(row[i], "%Y-%m-%d %H:%M:%S")
            else:
                d[key] = row[i]

        json_response.append(d)
    return json_response


def query_db(query, args=(), json_response=True):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    if not json_response:
        return rv
    cur.close()
    keys = extract_column_names(query)
    return build_json_response(rv, keys)
