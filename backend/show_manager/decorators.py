from functools import wraps


def disable_for_loaddata(signal_handler):
    @wraps(signal_handler)
    def wrapper(*args, **kwargs):
        if kwargs.get("created", True) and not kwargs.get("raw", False):
            signal_handler(*args, **kwargs)

    return wrapper
