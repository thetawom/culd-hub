from django.utils.translation import gettext as _

from common.exceptions import CustomException


class SlackBossException(CustomException):
    default_message = _("Problem with Slack!")
