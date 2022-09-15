from unittest.mock import patch

from django.test import TestCase
from faker import Faker

from slack.service import SlackBoss


def fake_slack_id(faker=None):
    if faker is None:
        faker = Faker()
        Faker.seed(1234)

    def func(*args, **kwargs):
        return faker.password(length=10, special_chars=False, lower_case=False)

    return func


class PatchSlackBossMixin(TestCase):
    def setUp(self):
        super().setUp()
        self._patch_fetch_user()

    def _patch_fetch_user(self):
        fetch_user_patcher = patch.object(
            SlackBoss, "fetch_user", side_effect=fake_slack_id()
        )
        self.mock_fetch_user = fetch_user_patcher.start()
        self.addCleanup(fetch_user_patcher.stop)

        create_channel_patcher = patch.object(
            SlackBoss, "create_channel", side_effect=fake_slack_id()
        )
        self.mock_create_channel = create_channel_patcher.start()
        self.addCleanup(create_channel_patcher.stop)
