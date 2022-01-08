"""
Executes a SQL query against a sqlite3 database.
Returns a list of rows, represented as a dict
where key = column_name
"""

import sqlite3


def get_query(source, query):
    cx = sqlite3.connect(source)
    cx.row_factory = sqlite3.Row

    result = cx.execute(query).fetchall()

    results = [{k: row[k] for k in row.keys()} for row in result]
    return results
