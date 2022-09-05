import inspect
from functools import wraps


def disable_for_loaddata(signal_handler):
    @wraps(signal_handler)
    def wrapper(*args, **kwargs):
        for fr in inspect.stack():
            if inspect.getmodulename(fr[1]) == "loaddata":
                return
        signal_handler(*args, **kwargs)

    return wrapper
