import logging
from datetime import datetime

from django.conf import settings
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

from shows.decorators import requires_slack_channel
from shows.models import Show, Member
from slack.exceptions import SlackBossException
from slack.models import SlackChannel, SlackUser


class SlackBoss(object):
    """
    Wrapper around Slack API WebClient with functions for show channel and member management.

    Note that SlackBoss functions are as close to atomic as possible to enhance re-usability,
    i.e., higher-level logic should be written where SlackBoss functions are invoked.

    Attributes:
        client (WebClient): the Slack web client configured with the workspace Slack token
    """

    def __init__(self, slack_token=None):
        """
        Initializes SlackBoss by creating a Slack API WebClient.

        If no `slack_token` is provided, SlackBoss will attempt to fetch the one configured in project settings.

        Args:
            slack_token (str or None): workspace Slack token to configure the WebClient
        """
        if not slack_token:
            if hasattr(settings, "SLACK_TOKEN"):
                slack_token = settings.SLACK_TOKEN
            else:
                raise SlackBossException(
                    "If slack_token is None, then SLACK_TOKEN must be configured in default settings."
                )
        self.client = WebClient(token=slack_token)

    def fetch_user(self, member=None):
        """
        Fetches Slack user for the specified member by email.

        Args:
            member (Member): the Member instance to fetch the Slack user for

        Returns:
            A string containing the fetched user's Slack ID.
            None if there was no match or the user was not fetched successfully.
        """
        logging.info(f"Fetching slack user for {member} ...")
        try:
            response = self.client.users_lookupByEmail(email=member.user.email)
        except SlackApiError as error:
            if error.response.get("error") == "users_not_found":
                logging.warning(f"{member} is not in the Slack workspace")
            else:
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

    def create_channel(self, show=None, name=None):
        """
        Creates a public Slack channel for the specified show.

        Unless `name` is specified, the channel name will use the default format `mm-dd-show-name`.

        Args:
            show (Show): the show to create the Slack channel for
            name (str or None): the Slack channel name to use

        Returns:
            A string containing the created channel's Slack ID.
            None if the channel was not created successfully.
        """
        logging.info(f"Creating channel for {show} ...")
        try:
            if not name:
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
    def invite_member_to_channel(self, show=None, member=None):
        """
        Invites a member's Slack user to the channel for a show.

        Args:
            show (Show): the show of the channel to invite the performer to
            member (Member): the member to invite to a Slack channel

        Raises:
            SlackBossException: If the show instance does not already have a Slack channel created
        """
        logging.info(f"Inviting member {member} to channel for {show} ...")
        try:
            if not hasattr(member, "slack_user"):
                self.fetch_user(member)
            response = None
            if hasattr(member, "slack_user"):
                response = self.client.conversations_invite(
                    channel=show.channel.id, users=member.slack_user.id
                )
        except SlackApiError as error:
            if error.response.get("error") == "already_in_channel":
                logging.info(f"{member} is already in the Slack channel")
            else:
                logging.error(f"Failed to invite to channel: {error}")
        else:
            if response:
                logging.debug(response)

    @requires_slack_channel
    def remove_member_from_channel(self, show=None, member=None):
        """
        Removes a member's Slack user from the channel for a show.

        Args:
            show (Show): the show of the channel to remove the performer from
            member (Member): the member to remove from the Slack channel

        Raises:
            SlackBossException: If the show instance does not already have a Slack channel created
        """
        logging.info(f"Removing member {member} from channel for {show} ...")
        try:
            if not hasattr(member, "slack_user"):
                self.fetch_user(member)
            response = None
            if hasattr(member, "slack_user"):
                response = self.client.conversations_kick(
                    channel=show.channel.id, user=member.slack_user.id
                )
        except SlackApiError as error:
            logging.error(f"Failed to remove from channel: {error}")
        else:
            if response:
                logging.debug(response)

    @requires_slack_channel
    def rename_channel(self, show=None, name=None):
        """
        Renames the Slack channel for a show.
        If name parameter is not specified, default format `mm-dd-show-name` is used.

        Args:
            show (Show): the show to rename the channel for
            name (str or None): new channel name to use

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
        self.rename_channel(show=show, name=archive_name)
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
                if is_update and update_fields:
                    delta_since_briefing = datetime.now() - datetime.fromtimestamp(
                        int(show.channel.briefing_timestamp.split(".")[0])
                    )
                    if delta_since_briefing.total_seconds() > 10:
                        self.send_update_message(show=show, update_fields=update_fields)
                show.channel.briefing_timestamp = response["ts"]
                show.channel.save()

    @requires_slack_channel
    def send_update_message(self, show=None, update_fields=None):
        logging.info(f"Sending update message for {update_fields} for {show} ...")
        update_fields = [
            field
            for field in update_fields
            if getattr(show, field) and getattr(show, field) != ""
        ]
        if update_fields:
            _, text = self._build_update_message(show, update_fields)
            try:
                response = self.client.chat_postMessage(
                    channel=show.channel.id, text=text
                )
            except SlackApiError as error:
                logging.error(f"Failed to send update message: {error}")
            else:
                logging.debug(response)
        else:
            logging.info(f"No non-null fields for update message")

    @staticmethod
    def _get_channel_name(show, archive=False):
        channel_name = SlackChannel.default_channel_name(show)
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
        text = f"New show on {show.date}!"
        return briefing, text

    @staticmethod
    def _build_update_message(show, update_fields):
        briefing = None
        updates = []
        for field in update_fields:
            update_value = getattr(show, field)
            if field == "time":
                update_value = update_value.strftime("%I:%M %p")
            updates.append(
                f"{Show._meta.get_field(field).verbose_name.lower()} is now {update_value}"
            )
        text = (
            "Quick update! The {} and the {}.".format(
                ", the ".join(updates[:-1]), updates[-1]
            )
            if len(updates) > 1
            else f"Quick update! The {updates[0]}."
        )
        return briefing, text


slack_boss = SlackBoss()
