from .api import api_data
from .sqlite import call_sqlite

def fn1(source_type, source, query=None, name=None):
    ''' Takes data_type, source, optional query
        returns Dict of the results
    '''

    if source_type == 'api':
        print('source_type is api')
        return api_data(source)
    elif source_type == 'sqlite':
        print('hanlder is sql')
        return call_sqlite
    else:
        return 'data type not currently supported'


def handler(data):
    ''' If passed a List of dicts, return a dict
            with key = item.name, apply fn1(item)
        If passed a single dict, apply fn1 return values
    '''
    print('entering handler')

    if type(data) == dict:
        print('data_type is dict')
        return fn1(**data)
    elif type(data) == list:
        return {i.name: fn1(*i) for i in data}
    else:
        return
