

def api_data(path: str) -> dict:
    '''Takes https path and returns results in a dict'''
    from requests import get
    #log path
    result = get(path)

    if result.status_code == 200:
        return result.json()
    else:
        print('failed', result.status_code)
    return None
