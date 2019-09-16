
#inspect the module temp 


import api


import inspect


for name, obj in inspect.getmembers(api):
    if inspect.isclass(obj):
        if issubclass(obj, api.A):
            print(obj)