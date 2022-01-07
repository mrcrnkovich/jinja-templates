import logging


def api_data(path: str) -> dict:
    """Takes https path and returns results in a dict"""
    from requests import get

    logging.info(f"API PATH: {path}")
    result = get(path)

    if result.status_code == 200:
        return result.json()
    else:
        logging.ERROR(f"failed to get data at {path}. Returned: {result.status_code}")
