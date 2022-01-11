"""
Module makes a request to an API and returns a Dict with the results
"""

import logging
from typing import Dict
from requests import get


def api_data(path: str) -> Dict:
    """Takes https path and returns results in a dict"""

    logging.info("API PATH: %s", path)
    result = get(path)

    if result.status_code == 200:
        results = result.json()
    else:
        logging.error(
            "failed to get data at %s. Returned: %s", path, result.status_code
        )
        results = {"result": None}
    return results
