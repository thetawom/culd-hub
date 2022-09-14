import re

from django.db import models
from django.utils.translation import gettext as _

from shows.models import Member, Show


# Create your models here.
class User(models.Model):
    id = models.CharField(primary_key=True, max_length=60, unique=True)
    member = models.OneToOneField(
        Member, related_name="slack_user", on_delete=models.CASCADE, unique=True
    )

    def __str__(self):
        return f"{self.id} ({self.member.user.get_full_name()})"


class Channel(models.Model):
    id = models.CharField(primary_key=True, max_length=60, unique=True)
    show = models.OneToOneField(Show, on_delete=models.CASCADE, related_name="channel")
    briefing_ts = models.CharField(
        max_length=24,
        default="",
        verbose_name="briefing timestamp",
        help_text=_("Slack ts for initial briefing message in the channel"),
    )

    def __str__(self):
        return self.default_channel_name(self.show)

    @staticmethod
    def default_channel_name(show):
        if show.name == "":
            raise ValueError(
                "Default channel name requires the name of the show to be set."
            )
        if show.date is None:
            raise ValueError(
                "Default channel name requires the date of the show to be set."
            )
        name = re.sub(r"[^\w\s]", "", show.name)
        date = show.date.strftime("%m-%d")
        return f"{date}-{name.replace(' ', '-').lower()}"
