from typing import Union, List

from django.db import models
from django.utils.translation import gettext as _

from slack.managers import SlackUserManager, SlackChannelManager
from slack.service import slack_boss


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

    objects = SlackChannelManager()

    def __str__(self):
        return self.show.default_channel_name()

    def invite_users(self, users: Union[SlackUser, List[SlackUser]]):
        """Invites Slack user or users to the Slack channel.

        Args:
            users: The Slack user or users to invite.
        """
        slack_boss.invite_users_to_channel(channel=self, users=users)

    def remove_users(self, users: Union[SlackUser, List[SlackUser]]):
        """Removes Slack user or users from the Slack channel.

        Args:
            users: The Slack user or users to remove.
        """
        slack_boss.remove_users_from_channel(channel=self, users=users)
