import time

from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.db import models
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField

from .managers import UserManager
from .tokens import action_token, TokenAction


class User(AbstractUser):
    username = None
    email = models.EmailField(_("email address"), unique=True)
    first_name = models.CharField(_("first name"), max_length=150)
    last_name = models.CharField(_("last name"), max_length=150)
    phone = PhoneNumberField(_("phone number"), null=True, blank=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]

    objects = UserManager()

    def __str__(self):
        return self.get_full_name()

    @classmethod
    def email_is_free(cls, email):
        return not User.objects.filter(email=email).exists()

    def send(self, subject, template, context, recipient_list=None):
        _subject = render_to_string(subject, context).replace("\n", " ").strip()
        html_message = render_to_string(template, context)
        message = strip_tags(html_message)
        return send_mail(
            subject=_subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            html_message=html_message,
            recipient_list=(recipient_list or [self.email]),
            fail_silently=False,
        )

    def get_email_context(self, info, path, action, **kwargs):
        # token = get_token(self, action, **kwargs)
        token = action_token.make_token(self, action)
        site = get_current_site(info.context)
        return {
            "user": self,
            "request": info.context,
            "token": token,
            "port": info.context.get_port(),
            "site_name": "CU Lion Dance Hub",
            "domain": site.domain,
            "protocol": "https" if info.context.is_secure() else "http",
            "path": path,
            "timestamp": time.time(),
        }

    def send_password_reset_email(self, info, *args, **kwargs):
        email_context = self.get_email_context(
            info, "password_reset", TokenAction.PASSWORD_RESET
        )
        template = "email/password_reset_email.html"
        subject = "email/password_reset_subject.txt"
        return self.send(subject, template, email_context, *args, **kwargs)
