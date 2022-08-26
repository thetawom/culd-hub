from django.utils.translation import gettext as _


class GraphQLAuthError(Exception):
    default_message = None

    def __init__(self, message=None):
        if message is None:
            message = self.default_message

        super().__init__(message)


class InvalidCredentials(GraphQLAuthError):
    default_message = _("Invalid credentials.")


class TokenScopeError(GraphQLAuthError):
    default_message = _("This token is for something else.")


class WrongUsage(GraphQLAuthError):
    default_message = _("Wrong usage, check your code!.")
