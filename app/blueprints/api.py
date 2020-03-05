from flask import (
    g,
    Blueprint,
    jsonify,
    request
)

from app.db import query_db

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
    conditions = [""]

    service = params.get("service")
    if service:
        conditions.append(f"service='{service}'")

    from_date = params.get("from")
    if from_date:
        conditions.append(f"datetime>='{from_date}'")

    to_date = params.get("to")
    if to_date:
        conditions.append(f"datetime<='{to_date}'")

    limit = limit or params.get("limit")
    if limit:
        limit = int(limit)

    conditions = " AND ".join(conditions)

    query = """
    SELECT service, datetime, urgency, lat, lon
    FROM calls
    WHERE lat IS NOT NULL {}
    ORDER BY date(datetime) DESC
    {}

    """.format(
        conditions,
        f"LIMIT {limit}" if limit else ""
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
