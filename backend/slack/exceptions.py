from django.utils.translation import gettext as _

from common.exceptions import CustomException


class SlackBossException(CustomException):
    default_message = _("Problem with Slack!")


class SlackTokenException(SlackBossException):
    default_message = _("Slack token is not configured properly")
