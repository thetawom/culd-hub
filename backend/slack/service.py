from __future__ import annotations

import logging
from typing import Optional, TYPE_CHECKING, Union, List, Tuple

from django.conf import settings
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

from common.exceptions import WrongUsage
from slack.exceptions import SlackBossException

if TYPE_CHECKING:
    from users.models import User
    from shows.models import Member, Show
    from slack.models import SlackUser, SlackChannel


class SlackBoss:
    """Custom Slack API WebClient wrapper.

    SlackBoss provides custom convenience functions, utilities, and
    error-handling around the Slack SDK WebClient class.

    Attributes:
        token: The Slack access token to use, typically a bot token
        client: The Slack web client configured with the Slackbot token
    """

    token: str
    client: WebClient

    def __init__(self, token: Optional[str] = None):
        """Initializes SlackBoss by creating a Slack API WebClient.

        If no `slack_token` is provided, SlackBoss will attempt to fetch the
        Slack access token configured with the `SLACK_TOKEN` project setting.

        Args:
            token: Slack access token to configure the WebClient
        """

        if not token:
            if hasattr(settings, "SLACK_TOKEN"):
                token = settings.SLACK_TOKEN
            else:
                raise SlackBossException(
                    "SLACK_TOKEN must be configured in default settings if slack_token is None"
                )

        self.token = token
        self.client = WebClient(token=self.token)

    def fetch_user(
        self,
        email: Optional[str] = None,
        user: Optional[User] = None,
        member: Optional[Member] = None,
    ) -> Optional[str]:
        """Fetches Slack user ID for the specified member by email.

        One of email, user, or member should be provided.

        Args:
            email: The email address associated with the Slack user.
            user: The user to fetch the Slack user ID for.
            member: The member to fetch the Slack user ID for.

        Returns:
            The fetched user's Slack ID. None if there was no match.

        Raises:
            SlackBossException: If there was an error fetching the user ID.
        """

        email, member_label = self._get_email_arg(email=email, user=user, member=member)

        logging.info(f"Fetching Slack user for {member_label} ...")
        try:
            response = self.client.users_lookupByEmail(email=email)
        except SlackApiError as api_error:
            error = api_error.response.get("error")
            if error == "users_not_found":
                logging.warning(f"{email} is not in the Slack workspace")
            else:
                raise SlackBossException(error)
        else:
            logging.debug(response)
            if not response.get("ok", False):
                raise SlackBossException("Error fetching Slack user ID")
            return response["user"]["id"]

    def create_channel(self, name: Optional[str] = None, show: Optional[Show] = None):
        """Creates Slack channel for the specified show.

        One of name or show should be provided.

        Args:
            name: The email address associated with the Slack user.
            show: The show to fetch the Slack user ID for.

        Returns:
            The created channel's Slack ID. None if there was no match.

        Raises:
            SlackBossException: If there was an error creating the channel.
        """

        name, show_label = self._get_channel_name_arg(name=name, show=show)

        logging.info(f"Creating Slack channel for {show_label} ...")
        try:
            response = self.client.conversations_create(name=name, is_private=False)
        except SlackApiError as api_error:
            error = api_error.response.get("error")
            raise SlackBossException(error)
        else:
            logging.debug(response)
            if not response.get("ok", False):
                raise SlackBossException("Error creating Slack channel")
            return response["channel"]["id"]

    def archive_channel(
        self,
        channel_id: Optional[str] = None,
        channel: Optional[SlackChannel] = None,
        show: Optional[Show] = None,
    ):
        """Archives the specified Slack channel.

        One of channel_id, channel, or show should be provided.

        Args:
            channel_id: The Slack ID for the channel to archive.
            channel: The Slack channel to archive.
            show: The show to archive the Slack channel for.

        Raises:
            SlackBossException: If there was an error archiving the channel.
        """

        channel_id, channel_label = self._get_slack_channel_id_arg(
            channel_id=channel_id, channel=channel, show=show
        )

        logging.info(f"Archiving channel {channel_label} ...")
        try:
            response = self.client.conversations_archive(channel=channel_id)
        except SlackApiError as api_error:
            error = api_error.response.get("error")
            raise SlackBossException(error)
        else:
            logging.debug(response)
            if not response.get("ok", False):
                raise SlackBossException("Error renaming Slack channel")
        return True

    def rename_channel(
        self,
        channel_id: Optional[str] = None,
        channel: Optional[SlackChannel] = None,
        show: Optional[Show] = None,
        name: Optional[str] = None,
    ):
        """Renames the specified Slack channel.

        One of channel_id, channel, or show should be provided.
        One of name or show should be provided.

        Args:
            channel_id: The Slack ID for the channel to rename.
            channel: The Slack channel to rename.
            show: The show to rename the Slack channel for.
            name: The name to use for the Slack channel.

        Raises:
            SlackBossException: If there was an error inviting the users.
        """

        name, _ = self._get_channel_name_arg(name=name, show=show)
        channel_id, channel_label = self._get_slack_channel_id_arg(
            channel_id=channel_id, channel=channel, show=show
        )

        logging.info(f"Renaming channel {channel_label} ...")
        try:
            response = self.client.conversations_rename(
                channel=show.channel.id, name=name
            )
        except SlackApiError as api_error:
            error = api_error.response.get("error")
            raise SlackBossException(error)
        else:
            logging.debug(response)
            if not response.get("ok", False):
                raise SlackBossException("Error renaming Slack channel")
            return response["channel"]["id"]

    def invite_users_to_channel(
        self,
        channel_id: Optional[str] = None,
        channel: Optional[SlackChannel] = None,
        show: Optional[Show] = None,
        user_ids: Union[str, List[str]] = None,
        users: Union[SlackUser, List[SlackUser]] = None,
    ):
        """Invites specified Slack users to the specified channel.

        One of channel_id, channel, or show should be provided.
        One of user_ids or users should be provided.

        Args:
            channel_id: The Slack ID for the channel to invite users to.
            channel: The Slack channel to invite users to.
            show: The show to invite users to the Slack channel for.
            user_ids: The Slack IDs of the user or users to invite.
            users: The Slack user or users to invite.

        Raises:
            SlackBossException: If there was an error inviting the users.
        """

        channel_id, channel_label = self._get_slack_channel_id_arg(
            channel_id=channel_id, channel=channel, show=show
        )
        user_ids, members_label = self._get_slack_user_ids_arg(
            user_ids=user_ids, users=users
        )

        logging.info(f"Inviting {members_label} to channel {channel_label} ...")
        try:
            response = self.client.conversations_invite(
                channel=channel_id, users=user_ids
            )
        except SlackApiError as api_error:
            error = api_error.response.get("error")
            if error == "already_in_channel":
                logging.info(f"{user_ids} is already in the Slack channel")
            else:
                raise SlackBossException(error)
        else:
            logging.debug(response)
            if not response.get("ok", False):
                raise SlackBossException("Error inviting users to channel")
        return True

    def remove_users_from_channel(
        self,
        channel_id: Optional[str] = None,
        channel: Optional[SlackChannel] = None,
        show: Optional[Show] = None,
        user_ids: Union[str, List[str]] = None,
        users: Union[SlackUser, List[SlackUser]] = None,
    ):
        """Removes specified Slack users from the specified channel.

        One of channel_id, channel, or show should be provided.
        One of user_ids or users should be provided.

        Args:
            channel_id: The Slack ID for the channel to remove users from.
            channel: The Slack channel to remove users from.
            show: The show to removes users from the Slack channel for.
            user_ids: The Slack IDs of the user or users to remove.
            users: The Slack user or users to remove.

        Raises:
            SlackBossException: If there was an error removing the users.
        """

        channel_id, channel_label = self._get_slack_channel_id_arg(
            channel_id=channel_id, channel=channel, show=show
        )
        user_ids, members_label = self._get_slack_user_ids_arg(
            user_ids=user_ids, users=users
        )

        logging.info(f"Removing {members_label} from channel {channel_label} ...")
        if not isinstance(user_ids, list):
            user_ids = [user_ids]
        for user_id in user_ids:
            try:
                response = self.client.conversations_kick(
                    channel=channel_id, user=user_id
                )
            except SlackApiError as api_error:
                error = api_error.response.get("error")
                if error == "not_in_channel":
                    logging.info(f"{user_id} is not in the Slack channel")
                else:
                    raise SlackBossException(error)
            else:
                logging.debug(response)
                if not response.get("ok", False):
                    raise SlackBossException("Error removing users from channel")
        return True

    @staticmethod
    def _get_email_arg(
        email: Optional[str] = None,
        user: Optional[User] = None,
        member: Optional[Member] = None,
    ) -> Tuple[str, str]:
        """Processes email argument from various types.

        Args:
            email: The email address.
            user: The user to get the email address for.
            member: The member to get the email address for.

        Returns:
            A tuple containing the email address along with a user label
            depending on input type to use for logging purposes.

        Raises:
            WrongUsage: If none of the optional inputs are provided.
        """

        if email is not None:
            return email, email
        elif user is not None:
            return user.email, str(user)
        elif member is not None:
            if hasattr(member, "user"):
                return member.user.email, str(member)
            raise SlackBossException(
                f"Member {member} does not have an associated user"
            )
        raise WrongUsage("At least one of email, user, or member must be specified")

    @staticmethod
    def _get_channel_name_arg(
        name: Optional[str] = None,
        show: Optional[Show] = None,
    ) -> Tuple[str, str]:
        """Processes Slack channel name argument from various types.

        Args:
            name: The channel name.
            show: The show to get the channel name for.

        Returns:
            A tuple containing the channel name along with a channel label
            depending on input type to use for logging purposes.

        Raises:
            WrongUsage: If none of the optional inputs are provided.
        """

        if name is not None:
            return name, name
        elif show is not None:
            channel_name = show.default_channel_name()
            return channel_name, str(show)
        raise WrongUsage("At least one of name or show must be specified")

    @staticmethod
    def _get_slack_channel_id_arg(
        channel_id: Optional[str] = None,
        channel: Optional[SlackChannel] = None,
        show: Optional[Show] = None,
    ) -> Tuple[str, str]:
        """Processes Slack channel ID argument from various types.

        Args:
            channel_id: The Slack channel ID.
            channel: The Slack channel to get the ID for.
            show: The show to get the Slack channel ID for.

        Returns:
            A tuple containing the Slack channel ID along with a channel
            label depending on input type to use for logging purposes.

        Raises:
            WrongUsage: If none of the optional inputs are provided.
        """

        if channel_id is not None:
            return channel_id, channel_id
        elif channel is not None:
            return channel.id, channel.show.default_channel_name()
        elif show is not None:
            if hasattr(show, "channel"):
                return show.channel.id, show.default_channel_name()
            raise SlackBossException(f"Show {show} does not have a Slack channel")
        raise WrongUsage(
            "At least one of channel_id, channel, or show must be specified"
        )

    @staticmethod
    def _get_slack_user_ids_arg(
        user_ids: Optional[Union[str, List[str]]] = None,
        users: Optional[Union[SlackUser, List[SlackUser]]] = None,
    ) -> Tuple[Union[str, List[str]], str]:
        """Processes Slack user ID arguments from various types.

        Args:
            user_ids: The Slack user ID or IDs.
            users: The Slack user or users to get the ID or IDs for.

        Returns:
            A tuple containing the Slack user ID or IDs along with a Slack users
            label depending on input type to use for logging purposes.

        Raises:
            WrongUsage: If none of the optional inputs are provided.
        """

        if user_ids is not None:
            return user_ids, str(user_ids)
        elif users is not None:
            if isinstance(users, list):
                return [user.id for user in users], str([user.member for user in users])
            return users.id, str(users)
        raise WrongUsage("At least one of user_ids or users must be specified")

    @staticmethod
    def _get_show_arg(
        show: Optional[Show] = None,
        channel: Optional[SlackChannel] = None,
    ) -> Tuple[Show, str]:
        """Processes show argument from various types.

        Args:
            show: The show to return.
            channel: The channel to the show for.

        Returns:
            A tuple containing the show along with a show label depending on
            input type to use for logging purposes.

        Raises:
            WrongUsage: If none of the optional inputs are provided.
        """

        if show is not None:
            return show, str(show)
        elif channel is not None:
            if channel.show is not None:
                return channel.show, str(channel.show)
            raise SlackBossException(f"Channel {channel} does not have a Show")
        raise WrongUsage("At least one of show or channel must be specified")


slack_boss = SlackBoss()
