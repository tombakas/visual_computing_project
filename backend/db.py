import sqlite3

from glob import glob
from datetime import datetime

from flask import g


DATABASE = glob('./db/*.db')[0]


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db


def extract_column_names(query):
    line = next(
        filter(
            lambda a: "SELECT" in a,
            query.split("\n")
        ))\
        .replace("SELECT", "")\
        .strip()
    column_name = [n.strip() for n in line.split(",")]
    return column_name


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


def query_db(query, args=()):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    keys = extract_column_names(query)
    return build_json_response(rv, keys)
