from flask import g

from backend.db import query_db

def build_conditions(params={}, column_param=None):
    conditions = [""]

    column = None
    if column_param is not None:
        column = params.get(column_param)
    if column:
        column_conditions = []
        for item in column.split(","):
            column_conditions.append("{}='{}'".format(column_param, item))

        conditions.append("(" + " OR ".join(column_conditions) + ")")

    from_date = params.get("from")
    if from_date:
        conditions.append("datetime>='{}'".format(from_date))

    to_date = params.get("to")
    if to_date:
        conditions.append("datetime<='{}'".format(to_date))

    conditions = " AND ".join(conditions)
    return conditions


def get_cbs_columns():
    columns = getattr(g, '_cbs_columns', None)
    if columns is None:
        db_response = query_db(
            """
            PRAGMA table_info(cbs)
            """,
            json_response=False
        )
        columns = [r[1] for r in db_response][1:]
        g._cbs_columns = columns

    return columns
