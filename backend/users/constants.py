from django.utils.translation import gettext as _


class Messages:
    INVALID_PASSWORD = [{"message": _("Invalid password."), "code": "invalid_password"}]
    UNAUTHENTICATED = [{"message": _("Unauthenticated."), "code": "unauthenticated"}]
    INVALID_TOKEN = [{"message": _("Invalid token."), "code": "invalid_token"}]
    EXPIRED_TOKEN = [{"message": _("Expired token."), "code": "expired_token"}]
    EMAIL_FAIL = [{"message": _("Failed to send email."), "code": "email_fail"}]
    LOGOUT_FAIL = [{"message": _("Failed to log out user."), "code": "logout_fail"}]
    INVALID_CREDENTIALS = [
        {
            "message": _("Please enter valid credentials."),
            "code": "invalid_credentials",
        }
    ]
    EMAIL_IN_USE = [
        {"message": _("A user with that email already exists."), "code": "unique"}
    ]
