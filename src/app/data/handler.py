""" Takes a single dict or a list of dicts representing
    the data instructions from the [report].yml file
"""

import logging
from .api import api_data
from .sqlite import get_query


def fn1(source_type: str, source: str, query: str = None, **kwargs):
    """Takes data_type, source, optional query
    returns Dict of the results
    """
    match source_type:
        case "api":
            results = api_data(source)
        case "sqlite":
            results = get_query(source, query)
        case "text":
            results = source
        case _:
            logging.info("Source Type: %s not currrently supported", source_type)
            results = f"Source Type: {source_type} not currently supported"

    return results


def handler(data) -> dict:
    """If passed a List of dicts, return a dict
        with key = item.name, apply fn1(item)
    If passed a single dict, apply fn1 return values
    """

    if isinstance(data, dict):
        results = fn1(**data)
    elif isinstance(data, list):
        results = {i["id"]: fn1(**i) for i in data}
    else:
        results = {"result": "not-found"}

    return results
