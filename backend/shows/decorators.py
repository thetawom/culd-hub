from functools import wraps

from django.utils.translation import gettext_lazy as _

from common.exceptions import WrongUsage
from shows.exceptions import SlackBossException


def requires_slack_channel(slack_function):
    @wraps(slack_function)
    def wrapper(**kwargs):
        show = kwargs.get("show", None)
        if not show:
            raise WrongUsage(
                "@requires_slack_channel must be applied to functions with parameter 'show'"
            )
        if not hasattr(show, "channel"):
            raise SlackBossException(_(f"{slack_function} requires channel to exist"))
        slack_function(**kwargs)

    return wrapper
