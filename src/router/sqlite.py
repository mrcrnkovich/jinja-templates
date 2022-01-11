"""
Executes a SQL query against a sqlite3 database.
Returns a list of rows, represented as a dict
where key = column_name
"""

import sqlite3


def get_query(source, query):
    """
    Executes SQL query, returning a List of Dicts as the result.
    """

    conn = sqlite3.connect(source)
    conn.row_factory = sqlite3.Row
    result = conn.execute(query).fetchall()
    return [{k: row[k] for k in row.keys()} for row in result]
