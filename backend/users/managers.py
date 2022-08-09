from django.contrib.auth.base_user import BaseUserManager
from django.core.validators import validate_email
from django.utils.translation import gettext_lazy as _


class UserManager(BaseUserManager):
    def create(self, email, password, **extra_fields):
        if not email:
            raise ValueError(_("The email must be set"))
        validate_email(email)
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        # if extra_fields.get("is_staff") is not True:
        #     raise ValueError(_("Superuser must have is_staff=True."))
        # if extra_fields.get("is_superuser") is not True:
        #     raise ValueError(_("Superuser must have is_superuser=True."))
        return self.create(email, password, **extra_fields)
