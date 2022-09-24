from datetime import datetime
from typing import Union, List, Optional

from django.db import models
from django.utils.translation import gettext as _

from common.exceptions import WrongUsage
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

    def mention(self) -> str:
        return f"<@{self.id}>"


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

    def invite_performers(self):
        """Invites all registered performers to the Slack channel."""

        if self.show.performers.count() > 0:
            self.invite_users(
                [
                    performer.fetch_slack_user()
                    for performer in self.show.performers.all()
                ]
            )

    def remove_users(self, users: Union[SlackUser, List[SlackUser]]):
        """Removes Slack user or users from the Slack channel.

        Args:
            users: The Slack user or users to remove.
        """

        slack_boss.remove_users_from_channel(channel_id=self.id, users=users)

    def send_update_message(self, updated_fields):
        """Sends message to the Slack channel.

        Args:
            updated_fields: The fields of the show that have been updated.
        """

        if self.briefing_ts is None:
            raise WrongUsage(
                "Update message should not be sent if briefing does not exist."
            )

        delta_since_briefing = datetime.now() - datetime.fromtimestamp(
            int(self.briefing_ts.split(".")[0])
        )
        if delta_since_briefing.total_seconds() > 10:
            field_str = (
                f"{', '.join(updated_fields[: -1])} and {updated_fields[-1]}"
                if len(updated_fields) > 1
                else updated_fields[0]
            )
            message = f"<!channel> The {field_str} {'has' if len(updated_fields) == 1 else 'have'} been updated."
            slack_boss.send_message_in_channel(
                channel_id=self.id,
                blocks=[
                    {"type": "section", "text": {"type": "mrkdwn", "text": message}}
                ],
                text=message,
            )

    def send_or_update_briefing(self):
        """Sends show briefing to Slack channel, or updates existing briefing."""

        name, date, time, point, lions = (
            self.show.name,
            self.show.formatted_date(),
            self.show.formatted_time(),
            self.show.point,
            self.show.lions,
        )

        if point is not None:
            slack_user = point.fetch_slack_user()
            formatted_point = slack_user.mention() if slack_user else str(point)
        else:
            formatted_point = "TBD"

        briefing = [
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"Hi everyone! Thank you for signing up to perform at {name}. "
                    "Below is a quick rundown of important information about the show. Please read carefully.",
                },
            },
            {
                "type": "header",
                "text": {
                    "type": "plain_text",
                    "text": ":lion_face:  Show Info",
                },
            },
            {
                "type": "section",
                "fields": [
                    {"type": "mrkdwn", "text": f"*Date:* {date if date else 'TBD'}"},
                    {"type": "mrkdwn", "text": f"*Time:* {time if time else 'TBD'}"},
                    {
                        "type": "mrkdwn",
                        "text": f"*Point Person:* {formatted_point}",
                    },
                    {
                        "type": "mrkdwn",
                        "text": f"*Lions:* {lions if lions else 'TBD'}",
                    },
                ],
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "<!channel> Please react :thumbsup: to this message to confirm that you can make it.",
                },
            },
        ]
        ts, created = slack_boss.send_message_in_channel(
            channel_id=self.id,
            ts=self.briefing_ts,
            blocks=briefing,
            text=f"New show on {date}",
        )
        if created:
            slack_boss.pin_message_in_channel(channel_id=self.id, ts=ts)
            self.briefing_ts = ts
            self.save()
