from django.utils.translation import gettext as _


class CustomException(Exception):
    default_message = "Custom exception thrown!"

    def __init__(self, message=None):
        if message is None:
            message = self.default_message

        super().__init__(message)


class WrongUsage(CustomException):
    """Internal exception for wrong usage"""

    default_message = _("Wrong usage, check your code!.")
