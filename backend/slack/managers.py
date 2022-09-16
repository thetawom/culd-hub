from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Tuple, Union, List

from django.db import models
from django.utils.translation import gettext_lazy as _

from slack.service import slack_boss

if TYPE_CHECKING:
    from django.db.models import QuerySet
    from slack.models import SlackUser, SlackChannel
    from shows.models import Member, Show


class SlackUserManager(models.Manager):
    """Model manager for SlackUser"""

    def create(self, member: Member, **extra_fields) -> SlackUser:
        """Creates SlackUser for a member.

        Args:
            member: The member to create the SlackUser for.

        Returns:
            The newly created SlackUser instance.

        Raises:
            SlackBossException: If there was an error fetching the user ID.
        """

        if not member:
            raise ValueError(_("The member must be set"))
        if hasattr(member, "slack_user"):
            raise ValueError(_("The member already has a SlackUser record"))
        user_id = slack_boss.fetch_user(member=member)
        if user_id is not None:
            logging.info(f"Creating SlackUser with ID {user_id} ...")
            user = self.model(id=user_id, member=member, **extra_fields)
            user.save()
            return user

    def get_or_create(self, member: Member, **extra_fields) -> Tuple[SlackUser, bool]:
        """Fetches SlackUser for a member, or creates one if necessary.

        Args:
            member: The member to fetch or create the SlackUser for.

        Returns:
            A tuple containing the fetched or newly created SlackUser instance
            and a boolean indicating if an instance was created.

        Raises:
            SlackBossException: If there was an error fetching the user ID.
        """

        try:
            return self.get(member=member, **extra_fields), False
        except self.model.DoesNotExist:
            return self.create(member=member, **extra_fields), True


class SlackChannelManager(models.Manager):
    """Model manager for SlackChannel"""

    def create(self, show: Show, **extra_fields) -> SlackChannel:
        """Creates SlackChannel for a show.

        Args:
            show: The show to create the SlackChannel for.

        Returns:
            The newly created SlackChannel instance.

        Raises:
            SlackBossException: If there was an error creating the channel.
        """

        if not show:
            raise ValueError(_("The show must be set"))
        if hasattr(show, "channel"):
            raise ValueError(_("The show already has a SlackChannel record"))
        channel_id = slack_boss.create_channel(show=show)
        if channel_id is not None:
            logging.info(f"Creating SlackChannel with ID {channel_id} ...")
            channel = self.model(id=channel_id, show=show, **extra_fields)
            channel.save()
            return channel

    def get_or_create(self, show: Show, **extra_fields) -> Tuple[SlackChannel, bool]:
        """Fetches SlackChannel for a show, or creates one if necessary.

        Args:
            show: The show to fetch or create the SlackChannel for.

        Returns:
            A tuple containing the fetched or newly created SlackChannel
            instance and a boolean indicating if an instance was created.

        Raises:
            SlackBossException: If there was an error creating the channel.
        """

        try:
            return self.get(show=show, **extra_fields), False
        except self.model.DoesNotExist:
            return self.create(show=show, **extra_fields), True

    def invite_users(self, users: Union[SlackUser, List[SlackUser]]) -> QuerySet:
        """Invites Slack user or users to all queried Slack channels.

        Args:
            users: The Slack user or users to invite.

        Returns:
            A query set containing all Slack channels previously queried.
        """

        channel_set = self.all()
        for channel in channel_set:
            channel.invite_users(users)
        return channel_set

    def remove_users(self, users: Union[SlackUser, List[SlackUser]]) -> QuerySet:
        """Removes Slack user or users from all queried Slack channels.

        Args:
            users: The Slack user or users to remove.

        Returns:
            A query set containing all Slack channels previously queried.
        """

        channel_set = self.all()
        for channel in channel_set:
            channel.remove_users(users)
        return channel_set
