import logging
from datetime import datetime

from django.conf import settings
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

from shows.decorators import requires_slack_channel
from shows.models import SlackChannel, Show, SlackUser

logging.basicConfig(level=logging.DEBUG)


class SlackBoss(object):
    def __init__(self):
        self.client = WebClient(token=settings.SLACK_TOKEN)

    def fetch_user(self, member=None):
        """
        Fetches Slack user for the specified member by email.

        Args:
            member (Member): the Member instance to fetch the Slack user for

        Returns:
            A string containing the fetched user's Slack ID. None if there was no match or the user was not fetched successfully.
        """
        logging.info(f"Fetching slack user for {member} ...")
        try:
            response = self.client.users_lookupByEmail(email=member.user.email)
        except SlackApiError as error:
            logging.error(f"Failed to fetch user: {error}")
        else:
            logging.debug(response)
            if response.get("ok", False):
                user_id = response["user"]["id"]
                if hasattr(member, "slack_user"):
                    member.slack_user.id = user_id
                    member.slack_user.save()
                else:
                    SlackUser.objects.create(id=user_id, member=member)
                return user_id

    def create_channel(self, show=None):
        """
        Creates a public Slack channel for the specified show using the channel name format `mm-dd-show-name`.

        Args:
            show (Show): the Show instance to create the Slack channel for

        Returns:
            A string containing the created channel's Slack ID. None if the channel was not created successfully.
        """
        logging.info(f"Creating channel for {show} ...")
        try:
            name = self._get_channel_name(show)
            response = self.client.conversations_create(name=name, is_private=False)
        except SlackApiError as error:
            logging.error(f"Failed to create channel: {error}")
        else:
            logging.debug(response)
            if response.get("ok", False):
                channel_id = response["channel"]["id"]
                SlackChannel.objects.create(id=channel_id, show=show)
                return channel_id

    @requires_slack_channel
    def rename_channel(self, show=None, name=None):
        """
        Renames the Slack channel for a show using the default channel name format `mm-dd-show-name`, or an override name if specified.

        Args:
            show (Show): the Show instance to rename the channel for
            name (str, optional): new channel name to use. If not specified, the default channel name format is used.

        Returns:
            A string containing the renamed channel's Slack ID. None if the channel was not renamed successfully.

        Raises:
            SlackBossException: If the show instance does not already have a Slack channel created
        """
        logging.info(f"Renaming channel for {show} ...")
        try:
            name = self._get_channel_name(show) if not name else name
            response = self.client.conversations_rename(
                channel=show.channel.id, name=name
            )
        except SlackApiError as error:
            logging.error(f"Failed to rename channel: {error}")
        else:
            logging.debug(response)
            if response.get("ok", False):
                return response["channel"]["id"]

    @requires_slack_channel
    def archive_channel(self, show=None):
        logging.info(f"Archiving channel for {show} ...")
        archive_name = self._get_channel_name(show, archive=True)
        self.rename_channel(show, name=archive_name)
        try:
            response = self.client.conversations_archive(channel=show.channel.id)
        except SlackApiError as error:
            logging.error(f"Failed to archive channel: {error}")
        else:
            logging.debug(response)
            if response.get("ok", False):
                show.channel.delete()

    @requires_slack_channel
    def send_or_update_briefing(self, show=None, update_fields=None):
        logging.info(f"Sending or updating briefing for {show} ...")
        briefing, text = self._build_briefing(show)
        is_update = show.channel.briefing_timestamp != ""
        try:
            if not is_update:
                logging.info("Creating new briefing ...")
                response = self.client.chat_postMessage(
                    channel=show.channel.id, blocks=briefing, text=text
                )
            else:
                logging.info(
                    f"Updating existing briefing ({show.channel.briefing_timestamp}) ..."
                )
                response = self.client.chat_update(
                    channel=show.channel.id,
                    ts=show.channel.briefing_timestamp,
                    blocks=briefing,
                    text=text,
                )
        except SlackApiError as error:
            logging.error(f"Failed to send briefing: {error}")
        else:
            logging.debug(response)
            if response.get("ok", False):
                channel = SlackChannel.objects.get(id=response["channel"])
                channel.briefing_timestamp = response["ts"]
                channel.save()
                if is_update and update_fields:
                    self.send_update_message(show, update_fields)

    @requires_slack_channel
    def send_update_message(self, show=None, update_fields=None):
        logging.info(f"Sending update message for {update_fields} for {show} ...")
        _, text = self._build_update_message(show, update_fields)
        try:
            response = self.client.chat_postMessage(channel=show.channel.id, text=text)
        except SlackApiError as error:
            logging.error(f"Failed to send update message: {error}")
        else:
            logging.debug(response)

    @staticmethod
    def _get_channel_name(show, archive=False):
        channel_name = SlackChannel.get_channel_name(show)
        if archive:
            channel_name = f"arch-{channel_name}-{str(datetime.now().timestamp()).replace('.', '-')}"
        return channel_name

    @staticmethod
    def _build_briefing(show):
        time = show.time.strftime("%I:%M %p") if show.time else "TBD"
        briefing = [
            {
                "type": "section",
                "text": {
                    "text": "*Show Information*",
                    "type": "mrkdwn",
                },
                "fields": [
                    {"type": "mrkdwn", "text": f"*Date:* {show.date}"},
                    {"type": "mrkdwn", "text": f"*Time:* {time}"},
                    {
                        "type": "mrkdwn",
                        "text": f"*Point Person:* {show.point}",
                    },
                    {
                        "type": "mrkdwn",
                        "text": f"*Lions:* {show.lions}",
                    },
                ],
            }
        ]
        text = f"New show on {show.date} at {time}!"
        return briefing, text

    @staticmethod
    def _build_update_message(show, update_fields):
        briefing = None
        updates = [
            f"{Show._meta.get_field(field).verbose_name.lower()} has been updated to {getattr(show, field)}"
            for field in update_fields
        ]
        text = (
            "The {} and the {}.".format(", the ".join(updates[:-1]), updates[-1])
            if len(updates) > 1
            else f"The {updates[0]}."
        )
        return briefing, text


slack_boss = SlackBoss()
