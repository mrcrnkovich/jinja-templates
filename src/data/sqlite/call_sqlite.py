import sqlite3
from dataclasses import dataclass


def get_query():
    _conn = "/home/mike/coding/jinja-templates/tmp/phl_crash_data.db"
    cx = sqlite3.connect(_conn)

    return cx.execute("select * from crash_by_year")
    
