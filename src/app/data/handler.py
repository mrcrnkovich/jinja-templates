from .api import api_data
from .sqlite import get_query


def fn1(source_type, source, query=None, id=None):
    """Takes data_type, source, optional query
    returns Dict of the results
    """
    if source_type == "api":
        return api_data(source)
    elif source_type == "sqlite":
        return get_query(source, query)
    elif source_type == "text":
        return source
    else:
        return "data type not currently supported"


def handler(data):
    """If passed a List of dicts, return a dict
        with key = item.name, apply fn1(item)
    If passed a single dict, apply fn1 return values
    """

    if type(data) == dict:
        return fn1(**data)
    elif type(data) == list:
        return {i["id"]: fn1(**i) for i in data}
    else:
        return
