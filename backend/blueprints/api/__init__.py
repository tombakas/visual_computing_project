import sqlite3

from flask import (
    g,
    Blueprint,
    jsonify,
    request
)

from backend.db import query_db

from .utils import build_conditions, get_cbs_columns

# A Blueprint is just a way to split a Flask app
# into separate components to make it more organised
# Reference: http://exploreflask.com/en/latest/blueprints.html
api = Blueprint('api', __name__, url_prefix="/api",
                   template_folder='templates')


@api.teardown_request
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


def calls_query_builder(params={}, limit=False, count=False):
    conditions = build_conditions(params, column_param="service")

    if not count:
        limit = limit or params.get("limit")
        if limit:
            limit = int(limit)

        query = """
        SELECT service, datetime, urgency, lat, lon
        FROM calls
        WHERE lat IS NOT NULL AND {}
        ORDER BY date(datetime) DESC
        {}

        """.format(
            conditions if conditions else "TRUE",
            "LIMIT {}".format(limit) if limit else ""
        )
    else:
        limit = None
        format_base = "strftime('{}',datetime)"
        count_interval = params["interval"]

        if count_interval == "year":
            date_format = format_base.format("%Y")

        if count_interval == "month":
            date_format = format_base.format("%Y %m")
            year = params.get("year")
            conditions = "strftime('%Y', datetime) = '{}'".format(year)

        if count_interval == "day":
            date_format = format_base.format("%Y %m %d")
            year = params.get("year")
            month = params.get("month")
            conditions = "strftime('%Y %m', datetime) = '{} {}'".format(year, month)

        if count_interval == "micro":
            date_format = format_base.format("%Y %m %d")
            year = params.get("year")
            month = params.get("month")
            day = params.get("day")
            conditions = "strftime('%Y %m %d', datetime) = '{} {} {}'".format(year, month, day)

        query = """
        SELECT {} service, count(service)
        FROM calls
        WHERE {}
        GROUP BY {} service

        """.format(
            "{} as date,".format(date_format) if date_format else "",
            conditions if conditions else "TRUE",
            "{},".format(date_format) or ""
        )

    r = query_db(query)
    print(query)
    return r


def events_query_builder(params={}, limit=False):
    conditions = build_conditions(params, "date", "service")

    city = params.get("city")
    city = "(" + " OR ".join(["city='{}'".format(c) for c in city.split(",")]) + ")"

    limit = limit or params.get("limit")
    if limit:
        limit = int(limit)

    query = """
    SELECT date, name, location, city
    FROM events
    WHERE {} AND {}
    GROUP BY name
    ORDER BY date(date) DESC
    {}

    """.format(
        city,
        conditions if conditions else "TRUE",
        "LIMIT {}".format(limit) if limit else ""
    )
    r = query_db(query)
    return r


def cbs_query_builder(params={}):

    region = params.get("region")
    columns = params.get("columns")

    region = "(" + " OR ".join(["region='{}'".format(r) for r in region.split(",")]) + ")"

    if columns:
        columns = columns.split(",")
    elif columns is None:
        columns = get_cbs_columns()

    quoted_columns = ",".join(
        "{}".format(c) for c in columns
    )

    query = """
    SELECT region,{}
    FROM cbs
    WHERE {}
    """.format(
        quoted_columns,
        region
    )

    try:
        return query_db(query)
    except sqlite3.OperationalError as e:
        return jsonify(
            {"Error": str(e)}
        )


@api.route("/calls/latest/")
def latest_calls():
    return jsonify(calls_query_builder(limit=100))


@api.route("/calls/")
def calls():
    params = request.args
    try:
        r = calls_query_builder(params)
    except sqlite3.OperationalError as e:
        return jsonify(
            {"Error": str(e)}
        )
    return jsonify(r)


@api.route("/calls/count")
def calls_count():
    params = request.args
    try:
        r = calls_query_builder(params, count=True)
    except sqlite3.OperationalError as e:
        return jsonify(
            {"Error": str(e)}
        )
    return jsonify(r)

@api.route("/cbs/")
def cbs():
    params = request.args
    if "region" not in params:
        return jsonify({"error": "no region supplied"})
    try:
        r = cbs_query_builder(params)
    except sqlite3.OperationalError as e:
        return jsonify(
            {"Error": str(e)}
        )

    return jsonify(r)

@api.route("/events/")
def events():
    params = request.args
    if "city" not in params:
        return jsonify({"error": "no city supplied"})
    try:
        r = events_query_builder(params)
    except sqlite3.OperationalError as e:
        return jsonify(
            {"Error": str(e)}
        )

    return jsonify(r)
