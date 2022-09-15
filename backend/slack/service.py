from __future__ import annotations

import logging
from typing import Optional, TYPE_CHECKING

from django.conf import settings
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

from common.exceptions import WrongUsage
from slack.exceptions import SlackBossException

if TYPE_CHECKING:
    from users.models import User
    from shows.models import Member, Show


class SlackBoss:
    """Custom Slack API WebClient wrapper

    SlackBoss provides custom convenience functions, utilities,
    and error-handling around the Slack SDK WebClient class.
    """

    def __init__(self, token: Optional[str] = None):
        """Initializes SlackBoss by creating a Slack API WebClient.

        If no `slack_token` is provided, SlackBoss will attempt to fetch the
        Slackbot token configured in the `SLACK_TOKEN` project setting.

        Args:
            token: workspace Slack token to configure the WebClient
        """

        if not token:
            if hasattr(settings, "SLACK_TOKEN"):
                token = settings.SLACK_TOKEN
            else:
                raise SlackBossException(
                    "SLACK_TOKEN must be configured in default settings if slack_token is None"
                )

        self.client = WebClient(token=token)

    def fetch_user(
        self,
        email: Optional[str] = None,
        user: Optional[User] = None,
        member: Optional[Member] = None,
    ) -> Optional[str]:
        """
        Fetches Slack user ID for the specified member by email.

        Args:
            email: The email address associated with the Slack user.
            user: The user to fetch the Slack user ID for.
            member: The member to fetch the Slack user ID for.

        Returns:
            The fetched user's Slack ID. None if there was no match.

        Raises:
            SlackBossException: If there was an error fetching the Slack user ID.
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
        """
        Fetches Slack user ID by the user's associated email address.

        Args:
            email: The email address associated with the Slack user.
            identifier: An identifier for the member for logging purposes.

        Returns:
            The fetched user's Slack ID. None if there was no match.

        Raises:
            SlackBossException: If there was an error fetching the Slack user ID.
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
        """
        Creates Slack channel for the specified show.

        Args:
            name: The email address associated with the Slack user.
            show: The show to fetch the Slack user ID for.

        Returns:
            The created channel's Slack ID. None if there was no match.

        Raises:
            SlackBossException: If there was an error creating the Slack channel.
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
        """
        Creates Slack channel with the specified name.

        Args:
            name: The name to use for the show channel.
            identifier: An identifier for the show for logging purposes.

        Returns:
            The created channel's Slack ID. None if there was no match.

        Raises:
            SlackBossException: If there was an error creating the Slack channel.
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


slack_boss = SlackBoss()
