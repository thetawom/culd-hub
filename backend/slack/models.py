import re

from django.db import models
from django.utils.translation import gettext as _

from slack.managers import SlackUserManager


class SlackUser(models.Model):
    """Model for a user in the Slack workspace.

    Each Slack user has a one-to-one relationship with a Member. The user's
    Slack ID is used as the primary key.
    """

    id = models.CharField(primary_key=True, max_length=60, unique=True)
    member = models.OneToOneField(
        "shows.Member", related_name="slack_user", on_delete=models.CASCADE, unique=True
    )

    objects = SlackUserManager()

    def __str__(self):
        return str(self.id)


class SlackChannel(models.Model):
    """Model for a show channel in the Slack workspace.

    Each channel has a one-to-one relationship with the show it is a channel
    for. The channel's Slack workspace conversation ID is used as the primary
    key. It also stores the unique timestamp for the channel's briefing message.
    """

    id = models.CharField(primary_key=True, max_length=60, unique=True)
    show = models.OneToOneField(
        "shows.Show", on_delete=models.CASCADE, related_name="channel"
    )
    briefing_ts = models.CharField(
        max_length=24,
        default="",
        verbose_name="briefing timestamp",
        help_text=_("Slack ts for initial briefing message in the channel"),
    )

    def __str__(self):
        return self.default_channel_name()

    def default_channel_name(self):
        if self.show.name == "":
            raise ValueError(
                "Default channel name requires the name of the show to be set."
            )
        if self.show.date is None:
            raise ValueError(
                "Default channel name requires the date of the show to be set."
            )
        name = re.sub(r"[^\w\s]", "", self.show.name)
        date = self.show.date.strftime("%m-%d")
        return f"{date}-{name.replace(' ', '-').lower()}"
