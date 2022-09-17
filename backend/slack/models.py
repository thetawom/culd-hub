from datetime import datetime
from typing import Union, List, Optional

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

    def update_name(self, name: Optional[str] = None):
        """Renames the Slack channel.
        The default channel name format is used if name is not provided.

        Args:
            name: The name to use for the Slack channel.
        """
        slack_boss.rename_channel(channel_id=self.id, name=name, show=self.show)

    def archive(self, rename: bool = True):
        """Archives the Slack channel.

        Currently, a bug in the Slack API prevents Slack bots from un-archiving
        channels. So to avoid name_taken errors if a new channel is recreated
        for a show in the place of un-archiving, any archived channel will first
        be renamed with a unique name using the timestamp.

        Args:
            rename: Whether to rename the channel before archiving.
        """

        if rename:
            timestamp = str(datetime.now().timestamp()).replace(".", "-")
            self.update_name(
                name=f"arch-{self.show.default_channel_name()}-{timestamp}"
            )
        slack_boss.archive_channel(channel_id=self.id)

    def invite_users(self, users: Union[SlackUser, List[SlackUser]]):
        """Invites Slack user or users to the Slack channel.

        Args:
            users: The Slack user or users to invite.
        """
        slack_boss.invite_users_to_channel(channel_id=self.id, users=users)

    def remove_users(self, users: Union[SlackUser, List[SlackUser]]):
        """Removes Slack user or users from the Slack channel.

        Args:
            users: The Slack user or users to remove.
        """
        slack_boss.remove_users_from_channel(channel_id=self.id, users=users)
