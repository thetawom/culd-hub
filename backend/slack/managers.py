from __future__ import annotations

from typing import TYPE_CHECKING, Tuple

from django.db import models
from django.utils.translation import gettext_lazy as _

from slack.service import slack_boss

if TYPE_CHECKING:
    from slack.models import SlackUser
    from shows.models import Member


class SlackUserManager(models.Manager):
    """Model manager for SlackUser"""

    def create(self, member: Member, **extra_fields) -> SlackUser:
        """Creates SlackUser for a member.

        Args:
            member: The member to create the SlackUser for.

        Returns:
            The newly created SlackUser instance.

        Raises:
            SlackBossException: If there was an error fetching the Slack user ID.
        """

        if not member:
            raise ValueError(_("The member must be set"))
        if hasattr(member, "slack_user"):
            raise ValueError(_("The member already has a SlackUser record"))
        user_id = slack_boss.fetch_user(member=member)
        user = self.model(id=user_id, member=member, **extra_fields)
        user.save()
        return user

    def get_or_create(self, member: Member, **extra_fields) -> Tuple[SlackUser, bool]:
        """Fetches SlackUser for a member, or creates one if necessary.

        Args:
            member: The member to fetch or create the SlackUser for.

        Returns:
            A tuple containing the fetched or newly created SlackUser instance and a boolean indicating if an instance was created.

        Raises:
            SlackBossException: If there was an error fetching the Slack user ID.
        """

        try:
            return self.get(member=member, **extra_fields), False
        except self.model.DoesNotExist:
            return self.create(member=member, **extra_fields), True
