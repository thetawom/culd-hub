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
    from shows.models import Member

logging.basicConfig(level=logging.INFO)


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
            user: The User to fetch the Slack user ID for.
            member: The Member to fetch the Slack user ID for.

        Returns:
            A string containing the fetched user's Slack ID.
            None if there was no match.

        Raises:
            SlackBossException: If there was an error fetching the Slack user ID.
        """

        if email is not None:
            return self._fetch_user_by_email(email)
        elif user is not None:
            return self._fetch_user_by_email(user.email, user)
        elif member is not None:
            if not hasattr(member, "user"):
                raise SlackBossException(
                    f"Member {member} does not have an associated User"
                )
            return self._fetch_user_by_email(member.user.email, member)
        raise WrongUsage(
            "At least one of email, user, or member must be " "specified")

    def _fetch_user_by_email(
            self, email: str, identifier: Optional[str] = None
    ) -> Optional[str]:
        """
        Fetches Slack user ID by the user's associated email address.

        Args:
            email: The email address associated with the Slack user.
            identifier: An identifier for the Slack user for logging purposes.

        Returns:
            A string containing the fetched user's Slack ID.
            None if there was no match.

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


slack_boss = SlackBoss()
