from typing import Optional, Union, List
from unittest.mock import patch

from django.test import TestCase
from faker import Faker

from common.exceptions import WrongUsage
from slack.service import SlackBoss


def fake_slack_id(
    faker: Optional[Faker] = None, count: int = 1, **kwargs
) -> Union[str, List[str]]:
    """Generate fake Slack IDs"""

    if count < 1:
        raise WrongUsage("Count must be at least 1")

    if faker is None:
        faker = Faker()
        Faker.seed(1234)

    ids = [
        faker.password(length=10, special_chars=False, lower_case=False)
        for _ in range(count)
    ]
    return ids[0] if count == 1 else ids


def fake_slack_token(faker: Optional[Faker] = None, **kwargs):
    if faker is None:
        faker = Faker()
        Faker.seed(1234)

    return faker.password(length=20, special_chars=False, lower_case=False)


def fake_slack_timestamp(faker: Optional[Faker] = None, **kwargs):
    if faker is None:
        faker = Faker()
        Faker.seed(1234)

    return f"{faker.unix_time()}.{faker.random_int()}"


class PatchSlackBossMixin(TestCase):
    def setUp(self):
        super().setUp()
        self._patch_fetch_user()
        self._patch_create_channel()
        self._patch_rename_channel()
        self._patch_archive_channel()
        self._patch_invite_users_to_channel()
        self._patch_remove_users_from_channel()
        self._patch_send_message_in_channel()

    def _patch_fetch_user(self):
        fetch_user_patcher = patch.object(
            SlackBoss, "fetch_user", side_effect=fake_slack_id
        )
        self.mock_fetch_user = fetch_user_patcher.start()
        self.addCleanup(fetch_user_patcher.stop)

    def _patch_create_channel(self):
        create_channel_patcher = patch.object(
            SlackBoss, "create_channel", side_effect=fake_slack_id
        )
        self.mock_create_channel = create_channel_patcher.start()
        self.addCleanup(create_channel_patcher.stop)

    def _patch_rename_channel(self):
        rename_channel_patcher = patch.object(
            SlackBoss, "rename_channel", side_effect=fake_slack_id
        )
        self.mock_rename_channel = rename_channel_patcher.start()
        self.addCleanup(rename_channel_patcher.stop)

    def _patch_archive_channel(self):
        archive_channel_patcher = patch.object(
            SlackBoss, "archive_channel", return_value=True
        )
        self.mock_archive_channel = archive_channel_patcher.start()
        self.addCleanup(archive_channel_patcher.stop)

    def _patch_invite_users_to_channel(self):
        invite_users_to_channel_patcher = patch.object(
            SlackBoss, "invite_users_to_channel", return_value=True
        )
        self.mock_invite_users_to_channel = invite_users_to_channel_patcher.start()
        self.addCleanup(invite_users_to_channel_patcher.stop)

    def _patch_remove_users_from_channel(self):
        remove_users_from_channel_patcher = patch.object(
            SlackBoss, "remove_users_from_channel", return_value=True
        )
        self.mock_remove_users_from_channel = remove_users_from_channel_patcher.start()
        self.addCleanup(remove_users_from_channel_patcher.stop)

    def _patch_send_message_in_channel(self):
        def mock_send(*args, ts: str = None, **kwargs):
            if ts is not None:
                return ts, False
            return fake_slack_timestamp(), True

        send_message_in_channel_patcher = patch.object(
            SlackBoss, "send_message_in_channel", side_effect=mock_send
        )
        self.mock_send_message_in_channel = send_message_in_channel_patcher.start()
        self.addCleanup(send_message_in_channel_patcher.stop)
