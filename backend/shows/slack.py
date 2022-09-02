import logging
from datetime import datetime

from django.conf import settings
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

from common.decorators import requires_slack_channel
from shows.models import Channel, Show

logger = logging.getLogger(__name__)


class SlackBoss(object):
    def __init__(self):
        self.client = WebClient(token=settings.SLACK_TOKEN)

    def create_channel(self, show):
        logger.info(f"Creating channel for {show} ...")
        try:
            name = self._get_channel_name(show)
            response = self.client.conversations_create(name=name, is_private=False)
        except SlackApiError as error:
            logger.error(f"Failed to create channel: {error}")
        else:
            logger.info(response)
            if response.get("ok", False):
                Channel.objects.create(id=response["channel"]["id"], show=show)

    @requires_slack_channel
    def rename_channel(self, show, name=None):
        logger.info(f"Renaming channel for {show} ...")
        try:
            if not name:
                name = self._get_channel_name(show)
            response = self.client.conversations_rename(
                channel=show.channel.id, name=name
            )
        except SlackApiError as error:
            logger.error(f"Failed to rename channel: {error}")
        else:
            logger.info(response)

    @requires_slack_channel
    def archive_channel(self, show):
        logger.info(f"Archiving channel for {show} ...")
        archive_name = self._get_channel_name(show, archive=True)
        self.rename_channel(show, name=archive_name)
        try:
            response = self.client.conversations_archive(channel=show.channel.id)
        except SlackApiError as error:
            logger.error(f"Failed to archive channel: {error}")
        else:
            logger.info(response)
            if response.get("ok", False):
                show.channel.delete()

    @requires_slack_channel
    def send_or_update_briefing(self, show, update_fields=None):
        logger.info(f"Sending or updating briefing for {show} ...")
        briefing, text = self._build_briefing(show)
        is_update = show.channel.briefing_timestamp != ""
        try:
            if not is_update:
                logger.info("Creating new briefing ...")
                response = self.client.chat_postMessage(
                    channel=show.channel.id, blocks=briefing, text=text
                )
            else:
                logger.info(
                    f"Updating existing briefing ({show.channel.briefing_timestamp}) ..."
                )
                response = self.client.chat_update(
                    channel=show.channel.id,
                    ts=show.channel.briefing_timestamp,
                    blocks=briefing,
                    text=text,
                )
        except SlackApiError as error:
            logger.error(f"Failed to send briefing: {error}")
        else:
            logger.info(response)
            if response.get("ok", False):
                channel = Channel.objects.get(id=response["channel"])
                channel.briefing_timestamp = response["ts"]
                channel.save()
                if is_update and update_fields:
                    self.send_update_message(show, update_fields)

    @requires_slack_channel
    def send_update_message(self, show, update_fields):
        logger.info(f"Sending update message for {update_fields} for {show} ...")
        _, text = self._build_update_message(show, update_fields)
        try:
            response = self.client.chat_postMessage(channel=show.channel.id, text=text)
        except SlackApiError as error:
            logger.error(f"Failed to send update message: {error}")
        else:
            logger.info(response)

    @staticmethod
    def _get_channel_name(show, archive=False):
        channel_name = Channel.get_channel_name(show)
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
