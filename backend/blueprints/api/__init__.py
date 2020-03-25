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


def calls_query_builder(params={}, limit=False):
    conditions = build_conditions(params, "service")

    limit = limit or params.get("limit")
    if limit:
        limit = int(limit)

    query = """
    SELECT service, datetime, urgency, lat, lon
    FROM calls
    WHERE lat IS NOT NULL {}
    ORDER BY date(datetime) DESC
    {}

    """.format(
        conditions,
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
    r = query_db(query)
    return r


@api.route("/calls/latest/")
def latest_calls():
    return jsonify(calls_query_builder(limit=100))


@api.route("/calls/")
def calls():
    params = request.args
    r = calls_query_builder(params)
    return jsonify(r)

@api.route("/cbs/")
def cbs():
    params = request.args
    if "region" not in params:
        return jsonify({"error": "no region supplied"})
    r = cbs_query_builder(params)
    return jsonify(r)
