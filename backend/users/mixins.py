from smtplib import SMTPException

from django.contrib.sessions.models import Session
from django.utils import timezone

from api.bases import Output
from .constants import Messages
from .models import User


class LogoutUserMixin(Output):
    def __new__(cls, *args, **kwargs):
        return super(LogoutUserMixin, cls).__new__(cls)

    @classmethod
    def mutate(cls, root, info, **kwargs):
        for session in Session.objects.filter(expire_date__gte=timezone.now()):
            if str(info.context.user.pk) == session.get_decoded().get("_auth_user_id"):
                session.delete()
        return cls(success=True)


class SendPasswordResetEmailMixin(Output):
    def __new__(cls, *args, **kwargs):
        return super(SendPasswordResetEmailMixin, cls).__new__(cls)

    @classmethod
    def mutate(cls, root, info, **kwargs):
        try:
            email = kwargs.get("email")
            user = User.objects.get(email=email)
            if user:
                user.send_password_reset_email(info, [email])
            return cls(success=True, errors=None)
        except SMTPException:
            return cls(success=False, errors=Messages.EMAIL_FAIL)
