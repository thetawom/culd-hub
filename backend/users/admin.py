from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _

from show_manager.admin import MemberInlineAdmin
from .models import User


class UserAdmin(BaseUserAdmin):
    model = User

    @admin.display(boolean=True)
    def board(self, user):
        return user.member.membership == "B"

    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (_("Personal info"), {"fields": ("first_name", "last_name", "phone")}),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                ),
            },
        ),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "first_name",
                    "last_name",
                    "phone",
                    "password1",
                    "password2",
                    "is_staff",
                    "is_active",
                ),
            },
        ),
    )
    list_display = (
        "email",
        "first_name",
        "last_name",
        "board",
        "is_staff",
    )
    search_fields = ("email", "first_name", "last_name")
    ordering = ("email",)

    inlines = [MemberInlineAdmin]


admin.site.register(User, UserAdmin)
