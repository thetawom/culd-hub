from __future__ import annotations

from typing import TYPE_CHECKING, Optional

from django.contrib.auth.base_user import BaseUserManager
from django.core.validators import validate_email
from django.db.models import QuerySet
from django.utils.translation import gettext_lazy as _

if TYPE_CHECKING:
    from users.models import User


class UserManager(BaseUserManager):
    def create(
        self,
        email: str,
        password: str,
        activate: Optional[bool] = False,
        **extra_fields,
    ) -> User:
        if not email:
            raise ValueError(_("The email must be set"))
        validate_email(email)
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        if activate:
            user.activate()
        return user

    def create_superuser(self, email: str, password: str, **extra_fields) -> User:
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("Superuser must have is_staff=True."))
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("Superuser must have is_superuser=True."))
        return self.create(email, password, activate=True, **extra_fields)

    def activate(self) -> QuerySet:
        user_set = self.all()
        for user in user_set:
            user.activate()
        return user_set
