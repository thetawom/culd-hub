from django.utils.translation import gettext as _

from common.exceptions import CustomException


class InvalidCredentials(CustomException):
    default_message = _("Invalid credentials.")


class TokenScopeError(CustomException):
    default_message = _("This token is for something else.")


class EmailAlreadyInUse(CustomException):
    default_message = _("This email is already in use.")
