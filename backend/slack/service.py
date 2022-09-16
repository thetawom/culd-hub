from __future__ import annotations

import logging
from typing import Optional, TYPE_CHECKING, Union, List

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

        if email is not None:
            return self._fetch_user_by_email(email)
        elif user is not None:
            return self._fetch_user_by_email(user.email, str(user))
        elif member is not None:
            if not hasattr(member, "user"):
                raise SlackBossException(
                    f"Member {member} does not have an associated User"
                )
            return self._fetch_user_by_email(member.user.email, str(member))
        raise WrongUsage("At least one of email, user, or member must be specified")

    def _fetch_user_by_email(
        self, email: str, identifier: Optional[str] = None
    ) -> Optional[str]:
        """Fetches Slack user ID by the user's associated email address.

        Args:
            email: The email address associated with the Slack user.
            identifier: An identifier for the member for logging purposes.

        Returns:
            The fetched user's Slack ID. None if there was no match.

        Raises:
            SlackBossException: If there was an error fetching the user ID.
        """

        identifier = email if not identifier else identifier
        logging.info(f"Fetching Slack user for {identifier} ...")
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

        if name is not None:
            return self._create_channel_by_name(name)
        elif show is not None:
            channel_name = show.default_channel_name()
            return self._create_channel_by_name(channel_name, str(show))
        raise WrongUsage("At least one of name or show must be specified")

    def _create_channel_by_name(
        self, name: str, identifier: Optional[str] = None
    ) -> Optional[str]:
        """Creates Slack channel with the specified name.

        Args:
            name: The name to use for the show channel.
            identifier: An identifier for the show for logging purposes.

        Returns:
            The created channel's Slack ID. None if there was no match.

        Raises:
            SlackBossException: If there was an error creating the channel.
        """

        identifier = name if not identifier else identifier
        logging.info(f"Creating Slack channel for {identifier} ...")
        try:
            response = self.client.conversations_create(name=name, is_private=False)
        except SlackApiError as api_error:
            error = api_error.response.get("error")
            raise SlackBossException(error)
        else:
            logging.debug(response)
            if not response.get("ok", False):
                raise SlackBossException("Error fetching Slack user ID")
            return response["channel"]["id"]

    def invite_users_to_channel(
        self,
        channel_id: Optional[str] = None,
        user_ids: Union[str, List[str]] = None,
        channel: Optional[SlackChannel] = None,
        users: Union[SlackUser, List[SlackUser]] = None,
    ):
        """Invites specified Slack users to the specified channel.

        One of channel_id or channel should be provided.
        One of user_ids or users should be provided.

        Args:
            channel_id: The Slack ID for the channel to invite users to.
            user_ids: The Slack IDs of the user or users to invite.
            channel: The Slack channel to invite users to.
            users: The Slack user or users to invite.

        Raises:
            SlackBossException: If there was an error inviting the users.
        """

        return self._invite_or_remove_users_from_channel(
            invite=True,
            channel_id=channel_id,
            user_ids=user_ids,
            channel=channel,
            users=users,
        )

    def remove_users_from_channel(
        self,
        channel_id: Optional[str] = None,
        user_ids: Union[str, List[str]] = None,
        channel: Optional[SlackChannel] = None,
        users: Union[SlackUser, List[SlackUser]] = None,
    ):
        """Removes specified Slack users from the specified channel.

        One of channel_id or channel should be provided.
        One of user_ids or users should be provided.

        Args:
            channel_id: The Slack ID for the channel to remove users from.
            user_ids: The Slack IDs of the user or users to remove.
            channel: The Slack channel to invite users to.
            users: The Slack user or users to invite.

        Raises:
            SlackBossException: If there was an error removing the users.
        """

        return self._invite_or_remove_users_from_channel(
            remove=True,
            channel_id=channel_id,
            user_ids=user_ids,
            channel=channel,
            users=users,
        )

    def _invite_or_remove_users_from_channel(
        self,
        invite: Optional[bool] = False,
        remove: Optional[bool] = False,
        channel_id: Optional[str] = None,
        user_ids: Union[str, List[str]] = None,
        channel: Optional[SlackChannel] = None,
        users: Union[SlackUser, List[SlackUser]] = None,
    ):
        """Invites or removes specified Slack users from the specified channel.

        One of channel_id or channel should be provided.
        One of user_ids or users should be provided.

        Args:
            invite: Whether to invite users from the channel.
            remove: Whether to remove users from the channel.
            channel_id: The Slack ID for the channel to invite or remove users from.
            user_ids: The Slack IDs of the user or users to invite or remove.
            channel: The Slack channel to invite or remove users from.
            users: The Slack user or users to invite or remove.

        Raises:
            SlackBossException: If there was an error inviting or removing the users.
        """

        if not invite and not remove:
            raise WrongUsage("Must specify whether to invite or remove users")

        if invite and remove:
            raise WrongUsage("Only one of invite or remove can be specified")

        channel_identifier, members_identifier = None, None

        if channel_id is None:
            if channel is None:
                raise WrongUsage(
                    "At least one of channel_id or channel must be specified"
                )
            channel_id = channel.id
            channel_identifier = channel.show.default_channel_name()

        if user_ids is None:
            if users is None:
                raise WrongUsage("At least one of user_ids or users must be specified")
            if isinstance(users, list):
                user_ids = [user.id for user in users]
                members_identifier = str([user.member for user in users])
            else:
                user_ids = users.id
                members_identifier = str(users)

        if invite:
            return self._invite_users_to_channel_by_id(
                channel_id=channel_id,
                user_ids=user_ids,
                channel_identifier=channel_identifier,
                members_identifier=members_identifier,
            )

        if remove:
            return self._remove_users_from_channel_by_id(
                channel_id=channel_id,
                user_ids=user_ids,
                channel_identifier=channel_identifier,
                members_identifier=members_identifier,
            )

    def _invite_users_to_channel_by_id(
        self,
        channel_id: str,
        user_ids: Union[str, List[str]],
        channel_identifier: Optional[str] = None,
        members_identifier: Optional[str] = None,
    ):
        """Invites specified Slack users to the specified channel.

        Args:
            channel_id: The Slack ID for the channel to invite users to.
            user_ids: The Slack IDs of the user or users to invite.
            channel_identifier: An identifier for the show for logging purposes.
            members_identifier: An identifier for the members for logging purposes.

        Raises:
            SlackBossException: If there was an error inviting the users.
        """

        channel_identifier = (
            channel_id if not channel_identifier else channel_identifier
        )
        members_identifier = user_ids if not members_identifier else members_identifier
        logging.info(
            f"Inviting {members_identifier} to channel {channel_identifier} ..."
        )
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

    def _remove_users_from_channel_by_id(
        self,
        channel_id: str,
        user_ids: Union[str, List[str]],
        channel_identifier: Optional[str] = None,
        members_identifier: Optional[str] = None,
    ):
        """Removes specified Slack users from the specified channel.

        Args:
            channel_id: The Slack ID for the channel to remove users from.
            user_ids: The Slack IDs of the user or users to remove.
            channel_identifier: An identifier for the show for logging purposes.
            members_identifier: An identifier for the members for logging purposes.

        Raises:
            SlackBossException: If there was an error removing the users.
        """

        channel_identifier = (
            channel_id if not channel_identifier else channel_identifier
        )
        members_identifier = user_ids if not members_identifier else members_identifier
        logging.info(
            f"Removing {members_identifier} from channel {channel_identifier} ..."
        )
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


slack_boss = SlackBoss()
