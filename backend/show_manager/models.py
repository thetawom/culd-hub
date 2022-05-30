from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

MEMBERSHIP_CHOICES = (
    ("G", "General Member"),
    ("B", "Executive Board Member"),
)


class Member(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, null=True, related_name="member"
    )
    membership = models.CharField(max_length=1, choices=MEMBERSHIP_CHOICES, default="G")

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"
