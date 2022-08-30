import inspect
from functools import wraps

from common.exceptions import WrongUsage


def disable_for_loaddata(signal_handler):
    @wraps(signal_handler)
    def wrapper(*args, **kwargs):
        for fr in inspect.stack():
            if inspect.getmodulename(fr[1]) == "loaddata":
                return
        signal_handler(*args, **kwargs)

    return wrapper


def requires_slack_channel(slack_function):
    @wraps(slack_function)
    def wrapper(*args, **kwargs):
        if len(args) < 2:
            raise WrongUsage(
                "@requires_slack_channel must be applied to functions with parameter 'show'"
            )
        show = args[1]
        if not hasattr(show, "channel"):
            raise Exception(f"{slack_function} requires channel to exist")
        slack_function(*args, **kwargs)

    return wrapper
